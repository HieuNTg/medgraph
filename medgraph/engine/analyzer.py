"""
Cascade Analyzer — core drug interaction analysis engine for MEDGRAPH.

Algorithm:
1. Direct lookup: check pairwise interactions from DB
2. Enzyme cascade detection: find shared enzymes, detect inhibition/induction cascades
3. Multi-hop BFS: max depth 3, find paths through enzyme nodes between input drugs
4. Score and classify all interactions
5. Generate structured InteractionReport

Usage:
    analyzer = CascadeAnalyzer()
    report = analyzer.analyze(drug_ids, graph, store)
"""

from __future__ import annotations

import itertools
import logging

import networkx as nx

from medgraph.engine.models import (
    CascadePath,
    DrugInteractionResult,
    EvidenceItem,
    InteractionReport,
)
from medgraph.engine.pathfinder import PathFinder
from medgraph.engine.scorer import RiskScorer
from medgraph.graph.models import AdverseEvent, Drug, Interaction, MEDICAL_DISCLAIMER
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

MAX_DRUG_PAIRS = 45  # n*(n-1)/2 for n=10 = 45


class CascadeAnalyzer:
    """
    Main entry point for multi-drug interaction cascade analysis.

    Takes a list of drug IDs, the pre-built NetworkX graph, and the GraphStore,
    and returns a comprehensive InteractionReport.
    """

    def __init__(self) -> None:
        self.pathfinder = PathFinder()
        self.scorer = RiskScorer()

    def analyze(
        self,
        drug_ids: list[str],
        graph: nx.DiGraph,
        store: GraphStore,
    ) -> InteractionReport:
        """
        Perform complete cascade analysis for a set of drugs.

        Args:
            drug_ids: List of drug IDs to analyze (max ~10 for performance)
            graph: NetworkX DiGraph from GraphBuilder.build()
            store: GraphStore for direct DB lookups

        Returns:
            InteractionReport with all interactions, cascades, scores, and disclaimer
        """
        if not drug_ids:
            return self._empty_report([])

        # Resolve drugs from store
        drugs: list[Drug] = []
        resolved_ids: list[str] = []
        for drug_id in drug_ids:
            drug = store.get_drug_by_id(drug_id)
            if drug:
                drugs.append(drug)
                resolved_ids.append(drug_id)
            else:
                logger.warning(f"Drug not found in store: {drug_id}")

        if len(drugs) < 2:
            return self._empty_report(drugs)

        # Generate all drug pairs
        pairs = list(itertools.combinations(resolved_ids, 2))
        if len(pairs) > MAX_DRUG_PAIRS:
            logger.warning(f"Too many drug pairs ({len(pairs)}), truncating to {MAX_DRUG_PAIRS}")
            pairs = pairs[:MAX_DRUG_PAIRS]

        # --- Batch-load all data upfront (avoids N*45 DB queries) ---
        drug_map: dict[str, Drug] = {d.id: d for d in drugs}

        # Load all interactions involving any of the input drugs in ONE query
        all_interactions = store.get_interactions_for_drugs(resolved_ids)
        # Build lookup: (sorted pair) -> Interaction
        interaction_lookup: dict[frozenset, Interaction] = {}
        for intr in all_interactions:
            key = frozenset([intr.drug_a_id, intr.drug_b_id])
            if key not in interaction_lookup or (
                intr.severity in ("critical", "major")
                and interaction_lookup[key].severity in ("moderate", "minor")
            ):
                interaction_lookup[key] = intr

        # Load all adverse events in ONE query
        all_adverse = store.get_adverse_events(resolved_ids)

        # Find all cascade paths once (across all drugs)
        all_cascade_paths = self.pathfinder.find_cascade_paths(graph, resolved_ids)

        # Analyze each pair using pre-loaded data (no further DB queries)
        results: list[DrugInteractionResult] = []
        for drug_a_id, drug_b_id in pairs:
            drug_a = drug_map.get(drug_a_id)
            drug_b = drug_map.get(drug_b_id)
            if not drug_a or not drug_b:
                continue

            result = self._analyze_pair_fast(
                drug_a, drug_b, all_cascade_paths, interaction_lookup, all_adverse
            )
            results.append(result)

        # Score all results
        for result in results:
            result.risk_score = self.scorer.score_interaction(result, store)
            result.severity = self.scorer.classify_severity(result.risk_score)

        # Sort results by risk score (highest first)
        results.sort(key=lambda r: r.risk_score, reverse=True)

        # Build report
        overall_score = self.scorer.score_report(
            InteractionReport(
                drugs=drugs,
                interactions=results,
                overall_risk="minor",
                overall_score=0.0,
            )
        )
        overall_risk = self.scorer.classify_severity(overall_score)

        report = InteractionReport(
            drugs=drugs,
            interactions=results,
            overall_risk=overall_risk,
            overall_score=overall_score,
            disclaimer=MEDICAL_DISCLAIMER,
        )
        return report

    def analyze_by_names(
        self,
        drug_names: list[str],
        graph: nx.DiGraph,
        store: GraphStore,
    ) -> InteractionReport:
        """
        Convenience method: analyze by drug names instead of IDs.

        Looks up each name in the store (case-insensitive). Names not found
        are logged as warnings.
        """
        drug_ids: list[str] = []
        for name in drug_names:
            drug = store.get_drug_by_name(name)
            if drug:
                drug_ids.append(drug.id)
            else:
                logger.warning(f"Drug not found by name: {name!r}")
        return self.analyze(drug_ids, graph, store)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _analyze_pair_fast(
        self,
        drug_a: Drug,
        drug_b: Drug,
        all_cascade_paths: list[CascadePath],
        interaction_lookup: dict[frozenset, Interaction],
        all_adverse: list[AdverseEvent],
    ) -> DrugInteractionResult:
        """
        Fast pair analysis using pre-loaded data (no DB queries).
        Called by analyze() after batch-loading all data upfront.
        """
        # Direct interaction from lookup
        direct = interaction_lookup.get(frozenset([drug_a.id, drug_b.id]))

        # Filter cascade paths for this pair
        pair_cascades = [
            p
            for p in all_cascade_paths
            if (
                p.drug_a_name.lower() == drug_a.name.lower()
                and p.drug_b_name.lower() == drug_b.name.lower()
            )
            or (
                p.drug_a_name.lower() == drug_b.name.lower()
                and p.drug_b_name.lower() == drug_a.name.lower()
            )
        ]

        # Build evidence from pre-loaded data
        evidence: list[EvidenceItem] = []
        if direct:
            evidence.append(
                EvidenceItem(
                    source=direct.source,
                    description=direct.description,
                    evidence_count=direct.evidence_count,
                )
            )
        for ae in all_adverse:
            if drug_a.id in ae.drug_ids and drug_b.id in ae.drug_ids:
                evidence.append(
                    EvidenceItem(
                        source="faers",
                        description=f"FAERS: {ae.reaction} ({ae.seriousness})",
                        evidence_count=ae.count,
                        url=ae.source_url,
                    )
                )

        return DrugInteractionResult(
            drug_a=drug_a,
            drug_b=drug_b,
            direct_interaction=direct,
            cascade_paths=pair_cascades,
            evidence=evidence,
        )

    def _empty_report(self, drugs: list[Drug]) -> InteractionReport:
        """Return an empty report for invalid inputs."""
        return InteractionReport(
            drugs=drugs,
            interactions=[],
            overall_risk="minor",
            overall_score=0.0,
            disclaimer=MEDICAL_DISCLAIMER,
        )
