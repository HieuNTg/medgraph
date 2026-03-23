"""
Tests for Phase 3: Observability & Monitoring features.

Covers: Prometheus metrics, health check split (live/ready),
Sentry env-gated init, request_id in structured logs.
"""

from __future__ import annotations

import json
import logging
import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from medgraph.api.server import create_app
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.api.search import DrugSearcher
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.store import GraphStore
from medgraph.logging_config import JSONFormatter


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("obs_test")
    store = GraphStore(tmp_path / "obs.db")
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
# Prometheus Metrics
# ---------------------------------------------------------------------------


class TestPrometheusMetrics:
    def test_metrics_endpoint_exists(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        assert resp.status_code == 200

    def test_metrics_returns_prometheus_format(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        text = resp.text
        # Prometheus text format contains HELP and TYPE lines
        assert "# HELP" in text or "# TYPE" in text

    def test_custom_graph_gauge_present(self, client: TestClient) -> None:
        # Trigger a request first to ensure metrics are populated
        client.get("/health")
        resp = client.get("/metrics")
        text = resp.text
        assert "medgraph_graph_nodes_total" in text
        assert "medgraph_graph_edges_total" in text

    def test_analysis_duration_metric_registered(self, client: TestClient) -> None:
        resp = client.get("/metrics")
        assert "medgraph_analysis_duration_seconds" in resp.text


# ---------------------------------------------------------------------------
# Health Check Split
# ---------------------------------------------------------------------------


class TestHealthChecks:
    def test_health_live_returns_200(self, client: TestClient) -> None:
        resp = client.get("/health/live")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_health_live_no_db_fields(self, client: TestClient) -> None:
        resp = client.get("/health/live")
        data = resp.json()
        assert "db_size" not in data
        assert "graph_nodes" not in data

    def test_health_ready_returns_200(self, client: TestClient) -> None:
        resp = client.get("/health/ready")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "db_size" in data
        assert "graph_nodes" in data

    def test_health_backward_compat(self, client: TestClient) -> None:
        """GET /health still works as alias for /health/ready."""
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "db_size" in data

    def test_health_live_no_auth_required(self, client: TestClient) -> None:
        """Health endpoints don't require API key."""
        resp = client.get("/health/live")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Sentry Integration
# ---------------------------------------------------------------------------


class TestSentryIntegration:
    def test_no_sentry_when_dsn_absent(self) -> None:
        """Sentry should NOT be initialized when SENTRY_DSN is not set."""
        env = os.environ.copy()
        env.pop("SENTRY_DSN", None)
        with patch.dict(os.environ, env, clear=True):
            # Should not raise even without sentry-sdk installed
            from medgraph.api.server import _init_sentry

            _init_sentry()  # no-op when DSN absent

    def test_sentry_skipped_when_sdk_missing(self) -> None:
        """Sentry logs warning if DSN set but SDK not installed."""
        import sys
        from medgraph.api.server import _init_sentry

        with patch.dict(os.environ, {"SENTRY_DSN": "https://fake@sentry.io/123"}):
            # Block sentry_sdk import by setting to None in sys.modules
            with patch.dict(
                sys.modules,
                {"sentry_sdk": None, "sentry_sdk.integrations.fastapi": None},
            ):
                # Should not raise — graceful fallback with warning
                _init_sentry()


# ---------------------------------------------------------------------------
# Request ID in Structured Logs
# ---------------------------------------------------------------------------


class TestRequestIDInLogs:
    def test_json_formatter_includes_request_id(self) -> None:
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )
        record.request_id = "test-req-abc"
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["request_id"] == "test-req-abc"

    def test_json_formatter_omits_request_id_when_absent(self) -> None:
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert "request_id" not in parsed

    def test_request_id_propagated_in_response(self, client: TestClient) -> None:
        """Middleware sets X-Request-ID on response."""
        resp = client.get("/health/live")
        assert "x-request-id" in resp.headers
