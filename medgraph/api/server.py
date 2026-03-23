"""
FastAPI server for MEDGRAPH.

Provides REST API for drug interaction analysis.
Graph and store are loaded once at startup and cached in app state.

All API endpoints are mounted at both /api/v1/ (canonical) and /api/ (backward compat).

Endpoints:
    GET  /health                                        — Health check with DB stats
    GET  /api/v1/drugs/search                           — Search drugs by name (paginated)
    GET  /api/v1/drugs/{drug_id}                        — Get drug details
    POST /api/v1/check                                  — Analyze drug interactions
    GET  /api/v1/stats                                  — DB statistics (cached hourly)
    GET  /api/v1/data/freshness                         — Data freshness and version info
    GET  /api/v1/interactions/{interaction_id}/evidence  — Evidence for an interaction
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from medgraph.api.auth import check_rate_limit, verify_api_key
from medgraph.api.errors import register_error_handlers
from medgraph.api.metrics import ANALYSIS_DURATION, GRAPH_EDGES, GRAPH_NODES, setup_metrics
from medgraph.api.middleware import RequestIDMiddleware
from medgraph.api.security import SecurityHeadersMiddleware

from medgraph import __version__
from medgraph.logging_config import configure_logging
from medgraph.api.models import (
    AlternativeRequest,
    AlternativeResponse,
    CheckRequest,
    CheckResponse,
    ContraindicationResponse,
    CSVReportRequest,
    DataFreshnessResponse,
    DeprescribeRequest,
    DeprescribingResponse,
    DrugResponse,
    EnzymeRelationResponse,
    EvidenceResponse,
    CascadePathResponse,
    CascadeStepResponse,
    HealthResponse,
    HubDrugResponse,
    InteractionResponse,
    LivenessResponse,
    JSONReportRequest,
    PaginatedResponse,
    PathwayEdge,
    PathwayNode,
    PathwayResponse,
    PDFReportRequest,
    PGxAnnotation,
    SearchResult,
    StatsResponse,
)
from medgraph.api.search import DrugSearcher
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.engine.explainer import explain_interaction, explain_report
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.models import Drug
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

DISCLAIMER = (
    "This tool is for informational purposes only. "
    "It does not constitute medical advice. "
    "Always consult a qualified healthcare professional."
)

_STATS_TTL = 3600.0  # 1 hour


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize graph and store on startup; clean up on shutdown."""
    db_path = Path(os.environ.get("MEDGRAPH_DB_PATH", "data/medgraph.db"))
    if not db_path.exists():
        logger.warning(
            "Database not found at data/medgraph.db. Run 'python -m medgraph.cli seed' first."
        )

    store = GraphStore(db_path)
    builder = GraphBuilder()
    graph = builder.build(store)

    analyzer = CascadeAnalyzer()
    searcher = DrugSearcher(store, use_rxnorm=False)

    app.state.store = store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher
    app.state.stats_cache = (None, 0.0)

    counts = store.get_counts()
    # Set Prometheus gauges
    GRAPH_NODES.set(graph.number_of_nodes())
    GRAPH_EDGES.set(graph.number_of_edges())

    logger.info(
        f"MEDGRAPH loaded: {counts['drugs']} drugs, "
        f"{counts['interactions']} interactions, "
        f"{graph.number_of_nodes()} graph nodes, "
        f"{graph.number_of_edges()} graph edges"
    )

    yield

    logger.info("MEDGRAPH server shutting down")


def _build_drug_response(
    drug: Drug, store: GraphStore, enzymes_by_id: dict | None = None
) -> DrugResponse:
    """Build DrugResponse including enzyme relations with names.

    Args:
        enzymes_by_id: Pre-built enzyme lookup dict. If None, builds one via
                       store.get_all_enzymes() (avoid in loops — pass a cached dict).
    """
    if enzymes_by_id is None:
        enzymes_by_id = {e.id: e for e in store.get_all_enzymes()}
    relations = store.get_enzyme_relations(drug.id)
    enzyme_relations = [
        EnzymeRelationResponse(
            enzyme_name=enzymes_by_id[rel.enzyme_id].name
            if rel.enzyme_id in enzymes_by_id
            else rel.enzyme_id,
            relation_type=rel.relation_type,
            strength=rel.strength,
        )
        for rel in relations
    ]
    return DrugResponse(
        id=drug.id,
        name=drug.name,
        brand_names=drug.brand_names,
        drug_class=drug.drug_class,
        enzyme_relations=enzyme_relations,
    )


