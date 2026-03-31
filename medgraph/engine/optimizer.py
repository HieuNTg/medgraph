"""
Polypharmacy optimizer engine for MEDGRAPH.

Given a drug regimen and optional must-keep constraints, performs greedy
risk-minimizing removal: iteratively removes the drug with the highest
marginal risk contribution until the regimen risk drops below a threshold
or only must-keep drugs remain. Suggests alternatives for removed drugs.

Usage:
    optimizer = PolypharmacyOptimizer(graph, store)
    result = optimizer.optimize(drug_ids, must_keep=["drug_id_1"])
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import networkx as nx

from medgraph.engine.alternatives import AlternativesFinder
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.engine.scorer import RiskScorer
from medgraph.graph.models import MEDICAL_DISCLAIMER
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Risk score threshold below which we consider the regimen acceptable
_ACCEPTABLE_RISK_THRESHOLD = 35.0  # "moderate" boundary


@dataclass
class OptimizationResult:
    original_risk: float
    optimized_risk: float
    drugs_to_remove: list[str]
    alternative_regimens: list[dict]
    rationale: str
    disclaimer: str = field(default=MEDICAL_DISCLAIMER)


class PolypharmacyOptimizer:
    """
    Greedy polypharmacy optimizer.

    Strategy:
    1. Score the full regimen using CascadeAnalyzer + RiskScorer.
    2. For each non-must-keep drug, compute marginal risk reduction
       by re-scoring the regimen without that drug.
    3. Remove the drug with the highest marginal reduction.
    4. Repeat until risk < threshold or no removable drugs remain.
    5. Suggest same-class alternatives for removed drugs via AlternativesFinder.
    """

    DISCLAIMER = MEDICAL_DISCLAIMER

    def __init__(self, graph: nx.DiGraph, store: GraphStore) -> None:
        self.graph = graph
        self.store = store
        self._analyzer = CascadeAnalyzer()
        self._scorer = RiskScorer()

    def optimize(
        self,
        drug_ids: list[str],
        must_keep: list[str] | None = None,
    ) -> OptimizationResult:
        """
        Optimize a drug regimen by greedily removing high-risk drugs.

        Args:
            drug_ids: Full list of drug IDs in the regimen.
            must_keep: Drug IDs that must not be removed.

        Returns:
            OptimizationResult with original/optimized scores, removed drugs,
            alternative suggestions, and a rationale string.
        """
        if len(drug_ids) < 2:
            return OptimizationResult(
                original_risk=0.0,
                optimized_risk=0.0,
                drugs_to_remove=[],
                alternative_regimens=[],
                rationale="Regimen has fewer than 2 drugs; no optimization needed.",
            )

        must_keep_set: set[str] = set(must_keep or [])

        # --- Step 1: Score current regimen (full analysis for accuracy) ---
        original_risk = self._score_regimen(drug_ids, use_full_analysis=True)
        logger.info(f"Optimizer: original regimen risk = {original_risk:.1f}")

        current_ids = list(drug_ids)
        removed: list[str] = []
        rationale_parts: list[str] = []

        # --- Step 2-4: Greedy removal loop ---
        while True:
            current_risk = self._score_regimen(current_ids)
            if current_risk < _ACCEPTABLE_RISK_THRESHOLD:
                logger.info("Optimizer: risk below threshold, stopping.")
                break

            removable = [d for d in current_ids if d not in must_keep_set]
            if not removable:
                logger.info("Optimizer: no removable drugs remain.")
                break

            if len(current_ids) < 2:
                break

            # Find drug with highest marginal risk reduction
            best_drug: str | None = None
            best_reduction = -1.0

            for candidate in removable:
                without = [d for d in current_ids if d != candidate]
                if len(without) < 2:
                    # Single drug left — score as 0 (no interactions)
                    reduced_risk = 0.0
                else:
                    reduced_risk = self._score_regimen(without)
                reduction = current_risk - reduced_risk
                if reduction > best_reduction:
                    best_reduction = reduction
                    best_drug = candidate

            if best_drug is None or best_reduction <= 0:
                logger.info("Optimizer: no beneficial removal found.")
                break

            drug_obj = self.store.get_drug_by_id(best_drug)
            drug_name = drug_obj.name if drug_obj else best_drug
            rationale_parts.append(
                f"Removing {drug_name} reduces risk score by {best_reduction:.1f} points."
            )
            removed.append(best_drug)
            current_ids.remove(best_drug)

        # --- Final risk score (full analysis for accuracy) ---
        if len(current_ids) >= 2:
            optimized_risk = self._score_regimen(current_ids, use_full_analysis=True)
        elif len(current_ids) == 1:
            optimized_risk = 0.0
        else:
            optimized_risk = 0.0

        # --- Step 5: Suggest alternatives for removed drugs ---
        alternatives_finder = AlternativesFinder(self.graph, self.store)
        alternative_regimens: list[dict] = []

        for removed_id in removed:
            alternatives = alternatives_finder.find_alternatives(
                removed_id,
                drug_ids,  # pass original regimen for context
            )
            drug_obj = self.store.get_drug_by_id(removed_id)
            drug_name = drug_obj.name if drug_obj else removed_id
            alternative_regimens.append(
                {
                    "removed_drug_id": removed_id,
                    "removed_drug_name": drug_name,
                    "alternatives": [
                        {
                            "drug_id": alt.drug_id,
                            "drug_name": alt.drug_name,
                            "reason": alt.reason,
                            "enzyme_overlap_count": alt.enzyme_overlap_count,
                        }
                        for alt in alternatives[:5]  # top 5 only
                    ],
                }
            )

        # Build rationale
        if removed:
            rationale = " ".join(rationale_parts)
            rationale += (
                f" Optimized risk score: {optimized_risk:.1f}/100 "
                f"(original: {original_risk:.1f}/100)."
            )
        else:
            rationale = (
                f"No removable drugs found that reduce risk below threshold. "
                f"Current risk: {original_risk:.1f}/100."
            )

        return OptimizationResult(
            original_risk=round(original_risk, 2),
            optimized_risk=round(optimized_risk, 2),
            drugs_to_remove=removed,
            alternative_regimens=alternative_regimens,
            rationale=rationale,
        )

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _score_regimen(self, drug_ids: list[str], use_full_analysis: bool = False) -> float:
        """Score the overall risk of a drug regimen.

        Uses lightweight graph-based scoring by default (O(drugs * enzymes))
        instead of full CascadeAnalyzer.analyze() which runs BFS + DB queries.
        Full analysis is only used for the initial and final scores.
        """
        if len(drug_ids) < 2:
            return 0.0
        try:
            if use_full_analysis:
                report = self._analyzer.analyze(drug_ids, self.graph, self.store)
                return report.overall_score

            # Lightweight scoring: count enzyme conflicts between drug pairs
            drug_nodes = [f"drug:{did}" for did in drug_ids if f"drug:{did}" in self.graph]
            if len(drug_nodes) < 2:
                return 0.0

            # Build enzyme index from graph (no DB query)
            drug_enzymes: dict[str, set[str]] = {}
            drug_relations: dict[str, dict[str, str]] = {}  # drug_node -> {enzyme: relation}
            for dn in drug_nodes:
                drug_enzymes[dn] = set()
                drug_relations[dn] = {}
                for neighbor in self.graph.successors(dn):
                    if self.graph.nodes[neighbor].get("node_type") == "enzyme":
                        edge = self.graph.edges.get((dn, neighbor), {})
                        relation = edge.get("relation", "")
                        strength = edge.get("strength", "moderate")
                        drug_enzymes[dn].add(neighbor)
                        drug_relations[dn][neighbor] = f"{relation}:{strength}"

            # Score pairwise enzyme conflicts
            total_score = 0.0
            pair_count = 0
            for i, da in enumerate(drug_nodes):
                for db in drug_nodes[i + 1 :]:
                    shared = drug_enzymes[da] & drug_enzymes[db]
                    if not shared:
                        continue
                    pair_count += 1
                    for enz in shared:
                        rel_a = drug_relations[da].get(enz, "")
                        rel_b = drug_relations[db].get(enz, "")
                        # Inhibitor + substrate = high risk
                        if ("inhibits" in rel_a and "metabolized_by" in rel_b) or (
                            "inhibits" in rel_b and "metabolized_by" in rel_a
                        ):
                            strength_bonus = (
                                20.0 if "strong" in rel_a or "strong" in rel_b else 10.0
                            )
                            total_score += 30.0 + strength_bonus
                        # Inducer + substrate = moderate risk
                        elif ("induces" in rel_a and "metabolized_by" in rel_b) or (
                            "induces" in rel_b and "metabolized_by" in rel_a
                        ):
                            total_score += 20.0
                        # Both substrates = minor competition
                        elif "metabolized_by" in rel_a and "metabolized_by" in rel_b:
                            total_score += 5.0

            return min(total_score, 100.0)
        except Exception as exc:
            logger.warning(f"Optimizer: scoring failed for {drug_ids}: {exc}")
            return 0.0
