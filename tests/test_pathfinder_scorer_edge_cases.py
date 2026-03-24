"""Edge case tests for PathFinder and RiskScorer."""

import networkx as nx
import pytest
from medgraph.engine.models import (
    CascadePath,
    CascadeStep,
    DrugInteractionResult,
    InteractionReport,
)
from medgraph.engine.pathfinder import PathFinder
from medgraph.engine.scorer import RiskScorer
from medgraph.graph.models import Drug, Interaction


# --------------- helpers ---------------


def _drug(i, name):
    return Drug(id=i, name=name)


def _interaction(a, b, sev, ev=0):
    return Interaction(
        id=f"{a}-{b}",
        drug_a_id=a,
        drug_b_id=b,
        severity=sev,
        description="test",
        source="seed",
        evidence_count=ev,
    )


def _step(relation, strength="moderate"):
    return CascadeStep(
        source_drug="DrugA",
        target="CYP3A4",
        target_type="enzyme",
        relation=relation,
        strength=strength,
        effect="effect",
    )


def _cascade(severity, steps=None):
    return CascadePath(
        steps=steps or [_step("inhibits")],
        net_severity=severity,
        description="test cascade",
        drug_a_name="DrugA",
        drug_b_name="DrugB",
    )


def _result(sev="none", cascades=None, ev=0):
    a, b = _drug("DA", "DrugA"), _drug("DB", "DrugB")
    direct = _interaction("DA", "DB", sev, ev) if sev != "none" else None
    return DrugInteractionResult(
        drug_a=a, drug_b=b, direct_interaction=direct, cascade_paths=cascades or []
    )


