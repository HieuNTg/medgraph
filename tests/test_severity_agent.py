"""
Unit tests for SeverityAgent — severity re-classification logic.

Tests cover:
- _score_description: keyword-based scoring
- _score_enzyme_involvement: CYP enzyme pattern scoring
- _classify: multi-factor severity computation
- _execute: escalation-only behavior
- run(): full lifecycle via GraphStore
"""

from __future__ import annotations

import pytest

from medgraph.agents.severity_agent import SeverityAgent
from medgraph.graph.models import Drug, DrugEnzymeRelation, Interaction
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def store(tmp_path) -> GraphStore:
    """Isolated SQLite store per test."""
    return GraphStore(tmp_path / "severity_test.db")


@pytest.fixture()
def agent(store: GraphStore) -> SeverityAgent:
    return SeverityAgent(store)


def _make_interaction(
    id: str = "I1",
    drug_a_id: str = "A",
    drug_b_id: str = "B",
    severity: str = "minor",
    description: str = "",
    mechanism: str | None = None,
    evidence_count: int = 0,
) -> Interaction:
    return Interaction(
        id=id,
        drug_a_id=drug_a_id,
        drug_b_id=drug_b_id,
        severity=severity,
        description=description,
        mechanism=mechanism,
        source="seed",
        evidence_count=evidence_count,
    )


def _make_drug(id: str, name: str) -> Drug:
    return Drug(id=id, name=name)


def _make_rel(
    drug_id: str, enzyme_id: str, relation_type: str, strength: str = "moderate"
) -> DrugEnzymeRelation:
    return DrugEnzymeRelation(
        drug_id=drug_id, enzyme_id=enzyme_id, relation_type=relation_type, strength=strength
    )


# ---------------------------------------------------------------------------
# _score_description tests
# ---------------------------------------------------------------------------


class TestScoreDescription:
    def test_critical_keyword_returns_4(self, agent: SeverityAgent) -> None:
        assert agent._score_description("patient developed rhabdomyolysis") == 4

    def test_major_keyword_returns_3(self, agent: SeverityAgent) -> None:
        assert agent._score_description("may lead to toxicity") == 3

    def test_no_keywords_returns_0(self, agent: SeverityAgent) -> None:
        assert agent._score_description("mild interaction observed") == 0

    def test_empty_string_returns_0(self, agent: SeverityAgent) -> None:
        assert agent._score_description("") == 0

    def test_critical_takes_priority_over_major(self, agent: SeverityAgent) -> None:
        # Text contains both; critical should win
        assert agent._score_description("hepatotoxicity and toxicity") == 4

    def test_case_insensitive(self, agent: SeverityAgent) -> None:
        assert agent._score_description("RHABDOMYOLYSIS risk") == 4


# ---------------------------------------------------------------------------
# _score_enzyme_involvement tests
# ---------------------------------------------------------------------------


class TestScoreEnzymeInvolvement:
    def test_strong_inhibitor_high_risk_enzyme_returns_4(self, agent: SeverityAgent) -> None:
        """Drug A strongly inhibits CYP3A4, Drug B metabolized by CYP3A4 → critical (4)."""
        rels = {
            "A": [_make_rel("A", "CYP3A4", "inhibits", "strong")],
            "B": [_make_rel("B", "CYP3A4", "metabolized_by")],
        }
        assert agent._score_enzyme_involvement("A", "B", rels) == 4

    def test_strong_inhibitor_low_risk_enzyme_returns_3(self, agent: SeverityAgent) -> None:
        """Drug A strongly inhibits a non-high-risk enzyme → major (3)."""
        rels = {
            "A": [_make_rel("A", "CYP1A2", "inhibits", "strong")],
            "B": [_make_rel("B", "CYP1A2", "metabolized_by")],
        }
        assert agent._score_enzyme_involvement("A", "B", rels) == 3

    def test_moderate_inhibitor_returns_2(self, agent: SeverityAgent) -> None:
        """Drug A moderately inhibits CYP3A4, Drug B metabolized by it → moderate (2)."""
        rels = {
            "A": [_make_rel("A", "CYP3A4", "inhibits", "moderate")],
            "B": [_make_rel("B", "CYP3A4", "metabolized_by")],
        }
        assert agent._score_enzyme_involvement("A", "B", rels) == 2

    def test_substrate_competition_returns_2(self, agent: SeverityAgent) -> None:
        """Both drugs metabolized by same enzyme → moderate (2)."""
        rels = {
            "A": [_make_rel("A", "CYP2D6", "metabolized_by")],
            "B": [_make_rel("B", "CYP2D6", "metabolized_by")],
        }
        assert agent._score_enzyme_involvement("A", "B", rels) == 2

    def test_no_shared_enzymes_returns_0(self, agent: SeverityAgent) -> None:
        rels = {
            "A": [_make_rel("A", "CYP3A4", "inhibits", "strong")],
            "B": [_make_rel("B", "CYP2D6", "metabolized_by")],
        }
        assert agent._score_enzyme_involvement("A", "B", rels) == 0

    def test_multi_enzyme_escalation_three_shared(self, agent: SeverityAgent) -> None:
        """3+ shared enzymes → at least major (3)."""
        rels = {
            "A": [
                _make_rel("A", "CYP1A2", "metabolized_by"),
                _make_rel("A", "CYP2B6", "metabolized_by"),
                _make_rel("A", "CYP2E1", "metabolized_by"),
            ],
            "B": [
                _make_rel("B", "CYP1A2", "metabolized_by"),
                _make_rel("B", "CYP2B6", "metabolized_by"),
                _make_rel("B", "CYP2E1", "metabolized_by"),
            ],
        }
        score = agent._score_enzyme_involvement("A", "B", rels)
        assert score >= 3

    def test_missing_relations_for_one_drug_returns_0(self, agent: SeverityAgent) -> None:
        rels = {"A": [_make_rel("A", "CYP3A4", "inhibits", "strong")]}
        assert agent._score_enzyme_involvement("A", "B", rels) == 0


