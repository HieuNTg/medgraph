"""
Unit tests for FDAEnrichmentAgent and LabelParserAgent.

Network calls are fully mocked via unittest.mock.patch; no real HTTP traffic.
All tests use an isolated SQLite database via tmp_path.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from medgraph.agents.fda_enrichment_agent import FDAEnrichmentAgent
from medgraph.agents.label_parser_agent import LabelParserAgent
from medgraph.graph.models import AdverseEvent, Drug, Interaction
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def make_store(tmp_path: Path) -> GraphStore:
    return GraphStore(tmp_path / "test.db")


def seed_drugs(store: GraphStore) -> tuple[Drug, Drug]:
    drug_a = Drug(id="DB001", name="Warfarin", description="Anticoagulant")
    drug_b = Drug(id="DB002", name="Aspirin", description="NSAID")
    store.upsert_drug(drug_a)
    store.upsert_drug(drug_b)
    return drug_a, drug_b


def seed_interaction(store: GraphStore, drug_a: Drug, drug_b: Drug) -> Interaction:
    ix = Interaction(
        id="IX001",
        drug_a_id=drug_a.id,
        drug_b_id=drug_b.id,
        severity="major",
        description="Increased bleeding risk",
        source="seed",
        evidence_count=0,
    )
    store.upsert_interaction(ix)
    return ix


# ---------------------------------------------------------------------------
# LabelParserAgent — pure-logic method tests (no agent run needed)
# ---------------------------------------------------------------------------


@pytest.fixture
def label_agent(tmp_path: Path) -> LabelParserAgent:
    """LabelParserAgent with a pre-loaded drug name map; client is irrelevant here."""
    store = make_store(tmp_path)
    drug_a, drug_b = seed_drugs(store)
    with patch("medgraph.agents.label_parser_agent.OpenFDAClient"):
        agent = LabelParserAgent(store, max_drugs=10)
    # Populate the name map as _execute would
    agent._drug_name_map = {
        "warfarin": drug_a,
        "aspirin": drug_b,
    }
    return agent


class TestExtractDrugMentions:
    def test_extract_drug_mentions_regex_patterns(self, label_agent: LabelParserAgent):
        """Regex pattern captures drug name from 'concomitant use of X' phrasing."""
        text = "Concomitant use of Warfarin may increase the risk of bleeding."
        mentions = label_agent._extract_drug_mentions(text)
        assert any(m.lower() == "warfarin" for m in mentions)

    def test_extract_drug_mentions_direct_match(self, label_agent: LabelParserAgent):
        """Drug names already in _drug_name_map are found via direct text scan."""
        text = "Patients taking aspirin should be monitored carefully."
        mentions = label_agent._extract_drug_mentions(text)
        assert any(m.lower() == "aspirin" for m in mentions)

    def test_extract_drug_mentions_short_names_ignored(self, label_agent: LabelParserAgent):
        """Tokens shorter than 4 characters must not be returned."""
        # Add a 3-char drug name to the map to confirm it is skipped
        label_agent._drug_name_map["ace"] = MagicMock()
        text = "Ace inhibitors are commonly used."
        mentions = label_agent._extract_drug_mentions(text)
        assert not any(m.lower() == "ace" for m in mentions)


class TestExtractRelevantSnippet:
    def test_extract_relevant_snippet_found(self, label_agent: LabelParserAgent):
        """Returns the sentence containing the drug name."""
        text = "This drug has many uses. Warfarin increases bleeding risk. Monitor INR."
        snippet = label_agent._extract_relevant_snippet(text, "Warfarin")
        assert snippet is not None
        assert "Warfarin" in snippet or "warfarin" in snippet.lower()

    def test_extract_relevant_snippet_not_found(self, label_agent: LabelParserAgent):
        """Returns None when drug name is absent from text."""
        text = "This drug has no relevant warnings in this sentence."
        snippet = label_agent._extract_relevant_snippet(text, "Metformin")
        assert snippet is None


class TestInferSeverityFromText:
    def test_infer_severity_contraindicated(self, label_agent: LabelParserAgent):
        text = "Warfarin is contraindicated with this medication."
        assert label_agent._infer_severity_from_text(text, "Warfarin") == "critical"

    def test_infer_severity_serious(self, label_agent: LabelParserAgent):
        text = "Serious adverse events have been reported with Warfarin."
        assert label_agent._infer_severity_from_text(text, "Warfarin") == "major"

    def test_infer_severity_monitor(self, label_agent: LabelParserAgent):
        text = "Monitor closely when Warfarin is co-administered."
        assert label_agent._infer_severity_from_text(text, "Warfarin") == "moderate"

    def test_infer_severity_default(self, label_agent: LabelParserAgent):
        """Falls back to 'moderate' when no severity keywords are found."""
        text = "Warfarin has been used in clinical trials."
        assert label_agent._infer_severity_from_text(text, "Warfarin") == "moderate"


# ---------------------------------------------------------------------------
# FDAEnrichmentAgent — unit tests with mocked OpenFDAClient
# ---------------------------------------------------------------------------


def _make_fda_agent(store: GraphStore) -> FDAEnrichmentAgent:
    with patch("medgraph.agents.fda_enrichment_agent.OpenFDAClient"):
        agent = FDAEnrichmentAgent(store, max_pairs=10, events_per_pair=5)
    return agent


class TestEnrichPair:
    def test_enrich_pair_updates_evidence(self, tmp_path: Path):
        """When client returns events, evidence_count is updated and True returned."""
        store = make_store(tmp_path)
        drug_a, drug_b = seed_drugs(store)
        ix = seed_interaction(store, drug_a, drug_b)

        agent = _make_fda_agent(store)
        fake_event = AdverseEvent(
            id="FAERS-test001",
            drug_ids=["DB001", "DB002"],
            reaction="Hemorrhage",
            count=42,
        )
        agent.client.search_adverse_events = MagicMock(return_value=[fake_event])

        result = agent._enrich_pair(ix)

        assert result is True
        updated = store.get_interaction_by_id("IX001")
        assert updated is not None
        assert updated.evidence_count == 42

    def test_enrich_pair_no_events(self, tmp_path: Path):
        """When client returns an empty list, _enrich_pair returns False."""
        store = make_store(tmp_path)
        drug_a, drug_b = seed_drugs(store)
        ix = seed_interaction(store, drug_a, drug_b)

        agent = _make_fda_agent(store)
        agent.client.search_adverse_events = MagicMock(return_value=[])

        result = agent._enrich_pair(ix)

        assert result is False

    def test_enrich_pair_stale_evidence_not_updated(self, tmp_path: Path):
        """When FAERS total <= existing evidence_count, interaction is not updated."""
        store = make_store(tmp_path)
        drug_a, drug_b = seed_drugs(store)
        ix = seed_interaction(store, drug_a, drug_b)
        # Set high existing evidence so FAERS result is stale
        ix.evidence_count = 999
        store.upsert_interaction(ix)

        agent = _make_fda_agent(store)
        fake_event = AdverseEvent(
            id="FAERS-stale01",
            drug_ids=["DB001", "DB002"],
            reaction="Nausea",
            count=10,
        )
        agent.client.search_adverse_events = MagicMock(return_value=[fake_event])

        result = agent._enrich_pair(ix)

        assert result is False
        # evidence_count should remain unchanged
        updated = store.get_interaction_by_id("IX001")
        assert updated.evidence_count == 999

    def test_enrich_pair_missing_drug(self, tmp_path: Path):
        """If either drug ID is not in the store, _enrich_pair returns False."""
        store = make_store(tmp_path)
        # Interaction references a drug that was never inserted
        ix = Interaction(
            id="IX999",
            drug_a_id="GHOST001",
            drug_b_id="GHOST002",
            severity="minor",
            description="Phantom interaction",
            source="seed",
            evidence_count=0,
        )
        store.upsert_interaction(ix)

        agent = _make_fda_agent(store)
        agent.client.search_adverse_events = MagicMock(return_value=[])

        result = agent._enrich_pair(ix)

        assert result is False
        agent.client.search_adverse_events.assert_not_called()


class TestExecuteProcessesInteractions:
    def test_execute_processes_interactions(self, tmp_path: Path):
        """_execute counts interactions and increments records_updated on hits."""
        store = make_store(tmp_path)
        drug_a, drug_b = seed_drugs(store)
        seed_interaction(store, drug_a, drug_b)

        agent = _make_fda_agent(store)
        fake_event = AdverseEvent(
            id="FAERS-exec01",
            drug_ids=["DB001", "DB002"],
            reaction="Nausea",
            count=10,
        )
        agent.client.search_adverse_events = MagicMock(return_value=[fake_event])

        from medgraph.agents.base import AgentResult

        result = AgentResult(agent_name="FDAEnrichmentAgent")
        agent._execute(result)

        assert result.records_processed == 1
        assert result.records_updated == 1
        assert result.records_skipped == 0
        assert result.errors == []
