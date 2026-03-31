"""
FAERS Auto-Refresh Service for MEDGRAPH.

Provides incremental OpenFDA FAERS refresh with:
- IncrementalFAERSClient: async httpx queries for events since last refresh
- Deduplication via hash-based keys (drug_pair + reaction)
- Quality scoring for reactions (normalized_count, meddra_level, signal_trend)
- In-memory job history (deque, max 100 entries)
- Retry logic with exponential backoff (max 3 retries)
- Persistence via refresh_metadata SQLite table

NOTE: Scheduling (APScheduler / systemd) is intentionally excluded here —
this module implements the refresh logic only. Integrate into a scheduler
externally (v0.3.0 roadmap item).
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import httpx

from medgraph.graph.models import AdverseEvent

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# OpenFDA endpoint
_OPENFDA_EVENT_URL = "https://api.fda.gov/drug/event.json"

# Retry configuration
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.0  # seconds

# Freshness threshold: treat data as stale if older than this
_FRESHNESS_DAYS = 7


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class RefreshJob:
    """Record of a single refresh run."""

    job_id: str
    status: str  # "running" | "completed" | "failed"
    sources_attempted: list[str] = field(default_factory=list)
    sources_succeeded: list[str] = field(default_factory=list)
    sources_failed: list[str] = field(default_factory=list)
    records_updated: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    errors: dict[str, str] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Incremental FAERS client (async)
# ---------------------------------------------------------------------------


class IncrementalFAERSClient:
    """
    Async httpx client for OpenFDA FAERS adverse event queries.

    Supports incremental fetches (events since a given datetime),
    quality scoring, deduplication, and exponential backoff retries.
    """

    def __init__(self, timeout: float = 15.0) -> None:
        self.timeout = timeout

    async def search_adverse_events_incremental(
        self,
        drug_names: list[str],
        since: datetime,
        limit: int = 1000,
    ) -> list[AdverseEvent]:
        """
        Query FAERS for reaction counts involving drug_names since `since`.

        Uses the count endpoint (aggregated reaction terms), so `since` is
        used as a filter hint in the search string.  Returns parsed,
        deduplicated, quality-scored AdverseEvent objects.
        """
        if not drug_names:
            return []

        query_parts = [f'patient.drug.openfda.generic_name:"{name}"' for name in drug_names]
        # Incremental date filter (receivedate >= since)
        since_str = since.strftime("%Y%m%d")
        date_filter = f"receivedate:[{since_str}+TO+*]"
        search = "+AND+".join(query_parts) + "+AND+" + date_filter

        params: dict = {
            "search": search,
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": limit,
        }

        data = await self._get_with_retry(_OPENFDA_EVENT_URL, params)
        return self._parse_and_validate(data, drug_names)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _get_with_retry(self, url: str, params: dict) -> dict:
        """GET with exponential backoff retry up to _MAX_RETRIES."""
        for attempt in range(_MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.get(url, params=params)
                    if resp.status_code == 200:
                        return resp.json()
                    elif resp.status_code == 404:
                        return {}  # No results — not an error
                    elif resp.status_code == 429:
                        wait = _BACKOFF_BASE * (2**attempt)
                        logger.warning(
                            "OpenFDA rate limited — backing off %.1fs (attempt %d/%d)",
                            wait,
                            attempt + 1,
                            _MAX_RETRIES,
                        )
                        await asyncio.sleep(wait)
                    else:
                        logger.warning("OpenFDA HTTP %d for %s", resp.status_code, url)
                        return {}
            except httpx.TimeoutException:
                wait = _BACKOFF_BASE * (2**attempt)
                logger.warning(
                    "OpenFDA timeout on attempt %d/%d — retrying in %.1fs",
                    attempt + 1,
                    _MAX_RETRIES,
                    wait,
                )
                if attempt < _MAX_RETRIES - 1:
                    await asyncio.sleep(wait)
            except httpx.RequestError as exc:
                logger.warning("OpenFDA request error: %s", exc)
                return {}
        logger.error("OpenFDA: exhausted %d retries for %s", _MAX_RETRIES, url)
        return {}

    def _parse_and_validate(self, data: dict, drug_names: list[str]) -> list[AdverseEvent]:
        """
        Parse count-endpoint response into AdverseEvent objects.

        Applies:
          - Reaction validity check (length, non-empty)
          - Quality scoring (normalized_count * 0.5 + meddra_score * 0.3)
          - Hash-based deduplication
          - Discard reactions with quality_score < 0.1
        """
        results = data.get("results", [])
        if not results:
            return []

        max_count = max((r.get("count", 0) for r in results), default=1) or 1
        seen: set[str] = set()
        events: list[AdverseEvent] = []

        for item in results:
            term = item.get("term", "")
            count = item.get("count", 0)

            # Validity check
            if not term or len(term) > 200:
                continue

            # Quality score
            normalized = count / max_count
            meddra = self._meddra_score(term)
            quality = normalized * 0.5 + meddra * 0.3
            if quality < 0.1:
                continue

            # Deduplication
            dedup_key = hashlib.md5(f"{':'.join(sorted(drug_names))}:{term}".encode()).hexdigest()
            if dedup_key in seen:
                continue
            seen.add(dedup_key)

            events.append(
                AdverseEvent(
                    id=f"FAERS-{dedup_key[:12]}",
                    drug_ids=list(drug_names),
                    reaction=term,
                    count=count,
                    seriousness="unknown",
                    source_url=_OPENFDA_EVENT_URL,
                )
            )

        return events

    @staticmethod
    def _meddra_score(term: str) -> float:
        """
        Heuristic MedDRA quality score.

        Known PT-level terms (single capitalised words / short phrases) score
        higher than generic or suspiciously long terms.
        """
        words = term.split()
        if len(words) == 0:
            return 0.0
        if len(words) <= 3:
            return 1.0  # Likely a Preferred Term
        if len(words) <= 6:
            return 0.6  # Possibly HLT or LLT
        return 0.3  # Long/free-text — lower confidence


# ---------------------------------------------------------------------------
# Refresh service
# ---------------------------------------------------------------------------


class RefreshService:
    """
    Orchestrates incremental FAERS data refresh.

    - Queries OpenFDA for new adverse events since last recorded refresh
    - Persists results via GraphStore
    - Tracks job history in-memory (max 100 entries) and in refresh_metadata table
    - No scheduler embedded — call trigger_refresh() from CLI or API handler
    """

    def __init__(self, store: GraphStore) -> None:
        self._store = store
        self._client = IncrementalFAERSClient()
        self._jobs: deque[dict] = deque(maxlen=100)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def trigger_refresh(
        self,
        sources: list[str] | None = None,
        force: bool = False,
    ) -> RefreshJob:
        """
        Run an incremental FAERS refresh.

        Args:
            sources: List of source names to refresh. Currently only "openfda"
                     is supported. Defaults to ["openfda"].
            force:   If True, bypass freshness check.

        Returns:
            RefreshJob summarising the run.
        """
        targets = sources if sources else ["openfda"]
        job = RefreshJob(
            job_id=f"refresh_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}",
            status="running",
            sources_attempted=list(targets),
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._jobs.append(self._job_to_dict(job))

        for source in targets:
            if source != "openfda":
                msg = f"Unsupported source: {source}"
                job.sources_failed.append(source)
                job.errors[source] = msg
                logger.warning(msg)
                continue

            try:
                updated = await self._refresh_openfda_incremental(force=force)
                job.sources_succeeded.append(source)
                job.records_updated += updated
                self._store.save_refresh_metadata(
                    source=source,
                    records_updated=updated,
                    status="completed",
                )
            except Exception as exc:
                logger.exception("FAERS incremental refresh failed for source '%s'", source)
                job.sources_failed.append(source)
                job.errors[source] = str(exc)
                self._store.save_refresh_metadata(
                    source=source,
                    records_updated=0,
                    status="failed",
                )

        job.status = "completed" if not job.sources_failed else "failed"
        # Update in-memory record (replace last entry)
        if self._jobs:
            self._jobs[-1] = self._job_to_dict(job)

        logger.info(
            "Refresh job %s finished — status=%s records_updated=%d",
            job.job_id,
            job.status,
            job.records_updated,
        )
        return job

    def get_job_history(self, limit: int = 20) -> list[dict]:
        """Return recent in-memory job records, newest first."""
        history = list(self._jobs)
        history.reverse()
        return history[:limit]

    def get_freshness(self, source: str = "openfda") -> dict:
        """
        Return freshness metadata for the given source.

        Checks refresh_metadata table (persistent) first; falls back to
        schema_metadata last_refresh_timestamp for backward compatibility.
        """
        row = self._store.get_last_refresh(source)
        if row:
            last_refresh_str: str | None = row["last_refresh"]
        else:
            # Backward-compat fallback: check old schema_metadata key
            last_refresh_str = self._get_legacy_metadata("last_refresh_timestamp")

        is_fresh = False
        days_since: float | None = None
        if last_refresh_str:
            try:
                last_dt = datetime.fromisoformat(last_refresh_str)
                if last_dt.tzinfo is None:
                    last_dt = last_dt.replace(tzinfo=timezone.utc)
                delta = datetime.now(timezone.utc) - last_dt
                days_since = delta.total_seconds() / 86400
                is_fresh = delta < timedelta(days=_FRESHNESS_DAYS)
            except ValueError:
                pass

        data_version = self._get_legacy_metadata("data_version") or "0"

        return {
            "last_refresh": last_refresh_str,
            "last_successful_source": source
            if (row and row.get("status") == "completed")
            else None,
            "days_since_refresh": round(days_since, 4) if days_since is not None else None,
            "is_fresh": is_fresh,
            "data_version": data_version,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _refresh_openfda_incremental(self, force: bool = False) -> int:
        """
        Run incremental FAERS refresh for all known drugs.

        Determines `since` from last recorded refresh; falls back to 30 days
        ago on first run. Batches drugs to avoid URL length limits.

        Returns number of adverse events upserted.
        """
        # Determine since-timestamp
        row = self._store.get_last_refresh("openfda")
        if row and row.get("status") == "completed" and not force:
            try:
                since = datetime.fromisoformat(row["last_refresh"])
                if since.tzinfo is None:
                    since = since.replace(tzinfo=timezone.utc)
            except ValueError:
                since = datetime.now(timezone.utc) - timedelta(days=30)
        else:
            since = datetime.now(timezone.utc) - timedelta(days=30)

        all_drugs = [d.name for d in self._store.get_all_drugs()]
        if not all_drugs:
            logger.info("No drugs in store — skipping FAERS refresh")
            return 0

        # Build name→id mapping for FK resolution
        name_to_id = {d.name.lower(): d.id for d in self._store.get_all_drugs()}

        total = 0
        for batch in _batch(all_drugs, size=5):
            events = await self._client.search_adverse_events_incremental(
                drug_names=batch,
                since=since,
                limit=1000,
            )
            for event in events:
                # Resolve drug names to IDs so FK constraints are satisfied
                resolved_ids = [name_to_id.get(name.lower(), name) for name in event.drug_ids]
                event = event.model_copy(update={"drug_ids": resolved_ids})
                try:
                    self._store.upsert_adverse_event(event)
                    total += 1
                except Exception:
                    logger.debug("Failed to upsert adverse event %s", event.id, exc_info=True)

        logger.info(
            "Incremental FAERS refresh: %d records upserted (since %s)", total, since.date()
        )
        return total

    def _get_legacy_metadata(self, key: str) -> str | None:
        """Read a value from schema_metadata (backward-compat)."""
        try:
            with self._store._connect() as conn:
                row = conn.execute(
                    "SELECT value FROM schema_metadata WHERE key = ?", (key,)
                ).fetchone()
            return row["value"] if row else None
        except Exception:
            return None

    @staticmethod
    def _job_to_dict(job: RefreshJob) -> dict:
        return {
            "job_id": job.job_id,
            "status": job.status,
            "sources_attempted": job.sources_attempted,
            "sources_succeeded": job.sources_succeeded,
            "sources_failed": job.sources_failed,
            "records_updated": job.records_updated,
            "timestamp": job.timestamp,
            "errors": job.errors,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _batch(items: list, size: int):
    """Yield successive fixed-size chunks from items."""
    for i in range(0, len(items), size):
        yield items[i : i + size]