def _inhibitor_graph():
    """DrugA --inhibits--> CYP3A4 <--metabolized_by-- DrugB."""
    g = nx.DiGraph()
    g.add_node("drug:A", node_type="drug", name="DrugA")
    g.add_node("drug:B", node_type="drug", name="DrugB")
    g.add_node("enzyme:CYP3A4", node_type="enzyme", name="CYP3A4", enzyme_id="CYP3A4")
    g.add_edge("drug:A", "enzyme:CYP3A4", relation="inhibits", strength="strong")
    g.add_edge("drug:B", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
    return g


# --------------- PathFinder tests ---------------


class TestPathFinderEdgeCases:
    pf = PathFinder()

    def test_enzyme_cascade_inhibitor_substrate(self):
        g = _inhibitor_graph()
        paths = self.pf.find_cascade_paths(g, ["A", "B"])
        assert len(paths) >= 1
        assert any("DrugA" in p.drug_a_name and "DrugB" in p.drug_b_name for p in paths)

    def test_enzyme_cascade_inducer_substrate(self):
        g = nx.DiGraph()
        g.add_node("drug:A", node_type="drug", name="DrugA")
        g.add_node("drug:B", node_type="drug", name="DrugB")
        g.add_node("enzyme:CYP3A4", node_type="enzyme", name="CYP3A4", enzyme_id="CYP3A4")
        g.add_edge("drug:A", "enzyme:CYP3A4", relation="induces", strength="strong")
        g.add_edge("drug:B", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
        paths = self.pf.find_cascade_paths(g, ["A", "B"])
        assert len(paths) >= 1
        assert any(p.net_severity in ("major", "moderate") for p in paths)

    def test_enzyme_cascade_same_drug_skipped(self):
        g = nx.DiGraph()
        g.add_node("drug:A", node_type="drug", name="DrugA")
        g.add_node("enzyme:CYP3A4", node_type="enzyme", name="CYP3A4", enzyme_id="CYP3A4")
        g.add_edge("drug:A", "enzyme:CYP3A4", relation="inhibits", strength="strong")
        g.add_edge("drug:A", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
        assert self.pf.find_cascade_paths(g, ["A"]) == []

    def test_is_valid_edge_drug_to_enzyme(self):
        assert self.pf._is_valid_edge("enzyme", "inhibits", "drug:A", "drug:A", {"drug:B"}) is True

    def test_is_valid_edge_drug_to_drug(self):
        assert (
            self.pf._is_valid_edge("drug", "interacts_with", "drug:A", "drug:A", {"drug:B"})
            is False
        )

    def test_is_valid_edge_enzyme_to_drug(self):
        assert (
            self.pf._is_valid_edge("drug", "metabolized_by", "enzyme:CYP3A4", "drug:A", {"drug:B"})
            is True
        )

    def test_infer_severity_strong_inhibition(self):
        steps = [_step("inhibits", "strong"), _step("metabolized_by")]
        assert self.pf._infer_cascade_severity(steps) == "major"

    def test_infer_severity_no_strong_no_inhibition(self):
        steps = [_step("induces", "moderate"), _step("metabolized_by")]
        assert self.pf._infer_cascade_severity(steps) == "moderate"

    def test_compute_effect_inhibits_enzyme(self):
        assert "reduction in" in self.pf._compute_effect(
            "inhibits", "strong", "DrugA", "CYP3A4", "enzyme"
        )

    def test_explain_path_no_steps(self):
        path = CascadePath(
            steps=[],
            net_severity="minor",
            description="Fallback",
            drug_a_name="DrugA",
            drug_b_name="DrugB",
        )
        assert self.pf.explain_path(path) == "Fallback"

    def test_deduplicate_reverse_paths(self):
        g = _inhibitor_graph()
        paths = self.pf.find_cascade_paths(g, ["A", "B"])
        descs = [p.description[:60] for p in paths]
        assert len(descs) == len(set(descs))


# --------------- RiskScorer tests ---------------


class TestRiskScorerEdgeCases:
    rs = RiskScorer()

    def test_score_capped_at_100(self):
        cascades = [_cascade("critical", [_step("inhibits", "strong")])] * 10
        assert self.rs.score_interaction(_result("critical", cascades, ev=99999)) <= 100.0

    def test_score_no_direct_no_cascade(self):
        assert self.rs.score_interaction(_result("none", [])) < 5.0

    def test_pgx_multiplier_increases_score(self):
        from unittest.mock import MagicMock
        from medgraph.graph.models import GeneticGuideline

        store = MagicMock()
        gl = GeneticGuideline(
            drug_id="DA",
            gene_id="CYP2D6",
            phenotype="poor",
            severity_multiplier=1.5,
            recommendation="Avoid",
        )
        store.get_genetic_guidelines.return_value = [gl]
        result = _result("moderate")
        base = self.rs.score_interaction(result)
        pgx = self.rs.score_interaction(
            result, store=store, metabolizer_phenotypes={"CYP2D6": "poor"}
        )
        assert pgx >= base

    def test_empty_report_score(self):
        report = InteractionReport(
            drugs=[], interactions=[], overall_risk="minor", overall_score=0.0
        )
        assert self.rs.score_report(report) == 0.0

    def test_rescore_updates_severity(self):
        result = _result("major")
        result.risk_score = 5.0
        result.severity = "minor"
        report = InteractionReport(
            drugs=[result.drug_a, result.drug_b],
            interactions=[result],
            overall_risk="minor",
            overall_score=5.0,
        )
        updated = self.rs.rescore_report(report)
        assert updated.interactions[0].severity == "major"
        assert updated.overall_risk == "major"

    def test_cascade_bonus_computation(self):
        # major weight=70, factor=0.5 → 35.0
        assert self.rs._compute_cascade_bonus(
            [_cascade("major", [_step("inhibits", "strong")])]
        ) == pytest.approx(35.0)


# --------------- PathFinder multi-drug / timeout / dedup tests ---------------


def _six_drug_graph():
    """
    6 drugs sharing CYP3A4:
      Drug1..Drug3 inhibit CYP3A4 (strong)
      Drug4..Drug6 are metabolized by CYP3A4
    Guarantees depth-3 paths (drug -> enzyme -> drug) are reachable.
    """
    g = nx.DiGraph()
    inhibitors = ["D1", "D2", "D3"]
    substrates = ["D4", "D5", "D6"]
    for d in inhibitors + substrates:
        g.add_node(f"drug:{d}", node_type="drug", name=f"Drug{d}")
    g.add_node("enzyme:CYP3A4", node_type="enzyme", name="CYP3A4", enzyme_id="CYP3A4")
    for d in inhibitors:
        g.add_edge(f"drug:{d}", "enzyme:CYP3A4", relation="inhibits", strength="strong")
    for d in substrates:
        g.add_edge(f"drug:{d}", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
    return g, inhibitors + substrates


def _ten_drug_graph():
    """
    10 drugs: 5 inhibitors + 5 substrates across CYP3A4 and CYP2D6.
    Enough combinations to stress the BFS timeout path.
    """
    g = nx.DiGraph()
    inhibitors = [f"I{i}" for i in range(5)]
    substrates = [f"S{i}" for i in range(5)]
    all_ids = inhibitors + substrates
    for d in all_ids:
        g.add_node(f"drug:{d}", node_type="drug", name=f"Drug{d}")
    for enz in ["CYP3A4", "CYP2D6"]:
        g.add_node(f"enzyme:{enz}", node_type="enzyme", name=enz, enzyme_id=enz)
    for d in inhibitors:
        g.add_edge(f"drug:{d}", "enzyme:CYP3A4", relation="inhibits", strength="strong")
        g.add_edge(f"drug:{d}", "enzyme:CYP2D6", relation="inhibits", strength="moderate")
    for d in substrates:
        g.add_edge(f"drug:{d}", "enzyme:CYP3A4", relation="metabolized_by", strength="moderate")
        g.add_edge(f"drug:{d}", "enzyme:CYP2D6", relation="metabolized_by", strength="weak")
    return g, all_ids


class TestPathFinderMultiDrug:
    pf = PathFinder()

    def test_pathfinder_six_drugs_finds_cascades(self):
        """6-drug scenario: enzyme cascade paths between inhibitors and substrates are found."""
        g, drug_ids = _six_drug_graph()
        paths = self.pf.find_cascade_paths(g, drug_ids)
        # Each of 3 inhibitors x 3 substrates = 9 unique cascade pairs expected
        assert len(paths) >= 9, f"Expected >=9 cascade paths, got {len(paths)}"
        # All returned paths should have net_severity set (not empty)
        assert all(p.net_severity in ("critical", "major", "moderate", "minor") for p in paths)
        # Verify depth-3 paths (drug->enzyme->drug) are included via enzyme_ids
        assert all(len(p.enzyme_ids) >= 1 for p in paths)

    def test_pathfinder_ten_drugs_completes_within_timeout(self):
        """10-drug scenario must return within 5 seconds (BFS timeout guard active)."""
        import time

        g, drug_ids = _ten_drug_graph()
        start = time.monotonic()
        paths = self.pf.find_cascade_paths(g, drug_ids)
        elapsed = time.monotonic() - start

        assert elapsed < 5.0, f"find_cascade_paths took {elapsed:.2f}s — exceeds 5s budget"
        # Should still return results (enzyme cascade paths are found via fast O(n) path)
        assert len(paths) >= 1

    def test_pathfinder_dedup_uses_structured_key(self):
        """
        No duplicate paths with the same drug pair + enzyme set should be present.
        The dedup key is (drug_a_name, drug_b_name, frozenset(enzyme_ids)).
        """
        g, drug_ids = _six_drug_graph()
        paths = self.pf.find_cascade_paths(g, drug_ids)

        seen: set[tuple] = set()
        for p in paths:
            key = (p.drug_a_name, p.drug_b_name, frozenset(p.enzyme_ids))
            rev_key = (p.drug_b_name, p.drug_a_name, frozenset(p.enzyme_ids))
            assert key not in seen, f"Duplicate path found: {key}"
            assert rev_key not in seen, f"Duplicate reverse path found: {rev_key}"
            seen.add(key)