def _init_sentry() -> None:
    """Initialize Sentry error tracking if SENTRY_DSN env var is set."""
    dsn = os.environ.get("SENTRY_DSN")
    if not dsn:
        return
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration

        try:
            traces_rate = float(os.environ.get("SENTRY_TRACES_RATE", "0.1"))
        except ValueError:
            logger.warning("Invalid SENTRY_TRACES_RATE, falling back to 0.1")
            traces_rate = 0.1

        sentry_sdk.init(
            dsn=dsn,
            traces_sample_rate=traces_rate,
            integrations=[FastApiIntegration()],
            environment=os.environ.get("MEDGRAPH_ENV", "development"),
        )
        logger.info("Sentry error tracking initialized")
    except ImportError:
        logger.warning("SENTRY_DSN set but sentry-sdk not installed — skipping")


def create_app() -> FastAPI:
    """Factory function for the FastAPI application."""
    configure_logging()

    app = FastAPI(
        title="MEDGRAPH API",
        description=(
            "Drug Interaction Cascade Analyzer — knowledge graph + cascade analysis. "
            "DISCLAIMER: For research use only. Not medical advice."
        ),
        version=__version__,
        lifespan=lifespan,
        openapi_tags=[
            {"name": "system", "description": "Health checks and statistics"},
            {"name": "drugs", "description": "Drug lookup and search"},
            {"name": "analysis", "description": "Drug interaction analysis"},
            {"name": "reports", "description": "Report generation (PDF, JSON, CSV)"},
            {"name": "pharmacogenomics", "description": "CPIC pharmacogenomics guidelines"},
        ],
        contact={"name": "MEDGRAPH Team", "url": "https://github.com/HieuNTg/medgraph"},
        license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    )

    # CORS origins: configurable via MEDGRAPH_CORS_ORIGINS env var (comma-separated)
    cors_origins_raw = os.environ.get(
        "MEDGRAPH_CORS_ORIGINS", "http://localhost:5173,http://localhost:3000"
    )
    cors_origins = [o.strip() for o in cors_origins_raw.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Api-Key", "X-Request-ID"],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # RFC 7807 Problem Details error handlers
    register_error_handlers(app)

    # Prometheus metrics (auto-instruments all endpoints)
    setup_metrics(app)

    # Sentry error tracking (only if SENTRY_DSN env var is set)
    _init_sentry()

    @app.get("/health/live", response_model=LivenessResponse, tags=["system"])
    async def health_live() -> LivenessResponse:
        """Liveness probe — returns 200 if process is responding (no DB check)."""
        return LivenessResponse(status="ok")

    @app.get("/health/ready", response_model=HealthResponse, tags=["system"])
    async def health_ready() -> HealthResponse:
        """Readiness probe — verifies DB accessible and graph loaded."""
        store: GraphStore = app.state.store
        graph = app.state.graph
        counts = store.get_counts()
        total = sum(counts.values())
        return HealthResponse(
            status="ok",
            db_size=total,
            graph_nodes=graph.number_of_nodes(),
            schema_version=store.get_schema_version(),
        )

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        """Backward-compatible alias for /health/ready."""
        return await health_ready()

    # ── Versioned API Router ──────────────────────────────────────────────
    # All endpoints live on an APIRouter, mounted at both /api/v1 (canonical)
    # and /api (backward compat). /health stays on the root app.
    router = APIRouter()
    _api_deps = [Depends(verify_api_key), Depends(check_rate_limit)]

    @router.get("/stats", response_model=StatsResponse, tags=["system"], dependencies=_api_deps)
    async def stats() -> StatsResponse:
        cached_result, expiry = app.state.stats_cache
        now = time.monotonic()
        if cached_result is not None and now < expiry:
            return cached_result

        store: GraphStore = app.state.store
        counts = store.get_counts()
        result = StatsResponse(
            drug_count=counts.get("drugs", 0),
            interaction_count=counts.get("interactions", 0),
            enzyme_count=counts.get("enzymes", 0),
            adverse_event_count=counts.get("adverse_events", 0),
        )
        app.state.stats_cache = (result, now + _STATS_TTL)
        return result

    @router.get(
        "/data/freshness",
        response_model=DataFreshnessResponse,
        tags=["system"],
        dependencies=_api_deps,
    )
    async def get_data_freshness() -> DataFreshnessResponse:
        """Return data freshness metadata: counts, last refresh timestamp, and data version."""
        from medgraph.data.refresh_pipeline import DataRefreshPipeline

        store: GraphStore = app.state.store
        pipeline = DataRefreshPipeline(store)
        info = pipeline.get_freshness()
        return DataFreshnessResponse(
            drug_count=info["drug_count"],
            interaction_count=info["interaction_count"],
            enzyme_count=info["enzyme_count"],
            last_updated=info["last_updated"],
            data_version=info["data_version"],
        )

    @router.get("/drugs/search", response_model=PaginatedResponse[SearchResult], tags=["drugs"], dependencies=_api_deps)
    async def search_drugs(
        q: str = Query(..., min_length=1, description="Drug name search query"),
        limit: int = Query(10, ge=1, le=50),
        offset: int = Query(0, ge=0, description="Number of results to skip"),
    ) -> PaginatedResponse[SearchResult]:
        store: GraphStore = app.state.store
        # Single DB connection for consistent count + results
        drugs, total = store.search_drugs_with_count(q, limit=limit, offset=offset)
        items = [
            SearchResult(
                id=drug.id,
                name=drug.name,
                brand_names=drug.brand_names,
                drug_class=drug.drug_class,
            )
            for drug in drugs
        ]
        return PaginatedResponse(
            items=items,
            total=total,
            offset=offset,
            limit=limit,
            has_more=(offset + limit) < total,
        )

    @router.get("/drugs/{drug_id}", response_model=DrugResponse, tags=["drugs"], dependencies=_api_deps)
    async def get_drug(drug_id: str) -> DrugResponse:
        store: GraphStore = app.state.store
        drug = store.get_drug_by_id(drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail=f"Drug not found: {drug_id}")
        return _build_drug_response(drug, store)

    @router.get(
        "/interactions/{interaction_id}/evidence",
        response_model=list[EvidenceResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_interaction_evidence(interaction_id: str) -> list[EvidenceResponse]:
        store: GraphStore = app.state.store
        interaction = store.get_interaction_by_id(interaction_id)
        if not interaction:
            raise HTTPException(status_code=404, detail=f"Interaction not found: {interaction_id}")

        drug_ids = [interaction.drug_a_id, interaction.drug_b_id]
        adverse_events = store.get_adverse_events(drug_ids)

        evidence: list[EvidenceResponse] = []
        for ae in adverse_events:
            if interaction.drug_a_id in ae.drug_ids and interaction.drug_b_id in ae.drug_ids:
                evidence.append(
                    EvidenceResponse(
                        source="faers",
                        description=f"FAERS: {ae.reaction} ({ae.seriousness})",
                        case_count=ae.count if ae.count > 0 else None,
                        url=ae.source_url,
                    )
                )
        return evidence

    @router.post("/check", response_model=CheckResponse, tags=["analysis"], dependencies=_api_deps)
    async def check(request: CheckRequest) -> CheckResponse:
        """
        Analyze drug-drug interactions for a set of drugs.

        Accepts drug names (2-10), returns full interaction report.
        """
        drug_names = request.drugs

        # Validation
        if len(drug_names) == 0:
            raise HTTPException(status_code=400, detail="No drugs provided")
        if len(drug_names) == 1:
            raise HTTPException(status_code=400, detail="minimum 2 drugs required")
        if len(drug_names) > 10:
            raise HTTPException(status_code=400, detail="maximum 10 drugs")

        store: GraphStore = app.state.store
        graph = app.state.graph
        analyzer: CascadeAnalyzer = app.state.analyzer
        searcher: DrugSearcher = app.state.searcher

        # Check DB is seeded
        counts = store.get_counts()
        if counts.get("drugs", 0) == 0:
            raise HTTPException(
                status_code=503,
                detail="Database not seeded. Run 'python -m medgraph.cli seed' first.",
            )

        # Resolve drug names → Drug objects
        found_drugs: list = []
        unresolved: list[str] = []
        for name in drug_names:
            matches = searcher.search(name, limit=5)
            if matches:
                found_drugs.append(matches[0])
            else:
                unresolved.append(name)

        if unresolved:
            # Try to provide suggestions for each unresolved drug
            suggestions: dict[str, list[str]] = {}
            for name in unresolved:
                # broad search for suggestions
                broad = searcher.search(name[:3], limit=5) if len(name) >= 3 else []
                suggestions[name] = [d.name for d in broad]
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Some drugs were not found",
                    "unresolved": unresolved,
                    "suggestions": suggestions,
                },
            )

        drug_ids = [d.id for d in found_drugs]

        # Run analysis (timed for Prometheus)
        _t0 = time.perf_counter()
        report = analyzer.analyze(drug_ids, graph, store)
        ANALYSIS_DURATION.observe(time.perf_counter() - _t0)

        # Apply pharmacogenomics adjustments if provided
        if request.metabolizer_phenotypes:
            for result in report.interactions:
                result.risk_score = analyzer.scorer.score_interaction(
                    result, store, metabolizer_phenotypes=request.metabolizer_phenotypes
                )
                result.severity = analyzer.scorer.classify_severity(result.risk_score)
            report.overall_score = analyzer.scorer.score_report(report)
            report.overall_risk = analyzer.scorer.classify_severity(report.overall_score)

        # Build enzyme name cache (avoid repeated full enzyme lookups)
        enzymes_by_id = {e.id: e for e in store.get_all_enzymes()}

        drugs_response = [_build_drug_response(d, store, enzymes_by_id) for d in report.drugs]

        interactions_response: list[InteractionResponse] = []
        for result in report.interactions:
            # Build cascade path responses
            cascade_paths_resp: list[CascadePathResponse] = []
            for cp in result.cascade_paths:
                steps_resp = [
                    CascadeStepResponse(
                        source=step.source_drug,
                        target=step.target,
                        relation=step.relation,
                        effect=step.effect,
                    )
                    for step in cp.steps
                ]
                cascade_paths_resp.append(
                    CascadePathResponse(
                        steps=steps_resp,
                        description=cp.description,
                        net_severity=cp.net_severity,
                    )
                )

            # Build evidence responses
            evidence_resp: list[EvidenceResponse] = []
            if request.include_evidence:
                for ev in result.evidence:
                    evidence_resp.append(
                        EvidenceResponse(
                            source=ev.source,
                            description=ev.description,
                            case_count=ev.evidence_count if ev.evidence_count > 0 else None,
                            url=ev.url,
                        )
                    )

            description = ""
            mechanism = None
            if result.direct_interaction:
                description = result.direct_interaction.description
                mechanism = result.direct_interaction.mechanism

            # Build PGx annotations if metabolizer_phenotypes provided
            pgx_annotations: list[PGxAnnotation] = []
            if request.metabolizer_phenotypes:
                for gene_id, phenotype in request.metabolizer_phenotypes.items():
                    for drug in [result.drug_a, result.drug_b]:
                        guidelines = store.get_genetic_guidelines(drug.id, gene_id)
                        for gl in guidelines:
                            if gl.phenotype == phenotype:
                                pgx_annotations.append(
                                    PGxAnnotation(
                                        gene=gene_id,
                                        phenotype=phenotype,
                                        drug_name=drug.name,
                                        recommendation=gl.recommendation,
                                        severity_multiplier=gl.severity_multiplier,
                                    )
                                )

            interactions_response.append(
                InteractionResponse(
                    drug_a=_build_drug_response(result.drug_a, store, enzymes_by_id),
                    drug_b=_build_drug_response(result.drug_b, store, enzymes_by_id),
                    severity=result.severity,
                    risk_score=result.risk_score,
                    description=description,
                    mechanism=mechanism,
                    cascade_paths=cascade_paths_resp,
                    evidence=evidence_resp,
                    pgx_annotations=pgx_annotations,
                    explanation=explain_interaction(result),
                )
            )

        return CheckResponse(
            drugs=drugs_response,
            interactions=interactions_response,
            overall_risk=report.overall_risk,
            overall_score=report.overall_score,
            drug_count=len(report.drugs),
            interaction_count=len(report.interactions),
            timestamp=datetime.now(timezone.utc).isoformat(),
            disclaimer=DISCLAIMER,
            summary=explain_report(report),
        )

    @router.post("/report/pdf", tags=["reports"], dependencies=_api_deps)
    async def generate_pdf_report(request: PDFReportRequest) -> Response:
        """Generate a PDF report from check results."""
        from medgraph.reports.pdf_generator import generate_report_pdf

        pdf_bytes = generate_report_pdf(
            check_result=request.check_result,
            graph_png_b64=request.graph_png_b64,
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=medgraph-report.pdf",
            },
        )

    @router.post("/report/json", tags=["reports"], dependencies=_api_deps)
    async def generate_json_report(request: JSONReportRequest) -> Response:
        """Generate a structured JSON report from check results."""
        from medgraph.reports.json_generator import generate_report_json

        json_str = generate_report_json(
            check_result=request.check_result.model_dump(),
            pretty=request.pretty,
        )
        return Response(
            content=json_str,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=medgraph-report.json",
            },
        )

    @router.post("/report/csv", tags=["reports"], dependencies=_api_deps)
    async def generate_csv_report(request: CSVReportRequest) -> Response:
        """Generate a CSV report of drug interactions."""
        from medgraph.reports.csv_generator import generate_report_csv

        csv_str = generate_report_csv(
            check_result=request.check_result.model_dump(),
        )
        return Response(
            content=csv_str,
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=medgraph-report.csv",
            },
        )

    @router.get("/pgx/guidelines", tags=["pharmacogenomics"], dependencies=_api_deps)
    async def get_pgx_guidelines(
        drug_id: str = Query(..., description="Drug ID (e.g. DB00318)"),
    ) -> list[dict]:
        """Get CPIC pharmacogenomics guidelines for a drug."""
        store: GraphStore = app.state.store
        guidelines = store.get_guidelines_for_drug(drug_id)
        return [
            {
                "gene": gl.gene_id,
                "phenotype": gl.phenotype,
                "recommendation": gl.recommendation,
                "severity_multiplier": gl.severity_multiplier,
            }
            for gl in guidelines
        ]

    # ── Graph & Advanced Analysis Endpoints ──────────────────────────────────
    # Engine modules are provided by another agent; import with graceful fallback.

    try:
        from medgraph.engine.alternatives import AlternativesFinder
        _has_alternatives = True
    except ImportError:
        _has_alternatives = False

    try:
        from medgraph.engine.centrality import CentralityAnalyzer
        _has_centrality = True
    except ImportError:
        _has_centrality = False

    try:
        from medgraph.engine.contraindication import ContraindicationNetwork
        _has_contraindication = True
    except ImportError:
        _has_contraindication = False

    try:
        from medgraph.engine.deprescriber import Deprescriber
        _has_deprescriber = True
    except ImportError:
        _has_deprescriber = False

    @router.post(
        "/alternatives",
        response_model=list[AlternativeResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_alternatives(request: AlternativeRequest) -> list[AlternativeResponse]:
        """Find alternative drugs with fewer interactions for the given regimen."""
        if not _has_alternatives:
            raise HTTPException(status_code=503, detail="Alternatives engine not available")
        store: GraphStore = app.state.store
        graph = app.state.graph
        finder = AlternativesFinder(graph, store)
        results = finder.find_alternatives(request.drug_id, request.regimen)
        return [
            AlternativeResponse(
                drug_id=alt.drug_id,
                drug_name=alt.drug_name,
                reason=alt.reason,
                enzyme_overlap_count=alt.enzyme_overlap_count,
            )
            for alt in results
        ]

    @router.get(
        "/graph/pathways",
        response_model=PathwayResponse,
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_pathways(
        drugs: str = Query(..., description="Comma-separated drug IDs"),
    ) -> PathwayResponse:
        """Return metabolic pathway graph for a set of drug IDs."""
        drug_ids = [d.strip() for d in drugs.split(",") if d.strip()]
        if not drug_ids:
            raise HTTPException(status_code=400, detail="No drug IDs provided")

        store: GraphStore = app.state.store
        graph = app.state.graph

        nodes: dict[str, PathwayNode] = {}
        edges: list[PathwayEdge] = []
        cascades: list[dict] = []

        enzymes_by_id = {e.id: e for e in store.get_all_enzymes()}

        for drug_id in drug_ids:
            drug = store.get_drug_by_id(drug_id)
            if not drug:
                continue
            nodes[drug_id] = PathwayNode(id=drug_id, type="drug", label=drug.name)
            for rel in store.get_enzyme_relations(drug_id):
                enz_id = rel.enzyme_id
                if enz_id not in nodes:
                    enz_label = enzymes_by_id[enz_id].name if enz_id in enzymes_by_id else enz_id
                    nodes[enz_id] = PathwayNode(id=enz_id, type="enzyme", label=enz_label)
                edges.append(
                    PathwayEdge(
                        source=drug_id,
                        target=enz_id,
                        relation=rel.relation_type,
                        strength=rel.strength,
                    )
                )

        # Collect cascade interactions between the supplied drugs
        if len(drug_ids) >= 2:
            cascade_analyzer: CascadeAnalyzer = app.state.analyzer
            report = cascade_analyzer.analyze(drug_ids, graph, store)
            for interaction in report.interactions:
                for cp in interaction.cascade_paths:
                    cascades.append(
                        {
                            "description": cp.description,
                            "net_severity": cp.net_severity,
                            "steps": [
                                {
                                    "source": step.source_drug,
                                    "target": step.target,
                                    "relation": step.relation,
                                    "effect": step.effect,
                                }
                                for step in cp.steps
                            ],
                        }
                    )

        return PathwayResponse(
            nodes=list(nodes.values()),
            edges=edges,
            cascades=cascades,
        )

    @router.get(
        "/graph/hub-drugs",
        response_model=list[HubDrugResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_hub_drugs(
        top_n: int = Query(20, ge=1, le=100, description="Number of top hub drugs to return"),
    ) -> list[HubDrugResponse]:
        """Return top hub drugs ranked by centrality metrics."""
        if not _has_centrality:
            raise HTTPException(status_code=503, detail="Centrality engine not available")
        graph = app.state.graph
        analyzer_obj = CentralityAnalyzer(graph)
        hubs = analyzer_obj.hub_drugs(top_n)
        return [
            HubDrugResponse(
                drug_id=h.drug_id,
                drug_name=h.drug_name,
                betweenness=h.betweenness,
                pagerank=h.pagerank,
                interaction_count=h.interaction_count,
            )
            for h in hubs
        ]

    @router.get(
        "/graph/contraindications",
        response_model=ContraindicationResponse,
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_contraindications(
        drugs: str = Query(..., description="Comma-separated drug IDs"),
    ) -> ContraindicationResponse:
        """Return contraindication network for a set of drug IDs."""
        if not _has_contraindication:
            raise HTTPException(status_code=503, detail="Contraindication engine not available")
        drug_ids = [d.strip() for d in drugs.split(",") if d.strip()]
        if not drug_ids:
            raise HTTPException(status_code=400, detail="No drug IDs provided")
        graph = app.state.graph
        store: GraphStore = app.state.store
        network = ContraindicationNetwork(graph, store)
        result = network.build_network(drug_ids)
        return ContraindicationResponse(
            nodes=result.get("nodes", []),
            edges=result.get("edges", []),
            clusters=result.get("clusters", []),
        )

    @router.post(
        "/deprescribe",
        response_model=list[DeprescribingResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def deprescribe(request: DeprescribeRequest) -> list[DeprescribingResponse]:
        """Return ordered deprescribing recommendations for a drug regimen."""
        if not _has_deprescriber:
            raise HTTPException(status_code=503, detail="Deprescriber engine not available")
        if not request.drugs:
            raise HTTPException(status_code=400, detail="No drugs provided")
        graph = app.state.graph
        store: GraphStore = app.state.store
        deprescriber = Deprescriber(graph, store)
        recs = deprescriber.recommend(request.drugs)
        return [
            DeprescribingResponse(
                drug_id=rec.drug_id,
                drug_name=rec.drug_name,
                removal_benefit=rec.removal_benefit,
                interactions_resolved=rec.interactions_resolved,
                rationale=rec.rationale,
                order=rec.order,
            )
            for rec in recs
        ]

    # Mount router at /api/v1 (canonical) and /api (backward compat)
    app.include_router(router, prefix="/api/v1")
    app.include_router(router, prefix="/api")

    return app


# Module-level app instance for uvicorn
app = create_app()
