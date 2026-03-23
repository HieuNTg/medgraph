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
