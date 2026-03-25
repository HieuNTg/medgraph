"""
Tests for API key authentication and rate limiting.

Covers:
- Auth disabled (default): all requests pass
- Auth enabled: valid key passes, invalid/missing key returns 401
- Rate limiting: requests within limit pass, exceeding limit returns 429
- Health endpoint: always accessible regardless of auth/rate limit
- JWT security: production secret validation, refresh token rotation, single-use
- Rate limit pruning: memory leak prevention for large request logs
"""

from __future__ import annotations

import os
import time

import pytest
from fastapi.testclient import TestClient

import medgraph.api.auth as auth_module
from medgraph.api.auth import reset_rate_limits, reload_api_keys, _request_log
from medgraph.api.server import create_app
from medgraph.engine.analyzer import CascadeAnalyzer
from medgraph.api.search import DrugSearcher
from medgraph.graph.builder import GraphBuilder
from medgraph.graph.store import GraphStore
from medgraph.api.user_auth import UserAuth


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
    app.state.user_auth = UserAuth(seeded_store)

    client = TestClient(app, raise_server_exceptions=True)
    # Re-inject after lifespan
    app.state.store = seeded_store
    app.state.graph = graph
    app.state.analyzer = analyzer
    app.state.searcher = searcher
    app.state.stats_cache = (None, 0.0)
    app.state.user_auth = UserAuth(seeded_store)
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


# ---------------------------------------------------------------------------
# JWT security tests
# ---------------------------------------------------------------------------


class TestJWTSecurity:
    """Tests for UserAuth JWT secret validation and refresh token rotation."""

    def _make_store(self, tmp_path_factory):
        """Create a minimal in-memory-backed store for JWT tests."""
        from medgraph.graph.store import GraphStore

        tmp_path = tmp_path_factory.mktemp("jwt_test")
        store = GraphStore(tmp_path / "jwt_test.db")
        return store

    def _make_user_auth(self, store, secret_key=None):
        from medgraph.api.user_auth import UserAuth

        return UserAuth(store, secret_key=secret_key)

    def _register_user(self, ua):
        """Register a throwaway user and return tokens."""
        import uuid

        email = f"test_{uuid.uuid4().hex[:8]}@example.com"
        return ua.register(email=email, password="Password123!", display_name="Test")

    def test_jwt_default_secret_raises_in_production(self, tmp_path_factory) -> None:
        """UserAuth should raise RuntimeError when MEDGRAPH_ENV=production and no secret set."""
        from medgraph.api.user_auth import UserAuth

        store = self._make_store(tmp_path_factory)
        old_env = os.environ.get("MEDGRAPH_ENV")
        old_secret = os.environ.get("MEDGRAPH_JWT_SECRET")
        try:
            os.environ["MEDGRAPH_ENV"] = "production"
            os.environ.pop("MEDGRAPH_JWT_SECRET", None)
            with pytest.raises(RuntimeError, match="MEDGRAPH_JWT_SECRET"):
                UserAuth(store)  # no secret_key passed, env secret absent → dev secret → raises
        finally:
            if old_env is None:
                os.environ.pop("MEDGRAPH_ENV", None)
            else:
                os.environ["MEDGRAPH_ENV"] = old_env
            if old_secret is None:
                os.environ.pop("MEDGRAPH_JWT_SECRET", None)
            else:
                os.environ["MEDGRAPH_JWT_SECRET"] = old_secret

    def test_jwt_refresh_token_rotation(self, tmp_path_factory) -> None:
        """After a successful refresh, old refresh token must be invalid."""
        store = self._make_store(tmp_path_factory)
        ua = self._make_user_auth(store, secret_key="test-secret-key-strong")

        tokens = self._register_user(ua)
        original_rt = tokens["refresh_token"]

        # First refresh succeeds and returns new tokens
        new_tokens = ua.refresh(original_rt)
        assert "refresh_token" in new_tokens
        assert new_tokens["refresh_token"] != original_rt

        # Old refresh token is now invalid (rotated out)
        with pytest.raises(ValueError, match="revoked|already used"):
            ua.refresh(original_rt)

    def test_jwt_refresh_token_single_use(self, tmp_path_factory) -> None:
        """Same refresh token used twice consecutively — second attempt must fail."""
        store = self._make_store(tmp_path_factory)
        ua = self._make_user_auth(store, secret_key="test-secret-key-strong")

        tokens = self._register_user(ua)
        rt = tokens["refresh_token"]

        # First use succeeds
        ua.refresh(rt)

        # Second use with the SAME token fails
        with pytest.raises(ValueError):
            ua.refresh(rt)


# ---------------------------------------------------------------------------
# Rate limit pruning test
# ---------------------------------------------------------------------------


class TestRateLimitPruning:
    def test_rate_limit_prunes_old_entries(self) -> None:
        """
        When _request_log exceeds 10,000 keys, stale entries are pruned.
        After pruning, the dict should not grow unboundedly.
        """
        reset_rate_limits()
        # Populate 10,001 fake stale client entries (timestamps far in the past)
        past_time = time.monotonic() - auth_module.RATE_WINDOW - 10
        for i in range(10_001):
            _request_log[f"ip:192.0.2.{i % 256}_{i}"] = [past_time]

        assert len(_request_log) > 10_000

        # Triggering _check_rate_limit on any new client triggers pruning
        from medgraph.api.auth import _check_rate_limit

        allowed = _check_rate_limit("ip:trigger-prune")
        assert allowed is True  # new client should be allowed

        # After pruning, stale keys should be removed — dict size should be small
        # (only the trigger client remains plus any non-stale entries)
        assert len(_request_log) < 10_001, (
            f"Expected pruning to reduce dict, still have {len(_request_log)} entries"
        )

        reset_rate_limits()  # cleanup
