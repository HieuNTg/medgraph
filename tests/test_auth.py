"""
Tests for API key authentication and rate limiting.

Covers:
- Auth disabled (default): all requests pass
- Auth enabled: valid key passes, invalid/missing key returns 401
- Rate limiting: requests within limit pass, exceeding limit returns 429
- Health endpoint: always accessible regardless of auth/rate limit
"""

from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

import medgraph.api.auth as auth_module
from medgraph.api.auth import reset_rate_limits, reload_api_keys
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

    tmp_path = tmp_path_factory.mktemp("auth_test")
    store = GraphStore(tmp_path / "auth_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


@pytest.fixture(autouse=True)
def _reset_auth_state():
    """Reset auth and rate limit state before each test."""
    yield
    # Cleanup: restore defaults
    os.environ.pop("MEDGRAPH_API_KEYS", None)
    reload_api_keys()
    reset_rate_limits()
    auth_module.RATE_LIMIT = 60


def _make_client(seeded_store: GraphStore) -> TestClient:
    """Create TestClient with pre-injected state."""
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

    client = TestClient(app, raise_server_exceptions=True)
    # Re-inject after lifespan
    app.state.store = seeded_store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher
    app.state.stats_cache = (None, 0.0)
    return client


# ---------------------------------------------------------------------------
# Auth disabled (default)
# ---------------------------------------------------------------------------


class TestAuthDisabled:
    def test_api_accessible_without_key(self, seeded_store: GraphStore) -> None:
        """When MEDGRAPH_API_KEYS is unset, API is open."""
        os.environ.pop("MEDGRAPH_API_KEYS", None)
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        resp = client.get("/api/stats")
        assert resp.status_code == 200

    def test_health_always_accessible(self, seeded_store: GraphStore) -> None:
        """Health endpoint has no auth dependency."""
        os.environ["MEDGRAPH_API_KEYS"] = "secret-key-1"
        reload_api_keys()
        client = _make_client(seeded_store)
        resp = client.get("/health")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Auth enabled
# ---------------------------------------------------------------------------


class TestAuthEnabled:
    def test_valid_key_passes(self, seeded_store: GraphStore) -> None:
        os.environ["MEDGRAPH_API_KEYS"] = "test-key-abc"
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        resp = client.get("/api/stats", headers={"X-Api-Key": "test-key-abc"})
        assert resp.status_code == 200

    def test_invalid_key_401(self, seeded_store: GraphStore) -> None:
        os.environ["MEDGRAPH_API_KEYS"] = "test-key-abc"
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        resp = client.get("/api/stats", headers={"X-Api-Key": "wrong-key"})
        assert resp.status_code == 401
        assert "API key" in resp.json()["detail"]

    def test_missing_key_401(self, seeded_store: GraphStore) -> None:
        os.environ["MEDGRAPH_API_KEYS"] = "test-key-abc"
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        resp = client.get("/api/stats")
        assert resp.status_code == 401

    def test_multiple_keys_supported(self, seeded_store: GraphStore) -> None:
        os.environ["MEDGRAPH_API_KEYS"] = "key-1,key-2,key-3"
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        resp = client.get("/api/stats", headers={"X-Api-Key": "key-2"})
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------


class TestRateLimiting:
    def test_within_limit_passes(self, seeded_store: GraphStore) -> None:
        os.environ.pop("MEDGRAPH_API_KEYS", None)
        reload_api_keys()
        reset_rate_limits()
        client = _make_client(seeded_store)
        for _ in range(3):
            resp = client.get("/api/stats")
            assert resp.status_code == 200

    def test_exceeding_limit_429(self, seeded_store: GraphStore) -> None:
        os.environ.pop("MEDGRAPH_API_KEYS", None)
        reload_api_keys()
        reset_rate_limits()
        auth_module.RATE_LIMIT = 3

        client = _make_client(seeded_store)
        for _ in range(3):
            resp = client.get("/api/stats")
            assert resp.status_code == 200

        resp = client.get("/api/stats")
        assert resp.status_code == 429
        assert "Rate limit" in resp.json()["detail"]

    def test_check_endpoint_rate_limited(self, seeded_store: GraphStore) -> None:
        """POST /api/check is also subject to rate limiting."""
        os.environ.pop("MEDGRAPH_API_KEYS", None)
        reload_api_keys()
        reset_rate_limits()
        auth_module.RATE_LIMIT = 1

        client = _make_client(seeded_store)
        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 200

        resp = client.post("/api/check", json={"drugs": ["Warfarin", "Aspirin"]})
        assert resp.status_code == 429
