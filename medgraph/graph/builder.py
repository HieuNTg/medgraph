"""
NetworkX knowledge graph builder for MEDGRAPH.

Builds a directed graph from SQLite data with drug and enzyme nodes.
The graph is small enough (~2700 drugs + ~5 main enzymes) to cache in memory.
"""

from __future__ import annotations


import networkx as nx

from medgraph.graph.store import GraphStore


class GraphBuilder:
    """
    Converts SQLite data into a NetworkX DiGraph for cascade analysis.

    Node naming convention:
        drug:{drug_id}      — Drug node
        enzyme:{enzyme_id}  — Enzyme node

    Edge labels (stored as 'relation' attribute):
        metabolized_by  — drug -> enzyme (drug is metabolized by this enzyme)
        inhibits        — drug -> enzyme (drug inhibits this enzyme)
        induces         — drug -> enzyme (drug induces/upregulates this enzyme)
        interacts_with  — drug -> drug (direct pharmacological interaction)
    """

    def build(self, store: GraphStore) -> nx.DiGraph:
        """Build full graph from all data in the store."""
        g = nx.DiGraph()

        # Add drug nodes
        for drug in store.get_all_drugs():
            g.add_node(
                f"drug:{drug.id}",
                node_type="drug",
                drug_id=drug.id,
                name=drug.name,
                drug_class=drug.drug_class or "",
            )

        # Add enzyme nodes
        for enzyme in store.get_all_enzymes():
            g.add_node(
                f"enzyme:{enzyme.id}",
                node_type="enzyme",
                enzyme_id=enzyme.id,
                name=enzyme.name,
                gene=enzyme.gene or "",
            )

        # Add drug->enzyme edges
        for rel in store.get_all_drug_enzyme_relations():
            src = f"drug:{rel.drug_id}"
            tgt = f"enzyme:{rel.enzyme_id}"
            if src in g and tgt in g:
                g.add_edge(
                    src,
                    tgt,
                    relation=rel.relation_type,
                    strength=rel.strength,
                )

        # Add food item nodes + food->enzyme edges
        food_interactions = store.get_food_interactions([drug.id for drug in store.get_all_drugs()])
        seen_foods: dict[str, dict] = {}
        for fi in food_interactions:
            food_node = f"food:{fi['food_name']}"
            if food_node not in seen_foods:
                seen_foods[food_node] = fi
                g.add_node(
                    food_node,
                    node_type="food",
                    food_id=fi["id"].rsplit("_", maxsplit=1)[0] if "_" in fi["id"] else fi["id"],
                    name=fi["food_name"],
                    category=fi["food_category"],
                )
            # food -> drug edge
            drug_node = f"drug:{fi['drug_id']}"
            if drug_node in g:
                g.add_edge(
                    food_node,
                    drug_node,
                    relation="food_interaction",
                    severity=fi["severity"],
                    mechanism=fi.get("mechanism") or "",
                )

        # Add drug->drug edges (direct interactions — bidirectional)
        for interaction in store.get_all_interactions():
            src = f"drug:{interaction.drug_a_id}"
            tgt = f"drug:{interaction.drug_b_id}"
            if src in g and tgt in g:
                attrs = dict(
                    relation="interacts_with",
                    severity=interaction.severity,
                    mechanism=interaction.mechanism or "",
                    interaction_id=interaction.id,
                    evidence_count=interaction.evidence_count,
                )
                g.add_edge(src, tgt, **attrs)
                g.add_edge(tgt, src, **attrs)  # bidirectional

        return g

    def build_subgraph(self, store: GraphStore, drug_ids: list[str]) -> nx.DiGraph:
        """
        Build a subgraph containing only the specified drugs plus their
        enzyme neighborhoods (1-hop). Faster for targeted queries.
        """
        full = self.build(store)
        nodes: set[str] = set()
        for drug_id in drug_ids:
            node = f"drug:{drug_id}"
            if node in full:
                nodes.add(node)
                # Include neighboring enzyme nodes
                for neighbor in list(full.successors(node)) + list(full.predecessors(node)):
                    nodes.add(neighbor)
                    # Also include other drugs sharing those enzymes
                    for n2 in list(full.predecessors(neighbor)):
                        if full.nodes[n2].get("node_type") == "drug":
                            nodes.add(n2)
        return full.subgraph(nodes).copy()

    def get_enzyme_neighbors(self, graph: nx.DiGraph, drug_id: str) -> set[str]:
        """
        Return drug node keys that share at least one enzyme with the given drug.
        Excludes the drug itself.
        """
        drug_node = f"drug:{drug_id}"
        if drug_node not in graph:
            return set()

        # Enzymes connected to this drug
        shared_enzymes = {
            n for n in graph.successors(drug_node) if graph.nodes[n].get("node_type") == "enzyme"
        }

        # Drugs sharing those enzymes
        neighbors: set[str] = set()
        for enzyme_node in shared_enzymes:
            for pred in graph.predecessors(enzyme_node):
                if graph.nodes[pred].get("node_type") == "drug" and pred != drug_node:
                    neighbors.add(pred)

        return neighbors
