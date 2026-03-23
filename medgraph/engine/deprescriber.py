"""
Deprescribing recommendation engine for MEDGRAPH.

Computes which drug(s) in a polypharmacy regimen, if removed, would most
reduce overall interaction risk. Uses the same cascade-detection patterns
as CascadeAnalyzer but focused on marginal benefit of removal.

MEDICAL DISCLAIMER: Recommendations are for informational purposes only and
do NOT constitute medical advice. Deprescribing decisions must be made by a
licensed healthcare professional in consultation with the patient.
"""

from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass

import networkx as nx

from medgraph.graph.models import MEDICAL_DISCLAIMER
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

_SEVERITY_WEIGHTS: dict[str, float] = {
    "critical": 90.0,
    "major": 70.0,
    "moderate": 40.0,
    "minor": 15.0,
    "none": 0.0,
}


@dataclass
class DeprescribingRecommendation:
    drug_id: str
    drug_name: str
    removal_benefit: float  # reduction in total regimen risk score (0–100)
    interactions_resolved: int
    rationale: str
    order: int  # suggested removal priority (1 = highest benefit)


class Deprescriber:
    """
    Recommends which drugs in a regimen to deprescribe first, based on
    the estimated reduction in total interaction risk upon removal.

    Algorithm:
    - Compute a "regimen interaction score" (sum of pairwise severity weights).
    - For each drug, re-compute the score with that drug removed.
    - removal_benefit = original_score − reduced_score.
    - Rank by highest benefit first.
    """

    def __init__(self, graph: nx.DiGraph, store: GraphStore) -> None:
        self.graph = graph
        self.store = store

    def recommend(self, drug_ids: list[str]) -> list[DeprescribingRecommendation]:
        """
        For each drug in the regimen, compute the removal benefit and return
        ordered deprescribing recommendations.

        Args:
            drug_ids: List of drug IDs in the current regimen.

        Returns:
            List of DeprescribingRecommendation sorted by removal_benefit descending.
            Includes medical disclaimer in each rationale.
        """
        if len(drug_ids) < 2:
            return []

        # Resolve drugs
        drug_map = {}
        for did in drug_ids:
            drug = self.store.get_drug_by_id(did)
            if drug:
                drug_map[did] = drug
            else:
                logger.warning(f"Deprescriber: drug not found: {did}")

        resolved = list(drug_map.keys())
        if len(resolved) < 2:
            return []

        # Batch-load interactions once
        all_interactions = self.store.get_interactions_for_drugs(resolved)
        interaction_lookup: dict[frozenset, str] = {}
        for intr in all_interactions:
            key = frozenset([intr.drug_a_id, intr.drug_b_id])
            # Keep highest severity
            existing = interaction_lookup.get(key, "none")
            if _SEVERITY_WEIGHTS.get(intr.severity, 0) > _SEVERITY_WEIGHTS.get(existing, 0):
                interaction_lookup[key] = intr.severity

        # Also detect cascade conflicts via enzyme index
        enzyme_conflicts = self._build_cascade_conflict_lookup(resolved)

        # Compute base regimen score
        base_score, base_count = self._score_regimen(resolved, interaction_lookup, enzyme_conflicts)

        recommendations: list[DeprescribingRecommendation] = []
        for drug_id in resolved:
            reduced_ids = [d for d in resolved if d != drug_id]
            reduced_score, reduced_count = self._score_regimen(
                reduced_ids, interaction_lookup, enzyme_conflicts
            )
            interactions_resolved = base_count - reduced_count
            benefit = max(0.0, base_score - reduced_score)

            drug_name = drug_map[drug_id].name

            if benefit > 50:
                impact = "major"
            elif benefit > 20:
                impact = "moderate"
            else:
                impact = "minor"

            rationale = (
                f"Removing {drug_name} is estimated to resolve "
                f"{interactions_resolved} interaction(s) and reduce overall "
                f"regimen risk by approximately {benefit:.1f} points ({impact} impact). "
                f"DISCLAIMER: {MEDICAL_DISCLAIMER}"
            )

            recommendations.append(
                DeprescribingRecommendation(
                    drug_id=drug_id,
                    drug_name=drug_name,
                    removal_benefit=round(benefit, 2),
                    interactions_resolved=interactions_resolved,
                    rationale=rationale,
                    order=0,  # assigned below after sorting
                )
            )

        # Sort by benefit descending; assign removal order
        recommendations.sort(key=lambda r: r.removal_benefit, reverse=True)
        for i, rec in enumerate(recommendations, start=1):
            rec.order = i

        return recommendations

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _score_regimen(
        self,
        drug_ids: list[str],
        interaction_lookup: dict[frozenset, str],
        cascade_lookup: dict[frozenset, str],
    ) -> tuple[float, int]:
        """
        Compute total severity-weighted interaction score for a drug set.
        Returns (total_score, interaction_count).
        """
        total = 0.0
        count = 0
        for a, b in itertools.combinations(drug_ids, 2):
            key = frozenset([a, b])
            # Use direct interaction severity if present, else cascade severity
            severity = interaction_lookup.get(key) or cascade_lookup.get(key) or "none"
            weight = _SEVERITY_WEIGHTS.get(severity, 0.0)
            if weight > 0:
                total += weight
                count += 1
        return total, count

    def _build_cascade_conflict_lookup(self, drug_ids: list[str]) -> dict[frozenset, str]:
        """
        Build pair → severity dict for enzyme cascade conflicts among drug_ids.
        Uses the same inhibitor/inducer/substrate patterns as ContraindicationNetwork.
        """
        # enzyme_id -> {inhibitors, inducers, substrates} for these drugs only
        enzyme_index: dict[str, dict[str, set[str]]] = {}
        drug_nodes = {f"drug:{did}" for did in drug_ids}

        for drug_node in drug_nodes:
            if drug_node not in self.graph:
                continue
            drug_id = self.graph.nodes[drug_node].get("drug_id", drug_node.replace("drug:", ""))
            for enzyme_node in self.graph.successors(drug_node):
                if self.graph.nodes[enzyme_node].get("node_type") != "enzyme":
                    continue
                enzyme_id = self.graph.nodes[enzyme_node].get(
                    "enzyme_id", enzyme_node.replace("enzyme:", "")
                )
                edge = self.graph.edges.get((drug_node, enzyme_node), {})
                relation = edge.get("relation", "")
                if relation not in ("inhibits", "induces", "metabolized_by"):
                    continue
                if enzyme_id not in enzyme_index:
                    enzyme_index[enzyme_id] = {
                        "inhibitors": set(),
                        "inducers": set(),
                        "substrates": set(),
                    }
                if relation == "inhibits":
                    enzyme_index[enzyme_id]["inhibitors"].add(drug_id)
                elif relation == "induces":
                    enzyme_index[enzyme_id]["inducers"].add(drug_id)
                elif relation == "metabolized_by":
                    enzyme_index[enzyme_id]["substrates"].add(drug_id)

        conflicts: dict[frozenset, str] = {}
        for enzyme_id, groups in enzyme_index.items():
            # Inhibitor → substrate cascades (major)
            for inh in groups["inhibitors"]:
                for sub in groups["substrates"]:
                    if inh == sub:
                        continue
                    key = frozenset([inh, sub])
                    existing = conflicts.get(key, "none")
                    if _SEVERITY_WEIGHTS["major"] > _SEVERITY_WEIGHTS.get(existing, 0):
                        conflicts[key] = "major"
            # Inducer → substrate cascades (moderate)
            for ind in groups["inducers"]:
                for sub in groups["substrates"]:
                    if ind == sub:
                        continue
                    key = frozenset([ind, sub])
                    existing = conflicts.get(key, "none")
                    if _SEVERITY_WEIGHTS["moderate"] > _SEVERITY_WEIGHTS.get(existing, 0):
                        conflicts[key] = "moderate"

        return conflicts
