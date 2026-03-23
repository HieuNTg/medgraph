"""
Drug alternative suggestion engine for MEDGRAPH.

Finds same-class drugs that avoid conflicting enzyme pathways with a given regimen.
Used to suggest therapeutic swaps when a drug causes interactions.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import networkx as nx

from medgraph.graph.models import DrugEnzymeRelation
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Evidence level ordering (best = lowest index)
_EVIDENCE_ORDER = ["A", "B", "C", "D"]


@dataclass
class Alternative:
    drug_id: str
    drug_name: str
    reason: str
    enzyme_overlap_count: int
    evidence_quality: str  # best evidence level among alternatives


class AlternativesFinder:
    """
    Suggests same-class drug alternatives that minimize enzyme conflicts
    with the rest of a patient's regimen.

    Strategy:
    1. Identify which enzymes the target drug uses.
    2. Identify which enzymes the regimen drugs (excluding target) use.
    3. Find same drug_class candidates from the store.
    4. Rank candidates by fewest shared enzymes with regimen.
    """

    def __init__(self, graph: nx.DiGraph, store: GraphStore) -> None:
        self.graph = graph
        self.store = store

    def find_alternatives(
        self, drug_id: str, regimen: list[str]
    ) -> list[Alternative]:
        """
        For a drug causing interactions in a regimen, find same-class alternatives
        that share fewer enzyme conflicts with the rest of the regimen.

        Args:
            drug_id: ID of the drug to replace.
            regimen: Full list of drug IDs in the regimen (including drug_id).

        Returns:
            List of Alternative objects sorted by enzyme_overlap_count ascending.
            Empty list if drug class unknown or no alternatives found.
        """
        target_drug = self.store.get_drug_by_id(drug_id)
        if not target_drug:
            logger.warning(f"AlternativesFinder: drug not found: {drug_id}")
            return []

        target_class = target_drug.drug_class
        if not target_class:
            logger.info(f"AlternativesFinder: no drug_class for {drug_id}")
            return []

        # Build enzyme index from store (one query)
        all_relations = self.store.get_all_drug_enzyme_relations()
        # drug_id -> set of enzyme_ids used
        enzyme_index: dict[str, set[str]] = {}
        for rel in all_relations:
            enzyme_index.setdefault(rel.drug_id, set()).add(rel.enzyme_id)

        # Collect enzymes used by regimen (excluding the target drug)
        regimen_enzymes: set[str] = set()
        for rid in regimen:
            if rid != drug_id:
                regimen_enzymes.update(enzyme_index.get(rid, set()))

        # Get all drugs and filter to same class, excluding target + regimen members
        regimen_set = set(regimen)
        all_drugs = self.store.get_all_drugs()

        alternatives: list[Alternative] = []
        for candidate in all_drugs:
            if candidate.id in regimen_set:
                continue
            if candidate.drug_class != target_class:
                continue

            candidate_enzymes = enzyme_index.get(candidate.id, set())
            overlap = candidate_enzymes & regimen_enzymes
            overlap_count = len(overlap)

            if overlap_count == 0:
                reason = (
                    f"Same class ({target_class}) as {target_drug.name}; "
                    "no shared enzyme pathways with current regimen."
                )
            else:
                enzyme_list = ", ".join(sorted(overlap))
                reason = (
                    f"Same class ({target_class}) as {target_drug.name}; "
                    f"shares {overlap_count} enzyme(s) with regimen: {enzyme_list}."
                )

            alternatives.append(
                Alternative(
                    drug_id=candidate.id,
                    drug_name=candidate.name,
                    reason=reason,
                    enzyme_overlap_count=overlap_count,
                    evidence_quality="D",  # No direct evidence scoring here; placeholder
                )
            )

        # Sort: fewest overlaps first, then alphabetically for stability
        alternatives.sort(key=lambda a: (a.enzyme_overlap_count, a.drug_name))
        return alternatives
