"""
Unit and integration tests for the FAERS Auto-Refresh Pipeline.

Tests:
  - IncrementalFAERSClient: quality scoring, deduplication, edge cases
  - RefreshService: trigger_refresh, get_job_history, get_freshness
  - GraphStore: save_refresh_metadata, get_last_refresh, get_refresh_history
  - API endpoints: POST /admin/refresh, GET /admin/refresh/jobs, GET /health/freshness
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from medgraph.data.refresh_service import (
    IncrementalFAERSClient,
    RefreshService,
    _batch,
)
from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_store(tmp_path: Path) -> GraphStore:
    return GraphStore(tmp_path / "test_refresh.db")


@pytest.fixture
def refresh_svc(tmp_store: GraphStore) -> RefreshService:
    return RefreshService(tmp_store)


# ---------------------------------------------------------------------------
# Helper: run async in sync test
# ---------------------------------------------------------------------------


def run(coro):
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# GraphStore refresh_metadata methods
# ---------------------------------------------------------------------------


class TestStoreRefreshMetadata:
    def test_save_and_get_last_refresh(self, tmp_store: GraphStore) -> None:
        tmp_store.save_refresh_metadata("openfda", 42, "completed")
        row = tmp_store.get_last_refresh("openfda")
        assert row is not None
        assert row["source"] == "openfda"
        assert row["records_updated"] == 42
        assert row["status"] == "completed"

    def test_get_last_refresh_none_when_empty(self, tmp_store: GraphStore) -> None:
        assert tmp_store.get_last_refresh("openfda") is None

    def test_get_refresh_history(self, tmp_store: GraphStore) -> None:
        tmp_store.save_refresh_metadata("openfda", 10, "completed")
        tmp_store.save_refresh_metadata("openfda", 5, "failed")
        history = tmp_store.get_refresh_history(limit=10)
        assert len(history) == 2
        # Newest first
        assert history[0]["records_updated"] == 5

    def test_get_refresh_history_respects_limit(self, tmp_store: GraphStore) -> None:
        for i in range(5):
            tmp_store.save_refresh_metadata("openfda", i, "completed")
        history = tmp_store.get_refresh_history(limit=3)
        assert len(history) == 3

    def test_multiple_sources(self, tmp_store: GraphStore) -> None:
        tmp_store.save_refresh_metadata("openfda", 10, "completed")
        tmp_store.save_refresh_metadata("drugbank", 20, "completed")
        openfda_row = tmp_store.get_last_refresh("openfda")
        drugbank_row = tmp_store.get_last_refresh("drugbank")
        assert openfda_row["source"] == "openfda"
        assert drugbank_row["source"] == "drugbank"


# ---------------------------------------------------------------------------
# IncrementalFAERSClient: _parse_and_validate
# ---------------------------------------------------------------------------


class TestIncrementalFAERSClientParsing:
    def setup_method(self) -> None:
        self.client = IncrementalFAERSClient()

    def test_empty_results(self) -> None:
        events = self.client._parse_and_validate({}, ["warfarin"])
        assert events == []

    def test_basic_parsing(self) -> None:
        data = {
            "results": [
                {"term": "Nausea", "count": 100},
                {"term": "Headache", "count": 50},
            ]
        }
        events = self.client._parse_and_validate(data, ["warfarin"])
        assert len(events) == 2
        terms = {e.reaction for e in events}
        assert "Nausea" in terms
        assert "Headache" in terms

    def test_deduplication(self) -> None:
        # Same drug names + reaction → deduplicated
        data = {
            "results": [
                {"term": "Nausea", "count": 100},
                {"term": "Nausea", "count": 80},  # duplicate
            ]
        }
        events = self.client._parse_and_validate(data, ["warfarin"])
        assert len(events) == 1

    def test_quality_filter_low_score(self) -> None:
        # A single item with count=1 vs max=100 → normalized=0.01
        # meddra_score for single word = 1.0 → quality = 0.01*0.5 + 1.0*0.3 = 0.305 → passes
        data = {
            "results": [
                {"term": "Nausea", "count": 100},
                {"term": "Rash", "count": 1},
            ]
        }
        events = self.client._parse_and_validate(data, ["warfarin"])
        # Both should pass (meddra component saves the low-count one)
        assert len(events) == 2

    def test_rejects_empty_term(self) -> None:
        data = {"results": [{"term": "", "count": 100}]}
        events = self.client._parse_and_validate(data, ["warfarin"])
        assert events == []

    def test_rejects_term_over_200_chars(self) -> None:
        long_term = "A" * 201
        data = {"results": [{"term": long_term, "count": 100}]}
        events = self.client._parse_and_validate(data, ["warfarin"])
        assert events == []

    def test_adverse_event_id_format(self) -> None:
        data = {"results": [{"term": "Nausea", "count": 50}]}
        events = self.client._parse_and_validate(data, ["warfarin"])
        assert len(events) == 1
        assert events[0].id.startswith("FAERS-")
        assert len(events[0].id) == len("FAERS-") + 12

    def test_drug_names_sorted_for_dedup(self) -> None:
        # Drug name order should not affect dedup key
        data = {"results": [{"term": "Nausea", "count": 50}]}
        events_ab = self.client._parse_and_validate(data, ["aspirin", "warfarin"])
        events_ba = self.client._parse_and_validate(data, ["warfarin", "aspirin"])
        assert events_ab[0].id == events_ba[0].id

    def test_meddra_score_single_word(self) -> None:
        assert IncrementalFAERSClient._meddra_score("Nausea") == 1.0

    def test_meddra_score_three_words(self) -> None:
        assert IncrementalFAERSClient._meddra_score("Nausea and vomiting") == 1.0

    def test_meddra_score_long_term(self) -> None:
        assert IncrementalFAERSClient._meddra_score("Very long free text term reaction here") == 0.3


# ---------------------------------------------------------------------------
# _batch helper
# ---------------------------------------------------------------------------


class TestBatch:
    def test_even_split(self) -> None:
        result = list(_batch([1, 2, 3, 4, 5, 6], 2))
        assert result == [[1, 2], [3, 4], [5, 6]]

    def test_uneven_split(self) -> None:
        result = list(_batch([1, 2, 3, 4, 5], 2))
        assert result == [[1, 2], [3, 4], [5]]

    def test_empty(self) -> None:
        assert list(_batch([], 5)) == []


# ---------------------------------------------------------------------------
# RefreshService
# ---------------------------------------------------------------------------


class TestRefreshService:
    def test_get_freshness_no_data(self, refresh_svc: RefreshService) -> None:
        info = refresh_svc.get_freshness("openfda")
        assert info["is_fresh"] is False
        assert info["last_refresh"] is None
        assert info["days_since_refresh"] is None

    def test_get_freshness_after_save(
        self, tmp_store: GraphStore, refresh_svc: RefreshService
    ) -> None:
        tmp_store.save_refresh_metadata("openfda", 10, "completed")
        info = refresh_svc.get_freshness("openfda")
        assert info["is_fresh"] is True
        assert info["days_since_refresh"] is not None
        assert info["days_since_refresh"] < 1.0

    def test_get_freshness_stale(
        self, tmp_store: GraphStore, refresh_svc: RefreshService
    ) -> None:
        # Manually insert old record
        with tmp_store._connect() as conn:
            old_ts = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
            conn.execute(
                "INSERT INTO refresh_metadata (source, last_refresh, records_updated, status, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                ("openfda", old_ts, 5, "completed", old_ts),
            )
        info = refresh_svc.get_freshness("openfda")
        assert info["is_fresh"] is False
        assert info["days_since_refresh"] > 7.0

    def test_job_history_empty_initially(self, refresh_svc: RefreshService) -> None:
        assert refresh_svc.get_job_history() == []

    def test_trigger_refresh_no_drugs(self, refresh_svc: RefreshService) -> None:
        """Refresh with empty drug store should return 0 records (no API call)."""
        job = run(refresh_svc.trigger_refresh(sources=["openfda"]))
        assert job.records_updated == 0
        assert "openfda" in job.sources_succeeded

    def test_trigger_refresh_unknown_source(self, refresh_svc: RefreshService) -> None:
        job = run(refresh_svc.trigger_refresh(sources=["unknown_source"]))
        assert "unknown_source" in job.sources_failed
        assert job.status == "failed"

    def test_trigger_refresh_records_job_history(self, refresh_svc: RefreshService) -> None:
        run(refresh_svc.trigger_refresh(sources=["openfda"]))
        history = refresh_svc.get_job_history()
        assert len(history) == 1
        assert history[0]["sources_attempted"] == ["openfda"]

    def test_trigger_refresh_persists_to_db(
        self, tmp_store: GraphStore, refresh_svc: RefreshService
    ) -> None:
        run(refresh_svc.trigger_refresh(sources=["openfda"]))
        row = tmp_store.get_last_refresh("openfda")
        assert row is not None
        assert row["status"] == "completed"

    def test_trigger_refresh_with_mocked_api(
        self, tmp_store: GraphStore
    ) -> None:
        """Test full refresh flow with mocked OpenFDA response."""
        from medgraph.data.seed import DataSeeder

        seeder = DataSeeder(store=tmp_store, skip_openfda=True)
        seeder.run()

        mock_response = {
            "results": [
                {"term": "Nausea", "count": 100},
                {"term": "Headache", "count": 60},
            ]
        }

        svc = RefreshService(tmp_store)

        with patch.object(
            svc._client,
            "_get_with_retry",
            new=AsyncMock(return_value=mock_response),
        ):
            job = run(svc.trigger_refresh(sources=["openfda"]))

        assert job.status == "completed"
        assert job.records_updated > 0


# ---------------------------------------------------------------------------
# API endpoint tests (light — no server startup required)
# ---------------------------------------------------------------------------


class TestHealthFreshnessEndpoint:
    """Test /health/freshness endpoint via TestClient."""

    def test_health_freshness_returns_200(self) -> None:
        """Ensure endpoint returns 200 with expected fields."""
        from fastapi.testclient import TestClient
        from medgraph.api.server import create_app

        app = create_app()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/freshness")
        assert resp.status_code == 200
        data = resp.json()
        assert "is_fresh" in data
        assert "last_refresh" in data
        assert "days_since_refresh" in data
