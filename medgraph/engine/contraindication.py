"""
Contraindication network builder for MEDGRAPH.

Builds a conflict network for a drug regimen by analysing direct interactions
and shared-enzyme cascade paths. Returns a graph-ready structure suitable for
visualisation or further analysis.
"""

from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass, field

import networkx as nx

from medgraph.engine.enzyme_indexer import EnzymeIndexer
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

_SEVERITY_ORDER: dict[str, int] = {
    "critical": 4,
    "major": 3,
    "moderate": 2,
    "minor": 1,
    "none": 0,
}


@dataclass
class ContraindicationEdge:
    drug_a_id: str
    drug_b_id: str
    severity: str
    mechanism: str
    via_enzymes: list[str] = field(default_factory=list)


class ContraindicationNetwork:
    """
    Builds a contraindication conflict network for a set of regimen drugs.

    Checks every pair of drugs for:
    1. Direct DB interactions (from GraphStore).
    2. Shared enzyme cascade paths (inhibitor/inducer → shared substrate).

    Returns a dict suitable for front-end graph rendering.
    """

    def __init__(self, graph: nx.DiGraph, store: GraphStore) -> None:
        self.graph = graph
        self.store = store

    def build_network(self, drug_ids: list[str]) -> dict:
        """
        Build a conflict network for the given drug regimen.

        Args:
            drug_ids: List of drug IDs in the regimen.

        Returns:
            {
                nodes: [{"id": str, "name": str, "drug_class": str}, ...],
                edges: [ContraindicationEdge as dict, ...],
                clusters: [{"enzyme": str, "drugs": [str, ...]}, ...],
            }
        """
        if len(drug_ids) < 2:
            return {"nodes": [], "edges": [], "clusters": []}

        # Resolve drug metadata
        drug_map = {}
        for did in drug_ids:
            drug = self.store.get_drug_by_id(did)
            if drug:
                drug_map[did] = drug
            else:
                logger.warning(f"ContraindicationNetwork: drug not found: {did}")

        resolved_ids = list(drug_map.keys())
        if len(resolved_ids) < 2:
            return {"nodes": [], "edges": [], "clusters": []}

        # Build nodes
        nodes = [
            {
                "id": d.id,
                "name": d.name,
                "drug_class": d.drug_class or "",
            }
            for d in drug_map.values()
        ]

        # Load direct interactions (single batch query)
        direct_interactions = self.store.get_interactions_for_drugs(resolved_ids)
        direct_lookup: dict[frozenset, list] = {}
        for intr in direct_interactions:
            key = frozenset([intr.drug_a_id, intr.drug_b_id])
            direct_lookup.setdefault(key, []).append(intr)

        # Build enzyme index from graph for cascade detection
        # enzyme_id -> {"inhibitors": set, "inducers": set, "substrates": set}
        enzyme_index = self._build_enzyme_index(resolved_ids)

        edges: list[ContraindicationEdge] = []
        seen_pairs: set[frozenset] = set()

        for drug_a_id, drug_b_id in itertools.combinations(resolved_ids, 2):
            pair_key = frozenset([drug_a_id, drug_b_id])
            if pair_key in seen_pairs:
                continue
            seen_pairs.add(pair_key)

            # Check direct interactions
            direct = direct_lookup.get(pair_key, [])
            via_direct = [
                ContraindicationEdge(
                    drug_a_id=drug_a_id,
                    drug_b_id=drug_b_id,
                    severity=intr.severity,
                    mechanism=intr.mechanism or intr.description[:120],
                    via_enzymes=[],
                )
                for intr in direct
            ]
            edges.extend(via_direct)

            # Check cascade paths via shared enzymes
            cascade_edges = self._detect_cascade_conflicts(drug_a_id, drug_b_id, enzyme_index)
            # Merge cascade edges that don't already have a direct entry at same severity
            direct_severities = {e.severity for e in via_direct}
            for ce in cascade_edges:
                if not via_direct or ce.severity not in direct_severities:
                    edges.append(ce)

        # Build enzyme clusters: groups of 3+ drugs sharing a single enzyme
        clusters = self._build_clusters(resolved_ids, enzyme_index, drug_map)

        return {
            "nodes": nodes,
            "edges": [self._edge_to_dict(e) for e in edges],
            "clusters": clusters,
        }

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _build_enzyme_index(self, drug_ids: list[str]) -> dict[str, dict[str, set[str]]]:
        """
        Build enzyme → {inhibitors, inducers, substrates} index from graph nodes.
        Only considers drugs in drug_ids.
        """
        return EnzymeIndexer(self.graph).build_index(drug_ids)

    def _detect_cascade_conflicts(
        self,
        drug_a_id: str,
        drug_b_id: str,
        enzyme_index: dict[str, dict[str, set[str]]],
    ) -> list[ContraindicationEdge]:
        """
        Detect cascade conflicts between two drugs via shared enzymes.
        Returns one edge per enzyme where a conflict pattern is found.
        """
        conflicts: list[ContraindicationEdge] = []

        for enzyme_id, groups in enzyme_index.items():
            inhibitors = groups["inhibitors"]
            inducers = groups["inducers"]
            substrates = groups["substrates"]

            # Pattern 1: A inhibits enzyme, B is substrate (or vice versa)
            if (drug_a_id in inhibitors and drug_b_id in substrates) or (
                drug_b_id in inhibitors and drug_a_id in substrates
            ):
                inhibitor = drug_a_id if drug_a_id in inhibitors else drug_b_id
                substrate = drug_b_id if drug_a_id in inhibitors else drug_a_id
                conflicts.append(
                    ContraindicationEdge(
                        drug_a_id=inhibitor,
                        drug_b_id=substrate,
                        severity="major",
                        mechanism=(
                            f"Enzyme inhibition cascade via {enzyme_id}: "
                            f"inhibitor reduces {enzyme_id} activity, substrate accumulates."
                        ),
                        via_enzymes=[enzyme_id],
                    )
                )

            # Pattern 2: A induces enzyme, B is substrate (or vice versa)
            elif (drug_a_id in inducers and drug_b_id in substrates) or (
                drug_b_id in inducers and drug_a_id in substrates
            ):
                inducer = drug_a_id if drug_a_id in inducers else drug_b_id
                substrate = drug_b_id if drug_a_id in inducers else drug_a_id
                conflicts.append(
                    ContraindicationEdge(
                        drug_a_id=inducer,
                        drug_b_id=substrate,
                        severity="moderate",
                        mechanism=(
                            f"Enzyme induction cascade via {enzyme_id}: "
                            f"inducer increases {enzyme_id} activity, substrate depleted."
                        ),
                        via_enzymes=[enzyme_id],
                    )
                )

        return conflicts

    def _build_clusters(
        self,
        drug_ids: list[str],
        enzyme_index: dict[str, dict[str, set[str]]],
        drug_map: dict,
    ) -> list[dict]:
        """
        Find enzyme clusters: shared enzymes involving 3+ drugs.
        Each cluster groups drugs that all interact with the same enzyme.
        """
        clusters: list[dict] = []
        for enzyme_id, groups in enzyme_index.items():
            involved = groups["inhibitors"] | groups["inducers"] | groups["substrates"]
            involved_in_regimen = [d for d in involved if d in drug_map]
            if len(involved_in_regimen) >= 3:
                clusters.append(
                    {
                        "enzyme": enzyme_id,
                        "drugs": sorted(involved_in_regimen),
                        "drug_names": [
                            drug_map[d].name for d in sorted(involved_in_regimen) if d in drug_map
                        ],
                    }
                )
        return clusters

    @staticmethod
    def _edge_to_dict(edge: ContraindicationEdge) -> dict:
        return {
            "drug_a_id": edge.drug_a_id,
            "drug_b_id": edge.drug_b_id,
            "severity": edge.severity,
            "mechanism": edge.mechanism,
            "via_enzymes": edge.via_enzymes,
        }
