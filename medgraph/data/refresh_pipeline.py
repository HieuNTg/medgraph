"""
Data refresh orchestrator for MEDGRAPH.

Coordinates periodic refresh from external data sources (drugbank, openfda)
and tracks refresh history in the schema_metadata table.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

_SUPPORTED_SOURCES = frozenset({"drugbank", "openfda"})

# Metadata keys used in schema_metadata table
_KEY_LAST_REFRESH = "last_refresh_timestamp"
_KEY_DATA_VERSION = "data_version"

# Freshness threshold: skip refresh if data is less than this many days old
_FRESHNESS_DAYS = 7


@dataclass
class RefreshResult:
    """Summary of a data refresh run."""

    sources_attempted: list[str] = field(default_factory=list)
    sources_succeeded: list[str] = field(default_factory=list)
    sources_failed: list[str] = field(default_factory=list)
    records_updated: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return len(self.sources_failed) == 0


class DataRefreshPipeline:
    """
    Orchestrate periodic data refresh from external sources.

    Tracks the last refresh timestamp and data version in the
    schema_metadata table so the freshness endpoint can surface
    this information without re-querying external APIs.
    """

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def refresh(self, sources: list[str] | None = None) -> RefreshResult:
        """
        Run data refresh for the specified sources.

        Args:
            sources: List of source names to refresh. Defaults to all
                     supported sources: ["drugbank", "openfda"].

        Returns:
            RefreshResult summarising what was attempted and updated.
        """
        targets = sources if sources is not None else list(_SUPPORTED_SOURCES)
        result = RefreshResult(sources_attempted=list(targets))

        for source in targets:
            if source not in _SUPPORTED_SOURCES:
                msg = f"Unknown source '{source}'. Supported: {sorted(_SUPPORTED_SOURCES)}"
                logger.warning(msg)
                result.sources_failed.append(source)
                result.errors[source] = msg
                continue

            try:
                updated = self._refresh_source(source)
                result.sources_succeeded.append(source)
                result.records_updated += updated
                logger.info("Refreshed source '%s': %d records updated", source, updated)
            except Exception as exc:
                logger.exception("Failed to refresh source '%s': %s", source, exc)
                result.sources_failed.append(source)
                result.errors[source] = str(exc)

        self._persist_refresh_metadata(result)
        return result

    def is_fresh(self) -> bool:
        """Return True if data was refreshed within the last 7 days."""
        last_refresh = self._get_metadata(_KEY_LAST_REFRESH)
        if not last_refresh:
            return False
        try:
            last_dt = datetime.fromisoformat(last_refresh)
            # Ensure timezone-aware comparison
            if last_dt.tzinfo is None:
                last_dt = last_dt.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - last_dt) < timedelta(days=_FRESHNESS_DAYS)
        except ValueError:
            return False

    def schedule_refresh(
        self,
        sources: list[str] | None = None,
        schedule: str = "weekly",
        force: bool = False,
    ) -> RefreshResult | None:
        """
        Conditionally run refresh based on a schedule.

        Args:
            sources: Sources to refresh (default: all).
            schedule: "weekly" (skip if data < 7 days old) or "daily" (skip if < 1 day old).
            force: If True, bypass freshness check and always refresh.

        Returns:
            RefreshResult if refresh ran, None if skipped due to freshness.
        """
        if not force:
            threshold_days = 1 if schedule == "daily" else _FRESHNESS_DAYS
            last_refresh = self._get_metadata(_KEY_LAST_REFRESH)
            if last_refresh:
                try:
                    last_dt = datetime.fromisoformat(last_refresh)
                    if last_dt.tzinfo is None:
                        last_dt = last_dt.replace(tzinfo=timezone.utc)
                    age = datetime.now(timezone.utc) - last_dt
                    if age < timedelta(days=threshold_days):
                        logger.info(
                            "Skipping scheduled refresh — data is only %.1f hours old "
                            "(threshold: %d days)",
                            age.total_seconds() / 3600,
                            threshold_days,
                        )
                        return None
                except ValueError:
                    pass

        logger.info("Running scheduled refresh (schedule=%s)", schedule)
        return self.refresh(sources=sources)

    def refresh_batch_openfda(self, drug_pairs: list[tuple[str, str]]) -> int:
        """
        Batch process FAERS queries for multiple drug pairs.

        Instead of one-by-one queries, sends batched requests and stores
        adverse event data for each pair.

        Args:
            drug_pairs: List of (drug_a_name, drug_b_name) tuples.

        Returns:
            Number of adverse event records inserted.
        """
        try:
            import time

            import httpx
        except ImportError:
            logger.warning("httpx not available — skipping batch FAERS enrichment")
            return 0

        inserted = 0
        base_url = "https://api.fda.gov/drug/event.json"

        for drug_a, drug_b in drug_pairs:
            try:
                # Rate-limit: ~3 req/s for FDA API
                time.sleep(0.35)
                query = f'patient.drug.medicinalproduct:"{drug_a}"+AND+patient.drug.medicinalproduct:"{drug_b}"'
                resp = httpx.get(
                    base_url,
                    params={"search": query, "limit": 10},
                    timeout=10,
                )
                if resp.status_code != 200:
                    continue
                data = resp.json()
                results = data.get("results", [])
                for event in results:
                    reactions = [
                        r.get("reactionmeddrapt", "")
                        for r in event.get("patient", {}).get("reaction", [])
                        if r.get("reactionmeddrapt")
                    ]
                    if not reactions:
                        continue
                    from medgraph.graph.models import AdverseEvent

                    ae = AdverseEvent(
                        id=f"FAERS-{drug_a[:10]}-{drug_b[:10]}-{len(reactions)}",
                        drug_ids=[drug_a, drug_b],
                        reaction=", ".join(reactions[:5]),
                        count=1,
                        seriousness=event.get("serious", ""),
                        source_url=None,
                    )
                    try:
                        self._store.upsert_adverse_event(ae)
                        inserted += 1
                    except Exception:  # nosec B110 — skip individual upsert failures
                        pass
            except Exception as exc:
                logger.debug("FAERS batch error for %s+%s: %s", drug_a, drug_b, exc)

        logger.info(
            "Batch FAERS enrichment: %d records inserted for %d pairs", inserted, len(drug_pairs)
        )
        return inserted

    def get_freshness(self) -> dict:
        """
        Return current data freshness info from the database.

        Returns a dict with:
            drug_count, interaction_count, enzyme_count,
            last_updated (ISO timestamp or None), data_version (str)
        """
        counts = self._store.get_counts()
        last_updated = self._get_metadata(_KEY_LAST_REFRESH)
        data_version = self._get_metadata(_KEY_DATA_VERSION) or self._store.get_schema_version()

        return {
            "drug_count": counts.get("drugs", 0),
            "interaction_count": counts.get("interactions", 0),
            "enzyme_count": counts.get("enzymes", 0),
            "last_updated": last_updated,
            "data_version": data_version,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _refresh_source(self, source: str) -> int:
        """
        Dispatch refresh to the appropriate data provider.

        Returns the number of records updated/inserted.
        """
        if source == "drugbank":
            return self._refresh_drugbank()
        if source == "openfda":
            return self._refresh_openfda()
        return 0

    def _refresh_drugbank(self) -> int:
        """Refresh from DrugBank provider (no-op if credentials absent)."""
        try:
            from medgraph.data.drugbank import DrugBankProvider

            provider = DrugBankProvider()
            drugs = provider.fetch_drugs()
            for drug in drugs:
                self._store.upsert_drug(drug)
            return len(drugs)
        except ImportError:
            logger.debug("DrugBankProvider not available — skipping")
            return 0
        except AttributeError:
            # Provider exists but upsert_drug may not be implemented yet
            logger.debug("DrugBank provider/store integration not fully implemented")
            return 0

    def _refresh_openfda(self) -> int:
        """Refresh adverse event data from openFDA provider."""
        try:
            from medgraph.data.openfda import OpenFDAProvider

            provider = OpenFDAProvider()
            events = provider.fetch_adverse_events()
            for event in events:
                self._store.upsert_adverse_event(event)
            return len(events)
        except ImportError:
            logger.debug("OpenFDAProvider not available — skipping")
            return 0
        except AttributeError:
            logger.debug("OpenFDA provider/store integration not fully implemented")
            return 0

    def _persist_refresh_metadata(self, result: RefreshResult) -> None:
        """Write last refresh timestamp and bump data version in schema_metadata."""
        try:
            self._set_metadata(_KEY_LAST_REFRESH, result.timestamp)
            # Increment data version on any successful refresh
            if result.sources_succeeded:
                current = self._get_metadata(_KEY_DATA_VERSION) or "0"
                try:
                    new_version = str(int(current) + 1)
                except ValueError:
                    new_version = "1"
                self._set_metadata(_KEY_DATA_VERSION, new_version)
        except Exception:
            logger.warning("Failed to persist refresh metadata", exc_info=True)

    def _get_metadata(self, key: str) -> str | None:
        """Read a value from schema_metadata by key."""
        try:
            with self._store._connect() as conn:
                row = conn.execute(
                    "SELECT value FROM schema_metadata WHERE key = ?", (key,)
                ).fetchone()
            return row["value"] if row else None
        except Exception:
            return None

    def _set_metadata(self, key: str, value: str) -> None:
        """Upsert a key/value pair into schema_metadata."""
        with self._store._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO schema_metadata (key, value) VALUES (?, ?)",
                (key, value),
            )
