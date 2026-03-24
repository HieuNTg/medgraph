"""
Shared enzyme index builder for MEDGRAPH engine modules.

Centralises the repeated logic of building an enzyme -> {inhibitors, inducers, substrates}
index from a NetworkX DiGraph for a given set of drug IDs.
"""

from __future__ import annotations

import networkx as nx


class EnzymeIndexer:
    """
    Builds an enzyme -> {inhibitors, inducers, substrates} index from a NetworkX DiGraph.

    All three sets contain drug_id strings (not graph node names).
    Only considers relations: inhibits, induces, metabolized_by.
    """

    def __init__(self, graph: nx.DiGraph) -> None:
        self.graph = graph

    def build_index(self, drug_ids: list[str]) -> dict[str, dict[str, set[str]]]:
        """
        Build enzyme index for the given drug IDs.

        Returns:
            {enzyme_id: {"inhibitors": {drug_id, ...}, "inducers": {...}, "substrates": {...}}}
        """
        drug_nodes = {f"drug:{did}" for did in drug_ids}
        index: dict[str, dict[str, set[str]]] = {}

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

                if enzyme_id not in index:
                    index[enzyme_id] = {"inhibitors": set(), "inducers": set(), "substrates": set()}

                if relation == "inhibits":
                    index[enzyme_id]["inhibitors"].add(drug_id)
                elif relation == "induces":
                    index[enzyme_id]["inducers"].add(drug_id)
                elif relation == "metabolized_by":
                    index[enzyme_id]["substrates"].add(drug_id)

        return index
