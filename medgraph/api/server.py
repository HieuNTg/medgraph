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

    POST /auth/register                                 — Register new user
    POST /auth/login                                    — Login and receive JWT tokens
    POST /auth/refresh                                  — Refresh access token
    POST /auth/logout                                   — Logout and blacklist access token
    GET  /auth/me                                       — Get current user info

    POST   /api/v1/profiles                             — Create medication profile
    GET    /api/v1/profiles                             — List user profiles
    GET    /api/v1/profiles/{profile_id}                — Get profile
    PUT    /api/v1/profiles/{profile_id}                — Update profile
    DELETE /api/v1/profiles/{profile_id}                — Delete profile

    GET  /api/v1/history                                — Analysis history for user
    POST /api/v1/share                                  — Share analysis result
    GET  /api/v1/shared/{token}                         — Get shared result (no auth)
    GET  /api/v1/audit                                  — Audit log (admin)

    POST /api/v1/optimize                               — Optimize polypharmacy regimen
"""

import asyncio
import json
import logging
import os
import secrets
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.concurrency import run_in_threadpool

from medgraph.api.audit import AuditLogger
from medgraph.api.auth import check_rate_limit, verify_api_key
from medgraph.api.user_auth import UserAuth
from medgraph.api.errors import register_error_handlers
from medgraph.api.metrics import ANALYSIS_DURATION, GRAPH_EDGES, GRAPH_NODES, setup_metrics
from medgraph.api.middleware import RequestIDMiddleware
from medgraph.api.security import SecurityHeadersMiddleware

from medgraph import __version__
from medgraph.logging_config import configure_logging
from medgraph.api.models import (
    AlternativeRequest,
    AlternativeResponse,
    AnalysisHistoryResponse,
    AuditLogResponse,
    CascadePathResponse,
    CascadeStepResponse,
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
    FoodInteractionResponse,
    HealthResponse,
    HubDrugResponse,
    InteractionResponse,
    LivenessResponse,
    JSONReportRequest,
    LoginRequest,
    OptimizeRequest,
    OptimizeResponse,
    PaginatedResponse,
    ScheduleRequest,
    ScheduleResponse,
    ScheduledDrugResponse,
    PathwayEdge,
    PathwayNode,
    PathwayResponse,
    PDFReportRequest,
    PGxAnnotation,
    PGxDrugAlert,
    PGxRiskRequest,
    PGxRiskResponse,
    ProfileRequest,
    ProfileResponse,
    RefreshRequest,
    RegisterRequest,
    SearchResult,
    SharedResultResponse,
    StatsResponse,
    TokenResponse,
    UserResponse,
)
from medgraph.api.search import DrugSearcher
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.engine.explainer import explain_interaction, explain_report
from medgraph.engine.optimizer import PolypharmacyOptimizer
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
_stats_lock = asyncio.Lock()


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

    secret_key = os.environ.get("MEDGRAPH_JWT_SECRET", "medgraph-dev-secret")
    user_auth = UserAuth(store, secret_key=secret_key)
    audit_logger = AuditLogger(store)

    app.state.store = store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher
    app.state.stats_cache = (None, 0.0)
    app.state.user_auth = user_auth
    app.state.audit_logger = audit_logger
    app.state.enzymes = {e.id: e for e in store.get_all_enzymes()}

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
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
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

    # ── Auth Dependency ───────────────────────────────────────────────────
    _bearer = HTTPBearer(auto_error=False)

    def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    ) -> dict | None:
        """Extract and verify JWT from Authorization header. Returns user dict or None."""
        if credentials is None:
            return None
        _user_auth: UserAuth = app.state.user_auth
        payload = _user_auth.verify_token(credentials.credentials)
        if not payload or payload.get("type") != "access":
            return None
        return _user_auth.get_user(payload["sub"])

    def require_current_user(
        user: dict | None = Depends(get_current_user),
    ) -> dict:
        """Like get_current_user but raises 401 if not authenticated."""
        if user is None:
            raise HTTPException(status_code=401, detail="Authentication required")
        return user

    def _client_ip(request: Request) -> str:
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "unknown"

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

        async with _stats_lock:
            # Double-check after acquiring lock
            cached_result, expiry = app.state.stats_cache
            now = time.monotonic()
            if cached_result is not None and now < expiry:
                return cached_result

            store: GraphStore = app.state.store
            counts = await run_in_threadpool(store.get_counts)
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

    @router.get(
        "/food-interactions",
        response_model=list[FoodInteractionResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_food_interactions(
        drugs: str = Query(..., description="Comma-separated drug names"),
    ) -> list[FoodInteractionResponse]:
        """Return food/supplement interactions for the given drugs via CYP450 pathways."""
        store: GraphStore = app.state.store
        searcher: DrugSearcher = app.state.searcher

        drug_names = [n.strip() for n in drugs.split(",") if n.strip()]
        if not drug_names:
            raise HTTPException(status_code=400, detail="At least one drug name required")

        drug_ids = []
        for name in drug_names:
            matches = searcher.search(name, limit=1)
            if matches:
                drug_ids.append(matches[0].id)

        rows = store.get_food_interactions(drug_ids)
        return [
            FoodInteractionResponse(
                food_name=r["food_name"],
                food_category=r["food_category"],
                drug_id=r["drug_id"],
                severity=r["severity"],
                description=r["description"],
                mechanism=r.get("mechanism"),
                evidence_level=r.get("evidence_level", "C"),
            )
            for r in rows
        ]

    @router.get(
        "/drugs/search",
        response_model=PaginatedResponse[SearchResult],
        tags=["drugs"],
        dependencies=_api_deps,
    )
    async def search_drugs(
        q: str = Query(..., min_length=1, description="Drug name search query"),
        limit: int = Query(10, ge=1, le=50),
        offset: int = Query(0, ge=0, description="Number of results to skip"),
    ) -> PaginatedResponse[SearchResult]:
        store: GraphStore = app.state.store
        # Single DB connection for consistent count + results
        drugs, total = await run_in_threadpool(store.search_drugs_with_count, q, limit, offset)
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

    @router.get(
        "/drugs/{drug_id}", response_model=DrugResponse, tags=["drugs"], dependencies=_api_deps
    )
    async def get_drug(drug_id: str) -> DrugResponse:
        store: GraphStore = app.state.store
        drug = await run_in_threadpool(store.get_drug_by_id, drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail=f"Drug not found: {drug_id}")
        return await run_in_threadpool(_build_drug_response, drug, store)

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
    async def check(
        request: CheckRequest,
        http_request: Request,
        current_user: dict | None = Depends(get_current_user),
    ) -> CheckResponse:
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
        counts = await run_in_threadpool(store.get_counts)
        if counts.get("drugs", 0) == 0:
            raise HTTPException(
                status_code=503,
                detail="Database not seeded. Run 'python -m medgraph.cli seed' first.",
            )

        # Resolve drug names → Drug objects
        found_drugs: list = []
        unresolved: list[str] = []
        for name in drug_names:
            matches = await run_in_threadpool(searcher.search, name, 5)
            if matches:
                found_drugs.append(matches[0])
            else:
                unresolved.append(name)

        if unresolved:
            # Try to provide suggestions for each unresolved drug
            suggestions: dict[str, list[str]] = {}
            for name in unresolved:
                # broad search for suggestions
                broad = (
                    await run_in_threadpool(searcher.search, name[:3], 5) if len(name) >= 3 else []
                )
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
        report = await run_in_threadpool(analyzer.analyze, drug_ids, graph, store)
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

        # Use startup-cached enzyme lookup dict (fall back to DB query if not cached)
        try:
            enzymes_by_id = http_request.app.state.enzymes
        except AttributeError:
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

            confidence = analyzer.scorer.compute_confidence(result)

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
                    confidence_score=confidence["score"],
                    confidence_level=confidence["level"],
                    confidence_factors=confidence["factors"],
                )
            )

        # Fetch food interactions for all resolved drugs
        food_rows = store.get_food_interactions(drug_ids)
        food_interactions_resp = [
            FoodInteractionResponse(
                food_name=r["food_name"],
                food_category=r["food_category"],
                drug_id=r["drug_id"],
                severity=r["severity"],
                description=r["description"],
                mechanism=r.get("mechanism"),
                evidence_level=r.get("evidence_level", "C"),
            )
            for r in food_rows
        ]

        check_response = CheckResponse(
            drugs=drugs_response,
            interactions=interactions_response,
            overall_risk=report.overall_risk,
            overall_score=report.overall_score,
            drug_count=len(report.drugs),
            interaction_count=len(report.interactions),
            timestamp=datetime.now(timezone.utc).isoformat(),
            disclaimer=DISCLAIMER,
            summary=explain_report(report),
            food_interactions=food_interactions_resp,
        )

        # Auto-save to analysis history
        try:
            analysis_id = str(uuid.uuid4())
            store.save_analysis(
                analysis_id=analysis_id,
                user_id=current_user["id"] if current_user else None,
                drug_ids=drug_ids,
                result_json=check_response.model_dump_json(),
                overall_risk=report.overall_risk,
                created_at=check_response.timestamp,
            )
        except Exception:
            pass  # History save must not break primary analysis

        return check_response

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

    @router.post(
        "/pgx/risk-profile",
        response_model=PGxRiskResponse,
        tags=["pharmacogenomics"],
        dependencies=_api_deps,
    )
    async def pgx_risk_profile(request: PGxRiskRequest) -> PGxRiskResponse:
        """Calculate personalized drug interaction risk based on pharmacogenomics."""
        from medgraph.data.seed_cpic_guidelines import ANCESTRY_ALLELE_FREQUENCIES

        store: GraphStore = app.state.store
        searcher: DrugSearcher = app.state.searcher

        # Resolve drug names to Drug objects
        resolved_drugs = []
        for name in request.drugs:
            matches = await run_in_threadpool(searcher.search, name, 1)
            if matches:
                resolved_drugs.append(matches[0])

        alerts: list[PGxDrugAlert] = []
        population_risk_factors: list[str] = []

        if request.known_phenotypes:
            # Direct phenotype match: return alerts for each drug × gene × phenotype
            for drug in resolved_drugs:
                for gene_id, phenotype in request.known_phenotypes.items():
                    guidelines = await run_in_threadpool(
                        store.get_genetic_guidelines, drug.id, gene_id
                    )
                    for gl in guidelines:
                        if gl.phenotype == phenotype:
                            pop_freq: float | None = None
                            if request.ancestry:
                                pop_freq = (
                                    ANCESTRY_ALLELE_FREQUENCIES.get(gene_id, {})
                                    .get(phenotype, {})
                                    .get(request.ancestry)
                                )
                            alerts.append(
                                PGxDrugAlert(
                                    drug_name=drug.name,
                                    gene=gene_id,
                                    phenotype=phenotype,
                                    recommendation=gl.recommendation,
                                    severity_multiplier=gl.severity_multiplier,
                                    population_frequency=pop_freq,
                                )
                            )
        elif request.ancestry:
            # Ancestry-only mode: flag high-frequency risk alleles (>= 5%) for each drug
            for drug in resolved_drugs:
                all_guidelines = await run_in_threadpool(store.get_guidelines_for_drug, drug.id)
                for gl in all_guidelines:
                    freq_map = ANCESTRY_ALLELE_FREQUENCIES.get(gl.gene_id, {}).get(gl.phenotype, {})
                    pop_freq = freq_map.get(request.ancestry)
                    if pop_freq is not None and pop_freq >= 0.05:
                        alerts.append(
                            PGxDrugAlert(
                                drug_name=drug.name,
                                gene=gl.gene_id,
                                phenotype=gl.phenotype,
                                recommendation=gl.recommendation,
                                severity_multiplier=gl.severity_multiplier,
                                population_frequency=pop_freq,
                            )
                        )

        # Build population risk factor strings from ancestry frequencies
        if request.ancestry:
            for gene_id, phenotypes in ANCESTRY_ALLELE_FREQUENCIES.items():
                for phenotype, ancestry_map in phenotypes.items():
                    freq = ancestry_map.get(request.ancestry)
                    if freq is not None and freq >= 0.05:
                        pct = round(freq * 100, 1)
                        population_risk_factors.append(
                            f"{request.ancestry.replace('_', ' ').title()} population: "
                            f"{pct}% carry {gene_id} {phenotype.replace('_', ' ')}"
                        )

        return PGxRiskResponse(
            alerts=alerts,
            ancestry=request.ancestry,
            population_risk_factors=sorted(set(population_risk_factors)),
            disclaimer=(
                "Pharmacogenomics data is for informational purposes only. "
                "Clinical genetic testing is required for actionable results. "
                "Always consult a qualified healthcare professional or clinical pharmacist."
            ),
        )

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
        try:
            results = finder.find_alternatives(request.drug_id, request.regimen)
        except Exception as exc:
            logger.exception("Alternatives engine error: %s", exc)
            raise HTTPException(status_code=503, detail="Alternatives engine failed")
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

        enzymes_by_id = app.state.enzymes

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
        try:
            hubs = analyzer_obj.hub_drugs(top_n)
        except Exception as exc:
            logger.exception("Hub-drugs engine error: %s", exc)
            raise HTTPException(status_code=503, detail="Centrality engine failed")
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
        try:
            result = network.build_network(drug_ids)
        except Exception as exc:
            logger.exception("Contraindications engine error: %s", exc)
            raise HTTPException(status_code=503, detail="Contraindication engine failed")
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
        try:
            recs = deprescriber.recommend(request.drugs)
        except Exception as exc:
            logger.exception("Deprescriber engine error: %s", exc)
            raise HTTPException(status_code=503, detail="Deprescriber engine failed")
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

    # ── Auth Router ───────────────────────────────────────────────────────
    auth_router = APIRouter(prefix="/auth", tags=["auth"])

    @auth_router.post(
        "/register", response_model=TokenResponse, dependencies=[Depends(check_rate_limit)]
    )
    async def register(request: Request, body: RegisterRequest) -> TokenResponse:
        user_auth: UserAuth = app.state.user_auth
        audit: AuditLogger = app.state.audit_logger
        try:
            result = user_auth.register(body.email, body.password, body.display_name)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        audit.log(
            "user.register",
            user_id=result["user"]["id"],
            resource_type="user",
            resource_id=result["user"]["id"],
            ip_address=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return TokenResponse(**result)

    @auth_router.post(
        "/login", response_model=TokenResponse, dependencies=[Depends(check_rate_limit)]
    )
    async def login(request: Request, body: LoginRequest) -> TokenResponse:
        user_auth: UserAuth = app.state.user_auth
        audit: AuditLogger = app.state.audit_logger
        try:
            result = user_auth.login(body.email, body.password)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        audit.log(
            "user.login",
            user_id=result["user"]["id"],
            resource_type="user",
            resource_id=result["user"]["id"],
            ip_address=_client_ip(request),
            user_agent=request.headers.get("user-agent"),
        )
        return TokenResponse(**result)

    @auth_router.post("/refresh", response_model=TokenResponse)
    async def refresh_token(body: RefreshRequest) -> TokenResponse:
        user_auth: UserAuth = app.state.user_auth
        try:
            result = user_auth.refresh(body.refresh_token)
        except ValueError as exc:
            raise HTTPException(status_code=401, detail=str(exc))
        return TokenResponse(**result)

    @auth_router.post("/logout")
    async def logout(
        credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    ) -> dict:
        if credentials is None:
            raise HTTPException(status_code=401, detail="Authorization header required")
        user_auth: UserAuth = app.state.user_auth
        # Verify the token is valid before blacklisting
        payload = user_auth.verify_token(credentials.credentials)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        user_auth.logout(credentials.credentials)
        return {"message": "Logged out successfully"}

    @auth_router.get("/me", response_model=UserResponse)
    async def get_me(user: dict = Depends(require_current_user)) -> UserResponse:
        return UserResponse(**user)

    app.include_router(auth_router)

    # ── Profile Endpoints ─────────────────────────────────────────────────

    @router.post(
        "/profiles", response_model=ProfileResponse, tags=["profiles"], dependencies=_api_deps
    )
    async def create_profile(
        body: ProfileRequest,
        request: Request,
        user: dict = Depends(require_current_user),
    ) -> ProfileResponse:
        store: GraphStore = app.state.store
        audit: AuditLogger = app.state.audit_logger
        now = datetime.now(timezone.utc).isoformat()
        profile_id = str(uuid.uuid4())
        store.create_profile(
            profile_id=profile_id,
            user_id=user["id"],
            name=body.name,
            drug_ids=body.drug_ids,
            notes=body.notes,
            created_at=now,
            updated_at=now,
        )
        audit.log(
            "profile.create",
            user_id=user["id"],
            resource_type="profile",
            resource_id=profile_id,
            ip_address=_client_ip(request),
        )
        return ProfileResponse(
            id=profile_id,
            name=body.name,
            drug_ids=body.drug_ids,
            notes=body.notes,
            created_at=now,
            updated_at=now,
        )

    @router.get(
        "/profiles", response_model=list[ProfileResponse], tags=["profiles"], dependencies=_api_deps
    )
    async def list_profiles(
        user: dict = Depends(require_current_user),
    ) -> list[ProfileResponse]:
        store: GraphStore = app.state.store
        rows = store.get_profiles_by_user(user["id"])
        return [ProfileResponse(**r) for r in rows]

    @router.get(
        "/profiles/{profile_id}",
        response_model=ProfileResponse,
        tags=["profiles"],
        dependencies=_api_deps,
    )
    async def get_profile(
        profile_id: str,
        user: dict = Depends(require_current_user),
    ) -> ProfileResponse:
        store: GraphStore = app.state.store
        row = store.get_profile_by_id(profile_id)
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        if row["user_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return ProfileResponse(**row)

    @router.put(
        "/profiles/{profile_id}",
        response_model=ProfileResponse,
        tags=["profiles"],
        dependencies=_api_deps,
    )
    async def update_profile(
        profile_id: str,
        body: ProfileRequest,
        request: Request,
        user: dict = Depends(require_current_user),
    ) -> ProfileResponse:
        store: GraphStore = app.state.store
        audit: AuditLogger = app.state.audit_logger
        row = store.get_profile_by_id(profile_id)
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        if row["user_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        now = datetime.now(timezone.utc).isoformat()
        store.update_profile(
            profile_id=profile_id,
            name=body.name,
            drug_ids=body.drug_ids,
            notes=body.notes,
            updated_at=now,
        )
        audit.log(
            "profile.update",
            user_id=user["id"],
            resource_type="profile",
            resource_id=profile_id,
            ip_address=_client_ip(request),
        )
        return ProfileResponse(
            id=profile_id,
            name=body.name,
            drug_ids=body.drug_ids,
            notes=body.notes,
            created_at=row["created_at"],
            updated_at=now,
        )

    @router.delete("/profiles/{profile_id}", tags=["profiles"], dependencies=_api_deps)
    async def delete_profile(
        profile_id: str,
        request: Request,
        user: dict = Depends(require_current_user),
    ) -> dict:
        store: GraphStore = app.state.store
        audit: AuditLogger = app.state.audit_logger
        row = store.get_profile_by_id(profile_id)
        if not row:
            raise HTTPException(status_code=404, detail="Profile not found")
        if row["user_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        store.delete_profile(profile_id)
        audit.log(
            "profile.delete",
            user_id=user["id"],
            resource_type="profile",
            resource_id=profile_id,
            ip_address=_client_ip(request),
        )
        return {"status": "deleted"}

    # ── History Endpoint ──────────────────────────────────────────────────

    @router.get(
        "/history",
        response_model=list[AnalysisHistoryResponse],
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def get_history(
        limit: int = Query(20, ge=1, le=100),
        offset: int = Query(0, ge=0),
        user: dict = Depends(require_current_user),
    ) -> list[AnalysisHistoryResponse]:
        store: GraphStore = app.state.store
        rows = store.get_history_by_user(user["id"], limit=limit, offset=offset)
        return [
            AnalysisHistoryResponse(
                id=r["id"],
                drug_ids=r["drug_ids"],
                overall_risk=r["overall_risk"],
                created_at=r["created_at"],
            )
            for r in rows
        ]

    # ── Sharing Endpoints ─────────────────────────────────────────────────

    @router.post(
        "/share", response_model=SharedResultResponse, tags=["analysis"], dependencies=_api_deps
    )
    async def share_analysis(
        analysis_id: str = Query(..., description="ID of analysis_history entry to share"),
        expires_days: int = Query(7, ge=1, le=30),
        request: Request = None,
        user: dict | None = Depends(get_current_user),
    ) -> SharedResultResponse:
        store: GraphStore = app.state.store
        row = store.get_analysis_by_id(analysis_id)
        if not row:
            raise HTTPException(status_code=404, detail="Analysis not found")
        if row.get("user_id") and (user is None or row["user_id"] != user["id"]):
            raise HTTPException(status_code=403, detail="Access denied")
        share_id = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        expires_at = (now + timedelta(days=expires_days)).isoformat()
        store.create_shared_result(
            share_id=share_id,
            analysis_id=analysis_id,
            expires_at=expires_at,
            created_at=now.isoformat(),
        )
        base_url = os.environ.get("MEDGRAPH_BASE_URL", "http://localhost:8000")
        return SharedResultResponse(
            id=share_id,
            url=f"{base_url}/api/v1/shared/{share_id}",
            expires_at=expires_at,
        )

    @router.get("/shared/{token}", tags=["analysis"])
    async def get_shared(token: str) -> dict:
        """Retrieve a shared analysis result. No authentication required."""
        store: GraphStore = app.state.store
        share = store.get_shared_result(token)
        if not share:
            raise HTTPException(status_code=404, detail="Shared result not found")
        if share.get("expires_at"):
            if share["expires_at"] < datetime.now(timezone.utc).isoformat():
                raise HTTPException(status_code=410, detail="Shared result has expired")
        analysis = store.get_analysis_by_id(share["analysis_id"])
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis data not found")
        return {
            "id": share["id"],
            "expires_at": share["expires_at"],
            "analysis": {
                "id": analysis["id"],
                "drug_ids": analysis["drug_ids"],
                "overall_risk": analysis["overall_risk"],
                "created_at": analysis["created_at"],
                "result": json.loads(analysis["result_json"]),
            },
        }

    # ── Optimize Endpoint ─────────────────────────────────────────────────

    @router.post(
        "/optimize",
        response_model=OptimizeResponse,
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def optimize_regimen(request: OptimizeRequest) -> OptimizeResponse:
        """
        Optimize a polypharmacy regimen by suggesting drug removals to reduce risk.

        Accepts drug names and optional must-keep list. Returns original/optimized
        risk scores, drugs to remove, alternatives, and rationale.
        """
        drug_names = request.drugs
        if len(drug_names) < 2:
            raise HTTPException(status_code=400, detail="At least 2 drugs required")
        if len(drug_names) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 drugs")

        store: GraphStore = app.state.store
        graph = app.state.graph
        searcher: DrugSearcher = app.state.searcher

        counts = await run_in_threadpool(store.get_counts)
        if counts.get("drugs", 0) == 0:
            raise HTTPException(
                status_code=503,
                detail="Database not seeded. Run 'python -m medgraph.cli seed' first.",
            )

        # Resolve drug names → IDs
        found_drugs: list = []
        unresolved: list[str] = []
        for name in drug_names:
            matches = await run_in_threadpool(searcher.search, name, 5)
            if matches:
                found_drugs.append(matches[0])
            else:
                unresolved.append(name)

        if unresolved:
            raise HTTPException(
                status_code=400,
                detail={"message": "Some drugs were not found", "unresolved": unresolved},
            )

        # Resolve must_keep names → IDs
        must_keep_ids: list[str] = []
        for name in request.must_keep:
            matches = await run_in_threadpool(searcher.search, name, 5)
            if matches:
                must_keep_ids.append(matches[0].id)

        drug_ids = [d.id for d in found_drugs]
        optimizer = PolypharmacyOptimizer(graph, store)
        try:
            result = await run_in_threadpool(optimizer.optimize, drug_ids, must_keep_ids)
        except Exception as exc:
            logger.exception("Optimizer engine error: %s", exc)
            raise HTTPException(status_code=503, detail="Optimizer engine failed")

        return OptimizeResponse(
            original_risk=result.original_risk,
            optimized_risk=result.optimized_risk,
            drugs_to_remove=result.drugs_to_remove,
            alternative_regimens=result.alternative_regimens,
            rationale=result.rationale,
            disclaimer=result.disclaimer,
        )

    # ── Medication Schedule Optimizer ─────────────────────────────────────

    @router.post(
        "/schedule",
        response_model=ScheduleResponse,
        tags=["analysis"],
        dependencies=_api_deps,
    )
    async def optimize_schedule(request: ScheduleRequest) -> ScheduleResponse:
        """
        Compute an optimized medication schedule that minimizes interaction windows.

        Assigns each drug to time slots (morning/noon/evening/night) so that
        interacting drugs are spaced at least 4 hours apart.
        """
        store: GraphStore = app.state.store
        searcher: DrugSearcher = app.state.searcher

        # Resolve drug names → Drug objects
        drug_inputs: list[dict] = []
        unresolved: list[str] = []
        for drug_input in request.drugs:
            matches = await run_in_threadpool(searcher.search, drug_input.drug_name, 5)
            if matches:
                drug_inputs.append(
                    {
                        "drug_id": matches[0].id,
                        "drug_name": matches[0].name,
                        "frequency": drug_input.frequency,
                    }
                )
            else:
                unresolved.append(drug_input.drug_name)

        if unresolved:
            raise HTTPException(
                status_code=400,
                detail={"message": "Some drugs were not found", "unresolved": unresolved},
            )

        from medgraph.engine.schedule_optimizer import ScheduleOptimizer

        optimizer = ScheduleOptimizer(store=store)
        try:
            result = await run_in_threadpool(optimizer.optimize, drug_inputs)
        except Exception as exc:
            logger.exception("Schedule optimizer error: %s", exc)
            raise HTTPException(status_code=503, detail="Schedule optimizer failed")

        # Convert to response model
        schedule_response: dict[str, list[ScheduledDrugResponse]] = {}
        for slot, drugs in result.schedule.items():
            schedule_response[slot] = [
                ScheduledDrugResponse(
                    drug_id=d.drug_id,
                    drug_name=d.drug_name,
                    frequency=d.frequency,
                )
                for d in drugs
            ]

        return ScheduleResponse(
            schedule=schedule_response,
            warnings=result.warnings,
            disclaimer=result.disclaimer,
        )

    # ── Audit Endpoint ────────────────────────────────────────────────────

    @router.get(
        "/audit", response_model=list[AuditLogResponse], tags=["system"], dependencies=_api_deps
    )
    async def get_audit_log(
        user_id: str | None = Query(None),
        action: str | None = Query(None),
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
        _user: dict = Depends(require_current_user),
    ) -> list[AuditLogResponse]:
        """Return audit log entries. Requires authentication."""
        store: GraphStore = app.state.store
        rows = store.get_audit_logs(user_id=user_id, action=action, limit=limit, offset=offset)
        return [
            AuditLogResponse(
                id=r["id"],
                action=r["action"],
                resource_type=r.get("resource_type"),
                resource_id=r.get("resource_id"),
                created_at=r["created_at"],
            )
            for r in rows
        ]

    # Mount router at /api/v1 (canonical) and /api (backward compat)
    app.include_router(router, prefix="/api/v1")
    app.include_router(router, prefix="/api")

    # ── FHIR R4 + CDS Hooks Router ────────────────────────────────────────
    # Gracefully skip if fhir modules are unavailable (import guard).
    try:
        from medgraph.fhir.cds_hooks import CDSHooksService
        from medgraph.fhir.capability import CapabilityStatement
        from medgraph.fhir.models import CDSRequest, CDSResponse
        from medgraph.fhir.parser import FHIRParser

        fhir_router = APIRouter(tags=["fhir"])

        def _get_cds_service() -> CDSHooksService:
            return CDSHooksService(app.state.store, app.state.graph)

        # CDS Hooks discovery
        @fhir_router.get(
            "/cds-services",
            summary="CDS Hooks discovery",
            description=(
                "Returns available CDS Hooks service definitions. FOR INFORMATIONAL PURPOSES ONLY."
            ),
        )
        async def cds_services_discovery() -> dict:
            svc = _get_cds_service()
            return {"services": svc.get_services()}

        # CDS Hooks order-select handler
        @fhir_router.post(
            "/cds-services/medgraph-order-select",
            response_model=CDSResponse,
            summary="CDS Hooks: order-select",
            description=(
                "Handle order-select CDS hook. Returns educational drug interaction cards. "
                "FOR INFORMATIONAL PURPOSES ONLY — not medical advice."
            ),
        )
        async def cds_order_select(request: CDSRequest) -> CDSResponse:
            svc = _get_cds_service()
            return svc.handle_order_select(request)

        # FHIR CapabilityStatement (metadata)
        @fhir_router.get(
            "/fhir/metadata",
            summary="FHIR R4 CapabilityStatement",
            description="Returns the server's FHIR R4 CapabilityStatement.",
        )
        async def fhir_metadata() -> dict:
            return CapabilityStatement().generate()

        # FHIR MedicationRequest $check operation
        @fhir_router.post(
            "/fhir/MedicationRequest/$check",
            response_model=CheckResponse,
            summary="FHIR: Check drug interactions",
            description=(
                "Accept a FHIR MedicationRequest, MedicationStatement, or Bundle and return "
                "a MEDGRAPH interaction analysis. FOR INFORMATIONAL PURPOSES ONLY."
            ),
        )
        async def fhir_medication_check(fhir_resource: dict) -> CheckResponse:
            store: GraphStore = app.state.store
            graph = app.state.graph
            analyzer: CascadeAnalyzer = app.state.analyzer

            parser = FHIRParser(store)
            drug_ids = parser.extract_drug_ids(fhir_resource)

            if len(drug_ids) < 2:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        f"At least 2 resolvable medications required; "
                        f"found {len(drug_ids)}. Ensure medications use RxNorm CUI codes "
                        f"or names matching the MEDGRAPH drug database."
                    ),
                )

            _t0 = time.perf_counter()
            report = analyzer.analyze(drug_ids, graph, store)
            ANALYSIS_DURATION.observe(time.perf_counter() - _t0)

            enzymes_by_id = app.state.enzymes

            def _drug_resp(drug) -> DrugResponse:
                return _build_drug_response(drug, store, enzymes_by_id)

            interactions_out: list[InteractionResponse] = []
            for result in report.interactions:
                direct = result.direct_interaction
                cascade_paths_out = [
                    CascadePathResponse(
                        steps=[
                            CascadeStepResponse(
                                source=s.source_drug,
                                target=s.target,
                                relation=s.relation,
                                effect=s.effect,
                            )
                            for s in path.steps
                        ],
                        description=path.description,
                        net_severity=path.net_severity,
                    )
                    for path in result.cascade_paths
                ]
                evidence_out = [
                    EvidenceResponse(
                        source=ev.source,
                        description=ev.description,
                        case_count=ev.evidence_count,
                        url=ev.url,
                    )
                    for ev in result.evidence
                ]
                interactions_out.append(
                    InteractionResponse(
                        drug_a=_drug_resp(result.drug_a),
                        drug_b=_drug_resp(result.drug_b),
                        severity=result.severity,
                        risk_score=result.risk_score,
                        description=direct.description if direct else "",
                        mechanism=direct.mechanism if direct else None,
                        cascade_paths=cascade_paths_out,
                        evidence=evidence_out,
                    )
                )

            drugs_out = [_drug_resp(d) for d in report.drugs]

            return CheckResponse(
                drugs=drugs_out,
                interactions=interactions_out,
                overall_risk=report.overall_risk,
                overall_score=report.overall_score,
                drug_count=len(drugs_out),
                interaction_count=len(interactions_out),
                timestamp=datetime.now(timezone.utc).isoformat(),
                disclaimer=DISCLAIMER,
            )

        app.include_router(fhir_router)
        logger.info("FHIR R4 + CDS Hooks endpoints registered")

    except ImportError as _fhir_err:
        logger.warning("FHIR/CDS Hooks endpoints not available: %s", _fhir_err)

    return app


# Module-level app instance for uvicorn
app = create_app()
