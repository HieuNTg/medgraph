"""
OpenFDA API client for MEDGRAPH.

Fetches adverse event data from FDA FAERS database.
API: https://api.fda.gov/drug/ (free, no key needed for <240 req/min)

Rate limiting: max 5 req/sec with exponential backoff.
Responses cached to avoid repeated calls.
Gracefully degrades if API is unavailable.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Optional

import httpx

from medgraph.graph.models import AdverseEvent

logger = logging.getLogger(__name__)

# FDA API base URL
OPENFDA_BASE = "https://api.fda.gov/drug"

# Rate limit: max 5 requests per second (conservative — actual limit is 240/min)
_REQUEST_INTERVAL = 0.2  # seconds between requests
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.0  # seconds for exponential backoff


class OpenFDAClient:
    """
    Client for the OpenFDA drug API.

    Provides methods to query FAERS adverse events and drug labels.
    Implements rate limiting, retries, and file-based caching.
    """

    def __init__(
        self,
        cache_dir: Path = Path("data/openfda_cache"),
        timeout: float = 10.0,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self._last_request_time: float = 0.0

    def search_adverse_events(
        self,
        drug_names: list[str],
        limit: int = 100,
    ) -> list[AdverseEvent]:
        """
        Search FDA FAERS for adverse events involving given drug combination.

        Args:
            drug_names: List of generic drug names to query together
            limit: Maximum results to return

        Returns:
            List of AdverseEvent records (may be empty if API unavailable)
        """
        if not drug_names:
            return []

        query_parts = [f'patient.drug.openfda.generic_name:"{name}"' for name in drug_names]
        query = "+AND+".join(query_parts)
        params = {
            "search": query,
            "count": "patient.reaction.reactionmeddrapt.exact",
            "limit": limit,
        }

        cached = self._load_cache("events", drug_names)
        if cached is not None:
            return self._parse_adverse_events(cached, drug_names)

        try:
            data = self._get(f"{OPENFDA_BASE}/event.json", params)
            self._save_cache("events", drug_names, data)
            return self._parse_adverse_events(data, drug_names)
        except Exception as e:
            logger.warning(f"OpenFDA adverse events unavailable for {drug_names}: {e}")
            return []

    def search_adverse_events_pairwise(
        self,
        drug_names: list[str],
        limit: int = 100,
    ) -> list[AdverseEvent]:
        """
        Search FDA FAERS for adverse events using pairwise drug combinations.

        For >2 drugs, queries each pair separately and merges results.
        This avoids the AND-all-drugs query that returns near-zero results.
        """
        if len(drug_names) <= 2:
            return self.search_adverse_events(drug_names, limit)

        from itertools import combinations
        seen_ids: set[str] = set()
        all_events: list[AdverseEvent] = []
        for pair in combinations(drug_names, 2):
            pair_events = self.search_adverse_events(list(pair), limit)
            for ev in pair_events:
                if ev.id not in seen_ids:
                    seen_ids.add(ev.id)
                    all_events.append(ev)
        return all_events

    def get_drug_label_interactions(self, drug_name: str) -> Optional[str]:
        """
        Fetch the drug interactions section from FDA drug labeling.

        Returns:
            String with interaction text, or None if unavailable
        """
        params = {
            "search": f'openfda.generic_name:"{drug_name}"',
            "limit": 1,
        }
        cached = self._load_cache("label", [drug_name])
        if cached is not None:
            return self._extract_interactions_text(cached)

        try:
            data = self._get(f"{OPENFDA_BASE}/label.json", params)
            self._save_cache("label", [drug_name], data)
            return self._extract_interactions_text(data)
        except Exception as e:
            logger.warning(f"OpenFDA label unavailable for {drug_name}: {e}")
            return None

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _get(self, url: str, params: dict) -> dict[str, Any]:
        """
        Make a GET request with rate limiting and exponential backoff retry.
        """
        self._rate_limit()
        for attempt in range(_MAX_RETRIES):
            try:
                with httpx.Client(timeout=self.timeout) as client:
                    resp = client.get(url, params=params)
                    if resp.status_code == 200:
                        return resp.json()
                    elif resp.status_code == 429:
                        # Rate limited — back off
                        wait = _BACKOFF_BASE * (2**attempt)
                        logger.warning(f"Rate limited by OpenFDA. Waiting {wait}s...")
                        time.sleep(wait)
                    elif resp.status_code == 404:
                        return {}  # No results
                    else:
                        logger.warning(f"OpenFDA HTTP {resp.status_code} for {url}")
                        return {}
            except httpx.TimeoutException:
                logger.warning(f"OpenFDA timeout on attempt {attempt + 1}")
                if attempt < _MAX_RETRIES - 1:
                    time.sleep(_BACKOFF_BASE * (2**attempt))
            except httpx.RequestError as e:
                logger.warning(f"OpenFDA request error: {e}")
                return {}
        return {}

    def _rate_limit(self) -> None:
        """Enforce minimum interval between requests."""
        now = time.monotonic()
        elapsed = now - self._last_request_time
        if elapsed < _REQUEST_INTERVAL:
            time.sleep(_REQUEST_INTERVAL - elapsed)
        self._last_request_time = time.monotonic()

    def _cache_key(self, endpoint: str, drug_names: list[str]) -> str:
        """Generate a filesystem-safe cache key."""
        raw = f"{endpoint}:{':'.join(sorted(drug_names))}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _load_cache(self, endpoint: str, drug_names: list[str]) -> Optional[dict]:
        """Load cached API response if available and not expired (30-day TTL)."""
        key = self._cache_key(endpoint, drug_names)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            # Check cache age — 30-day TTL
            cache_age = time.time() - cache_file.stat().st_mtime
            if cache_age > 30 * 86400:
                logger.info(f"Cache expired for {endpoint}:{drug_names} (age: {cache_age/86400:.1f}d)")
                cache_file.unlink(missing_ok=True)
                return None
            try:
                with open(cache_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    def _save_cache(self, endpoint: str, drug_names: list[str], data: dict) -> None:
        """Save API response to disk cache."""
        key = self._cache_key(endpoint, drug_names)
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.debug(f"Failed to cache OpenFDA response: {e}")

    def _parse_adverse_events(self, data: dict, drug_names: list[str]) -> list[AdverseEvent]:
        """Parse FDA event count response into AdverseEvent objects."""
        results = data.get("results", [])
        events: list[AdverseEvent] = []
        for i, item in enumerate(results):
            term = item.get("term", "Unknown reaction")
            count = item.get("count", 0)
            key = hashlib.md5(f"{':'.join(sorted(drug_names))}:{term}".encode()).hexdigest()[:12]
            events.append(
                AdverseEvent(
                    id=f"FAERS-{key}",
                    drug_ids=drug_names,  # names as IDs here — store can normalize
                    reaction=term,
                    count=count,
                    seriousness="unknown",  # FAERS count endpoint doesn't give seriousness
                    source_url="https://api.fda.gov/drug/event.json",
                )
            )
        return events

    def _extract_interactions_text(self, data: dict) -> Optional[str]:
        """Extract drug_interactions field from FDA label response."""
        results = data.get("results", [])
        if not results:
            return None
        label = results[0]
        interactions = label.get("drug_interactions", [])
        if interactions:
            return "\n".join(interactions)
        return None
