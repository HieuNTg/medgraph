"""
Tests for MEDGRAPH data layer: GraphStore CRUD, seed data, search.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from medgraph.graph.models import (
    AdverseEvent,
    Drug,
    DrugEnzymeRelation,
    Enzyme,
    Interaction,
)
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_store(tmp_path: Path) -> GraphStore:
    """Provide a fresh in-memory-style store backed by a temp file."""
    return GraphStore(tmp_path / "test.db")


@pytest.fixture
def seeded_store(tmp_path: Path) -> GraphStore:
    """Provide a store seeded with built-in data."""
    from medgraph.data.seed import DataSeeder

    store = GraphStore(tmp_path / "seeded.db")
    seeder = DataSeeder(
        store=store,
        db_path=tmp_path / "seeded.db",
        skip_openfda=True,
    )
    seeder.run()
    return store


# ---------------------------------------------------------------------------
# GraphStore CRUD tests
# ---------------------------------------------------------------------------


class TestGraphStoreCRUD:
    def test_upsert_and_get_drug(self, tmp_store: GraphStore) -> None:
        drug = Drug(
            id="DB99999",
            name="TestDrug",
            brand_names=["Brand1", "Brand2"],
            description="A test drug",
            drug_class="Test",
            rxnorm_cui="12345",
        )
        tmp_store.upsert_drug(drug)
        fetched = tmp_store.get_drug_by_id("DB99999")
        assert fetched is not None
        assert fetched.name == "TestDrug"
        assert fetched.brand_names == ["Brand1", "Brand2"]
        assert fetched.rxnorm_cui == "12345"

    def test_upsert_drug_updates_on_conflict(self, tmp_store: GraphStore) -> None:
        drug = Drug(id="DB99999", name="Original", description="Old desc")
        tmp_store.upsert_drug(drug)
        drug2 = Drug(id="DB99999", name="Updated", description="New desc")
        tmp_store.upsert_drug(drug2)
        fetched = tmp_store.get_drug_by_id("DB99999")
        assert fetched.name == "Updated"

    def test_upsert_and_get_enzyme(self, tmp_store: GraphStore) -> None:
        enzyme = Enzyme(id="CYP3A4", name="Cytochrome P450 3A4", gene="CYP3A4")
        tmp_store.upsert_enzyme(enzyme)
        enzymes = tmp_store.get_all_enzymes()
        assert any(e.id == "CYP3A4" for e in enzymes)

    def test_upsert_and_get_interaction(self, tmp_store: GraphStore) -> None:
        # Insert drugs first to satisfy FK
        tmp_store.upsert_drug(Drug(id="DB00001", name="DrugA"))
        tmp_store.upsert_drug(Drug(id="DB00002", name="DrugB"))

        interaction = Interaction(
            id="INT-001",
            drug_a_id="DB00001",
            drug_b_id="DB00002",
            severity="major",
            description="Test interaction",
            mechanism="Test mechanism",
            source="seed",
            evidence_count=100,
        )
        tmp_store.upsert_interaction(interaction)
        results = tmp_store.get_interactions_for_drugs(["DB00001", "DB00002"])
        assert len(results) >= 1
        assert results[0].severity == "major"

    def test_get_direct_interaction_bidirectional(self, tmp_store: GraphStore) -> None:
        tmp_store.upsert_drug(Drug(id="DB00001", name="DrugA"))
        tmp_store.upsert_drug(Drug(id="DB00002", name="DrugB"))
        interaction = Interaction(
            id="INT-001",
            drug_a_id="DB00001",
            drug_b_id="DB00002",
            severity="major",
            description="Test",
            source="seed",
            evidence_count=0,
        )
        tmp_store.upsert_interaction(interaction)

        # Should find regardless of order
        result_ab = tmp_store.get_direct_interaction("DB00001", "DB00002")
        result_ba = tmp_store.get_direct_interaction("DB00002", "DB00001")
        assert result_ab is not None
        assert result_ba is not None

    def test_upsert_drug_enzyme_relation(self, tmp_store: GraphStore) -> None:
        tmp_store.upsert_drug(Drug(id="DB00001", name="DrugA"))
        tmp_store.upsert_enzyme(Enzyme(id="CYP3A4", name="CYP3A4"))
        relation = DrugEnzymeRelation(
            drug_id="DB00001",
            enzyme_id="CYP3A4",
            relation_type="inhibits",
            strength="strong",
        )
        tmp_store.upsert_drug_enzyme_relation(relation)
        relations = tmp_store.get_enzyme_relations("DB00001")
        assert len(relations) == 1
        assert relations[0].relation_type == "inhibits"
        assert relations[0].strength == "strong"

    def test_upsert_adverse_event(self, tmp_store: GraphStore) -> None:
        tmp_store.upsert_drug(Drug(id="DB00001", name="DrugA"))
        tmp_store.upsert_drug(Drug(id="DB00002", name="DrugB"))
        event = AdverseEvent(
            id="AE-001",
            drug_ids=["DB00001", "DB00002"],
            reaction="Bleeding",
            count=500,
            seriousness="serious",
        )
        tmp_store.upsert_adverse_event(event)
        events = tmp_store.get_adverse_events(["DB00001"])
        assert len(events) == 1
        assert events[0].reaction == "Bleeding"

    def test_search_drugs_returns_results(self, tmp_store: GraphStore) -> None:
        for name in ["Aspirin", "Astemizole", "Acetaminophen"]:
            tmp_store.upsert_drug(Drug(id=f"DB-{name}", name=name))
        results = tmp_store.search_drugs("asp", limit=10)
        assert len(results) >= 1
        assert any(r.name == "Aspirin" for r in results)

    def test_search_drugs_case_insensitive(self, tmp_store: GraphStore) -> None:
        tmp_store.upsert_drug(Drug(id="DB00001", name="Warfarin"))
        results = tmp_store.search_drugs("warfarin")
        assert len(results) >= 1
        results2 = tmp_store.search_drugs("WARFARIN")
        assert len(results2) >= 1

    def test_get_counts_empty_store(self, tmp_store: GraphStore) -> None:
        counts = tmp_store.get_counts()
        assert counts["drugs"] == 0
        assert counts["enzymes"] == 0
        assert counts["interactions"] == 0


# ---------------------------------------------------------------------------
# Seed data tests
# ---------------------------------------------------------------------------


class TestSeedData:
    def test_seed_populates_drugs(self, seeded_store: GraphStore) -> None:
        counts = seeded_store.get_counts()
        assert counts["drugs"] >= 60, f"Expected >=60 drugs, got {counts['drugs']}"

    def test_seed_populates_enzymes(self, seeded_store: GraphStore) -> None:
        counts = seeded_store.get_counts()
        assert counts["enzymes"] >= 5, f"Expected >=5 enzymes, got {counts['enzymes']}"

    def test_seed_populates_interactions(self, seeded_store: GraphStore) -> None:
        counts = seeded_store.get_counts()
        assert counts["interactions"] >= 20, (
            f"Expected >=20 interactions, got {counts['interactions']}"
        )

    def test_seed_populates_enzyme_relations(self, seeded_store: GraphStore) -> None:
        counts = seeded_store.get_counts()
        assert counts["drug_enzyme_relations"] >= 50, (
            f"Expected >=50 enzyme relations, got {counts['drug_enzyme_relations']}"
        )

    def test_common_drugs_searchable(self, seeded_store: GraphStore) -> None:
        """Key drugs must be findable by name."""
        for drug_name in ["Warfarin", "Aspirin", "Metformin", "Atorvastatin", "Simvastatin"]:
            drug = seeded_store.get_drug_by_name(drug_name)
            assert drug is not None, f"Drug not found: {drug_name}"

    def test_cyp450_enzymes_present(self, seeded_store: GraphStore) -> None:
        enzymes = {e.id for e in seeded_store.get_all_enzymes()}
        for cyp in ["CYP3A4", "CYP2D6", "CYP2C9", "CYP2C19", "CYP1A2"]:
            assert cyp in enzymes, f"Enzyme not found: {cyp}"

    def test_warfarin_aspirin_interaction_exists(self, seeded_store: GraphStore) -> None:
        warfarin = seeded_store.get_drug_by_name("Warfarin")
        aspirin = seeded_store.get_drug_by_name("Aspirin")
        assert warfarin and aspirin
        interaction = seeded_store.get_direct_interaction(warfarin.id, aspirin.id)
        assert interaction is not None, "Warfarin-Aspirin interaction should exist"
        assert interaction.severity in ("major", "critical")

    def test_warfarin_cyp2c9_relation(self, seeded_store: GraphStore) -> None:
        warfarin = seeded_store.get_drug_by_name("Warfarin")
        assert warfarin
        relations = seeded_store.get_enzyme_relations(warfarin.id)
        enzyme_ids = {r.enzyme_id for r in relations}
        assert "CYP2C9" in enzyme_ids, "Warfarin should have CYP2C9 relation"

    def test_fluoxetine_cyp2d6_inhibitor(self, seeded_store: GraphStore) -> None:
        fluoxetine = seeded_store.get_drug_by_name("Fluoxetine")
        assert fluoxetine
        relations = seeded_store.get_enzyme_relations(fluoxetine.id)
        inhibits_2d6 = [
            r for r in relations if r.enzyme_id == "CYP2D6" and r.relation_type == "inhibits"
        ]
        assert inhibits_2d6, "Fluoxetine should inhibit CYP2D6"
        assert inhibits_2d6[0].strength == "strong"

    def test_ketoconazole_simvastatin_interaction(self, seeded_store: GraphStore) -> None:
        keto = seeded_store.get_drug_by_name("Ketoconazole")
        simva = seeded_store.get_drug_by_name("Simvastatin")
        assert keto and simva
        interaction = seeded_store.get_direct_interaction(keto.id, simva.id)
        assert interaction is not None, "Ketoconazole-Simvastatin should have a direct interaction"
        assert interaction.severity == "critical"

    def test_rifampin_warfarin_interaction(self, seeded_store: GraphStore) -> None:
        rifampin = seeded_store.get_drug_by_name("Rifampin")
        warfarin = seeded_store.get_drug_by_name("Warfarin")
        assert rifampin and warfarin
        interaction = seeded_store.get_direct_interaction(rifampin.id, warfarin.id)
        assert interaction is not None
        assert interaction.severity in ("major", "critical")


# ---------------------------------------------------------------------------
# Expanded data tests
# ---------------------------------------------------------------------------


@pytest.fixture
def expanded_store(tmp_path: Path) -> GraphStore:
    """Provide a store seeded with built-in + expanded data."""
    from medgraph.data.seed import DataSeeder

    store = GraphStore(tmp_path / "expanded.db")
    seeder = DataSeeder(
        store=store,
        db_path=tmp_path / "expanded.db",
        skip_openfda=True,
    )
    seeder.run()
    return store


class TestExpandedData:
    def test_expanded_drugs_count(self, expanded_store: GraphStore) -> None:
        pytest.importorskip("medgraph.data.seed_drugs_expanded")
        counts = expanded_store.get_counts()
        assert counts["drugs"] > 200, f"Expected >200 drugs after expansion, got {counts['drugs']}"

    def test_food_items_searchable(self, expanded_store: GraphStore) -> None:
        pytest.importorskip("medgraph.data.seed_drugs_expanded")
        grapefruit = expanded_store.search_drugs("grapefruit", limit=5)
        assert len(grapefruit) >= 1, "Grapefruit should be searchable after expansion"
        stjohn = expanded_store.search_drugs("St. John", limit=5)
        assert len(stjohn) >= 1, "St. John's Wort should be searchable after expansion"

    def test_expanded_interactions_count(self, expanded_store: GraphStore) -> None:
        pytest.importorskip("medgraph.data.seed_interactions_expanded")
        counts = expanded_store.get_counts()
        assert counts["interactions"] >= 100, (
            f"Expected >=100 interactions after expansion, got {counts['interactions']}"
        )

    def test_expanded_enzyme_relations_count(self, expanded_store: GraphStore) -> None:
        pytest.importorskip("medgraph.data.seed_interactions_expanded")
        counts = expanded_store.get_counts()
        assert counts["drug_enzyme_relations"] > 200, (
            f"Expected >200 enzyme relations after expansion, got {counts['drug_enzyme_relations']}"
        )


# ---------------------------------------------------------------------------
# DrugBank parser tests (with mock data)
# ---------------------------------------------------------------------------


class TestDrugBankParser:
    def test_classify_severity_keywords(self) -> None:
        from medgraph.data.drugbank import classify_severity

        assert classify_severity("This is a life-threatening interaction") == "critical"
        assert classify_severity("Serious risk of bleeding") == "major"
        assert classify_severity("Use with caution, monitor closely") == "moderate"
        assert classify_severity("Minor clinical significance") == "minor"
        assert classify_severity("Some unknown text") == "minor"

    def test_normalize_enzyme_id(self) -> None:
        from medgraph.data.drugbank import normalize_enzyme_id

        assert normalize_enzyme_id("CYP3A4") == "CYP3A4"
        assert normalize_enzyme_id("Cytochrome P450 3A4") == "CYP3A4"
        assert normalize_enzyme_id("P-glycoprotein") == "PGLYCO"
        assert normalize_enzyme_id("Unknown enzyme") is None

    def test_parser_returns_empty_without_files(self, tmp_path: Path) -> None:
        from medgraph.data.drugbank import DrugBankParser

        parser = DrugBankParser(tmp_path / "nonexistent")
        assert not parser.is_available()
        assert parser.parse_drugs() == []
        assert parser.parse_interactions() == []
        assert parser.parse_enzyme_relations() == []
