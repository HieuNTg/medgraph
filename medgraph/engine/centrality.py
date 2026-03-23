"""
Hub drug identification via graph centrality for MEDGRAPH.

Computes betweenness centrality and PageRank on the drug-enzyme knowledge graph
to identify pharmacokinetically influential ("hub") drugs.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import networkx as nx

logger = logging.getLogger(__name__)


@dataclass
class HubDrug:
    drug_id: str
    drug_name: str
    betweenness: float
    pagerank: float
    interaction_count: int  # out-degree in the graph (enzyme + drug edges)


class CentralityAnalyzer:
    """
    Identifies hub drugs in the knowledge graph using standard network metrics.

    Betweenness centrality: drugs that frequently sit on shortest paths
    (strong mediators of pharmacokinetic cascades).

    PageRank: drugs that are highly connected to other well-connected nodes
    (globally influential drugs in the network).
    """

    def __init__(self, graph: nx.DiGraph) -> None:
        self.graph = graph

    def hub_drugs(self, top_n: int = 20) -> list[HubDrug]:
        """
        Compute betweenness centrality and PageRank; return top_n drug nodes.

        Args:
            top_n: Number of hub drugs to return.

        Returns:
            List of HubDrug sorted by combined score (betweenness + pagerank) descending.
        """
        if not self.graph or self.graph.number_of_nodes() == 0:
            return []

        # Compute metrics on the full graph (drug + enzyme nodes)
        betweenness: dict[str, float] = nx.betweenness_centrality(self.graph, normalized=True)
        pagerank: dict[str, float] = nx.pagerank(self.graph, alpha=0.85, max_iter=100)

        results: list[HubDrug] = []
        for node, data in self.graph.nodes(data=True):
            if data.get("node_type") != "drug":
                continue

            drug_id = data.get("drug_id", node.replace("drug:", ""))
            drug_name = data.get("name", drug_id)
            b_score = betweenness.get(node, 0.0)
            pr_score = pagerank.get(node, 0.0)
            # interaction_count = total edges (in + out) from this drug node
            in_deg = self.graph.in_degree(node)
            out_deg = self.graph.out_degree(node)
            interaction_count = (in_deg if isinstance(in_deg, int) else 0) + (
                out_deg if isinstance(out_deg, int) else 0
            )

            results.append(
                HubDrug(
                    drug_id=drug_id,
                    drug_name=drug_name,
                    betweenness=round(b_score, 6),
                    pagerank=round(pr_score, 6),
                    interaction_count=interaction_count,
                )
            )

        # Sort by combined score (equal weighting), descending
        results.sort(key=lambda h: h.betweenness + h.pagerank, reverse=True)
        return results[:top_n]
