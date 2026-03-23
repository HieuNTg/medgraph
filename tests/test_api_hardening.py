"""
Tests for Phase 2: API Hardening features.

Covers: API v1 prefix routing, RFC 7807 errors, pagination,
X-Request-ID middleware, OpenAPI metadata.
"""

from __future__ import annotations

import uuid

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
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("hardening_test")
    store = GraphStore(tmp_path / "hardening.db")
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
# API v1 prefix routing
# ---------------------------------------------------------------------------


class TestV1Prefix:
    """All API endpoints accessible at /api/v1/* prefix."""

    def test_v1_stats(self, client: TestClient) -> None:
        resp = client.get("/api/v1/stats")
        assert resp.status_code == 200
        assert "drug_count" in resp.json()

    def test_v1_search(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/search?q=asp")
        assert resp.status_code == 200
        assert "items" in resp.json()

    def test_v1_check(self, client: TestClient) -> None:
        resp = client.post("/api/v1/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200
        assert "interactions" in resp.json()

    def test_backward_compat_api_prefix(self, client: TestClient) -> None:
        """Old /api/* paths still work (backward compat)."""
        resp = client.get("/api/stats")
        assert resp.status_code == 200

    def test_health_not_versioned(self, client: TestClient) -> None:
        """/health stays at root, not behind /api/v1."""
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


# ---------------------------------------------------------------------------
# RFC 7807 Problem Details errors
# ---------------------------------------------------------------------------


class TestRFC7807Errors:
    """Errors return application/problem+json with RFC 7807 fields."""

    def test_404_returns_problem_json(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/NONEXISTENT_ID")
        assert resp.status_code == 404
        assert resp.headers["content-type"] == "application/problem+json"
        body = resp.json()
        assert body["type"] == "about:blank"
        assert body["title"] == "Not Found"
        assert body["status"] == 404
        assert "detail" in body
        assert "instance" in body

    def test_400_returns_problem_json(self, client: TestClient) -> None:
        resp = client.post("/api/v1/check", json={"drugs": ["Warfarin"]})
        assert resp.status_code == 400
        body = resp.json()
        assert body["status"] == 400
        assert body["title"] == "Bad Request"
        assert "detail" in body

    def test_422_validation_error_returns_problem_json(self, client: TestClient) -> None:
        resp = client.post("/api/v1/check", json={"drugs": 123})
        assert resp.status_code == 422
        body = resp.json()
        assert body["status"] == 422
        assert "detail" in body

    def test_error_with_dict_detail_has_extensions(self, client: TestClient) -> None:
        """When HTTPException detail is a dict, it goes into extensions."""
        resp = client.post("/api/v1/check", json={"drugs": ["notadrug123xyz", "Aspirin"]})
        assert resp.status_code == 400
        body = resp.json()
        assert "extensions" in body
        assert "unresolved" in body["extensions"]


# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------


class TestPagination:
    """Search endpoint returns PaginatedResponse with offset support."""

    def test_paginated_response_shape(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/search?q=a")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "offset" in data
        assert "limit" in data
        assert "has_more" in data
        assert isinstance(data["items"], list)
        assert isinstance(data["total"], int)

    def test_offset_skips_results(self, client: TestClient) -> None:
        # Get first page
        resp1 = client.get("/api/v1/drugs/search?q=a&limit=2&offset=0")
        # Get second page
        resp2 = client.get("/api/v1/drugs/search?q=a&limit=2&offset=2")
        assert resp1.status_code == 200
        assert resp2.status_code == 200
        ids1 = {r["id"] for r in resp1.json()["items"]}
        ids2 = {r["id"] for r in resp2.json()["items"]}
        # Pages should not overlap
        assert ids1.isdisjoint(ids2) or len(ids2) == 0

    def test_has_more_true_when_more_results(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/search?q=a&limit=1&offset=0")
        assert resp.status_code == 200
        data = resp.json()
        if data["total"] > 1:
            assert data["has_more"] is True

    def test_has_more_false_on_last_page(self, client: TestClient) -> None:
        # Use a specific query that returns few results
        resp = client.get("/api/v1/drugs/search?q=Warfarin&limit=50&offset=0")
        data = resp.json()
        # Warfarin exact match returns 1 result, well within limit=50
        assert data["has_more"] is False

    def test_default_offset_is_zero(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/search?q=asp")
        assert resp.json()["offset"] == 0

    def test_negative_offset_rejected(self, client: TestClient) -> None:
        resp = client.get("/api/v1/drugs/search?q=asp&offset=-1")
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# X-Request-ID middleware
# ---------------------------------------------------------------------------


class TestRequestID:
    """Every response has X-Request-ID header."""

    def test_response_has_request_id(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert "x-request-id" in resp.headers
        # Should be valid UUID4
        uuid.UUID(resp.headers["x-request-id"])

    def test_api_response_has_request_id(self, client: TestClient) -> None:
        resp = client.get("/api/v1/stats")
        assert "x-request-id" in resp.headers

    def test_provided_request_id_preserved(self, client: TestClient) -> None:
        custom_id = "test-req-12345"
        resp = client.get("/health", headers={"X-Request-ID": custom_id})
        assert resp.headers["x-request-id"] == custom_id

    def test_generated_request_id_is_uuid4(self, client: TestClient) -> None:
        resp = client.get("/health")
        rid = resp.headers["x-request-id"]
        parsed = uuid.UUID(rid)
        assert parsed.version == 4


# ---------------------------------------------------------------------------
# OpenAPI metadata
# ---------------------------------------------------------------------------


class TestOpenAPIMetadata:
    """OpenAPI spec has proper metadata."""

    def test_openapi_has_tags(self, client: TestClient) -> None:
        resp = client.get("/openapi.json")
        assert resp.status_code == 200
        spec = resp.json()
        tag_names = [t["name"] for t in spec.get("tags", [])]
        assert "system" in tag_names
        assert "drugs" in tag_names
        assert "analysis" in tag_names

    def test_openapi_has_contact(self, client: TestClient) -> None:
        resp = client.get("/openapi.json")
        spec = resp.json()
        assert "contact" in spec["info"]
        assert spec["info"]["contact"]["name"] == "MEDGRAPH Team"

    def test_openapi_has_license(self, client: TestClient) -> None:
        resp = client.get("/openapi.json")
        spec = resp.json()
        assert "license" in spec["info"]
        assert spec["info"]["license"]["name"] == "MIT"

    def test_openapi_has_version(self, client: TestClient) -> None:
        resp = client.get("/openapi.json")
        spec = resp.json()
        assert spec["info"]["version"]  # non-empty version string
