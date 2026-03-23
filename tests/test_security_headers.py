"""
Tests for security headers middleware and CORS configuration.

Covers: SecurityHeadersMiddleware response headers, HSTS env gating, CORS env var parsing.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

from medgraph.api.server import create_app
from medgraph.api.search import DrugSearcher
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("sec_test")
    store = GraphStore(tmp_path / "sec_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


@contextmanager
def _make_client(seeded_store: GraphStore, env_overrides: dict | None = None):
    """Build a TestClient with optional env var overrides."""
    env = env_overrides or {}
    with patch.dict(os.environ, env, clear=False):
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
            yield c


@pytest.fixture(scope="module")
def client(seeded_store: GraphStore):
    with _make_client(seeded_store) as c:
        yield c


# ---------------------------------------------------------------------------
# Security Headers
# ---------------------------------------------------------------------------


class TestSecurityHeaders:
    def test_x_content_type_options(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.headers.get("x-frame-options") == "DENY"

    def test_referrer_policy(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.headers.get("referrer-policy") == "strict-origin-when-cross-origin"

    def test_permissions_policy(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert "geolocation=()" in resp.headers.get("permissions-policy", "")

    def test_csp_report_only(self, client: TestClient) -> None:
        resp = client.get("/health")
        csp = resp.headers.get("content-security-policy-report-only", "")
        assert "default-src 'self'" in csp

    def test_no_hsts_in_development(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert "strict-transport-security" not in resp.headers

    def test_hsts_in_production(self, seeded_store: GraphStore) -> None:
        with _make_client(seeded_store, {"MEDGRAPH_ENV": "production"}) as prod_client:
            resp = prod_client.get("/health")
            assert "max-age=63072000" in resp.headers.get("strict-transport-security", "")

    def test_headers_on_health_endpoint(self, client: TestClient) -> None:
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.headers.get("x-content-type-options") == "nosniff"
        assert resp.headers.get("x-frame-options") == "DENY"


# ---------------------------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------------------------


class TestCORSConfig:
    def test_default_cors_allows_localhost(self, client: TestClient) -> None:
        resp = client.options(
            "/health",
            headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
        )
        assert resp.headers.get("access-control-allow-origin") == "http://localhost:5173"

    def test_custom_cors_origin(self, seeded_store: GraphStore) -> None:
        with _make_client(
            seeded_store, {"MEDGRAPH_CORS_ORIGINS": "https://myapp.example.com"}
        ) as custom_client:
            resp = custom_client.options(
                "/health",
                headers={
                    "Origin": "https://myapp.example.com",
                    "Access-Control-Request-Method": "GET",
                },
            )
            assert (
                resp.headers.get("access-control-allow-origin") == "https://myapp.example.com"
            )
