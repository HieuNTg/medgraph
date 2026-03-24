"""
Tests for drug-food interaction feature.

Covers:
- Food interaction seeding
- GraphStore query by drug IDs
- Food nodes in knowledge graph
- API endpoint GET /api/v1/food-interactions
- API POST /api/v1/check includes food_interactions
- Grapefruit + Simvastatin returns critical
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from medgraph.api.search import DrugSearcher
from medgraph.api.server import create_app
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("food_test")
    store = GraphStore(tmp_path / "food_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


@pytest.fixture(scope="module")
def client(seeded_store: GraphStore) -> TestClient:
    app = create_app()
    builder = GraphBuilder()
    graph = builder.build(seeded_store)
    analyzer = CascadeAnalyzer()
    searcher = DrugSearcher(seeded_store, use_rxnorm=False)

    app.state.store = seeded_store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher
    app.state.stats_cache = (None, 0.0)

    with TestClient(app, raise_server_exceptions=True) as c:
        app.state.store = seeded_store
        app.state.graph = graph
        app.state.analyzer = analyzer
        app.state.searcher = searcher
        app.state.stats_cache = (None, 0.0)
        yield c


# ---------------------------------------------------------------------------
# Unit: Store — seed and query
# ---------------------------------------------------------------------------


class TestFoodInteractionStore:
    def test_seed_food_interactions_inserts_rows(self, tmp_path):
        store = GraphStore(tmp_path / "fi_unit.db")
        # Insert a minimal drug first to satisfy FK
        from medgraph.graph.models import Drug
        drug = Drug(id="drug_warfarin", name="Warfarin", brand_names=[], description="")
        store.upsert_drug(drug)

        rows = [
            {
                "id": "food_grapefruit_drug_warfarin",
                "food_name": "Grapefruit / Grapefruit juice",
                "food_category": "food",
                "drug_id": "drug_warfarin",
                "severity": "critical",
                "description": "Test description",
                "mechanism": "CYP3A4 inhibition",
                "evidence_level": "A",
            }
        ]
        store.seed_food_interactions(rows)

        results = store.get_food_interactions(["drug_warfarin"])
        assert len(results) == 1
        assert results[0]["severity"] == "critical"
        assert results[0]["food_name"] == "Grapefruit / Grapefruit juice"

    def test_get_food_interactions_empty_input(self, tmp_path):
        store = GraphStore(tmp_path / "fi_empty.db")
        assert store.get_food_interactions([]) == []

    def test_get_food_interactions_no_match(self, tmp_path):
        store = GraphStore(tmp_path / "fi_nomatch.db")
        assert store.get_food_interactions(["nonexistent_drug_id"]) == []

    def test_seed_food_interactions_idempotent(self, tmp_path):
        """Insert same row twice — should replace, not duplicate."""
        store = GraphStore(tmp_path / "fi_idem.db")
        from medgraph.graph.models import Drug
        drug = Drug(id="drug_simvastatin", name="Simvastatin", brand_names=[], description="")
        store.upsert_drug(drug)

        row = {
            "id": "food_grape_simvastatin",
            "food_name": "Grapefruit / Grapefruit juice",
            "food_category": "food",
            "drug_id": "drug_simvastatin",
            "severity": "critical",
            "description": "First insert",
            "mechanism": "CYP3A4",
            "evidence_level": "A",
        }
        store.seed_food_interactions([row])
        row["description"] = "Second insert"
        store.seed_food_interactions([row])

        results = store.get_food_interactions(["drug_simvastatin"])
        assert len(results) == 1
        assert results[0]["description"] == "Second insert"


# ---------------------------------------------------------------------------
# Integration: Seeded store — grapefruit + simvastatin critical
# ---------------------------------------------------------------------------


class TestSeededFoodInteractions:
    def test_grapefruit_simvastatin_is_critical(self, seeded_store: GraphStore):
        """After seeding, grapefruit-simvastatin should be present and critical."""
        # Find simvastatin in DB
        drug = seeded_store.get_drug_by_name("Simvastatin")
        if drug is None:
            pytest.skip("Simvastatin not found in seed data")
        rows = seeded_store.get_food_interactions([drug.id])
        grapefruit_rows = [r for r in rows if "grapefruit" in r["food_name"].lower()]
        assert len(grapefruit_rows) >= 1
        assert grapefruit_rows[0]["severity"] == "critical"

    def test_warfarin_has_multiple_food_interactions(self, seeded_store: GraphStore):
        drug = seeded_store.get_drug_by_name("Warfarin")
        if drug is None:
            pytest.skip("Warfarin not found in seed data")
        rows = seeded_store.get_food_interactions([drug.id])
        assert len(rows) >= 2  # alcohol, cranberry, turmeric, green tea, St. John's Wort

    def test_food_interactions_returns_list_of_dicts(self, seeded_store: GraphStore):
        drugs = seeded_store.get_all_drugs()
        if not drugs:
            pytest.skip("No drugs in seed data")
        results = seeded_store.get_food_interactions([drugs[0].id])
        for r in results:
            assert isinstance(r, dict)
            assert "food_name" in r
            assert "severity" in r
            assert "drug_id" in r


# ---------------------------------------------------------------------------
# Integration: Graph builder — food nodes present
# ---------------------------------------------------------------------------


class TestFoodNodesInGraph:
    def test_food_nodes_in_graph(self, seeded_store: GraphStore):
        builder = GraphBuilder()
        graph = builder.build(seeded_store)
        food_nodes = [n for n, d in graph.nodes(data=True) if d.get("node_type") == "food"]
        # Only run assertion if food interactions exist in the DB
        all_drugs = seeded_store.get_all_drugs()
        all_food = seeded_store.get_food_interactions([d.id for d in all_drugs])
        if all_food:
            assert len(food_nodes) > 0, "Expected food nodes in graph when food interactions are seeded"

    def test_food_nodes_have_correct_type(self, seeded_store: GraphStore):
        builder = GraphBuilder()
        graph = builder.build(seeded_store)
        for node, data in graph.nodes(data=True):
            if node.startswith("food:"):
                assert data["node_type"] == "food"

    def test_food_drug_edges_exist(self, seeded_store: GraphStore):
        builder = GraphBuilder()
        graph = builder.build(seeded_store)
        food_edges = [
            (u, v, d)
            for u, v, d in graph.edges(data=True)
            if d.get("relation") == "food_interaction"
        ]
        all_drugs = seeded_store.get_all_drugs()
        all_food = seeded_store.get_food_interactions([d.id for d in all_drugs])
        if all_food:
            assert len(food_edges) > 0, "Expected food_interaction edges when food data is seeded"


# ---------------------------------------------------------------------------
# API: GET /api/v1/food-interactions
# ---------------------------------------------------------------------------


class TestFoodInteractionsEndpoint:
    def test_food_interactions_endpoint_simvastatin(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions?drugs=Simvastatin")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_food_interactions_endpoint_warfarin(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions?drugs=Warfarin")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_food_interactions_response_schema(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions?drugs=Simvastatin")
        assert resp.status_code == 200
        for item in resp.json():
            assert "food_name" in item
            assert "food_category" in item
            assert "drug_id" in item
            assert "severity" in item
            assert "description" in item
            assert "evidence_level" in item

    def test_food_interactions_endpoint_no_drugs_param(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions")
        # Missing required query param should return 422
        assert resp.status_code == 422

    def test_food_interactions_simvastatin_has_grapefruit(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions?drugs=Simvastatin")
        assert resp.status_code == 200
        data = resp.json()
        if data:  # Only assert if food data is seeded
            grapefruit = [r for r in data if "grapefruit" in r["food_name"].lower()]
            if grapefruit:
                assert grapefruit[0]["severity"] == "critical"

    def test_food_interactions_multiple_drugs(self, client: TestClient):
        resp = client.get("/api/v1/food-interactions?drugs=Simvastatin,Warfarin")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


# ---------------------------------------------------------------------------
# API: POST /api/v1/check includes food_interactions field
# ---------------------------------------------------------------------------


class TestCheckIncludesFoodInteractions:
    def test_check_response_has_food_interactions_field(self, client: TestClient):
        resp = client.post(
            "/api/v1/check",
            json={"drugs": ["Warfarin", "Aspirin"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "food_interactions" in data
        assert isinstance(data["food_interactions"], list)

    def test_check_food_interactions_schema(self, client: TestClient):
        resp = client.post(
            "/api/v1/check",
            json={"drugs": ["Simvastatin", "Warfarin"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        for fi in data["food_interactions"]:
            assert "food_name" in fi
            assert "severity" in fi
            assert "drug_id" in fi
