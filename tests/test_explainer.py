"""
Tests for natural language explanation generator.

Covers: interaction explanations, cascade paths, PGx impact, report summaries.
"""

from __future__ import annotations

from medgraph.engine.explainer import (
    explain_cascade_path,
    explain_interaction,
    explain_pgx_impact,
    explain_report,
)
from medgraph.engine.models import (
    CascadePath,
    CascadeStep,
    DrugInteractionResult,
    EvidenceItem,
    InteractionReport,
)
from medgraph.graph.models import Drug, GeneticGuideline, Interaction


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _drug(name: str, id: str = "DB00001") -> Drug:
    return Drug(id=id, name=name)


def _interaction(severity: str = "major", desc: str = "bleeding risk") -> Interaction:
    return Interaction(
        id="IX1", drug_a_id="A", drug_b_id="B",
        severity=severity, description=desc, source="seed",
    )


def _cascade_step(
    source: str = "Fluoxetine", target: str = "CYP2D6",
    relation: str = "inhibits", strength: str = "strong",
    target_type: str = "enzyme", effect: str = "reduced enzyme activity",
) -> CascadeStep:
    return CascadeStep(
        source_drug=source, target=target, relation=relation,
        strength=strength, target_type=target_type, effect=effect,
    )


def _cascade_path(steps=None, severity: str = "major") -> CascadePath:
    return CascadePath(
        steps=steps or [_cascade_step()],
        net_severity=severity,
        description="test cascade",
        drug_a_name="Fluoxetine",
        drug_b_name="Codeine",
    )


def _result(
    severity: str = "major", score: float = 72.0,
    cascade_paths=None, evidence=None,
) -> DrugInteractionResult:
    return DrugInteractionResult(
        drug_a=_drug("Warfarin", "DB00001"),
        drug_b=_drug("Aspirin", "DB00002"),
        direct_interaction=_interaction(severity),
        cascade_paths=cascade_paths or [],
        risk_score=score,
        severity=severity,
        evidence=evidence or [],
    )


# ---------------------------------------------------------------------------
# explain_interaction
# ---------------------------------------------------------------------------


class TestExplainInteraction:
    def test_basic_explanation(self) -> None:
        text = explain_interaction(_result())
        assert "Warfarin" in text
        assert "Aspirin" in text
        assert "72/100" in text
        assert "clinically significant" in text

    def test_includes_direct_description(self) -> None:
        text = explain_interaction(_result())
        assert "bleeding risk" in text

    def test_includes_cascade_info(self) -> None:
        r = _result(cascade_paths=[_cascade_path()])
        text = explain_interaction(r)
        assert "cascade" in text.lower() or "enzyme" in text.lower()

    def test_includes_evidence_count(self) -> None:
        ev = [EvidenceItem(source="faers", description="Hemorrhage", evidence_count=500)]
        text = explain_interaction(_result(evidence=ev))
        assert "500" in text
        assert "adverse event" in text.lower()

    def test_minor_interaction(self) -> None:
        text = explain_interaction(_result(severity="minor", score=15.0))
        assert "well-tolerated" in text

    def test_critical_interaction(self) -> None:
        text = explain_interaction(_result(severity="critical", score=90.0))
        assert "life-threatening" in text

    def test_no_direct_interaction(self) -> None:
        r = DrugInteractionResult(
            drug_a=_drug("DrugA"), drug_b=_drug("DrugB"),
            cascade_paths=[_cascade_path()],
            risk_score=45.0, severity="moderate",
        )
        text = explain_interaction(r)
        assert "DrugA" in text
        assert "DrugB" in text


# ---------------------------------------------------------------------------
# explain_cascade_path
# ---------------------------------------------------------------------------


class TestExplainCascadePath:
    def test_single_step_cascade(self) -> None:
        text = explain_cascade_path(_cascade_path())
        assert "Fluoxetine" in text
        assert "CYP2D6" in text
        assert "inhibits" in text

    def test_empty_steps_returns_empty(self) -> None:
        path = CascadePath(
            steps=[], net_severity="minor", description="",
            drug_a_name="A", drug_b_name="B",
        )
        assert explain_cascade_path(path) == ""

    def test_severity_described(self) -> None:
        text = explain_cascade_path(_cascade_path(severity="critical"))
        assert "life-threatening" in text

    def test_multi_step_chain(self) -> None:
        steps = [
            _cascade_step(source="Fluoxetine", target="CYP2D6", relation="inhibits"),
            _cascade_step(
                source="Codeine", target="CYP2D6", relation="metabolized_by",
                target_type="enzyme", effect="reduced metabolism",
            ),
        ]
        text = explain_cascade_path(_cascade_path(steps=steps))
        assert "which" in text  # chain connector


# ---------------------------------------------------------------------------
# explain_pgx_impact
# ---------------------------------------------------------------------------


class TestExplainPGxImpact:
    def test_increased_risk(self) -> None:
        gl = GeneticGuideline(
            drug_id="DB00001", gene_id="CYP2D6", phenotype="poor",
            recommendation="Consider dose reduction", severity_multiplier=1.5,
        )
        text = explain_pgx_impact("Fluoxetine", "CYP2D6", "poor", gl)
        assert "poor metabolizer" in text
        assert "increases" in text
        assert "50%" in text
        assert "Consider dose reduction" in text

    def test_decreased_risk(self) -> None:
        gl = GeneticGuideline(
            drug_id="DB00318", gene_id="CYP2D6", phenotype="poor",
            recommendation="Avoid codeine", severity_multiplier=0.5,
        )
        text = explain_pgx_impact("Codeine", "CYP2D6", "poor", gl)
        assert "decreases" in text
        assert "50%" in text

    def test_normal_no_impact(self) -> None:
        gl = GeneticGuideline(
            drug_id="DB00001", gene_id="CYP2D6", phenotype="normal",
            recommendation="", severity_multiplier=1.0,
        )
        text = explain_pgx_impact("Warfarin", "CYP2D6", "normal", gl)
        assert "No significant impact" in text


# ---------------------------------------------------------------------------
# explain_report
# ---------------------------------------------------------------------------


class TestExplainReport:
    def test_empty_report(self) -> None:
        report = InteractionReport(
            drugs=[], interactions=[], overall_risk="minor", overall_score=0.0,
        )
        text = explain_report(report)
        assert "No drug interactions" in text

    def test_report_with_interactions(self) -> None:
        report = InteractionReport(
            drugs=[_drug("Warfarin"), _drug("Aspirin")],
            interactions=[_result()],
            overall_risk="major", overall_score=72.0,
        )
        text = explain_report(report)
        assert "2 medications" in text
        assert "Warfarin" in text
        assert "Aspirin" in text
        assert "1 interaction" in text
        assert "72/100" in text

    def test_highlights_critical(self) -> None:
        report = InteractionReport(
            drugs=[_drug("W"), _drug("A")],
            interactions=[_result(severity="critical", score=90.0)],
            overall_risk="critical", overall_score=90.0,
        )
        text = explain_report(report)
        assert "Key concerns" in text
        assert "critical" in text

    def test_cascade_count_mentioned(self) -> None:
        report = InteractionReport(
            drugs=[_drug("W"), _drug("A")],
            interactions=[_result(cascade_paths=[_cascade_path(), _cascade_path()])],
            overall_risk="major", overall_score=72.0,
        )
        text = explain_report(report)
        assert "cascade" in text.lower()
        assert "CYP450" in text
