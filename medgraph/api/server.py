"""
FastAPI server for MEDGRAPH.

Provides REST API for drug interaction analysis.
Graph and store are loaded once at startup and cached in app state.

Endpoints:
    GET  /health                                    — Health check with DB stats
    GET  /api/drugs/search                          — Search drugs by name
    GET  /api/drugs/{drug_id}                       — Get drug details
    POST /api/check                                 — Analyze drug interactions
    GET  /api/stats                                 — DB statistics (cached hourly)
    GET  /api/interactions/{interaction_id}/evidence — Evidence for an interaction
"""

from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from medgraph import __version__
from medgraph.api.models import (
    CheckRequest,
    CheckResponse,
    DrugResponse,
    EnzymeRelationResponse,
    EvidenceResponse,
    CascadePathResponse,
    CascadeStepResponse,
    HealthResponse,
    InteractionResponse,
    PDFReportRequest,
    SearchResult,
    StatsResponse,
)
from medgraph.api.search import DrugSearcher
from medgraph.engine.analyzer import CascadeAnalyzer
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
    logger.info(
        f"MEDGRAPH loaded: {counts['drugs']} drugs, "
        f"{counts['interactions']} interactions, "
        f"{graph.number_of_nodes()} graph nodes, "
        f"{graph.number_of_edges()} graph edges"
    )

    yield

    logger.info("MEDGRAPH server shutting down")


def _build_drug_response(drug: Drug, store: GraphStore) -> DrugResponse:
    """Build DrugResponse including enzyme relations with names."""
    relations = store.get_enzyme_relations(drug.id)
    enzyme_relations: list[EnzymeRelationResponse] = []
    for rel in relations:
        # Look up enzyme name
        enzyme = next((e for e in store.get_all_enzymes() if e.id == rel.enzyme_id), None)
        enzyme_name = enzyme.name if enzyme else rel.enzyme_id
        enzyme_relations.append(
            EnzymeRelationResponse(
                enzyme_name=enzyme_name,
                relation_type=rel.relation_type,
                strength=rel.strength,
            )
        )
    return DrugResponse(
        id=drug.id,
        name=drug.name,
        brand_names=drug.brand_names,
        drug_class=drug.drug_class,
        enzyme_relations=enzyme_relations,
    )


def create_app() -> FastAPI:
    """Factory function for the FastAPI application."""
    app = FastAPI(
        title="MEDGRAPH API",
        description=(
            "Drug Interaction Cascade Analyzer — knowledge graph + cascade analysis. "
            "DISCLAIMER: For research use only. Not medical advice."
        ),
        version=__version__,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        store: GraphStore = app.state.store
        graph = app.state.graph
        counts = store.get_counts()
        total = sum(counts.values())
        return HealthResponse(
            status="ok",
            db_size=total,
            graph_nodes=graph.number_of_nodes(),
        )

    @app.get("/api/stats", response_model=StatsResponse, tags=["system"])
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

    @app.get("/api/drugs/search", response_model=list[SearchResult], tags=["drugs"])
    async def search_drugs(
        q: str = Query(..., min_length=1, description="Drug name search query"),
        limit: int = Query(10, ge=1, le=50),
    ) -> list[SearchResult]:
        searcher: DrugSearcher = app.state.searcher
        results = searcher.search(q, limit=limit)
        return [
            SearchResult(
                id=drug.id,
                name=drug.name,
                brand_names=drug.brand_names,
                drug_class=drug.drug_class,
            )
            for drug in results
        ]

    @app.get("/api/drugs/{drug_id}", response_model=DrugResponse, tags=["drugs"])
    async def get_drug(drug_id: str) -> DrugResponse:
        store: GraphStore = app.state.store
        drug = store.get_drug_by_id(drug_id)
        if not drug:
            raise HTTPException(status_code=404, detail=f"Drug not found: {drug_id}")
        return _build_drug_response(drug, store)

    @app.get(
        "/api/interactions/{interaction_id}/evidence",
        response_model=list[EvidenceResponse],
        tags=["analysis"],
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

    @app.post("/api/check", response_model=CheckResponse, tags=["analysis"])
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

        # Run analysis
        report = analyzer.analyze(drug_ids, graph, store)

        # Build enzyme name cache (avoid repeated full enzyme lookups)
        all_enzymes = {e.id: e for e in store.get_all_enzymes()}

        def make_drug_response(drug) -> DrugResponse:
            relations = store.get_enzyme_relations(drug.id)
            er = [
                EnzymeRelationResponse(
                    enzyme_name=all_enzymes[rel.enzyme_id].name
                    if rel.enzyme_id in all_enzymes
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
                enzyme_relations=er,
            )

        drugs_response = [make_drug_response(d) for d in report.drugs]

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

            interactions_response.append(
                InteractionResponse(
                    drug_a=make_drug_response(result.drug_a),
                    drug_b=make_drug_response(result.drug_b),
                    severity=result.severity,
                    risk_score=result.risk_score,
                    description=description,
                    mechanism=mechanism,
                    cascade_paths=cascade_paths_resp,
                    evidence=evidence_resp,
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
        )

    @app.post("/api/report/pdf", tags=["reports"])
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

    return app


# Module-level app instance for uvicorn
app = create_app()