# ---------------------------------------------------------------------------
# _classify tests
# ---------------------------------------------------------------------------


class TestClassify:
    def _empty_rels(self) -> dict:
        return {}

    def test_nti_drug_gets_at_least_major(self, agent: SeverityAgent) -> None:
        """Warfarin (NTI) → at least major baseline."""
        interaction = _make_interaction(drug_a_id="W", drug_b_id="X")
        drug_map = {"W": _make_drug("W", "Warfarin"), "X": _make_drug("X", "SomeDrug")}
        result = agent._classify(interaction, self._empty_rels(), drug_map)
        assert result in ("major", "critical")

    def test_faers_critical_threshold(self, agent: SeverityAgent) -> None:
        """evidence_count >= 1000 → critical."""
        interaction = _make_interaction(evidence_count=1000)
        result = agent._classify(interaction, self._empty_rels(), {})
        assert result == "critical"

    def test_faers_major_threshold(self, agent: SeverityAgent) -> None:
        """evidence_count >= 100 → major."""
        interaction = _make_interaction(evidence_count=100)
        result = agent._classify(interaction, self._empty_rels(), {})
        assert result == "major"

    def test_critical_keyword_yields_critical(self, agent: SeverityAgent) -> None:
        interaction = _make_interaction(description="serotonin syndrome documented")
        result = agent._classify(interaction, self._empty_rels(), {})
        assert result == "critical"

    def test_no_factors_yields_minor(self, agent: SeverityAgent) -> None:
        interaction = _make_interaction(description="minimal effect")
        result = agent._classify(interaction, self._empty_rels(), {})
        assert result == "minor"


# ---------------------------------------------------------------------------
# _execute (escalation-only) tests
# ---------------------------------------------------------------------------


class TestExecute:
    def test_execute_only_escalates_never_downgrades(self, store: GraphStore) -> None:
        """An interaction already at 'critical' must not be downgraded."""
        # Seed a drug pair with no escalation triggers
        store.upsert_drug(_make_drug("A", "DrugA"))
        store.upsert_drug(_make_drug("B", "DrugB"))
        interaction = _make_interaction(severity="critical", description="minimal effect")
        store.upsert_interaction(interaction)

        agent = SeverityAgent(store)
        result = agent.run()

        # Interaction should still be critical
        interactions = store.get_all_interactions()
        assert interactions[0].severity == "critical"
        assert result.records_updated == 0


# ---------------------------------------------------------------------------
# Full run() lifecycle test
# ---------------------------------------------------------------------------


class TestRun:
    def test_run_returns_agent_result(self, store: GraphStore) -> None:
        """run() completes and returns a valid AgentResult with stats."""
        store.upsert_drug(_make_drug("W", "Warfarin"))
        store.upsert_drug(_make_drug("X", "Aspirin"))
        interaction = _make_interaction(
            id="I1",
            drug_a_id="W",
            drug_b_id="X",
            severity="minor",
            description="bleeding risk",  # major keyword
        )
        store.upsert_interaction(interaction)

        agent = SeverityAgent(store)
        result = agent.run()

        assert result.agent_name == "SeverityAgent"
        assert result.records_processed >= 1
        assert result.success
        assert result.duration_seconds >= 0

    def test_run_escalates_severity_via_keyword(self, store: GraphStore) -> None:
        """Interaction with 'rhabdomyolysis' in description must be escalated to critical."""
        store.upsert_drug(_make_drug("A", "DrugA"))
        store.upsert_drug(_make_drug("B", "DrugB"))
        interaction = _make_interaction(
            id="I2",
            drug_a_id="A",
            drug_b_id="B",
            severity="minor",
            description="can cause rhabdomyolysis",
        )
        store.upsert_interaction(interaction)

        agent = SeverityAgent(store)
        agent.run()

        updated = store.get_all_interactions()
        assert updated[0].severity == "critical"

    def test_run_empty_store_no_crash(self, store: GraphStore) -> None:
        """Empty store must not crash the agent."""
        agent = SeverityAgent(store)
        result = agent.run()
        assert result.success
        assert result.records_processed == 0
