"""
Drug search utilities for MEDGRAPH API.

Provides fuzzy and exact drug name search against the SQLite store,
with optional RxNorm normalization for user input.
"""

from __future__ import annotations

import logging
from typing import Optional

from medgraph.data.rxnorm import RxNormClient
from medgraph.graph.models import Drug
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)


class DrugSearcher:
    """
    Handles drug name lookup with multiple fallback strategies:
    1. Exact case-insensitive match in SQLite
    2. LIKE search in SQLite
    3. RxNorm normalization + re-query (optional, requires network)
    """

    def __init__(
        self,
        store: GraphStore,
        use_rxnorm: bool = False,
    ) -> None:
        self.store = store
        self.use_rxnorm = use_rxnorm
        self._rxnorm: Optional[RxNormClient] = RxNormClient() if use_rxnorm else None

    def search(self, query: str, limit: int = 10, offset: int = 0) -> list[Drug]:
        """
        Search for drugs by name.

        Args:
            query: Drug name or partial name
            limit: Maximum results
            offset: Number of results to skip (for pagination)

        Returns:
            List of matching Drug objects
        """
        # 1. Try exact match (only on first page)
        if offset == 0:
            exact = self.store.get_drug_by_name(query)
            if exact:
                return [exact]

        # 2. LIKE search
        results = self.store.search_drugs(query, limit=limit, offset=offset)
        if results:
            return results

        # 3. RxNorm normalization fallback (only on first page)
        if offset == 0 and self._rxnorm:
            normalized = self._rxnorm.normalize_drug_name(query)
            if normalized:
                rxcui, norm_name = normalized
                results = self.store.search_drugs(norm_name, limit=limit)
                if results:
                    return results

        return []

    def count(self, query: str) -> int:
        """Count total matching drugs for a search query."""
        return self.store.count_search_drugs(query)

    def resolve_drug_names(self, names: list[str]) -> tuple[list[Drug], list[str]]:
        """
        Resolve a list of drug names to Drug objects.

        Returns:
            Tuple of (found_drugs, unresolved_names)
        """
        found: list[Drug] = []
        unresolved: list[str] = []
        for name in names:
            results = self.search(name, limit=1)
            if results:
                found.append(results[0])
            else:
                unresolved.append(name)
        return found, unresolved
