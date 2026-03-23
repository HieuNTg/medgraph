"""
RxNorm API client for MEDGRAPH.

Normalizes drug names to standard RxCUI identifiers using the NLM RxNorm REST API.
API: https://rxnav.nlm.nih.gov/REST/ (free, no key required)
"""

from __future__ import annotations

import logging
from typing import Optional, TYPE_CHECKING

import httpx

if TYPE_CHECKING:
    from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

RXNORM_BASE = "https://rxnav.nlm.nih.gov/REST"
_TIMEOUT = 8.0


class RxNormClient:
    """
    Client for the NLM RxNorm REST API.

    Normalizes drug name strings to standard RxCUI codes.
    Falls back to approximate (fuzzy) matching when exact match fails.

    Includes a simple in-memory cache to avoid duplicate API calls within
    the same process lifetime.
    """

    def __init__(self) -> None:
        # In-memory cache: name -> (rxcui, normalized_name) | None
        self._cache: dict[str, Optional[tuple[str, str]]] = {}

    def normalize_drug_name(self, name: str) -> Optional[tuple[str, str]]:
        """
        Normalize a drug name to its RxNorm concept.

        Args:
            name: Drug name string (e.g., "aspirin", "Bayer Aspirin")

        Returns:
            Tuple of (rxcui, normalized_name) or None if no match found
        """
        key = name.strip().lower()
        if key in self._cache:
            return self._cache[key]

        # Try exact match first
        result = self._exact_match(name)
        if not result:
            # Fuzzy fallback
            result = self._approximate_match(name)

        self._cache[key] = result
        return result

    def resolve_batch(self, names: list[str]) -> dict[str, Optional[str]]:
        """
        Resolve multiple drug names to RxNorm CUIs in a single call.

        Returns a dict mapping each input name to its RxCUI (or None if not found).
        Uses in-memory cache to avoid redundant API calls.
        """
        results: dict[str, Optional[str]] = {}
        for name in names:
            match = self.normalize_drug_name(name)
            results[name] = match[0] if match else None
        return results

    def resolve_rxcui_to_drug_id(self, rxcui: str, store: "GraphStore") -> Optional[str]:
        """
        Resolve a RxNorm CUI to a MEDGRAPH drug ID using the store.

        Returns the MEDGRAPH drug ID string, or None if not found.
        """
        try:
            with store._connect() as conn:
                row = conn.execute(
                    "SELECT id FROM drugs WHERE rxnorm_cui = ? LIMIT 1",
                    (rxcui,),
                ).fetchone()
            if row:
                return row["id"]
        except Exception as exc:
            logger.warning("resolve_rxcui_to_drug_id failed for %r: %s", rxcui, exc)
        return None

    def get_drug_info(self, rxcui: str) -> dict:
        """
        Fetch drug information for a given RxCUI.

        Returns:
            Dict with drug properties from RxNorm, or empty dict if unavailable
        """
        try:
            with httpx.Client(timeout=_TIMEOUT) as client:
                resp = client.get(f"{RXNORM_BASE}/rxcui/{rxcui}/properties.json")
                if resp.status_code == 200:
                    data = resp.json()
                    props = data.get("properties", {})
                    return {
                        "rxcui": props.get("rxcui", rxcui),
                        "name": props.get("name", ""),
                        "synonym": props.get("synonym", ""),
                        "tty": props.get("tty", ""),  # term type
                    }
        except Exception as e:
            logger.warning(f"RxNorm get_drug_info failed for {rxcui}: {e}")
        return {}

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _exact_match(self, name: str) -> Optional[tuple[str, str]]:
        """Query /rxcui.json for exact name match."""
        try:
            with httpx.Client(timeout=_TIMEOUT) as client:
                resp = client.get(
                    f"{RXNORM_BASE}/rxcui.json",
                    params={"name": name},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    rxcui = data.get("idGroup", {}).get("rxnormId", [])
                    if rxcui:
                        return (rxcui[0], name)
        except Exception as e:
            logger.debug(f"RxNorm exact match failed for {name!r}: {e}")
        return None

    def _approximate_match(self, name: str) -> Optional[tuple[str, str]]:
        """Query /approximateTerm.json for fuzzy match."""
        try:
            with httpx.Client(timeout=_TIMEOUT) as client:
                resp = client.get(
                    f"{RXNORM_BASE}/approximateTerm.json",
                    params={"term": name, "maxEntries": 3},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("approximateGroup", {}).get("candidate", [])
                    if candidates:
                        best = candidates[0]
                        return (best["rxcui"], best.get("name", name))
        except Exception as e:
            logger.debug(f"RxNorm approximate match failed for {name!r}: {e}")
        return None
