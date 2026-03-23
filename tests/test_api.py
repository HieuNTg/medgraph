"""
Tests for MEDGRAPH FastAPI endpoints.

Uses FastAPI TestClient with a seeded in-memory SQLite store.
The app's lifespan is bypassed by patching app state directly.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from medgraph.api.server import create_app
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.api.search import DrugSearcher
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    """Module-scoped seeded store."""
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("api_test")
    store = GraphStore(tmp_path / "api_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


@pytest.fixture(scope="module")
def client(seeded_store: GraphStore) -> TestClient:
    """
    TestClient with app state pre-populated (bypasses lifespan/DB path).
    """
    app = create_app()
    builder = GraphBuilder()
    graph = builder.build(seeded_store)
    analyzer = CascadeAnalyzer()
    searcher = DrugSearcher(seeded_store, use_rxnorm=False)

    # Inject state before TestClient starts
    app.state.store = seeded_store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher

    # Use lifespan=False so our injected state is not overwritten
    with TestClient(app, raise_server_exceptions=True) as c:
        # Override state again after lifespan runs (lifespan rebuilds from data/medgraph.db)
        app.state.store = seeded_store
        app.state.graph = graph
        app.state.analyzer = analyzer
        app.state.searcher = searcher
        yield c


# ---------------------------------------------------------------------------
# POST /api/check
# ---------------------------------------------------------------------------


class TestCheckEndpoint:
    def test_check_warfarin_aspirin_200(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        data = resp.json()
        assert data["drug_count"] == 2
        assert data["interaction_count"] >= 1
        assert data["overall_risk"] in ("minor", "moderate", "major", "critical")
        assert "disclaimer" in data
        assert "timestamp" in data

    def test_check_has_interactions(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        data = resp.json()
        interactions = data["interactions"]
        assert len(interactions) >= 1
        first = interactions[0]
        assert "drug_a" in first
        assert "drug_b" in first
        assert "severity" in first
        assert "risk_score" in first

    def test_check_unknown_drug_400(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["notadrug123xyz", "Aspirin"]})
        assert resp.status_code == 400
        detail = resp.json()["detail"]
        assert isinstance(detail, dict)
        assert "unresolved" in detail
        assert len(detail["unresolved"]) > 0

    def test_check_completely_unknown_drug_400(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["zzzdrug999"]})
        # single drug → 400 first
        assert resp.status_code == 400

    def test_check_empty_list_422(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": []})
        # Pydantic validator rejects empty list before endpoint code runs
        assert resp.status_code == 422

    def test_check_single_drug_400(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["Warfarin"]})
        assert resp.status_code == 400
        assert "minimum 2" in resp.json()["detail"].lower()

    def test_check_too_many_drugs_400(self, client: TestClient) -> None:
        drugs = ["Warfarin"] * 11
        resp = client.post("/api/check", json={"drugs": drugs})
        assert resp.status_code == 400
        assert "maximum 10" in resp.json()["detail"].lower()

    def test_check_disclaimer_present(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        data = resp.json()
        assert "informational" in data["disclaimer"].lower()

    def test_check_has_explanation_and_summary(self, client: TestClient) -> None:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] != ""
        assert "medication" in data["summary"].lower()
        for ix in data["interactions"]:
            assert ix["explanation"] != ""

    def test_check_include_evidence_false(self, client: TestClient) -> None:
        resp = client.post(
            "/api/check",
            json={"drugs": ["Warfarin", "Aspirin"], "include_evidence": False},
        )
        assert resp.status_code == 200
        data = resp.json()
        for interaction in data["interactions"]:
            assert interaction["evidence"] == []


# ---------------------------------------------------------------------------
# GET /api/drugs/search
# ---------------------------------------------------------------------------


class TestDrugSearch:
    def test_search_asp_returns_aspirin(self, client: TestClient) -> None:
        resp = client.get("/api/drugs/search?q=asp")
        assert resp.status_code == 200
        names = [r["name"] for r in resp.json()]
        assert any("aspirin" in n.lower() or "Aspirin" in n for n in names)

    def test_search_no_results_returns_empty(self, client: TestClient) -> None:
        resp = client.get("/api/drugs/search?q=zzzzzzzznotadrug")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_search_result_has_expected_fields(self, client: TestClient) -> None:
        resp = client.get("/api/drugs/search?q=war")
        assert resp.status_code == 200
        results = resp.json()
        if results:
            first = results[0]
            assert "id" in first
            assert "name" in first
            assert "brand_names" in first
            assert "drug_class" in first

    def test_search_limit_respected(self, client: TestClient) -> None:
        resp = client.get("/api/drugs/search?q=a&limit=3")
        assert resp.status_code == 200
        assert len(resp.json()) <= 3


# ---------------------------------------------------------------------------
# GET /api/drugs/{drug_id}
# ---------------------------------------------------------------------------


class TestGetDrug:
    def _get_warfarin_id(self, client: TestClient) -> str:
        resp = client.get("/api/drugs/search?q=Warfarin")
        assert resp.status_code == 200
        results = resp.json()
        assert results, "Warfarin must be in seeded store"
        return results[0]["id"]

    def test_get_valid_drug_200(self, client: TestClient) -> None:
        drug_id = self._get_warfarin_id(client)
        resp = client.get(f"/api/drugs/{drug_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == drug_id
        assert "name" in data
        assert "brand_names" in data
        assert "enzyme_relations" in data

    def test_get_invalid_drug_404(self, client: TestClient) -> None:
        resp = client.get("/api/drugs/INVALID_ID_XYZ")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_200(self, client: TestClient) -> None:
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert "drug_count" in data
        assert "interaction_count" in data
        assert "enzyme_count" in data
        assert "adverse_event_count" in data

    def test_stats_positive_counts(self, client: TestClient) -> None:
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["drug_count"] >= 60
        assert data["enzyme_count"] >= 5
        assert data["interaction_count"] >= 20


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------


class TestHealth:
    def test_health_200(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "db_size" in data
        assert "graph_nodes" in data


# ---------------------------------------------------------------------------
# POST /api/report/json
# ---------------------------------------------------------------------------


class TestJSONReportEndpoint:
    def _get_check_result(self, client: TestClient) -> dict:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        return resp.json()

    def test_json_report_200(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post("/api/report/json", json={"check_result": check})
        assert resp.status_code == 200
        assert resp.headers["content-type"] == "application/json"
        data = resp.json()
        assert data["report_format"] == "medgraph-json-v1"
        assert data["summary"]["drug_count"] == 2

    def test_json_report_attachment_header(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post("/api/report/json", json={"check_result": check})
        assert "medgraph-report.json" in resp.headers.get("content-disposition", "")

    def test_json_report_compact(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post(
            "/api/report/json", json={"check_result": check, "pretty": False}
        )
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /api/report/csv
# ---------------------------------------------------------------------------


class TestCSVReportEndpoint:
    def _get_check_result(self, client: TestClient) -> dict:
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        return resp.json()

    def test_csv_report_200(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post("/api/report/csv", json={"check_result": check})
        assert resp.status_code == 200
        assert "text/csv" in resp.headers["content-type"]

    def test_csv_report_attachment_header(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post("/api/report/csv", json={"check_result": check})
        assert "medgraph-report.csv" in resp.headers.get("content-disposition", "")

    def test_csv_report_has_data_rows(self, client: TestClient) -> None:
        check = self._get_check_result(client)
        resp = client.post("/api/report/csv", json={"check_result": check})
        import csv
        import io

        rows = list(csv.reader(io.StringIO(resp.text)))
        assert len(rows) >= 2  # header + interactions


# ---------------------------------------------------------------------------
# Pharmacogenomics Endpoints
# ---------------------------------------------------------------------------


class TestPGxAnnotations:
    def test_check_with_pgx_returns_annotations(self, client: TestClient) -> None:
        """POST /api/check with metabolizer_phenotypes returns pgx_annotations."""
        resp = client.post(
            "/api/check",
            json={
                "drugs": ["Codeine", "Fluoxetine"],
                "metabolizer_phenotypes": {"CYP2D6": "poor"},
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        # At least one interaction should have PGx annotations
        all_pgx = []
        for ix in data["interactions"]:
            all_pgx.extend(ix.get("pgx_annotations", []))
        assert len(all_pgx) > 0
        # Verify annotation structure
        pgx = all_pgx[0]
        assert "gene" in pgx
        assert "phenotype" in pgx
        assert "drug_name" in pgx
        assert "recommendation" in pgx
        assert "severity_multiplier" in pgx

    def test_check_without_pgx_no_annotations(self, client: TestClient) -> None:
        """Without metabolizer_phenotypes, pgx_annotations is empty."""
        resp = client.post(
            "/api/check",
            json={"drugs": ["Warfarin", "Aspirin"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        for ix in data["interactions"]:
            assert ix["pgx_annotations"] == []


class TestPGxGuidelinesEndpoint:
    def test_pgx_guidelines_for_codeine(self, client: TestClient) -> None:
        """GET /api/pgx/guidelines returns CPIC guidelines for a drug."""
        # First find Codeine's drug ID
        search = client.get("/api/drugs/search?q=Codeine")
        assert search.status_code == 200
        results = search.json()
        if not results:
            pytest.skip("Codeine not in seeded store")

        drug_id = results[0]["id"]
        resp = client.get(f"/api/pgx/guidelines?drug_id={drug_id}")
        assert resp.status_code == 200
        guidelines = resp.json()
        assert len(guidelines) > 0
        gl = guidelines[0]
        assert "gene" in gl
        assert "phenotype" in gl
        assert "recommendation" in gl
        assert "severity_multiplier" in gl

    def test_pgx_guidelines_unknown_drug_empty(self, client: TestClient) -> None:
        resp = client.get("/api/pgx/guidelines?drug_id=UNKNOWN_XYZ")
        assert resp.status_code == 200
        assert resp.json() == []
