"""
RxNorm API client for MEDGRAPH.

Normalizes drug names to standard RxCUI identifiers using the NLM RxNorm REST API.
API: https://rxnav.nlm.nih.gov/REST/ (free, no key required)
"""

from __future__ import annotations

import logging
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

RXNORM_BASE = "https://rxnav.nlm.nih.gov/REST"
_TIMEOUT = 8.0


class RxNormClient:
    """
    Client for the NLM RxNorm REST API.

    Normalizes drug name strings to standard RxCUI codes.
    Falls back to approximate (fuzzy) matching when exact match fails.
    """

    def normalize_drug_name(self, name: str) -> Optional[tuple[str, str]]:
        """
        Normalize a drug name to its RxNorm concept.

        Args:
            name: Drug name string (e.g., "aspirin", "Bayer Aspirin")

        Returns:
            Tuple of (rxcui, normalized_name) or None if no match found
        """
        # Try exact match first
        result = self._exact_match(name)
        if result:
            return result

        # Fuzzy fallback
        return self._approximate_match(name)

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
