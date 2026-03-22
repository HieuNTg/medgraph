"""
Tests for MEDGRAPH engine: cascade analysis, risk scoring, pathfinding.

Known interaction test cases:
1. Warfarin + Aspirin — direct interaction, major bleeding risk
2. Fluoxetine + Codeine — CYP2D6 inhibition cascade
3. Ketoconazole + Simvastatin — CYP3A4 inhibition, critical
4. Rifampin + Warfarin + Aspirin — 3-drug cascade
5. No-interaction case — drugs with no shared enzymes
"""

from __future__ import annotations

import time

import pytest

from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.engine.models import CascadePath, CascadeStep, DrugInteractionResult
from medgraph.engine.pathfinder import PathFinder
from medgraph.engine.scorer import RiskScorer
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.models import Drug, Interaction
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    """Module-scoped seeded store (expensive to create)."""
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("engine_test")
    store = GraphStore(tmp_path / "engine_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


@pytest.fixture(scope="module")
def graph(seeded_store: GraphStore):
    """Module-scoped knowledge graph."""
    builder = GraphBuilder()
    return builder.build(seeded_store)


@pytest.fixture(scope="module")
def analyzer() -> CascadeAnalyzer:
    return CascadeAnalyzer()


@pytest.fixture(scope="module")
def scorer() -> RiskScorer:
    return RiskScorer()


@pytest.fixture(scope="module")
def pathfinder() -> PathFinder:
    return PathFinder()


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def get_drug_id(store: GraphStore, name: str) -> str:
    drug = store.get_drug_by_name(name)
    assert drug is not None, f"Drug not in store: {name}"
    return drug.id


# ---------------------------------------------------------------------------
# Test Case 1: Warfarin + Aspirin — direct interaction
# ---------------------------------------------------------------------------


class TestWarfarinAspirin:
    def test_direct_interaction_detected(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")

        report = analyzer.analyze([warfarin_id, aspirin_id], graph, seeded_store)
        assert len(report.interactions) >= 1

        pair = report.interactions[0]
        assert pair.direct_interaction is not None
        assert pair.direct_interaction.severity in ("major", "critical")

    def test_risk_score_is_major_or_critical(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")

        report = analyzer.analyze([warfarin_id, aspirin_id], graph, seeded_store)
        assert report.overall_risk in ("major", "critical")
        assert report.overall_score >= 60


# ---------------------------------------------------------------------------
# Test Case 2: Fluoxetine + Codeine — CYP2D6 cascade
# ---------------------------------------------------------------------------


class TestFluoxetineCodeine:
    def test_cyp2d6_cascade_detected(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        fluoxetine_id = get_drug_id(seeded_store, "Fluoxetine")
        codeine_id = get_drug_id(seeded_store, "Codeine")

        report = analyzer.analyze([fluoxetine_id, codeine_id], graph, seeded_store)

        # Either direct interaction or cascade path should exist
        assert len(report.interactions) >= 1
        pair = report.interactions[0]

        has_direct = pair.direct_interaction is not None
        has_cascade = len(pair.cascade_paths) > 0
        assert has_direct or has_cascade, "Should detect fluoxetine-codeine interaction"

    def test_cyp2d6_shared_enzyme(
        self, seeded_store: GraphStore, graph, pathfinder: PathFinder
    ) -> None:
        fluoxetine_id = get_drug_id(seeded_store, "Fluoxetine")
        codeine_id = get_drug_id(seeded_store, "Codeine")

        shared = pathfinder.find_shared_enzymes(graph, fluoxetine_id, codeine_id)
        assert "CYP2D6" in shared, (
            f"CYP2D6 should be shared between Fluoxetine and Codeine. Got: {shared}"
        )

    def test_direct_interaction_severity_major(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        fluoxetine_id = get_drug_id(seeded_store, "Fluoxetine")
        codeine_id = get_drug_id(seeded_store, "Codeine")

        report = analyzer.analyze([fluoxetine_id, codeine_id], graph, seeded_store)
        pair = report.interactions[0]
        if pair.direct_interaction:
            assert pair.direct_interaction.severity in ("major", "critical")


# ---------------------------------------------------------------------------
# Test Case 3: Ketoconazole + Simvastatin — CYP3A4, critical
# ---------------------------------------------------------------------------


class TestKetoconazoleSimvastatin:
    def test_critical_interaction_detected(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        keto_id = get_drug_id(seeded_store, "Ketoconazole")
        simva_id = get_drug_id(seeded_store, "Simvastatin")

        report = analyzer.analyze([keto_id, simva_id], graph, seeded_store)
        assert len(report.interactions) >= 1

        pair = report.interactions[0]
        assert pair.direct_interaction is not None
        assert pair.direct_interaction.severity == "critical"

    def test_risk_score_exceeds_80(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        keto_id = get_drug_id(seeded_store, "Ketoconazole")
        simva_id = get_drug_id(seeded_store, "Simvastatin")

        report = analyzer.analyze([keto_id, simva_id], graph, seeded_store)
        assert report.overall_score >= 80

    def test_cyp3a4_shared_enzyme(
        self, seeded_store: GraphStore, graph, pathfinder: PathFinder
    ) -> None:
        keto_id = get_drug_id(seeded_store, "Ketoconazole")
        simva_id = get_drug_id(seeded_store, "Simvastatin")

        shared = pathfinder.find_shared_enzymes(graph, keto_id, simva_id)
        assert "CYP3A4" in shared, f"CYP3A4 should be shared. Got: {shared}"


# ---------------------------------------------------------------------------
# Test Case 4: Rifampin + Warfarin + Aspirin — 3-drug cascade
# ---------------------------------------------------------------------------


class TestThreeDrugCascade:
    def test_three_drug_analysis_runs(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        rifampin_id = get_drug_id(seeded_store, "Rifampin")
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")

        report = analyzer.analyze([rifampin_id, warfarin_id, aspirin_id], graph, seeded_store)

        # Should produce 3 pairwise interactions (3 drugs = 3 pairs)
        assert len(report.interactions) == 3
        assert len(report.drugs) == 3

    def test_rifampin_warfarin_in_report(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        rifampin_id = get_drug_id(seeded_store, "Rifampin")
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")

        report = analyzer.analyze([rifampin_id, warfarin_id, aspirin_id], graph, seeded_store)

        drug_name_pairs = [{r.drug_a.name, r.drug_b.name} for r in report.interactions]
        assert {"Rifampin", "Warfarin"} in drug_name_pairs

    def test_warfarin_aspirin_still_major_in_three_drug(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        rifampin_id = get_drug_id(seeded_store, "Rifampin")
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")

        report = analyzer.analyze([rifampin_id, warfarin_id, aspirin_id], graph, seeded_store)

        war_asp_result = next(
            (
                r
                for r in report.interactions
                if {r.drug_a.name, r.drug_b.name} == {"Warfarin", "Aspirin"}
            ),
            None,
        )
        assert war_asp_result is not None
        assert war_asp_result.direct_interaction is not None


# ---------------------------------------------------------------------------
# Test Case 5: No-interaction case
# ---------------------------------------------------------------------------


class TestNoInteraction:
    def test_metformin_lisinopril_low_risk(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        """Metformin and Lisinopril have minimal CYP interactions."""
        metformin_id = get_drug_id(seeded_store, "Metformin")
        lisinopril_id = get_drug_id(seeded_store, "Lisinopril")

        report = analyzer.analyze([metformin_id, lisinopril_id], graph, seeded_store)
        # Should not be critical or major
        assert report.overall_risk in ("minor", "moderate")

    def test_empty_input_returns_empty_report(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        report = analyzer.analyze([], graph, seeded_store)
        assert report.interactions == []
        assert report.overall_score == 0.0

    def test_single_drug_returns_empty_report(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        report = analyzer.analyze([warfarin_id], graph, seeded_store)
        assert report.interactions == []


# ---------------------------------------------------------------------------
# Risk Scorer tests
# ---------------------------------------------------------------------------


class TestRiskScorer:
    def test_severity_classification_thresholds(self, scorer: RiskScorer) -> None:
        assert scorer.classify_severity(85.0) == "critical"
        assert scorer.classify_severity(80.0) == "critical"
        assert scorer.classify_severity(65.0) == "major"
        assert scorer.classify_severity(60.0) == "major"
        assert scorer.classify_severity(40.0) == "moderate"
        assert scorer.classify_severity(35.0) == "moderate"
        assert scorer.classify_severity(20.0) == "minor"
        assert scorer.classify_severity(0.0) == "minor"

    def test_critical_scores_higher_than_major(self, scorer: RiskScorer) -> None:
        critical_drug = Drug(id="A", name="A")
        major_drug = Drug(id="B", name="B")

        critical_result = DrugInteractionResult(
            drug_a=critical_drug,
            drug_b=major_drug,
            direct_interaction=Interaction(
                id="I1",
                drug_a_id="A",
                drug_b_id="B",
                severity="critical",
                description="critical",
                source="seed",
                evidence_count=1000,
            ),
        )
        major_result = DrugInteractionResult(
            drug_a=critical_drug,
            drug_b=major_drug,
            direct_interaction=Interaction(
                id="I2",
                drug_a_id="A",
                drug_b_id="B",
                severity="major",
                description="major",
                source="seed",
                evidence_count=100,
            ),
        )
        minor_result = DrugInteractionResult(
            drug_a=critical_drug,
            drug_b=major_drug,
            direct_interaction=Interaction(
                id="I3",
                drug_a_id="A",
                drug_b_id="B",
                severity="minor",
                description="minor",
                source="seed",
                evidence_count=0,
            ),
        )

        critical_score = scorer.score_interaction(critical_result)
        major_score = scorer.score_interaction(major_result)
        minor_score = scorer.score_interaction(minor_result)

        assert critical_score > major_score, "Critical must score higher than major"
        assert major_score > minor_score, "Major must score higher than minor"

    def test_cascade_bonus_increases_score(self, scorer: RiskScorer) -> None:
        drug_a = Drug(id="A", name="A")
        drug_b = Drug(id="B", name="B")

        step = CascadeStep(
            source_drug="A",
            target="CYP3A4",
            target_type="enzyme",
            relation="inhibits",
            strength="strong",
            effect="blocks metabolism",
        )
        cascade = CascadePath(
            steps=[step],
            net_severity="major",
            description="A inhibits CYP3A4 affecting B",
            drug_a_name="A",
            drug_b_name="B",
            enzyme_ids=["CYP3A4"],
        )

        result_no_cascade = DrugInteractionResult(drug_a=drug_a, drug_b=drug_b)
        result_with_cascade = DrugInteractionResult(
            drug_a=drug_a, drug_b=drug_b, cascade_paths=[cascade]
        )

        score_no = scorer.score_interaction(result_no_cascade)
        score_with = scorer.score_interaction(result_with_cascade)
        assert score_with > score_no, "Cascade paths should increase risk score"

    def test_evidence_modifier_increases_score(self, scorer: RiskScorer) -> None:
        drug_a = Drug(id="A", name="A")
        drug_b = Drug(id="B", name="B")

        base_result = DrugInteractionResult(
            drug_a=drug_a,
            drug_b=drug_b,
            direct_interaction=Interaction(
                id="I1",
                drug_a_id="A",
                drug_b_id="B",
                severity="moderate",
                description="test",
                source="seed",
                evidence_count=0,
            ),
        )
        evidence_result = DrugInteractionResult(
            drug_a=drug_a,
            drug_b=drug_b,
            direct_interaction=Interaction(
                id="I2",
                drug_a_id="A",
                drug_b_id="B",
                severity="moderate",
                description="test",
                source="seed",
                evidence_count=10000,
            ),
        )
        score_base = scorer.score_interaction(base_result)
        score_evidence = scorer.score_interaction(evidence_result)
        assert score_evidence > score_base

    def test_score_ordering_ketoconazole_vs_fluoxetine(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer, scorer: RiskScorer
    ) -> None:
        """Ketoconazole+Simvastatin should score higher than Fluoxetine+Codeine."""
        keto_id = get_drug_id(seeded_store, "Ketoconazole")
        simva_id = get_drug_id(seeded_store, "Simvastatin")
        fluoxetine_id = get_drug_id(seeded_store, "Fluoxetine")
        codeine_id = get_drug_id(seeded_store, "Codeine")

        report_keto = analyzer.analyze([keto_id, simva_id], graph, seeded_store)
        report_fluox = analyzer.analyze([fluoxetine_id, codeine_id], graph, seeded_store)

        assert report_keto.overall_score >= report_fluox.overall_score, (
            f"Ketoconazole+Simvastatin ({report_keto.overall_score:.1f}) should be "
            f">= Fluoxetine+Codeine ({report_fluox.overall_score:.1f})"
        )


# ---------------------------------------------------------------------------
# Pathfinder tests
# ---------------------------------------------------------------------------


class TestPathFinder:
    def test_max_depth_limits_path_length(
        self, seeded_store: GraphStore, graph, pathfinder: PathFinder
    ) -> None:
        """Paths should not exceed max_depth hops."""
        drug_ids = [d.id for d in seeded_store.get_all_drugs()[:5]]
        paths = pathfinder.find_cascade_paths(graph, drug_ids, max_depth=2)
        for path in paths:
            assert len(path.steps) <= 2, f"Path has {len(path.steps)} steps, max_depth=2"

    def test_find_shared_enzymes_cyp3a4(
        self, seeded_store: GraphStore, graph, pathfinder: PathFinder
    ) -> None:
        keto_id = get_drug_id(seeded_store, "Ketoconazole")
        simva_id = get_drug_id(seeded_store, "Simvastatin")
        shared = pathfinder.find_shared_enzymes(graph, keto_id, simva_id)
        assert "CYP3A4" in shared

    def test_explain_path_returns_string(self, pathfinder: PathFinder) -> None:
        step = CascadeStep(
            source_drug="Fluoxetine",
            target="CYP2D6",
            target_type="enzyme",
            relation="inhibits",
            strength="strong",
            effect="reduces CYP2D6 activity",
        )
        path = CascadePath(
            steps=[step],
            net_severity="major",
            description="Fluoxetine inhibits CYP2D6 pathway used by Codeine",
            drug_a_name="Fluoxetine",
            drug_b_name="Codeine",
            enzyme_ids=["CYP2D6"],
        )
        explanation = pathfinder.explain_path(path)
        assert isinstance(explanation, str)
        assert len(explanation) > 10

    def test_single_drug_returns_no_paths(
        self, seeded_store: GraphStore, graph, pathfinder: PathFinder
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        paths = pathfinder.find_cascade_paths(graph, [warfarin_id])
        assert paths == []

    def test_empty_input_returns_no_paths(self, graph, pathfinder: PathFinder) -> None:
        paths = pathfinder.find_cascade_paths(graph, [])
        assert paths == []


# ---------------------------------------------------------------------------
# Graph builder tests
# ---------------------------------------------------------------------------


class TestGraphBuilder:
    def test_graph_has_drug_nodes(self, seeded_store: GraphStore, graph) -> None:
        drug_nodes = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "drug"]
        assert len(drug_nodes) >= 60

    def test_graph_has_enzyme_nodes(self, graph) -> None:
        enzyme_nodes = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "enzyme"]
        assert len(enzyme_nodes) >= 5

    def test_graph_has_edges(self, graph) -> None:
        assert graph.number_of_edges() >= 50

    def test_drug_nodes_have_name_attribute(self, graph) -> None:
        for node, data in graph.nodes(data=True):
            if data.get("node_type") == "drug":
                assert "name" in data and data["name"], f"Drug node {node} missing name"
                break


# ---------------------------------------------------------------------------
# Performance test
# ---------------------------------------------------------------------------


class TestPerformance:
    def test_ten_drug_analysis_under_500ms(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        """10-drug analysis must complete in <500ms (per spec)."""
        drugs = seeded_store.get_all_drugs()[:10]
        drug_ids = [d.id for d in drugs]
        assert len(drug_ids) == 10

        start = time.monotonic()
        report = analyzer.analyze(drug_ids, graph, seeded_store)
        elapsed_ms = (time.monotonic() - start) * 1000

        assert elapsed_ms < 500, f"10-drug analysis took {elapsed_ms:.1f}ms (limit: 500ms)"
        assert len(report.interactions) > 0  # Should produce results


# ---------------------------------------------------------------------------
# Pharmacogenomics tests
# ---------------------------------------------------------------------------


class TestPharmacogenomics:
    """Test pharmacogenomics scoring adjustments."""

    def test_pgx_multiplier_increases_score(self, seeded_store: GraphStore, graph) -> None:
        """CYP2D6 poor metabolizer should increase score for affected drugs."""
        analyzer = CascadeAnalyzer()
        # Fluoxetine + Codeine — both CYP2D6 dependent
        report_normal = analyzer.analyze(["DB00472", "DB00318"], graph, seeded_store)

        # Re-score with CYP2D6 poor metabolizer
        for result in report_normal.interactions:
            score_normal = result.risk_score
            score_pgx = analyzer.scorer.score_interaction(
                result, seeded_store, metabolizer_phenotypes={"CYP2D6": "poor"}
            )
            # PGX score should be >= normal score (multiplier >= 1.0)
            assert score_pgx >= score_normal

    def test_no_pgx_phenotype_no_change(self, seeded_store: GraphStore, graph) -> None:
        """Without metabolizer info, score should be unchanged."""
        analyzer = CascadeAnalyzer()
        report = analyzer.analyze(["DB00682", "DB00945"], graph, seeded_store)
        for result in report.interactions:
            score_without = result.risk_score
            score_with = analyzer.scorer.score_interaction(
                result, seeded_store, metabolizer_phenotypes={"CYP2D6": "normal"}
            )
            # Normal metabolizer should not change score (multiplier = 1.0, default)
            assert score_with == score_without


# ---------------------------------------------------------------------------
# Report structure tests
# ---------------------------------------------------------------------------


class TestReportStructure:
    def test_report_always_has_disclaimer(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")
        report = analyzer.analyze([warfarin_id, aspirin_id], graph, seeded_store)
        assert report.disclaimer
        assert len(report.disclaimer) > 50

    def test_report_timestamp_present(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        warfarin_id = get_drug_id(seeded_store, "Warfarin")
        aspirin_id = get_drug_id(seeded_store, "Aspirin")
        report = analyzer.analyze([warfarin_id, aspirin_id], graph, seeded_store)
        assert report.timestamp
        assert "T" in report.timestamp  # ISO format

    def test_analyze_by_names_works(
        self, seeded_store: GraphStore, graph, analyzer: CascadeAnalyzer
    ) -> None:
        report = analyzer.analyze_by_names(["Warfarin", "Aspirin"], graph, seeded_store)
        assert len(report.drugs) == 2
        assert len(report.interactions) == 1
