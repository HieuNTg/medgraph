"""Tests for medgraph.engine.enzyme_indexer.EnzymeIndexer."""

from __future__ import annotations

import networkx as nx

from medgraph.engine.enzyme_indexer import EnzymeIndexer


# ---------------------------------------------------------------------------
# Graph fixtures
# ---------------------------------------------------------------------------


def _make_graph() -> nx.DiGraph:
    """
    Minimal knowledge graph with:
      Drug A --inhibits--> CYP3A4
      Drug B --metabolized_by--> CYP3A4
      Drug C --induces--> CYP2D6
      Drug D --metabolized_by--> CYP2D6
    """
    g = nx.DiGraph()
    g.add_node("drug:A", node_type="drug", drug_id="A", name="DrugA")
    g.add_node("drug:B", node_type="drug", drug_id="B", name="DrugB")
    g.add_node("drug:C", node_type="drug", drug_id="C", name="DrugC")
    g.add_node("drug:D", node_type="drug", drug_id="D", name="DrugD")
    g.add_node("enzyme:CYP3A4", node_type="enzyme", enzyme_id="CYP3A4", name="CYP3A4")
    g.add_node("enzyme:CYP2D6", node_type="enzyme", enzyme_id="CYP2D6", name="CYP2D6")

    g.add_edge("drug:A", "enzyme:CYP3A4", relation="inhibits", strength="strong")
    g.add_edge("drug:B", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
    g.add_edge("drug:C", "enzyme:CYP2D6", relation="induces", strength="moderate")
    g.add_edge("drug:D", "enzyme:CYP2D6", relation="metabolized_by", strength="weak")
    return g


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEnzymeIndexer:
    def test_enzyme_indexer_builds_substrate_map(self) -> None:
        """Drugs with metabolized_by edges appear in the substrates set."""
        g = _make_graph()
        indexer = EnzymeIndexer(g)
        index = indexer.build_index(["A", "B", "C", "D"])

        assert "CYP3A4" in index, "CYP3A4 should be indexed"
        assert "B" in index["CYP3A4"]["substrates"], "DrugB should be a substrate of CYP3A4"
        assert "D" in index["CYP2D6"]["substrates"], "DrugD should be a substrate of CYP2D6"

    def test_enzyme_indexer_builds_inhibitor_map(self) -> None:
        """Drugs with inhibits/induces edges appear in the correct sets."""
        g = _make_graph()
        indexer = EnzymeIndexer(g)
        index = indexer.build_index(["A", "B", "C", "D"])

        assert "A" in index["CYP3A4"]["inhibitors"], "DrugA should be an inhibitor of CYP3A4"
        # DrugA should NOT appear in substrates or inducers for CYP3A4
        assert "A" not in index["CYP3A4"]["substrates"]
        assert "A" not in index["CYP3A4"]["inducers"]

        assert "C" in index["CYP2D6"]["inducers"], "DrugC should be an inducer of CYP2D6"
        assert "C" not in index["CYP2D6"]["inhibitors"]
        assert "C" not in index["CYP2D6"]["substrates"]

    def test_enzyme_indexer_empty_graph(self) -> None:
        """Empty graph with no nodes returns an empty index dict."""
        g = nx.DiGraph()
        indexer = EnzymeIndexer(g)
        index = indexer.build_index(["X", "Y", "Z"])
        assert index == {}, f"Expected empty index, got {index}"

    def test_enzyme_indexer_partial_drug_ids(self) -> None:
        """Only requested drug IDs are indexed — extra drugs in graph are ignored."""
        g = _make_graph()
        indexer = EnzymeIndexer(g)
        # Only request drugs A and B (not C or D)
        index = indexer.build_index(["A", "B"])

        assert "CYP3A4" in index
        # CYP2D6 should NOT appear because C and D were not requested
        assert "CYP2D6" not in index, "CYP2D6 should not appear when C/D are not in drug_ids"

    def test_enzyme_indexer_drug_not_in_graph(self) -> None:
        """Drug IDs not present in the graph are silently skipped."""
        g = _make_graph()
        indexer = EnzymeIndexer(g)
        # "Z" does not exist in graph
        index = indexer.build_index(["A", "Z"])

        # "A" edges should still be indexed correctly
        assert "CYP3A4" in index
        assert "A" in index["CYP3A4"]["inhibitors"]

    def test_enzyme_indexer_sets_are_disjoint_per_role(self) -> None:
        """A drug ID appears in at most one role set per enzyme."""
        g = _make_graph()
        indexer = EnzymeIndexer(g)
        index = indexer.build_index(["A", "B", "C", "D"])

        for enzyme_id, roles in index.items():
            inhibitors = roles["inhibitors"]
            inducers = roles["inducers"]
            # Sets should be disjoint (a drug can't both inhibit and induce same enzyme here)
            assert not (inhibitors & inducers), f"{enzyme_id}: same drug in inhibitors AND inducers"
