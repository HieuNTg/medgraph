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

        # --- Step 1: Score current regimen ---
        original_risk = self._score_regimen(drug_ids)
        logger.info(f"Optimizer: original regimen risk = {original_risk:.1f}")

        current_ids = list(drug_ids)
        removed: list[str] = []
        rationale_parts: list[str] = []

        # --- Step 2-4: Greedy removal loop ---
        while True:
            if self._score_regimen(current_ids) < _ACCEPTABLE_RISK_THRESHOLD:
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
                reduction = self._score_regimen(current_ids) - reduced_risk
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

        # --- Final risk score ---
        if len(current_ids) >= 2:
            optimized_risk = self._score_regimen(current_ids)
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

    def _score_regimen(self, drug_ids: list[str]) -> float:
        """Score the overall risk of a drug regimen using CascadeAnalyzer."""
        if len(drug_ids) < 2:
            return 0.0
        try:
            report = self._analyzer.analyze(drug_ids, self.graph, self.store)
            return report.overall_score
        except Exception as exc:
            logger.warning(f"Optimizer: scoring failed for {drug_ids}: {exc}")
            return 0.0
