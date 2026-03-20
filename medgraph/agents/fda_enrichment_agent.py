"""
FDA Enrichment Agent — fetches real FAERS adverse event data from OpenFDA API.

Enriches the knowledge graph with evidence counts from FDA's adverse event
reporting system (FAERS). For each drug pair with known interactions, queries
OpenFDA for co-reported adverse events and updates evidence_count fields.

This agent:
- Queries OpenFDA FAERS API for drug pairs with existing interactions
- Adds AdverseEvent records with real FDA case counts
- Updates Interaction.evidence_count with FAERS report totals
- Respects rate limits (5 req/sec, exponential backoff on 429)
- Caches responses to avoid redundant API calls
- Runs as a background job, not user-facing

Data source: https://api.fda.gov/drug/event.json (free, no API key needed)
"""

from __future__ import annotations

import logging

from medgraph.agents.base import AgentResult, BaseAgent
from medgraph.data.openfda import OpenFDAClient
from medgraph.graph.models import Interaction
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)


class FDAEnrichmentAgent(BaseAgent):
    """
    Enriches drug interactions with FDA FAERS adverse event evidence.

    For each interaction pair in the DB, queries OpenFDA for co-reported
    adverse events. Updates evidence_count on the interaction record and
    stores individual adverse event records.

    Args:
        store: GraphStore for reading/writing data
        max_pairs: Maximum interaction pairs to enrich (for rate limiting)
        events_per_pair: Max adverse events to store per drug pair
    """

    def __init__(
        self,
        store: GraphStore,
        max_pairs: int = 50,
        events_per_pair: int = 10,
    ) -> None:
        super().__init__(store, name="FDAEnrichmentAgent")
        self.max_pairs = max_pairs
        self.events_per_pair = events_per_pair
        self.client = OpenFDAClient()

    def _execute(self, result: AgentResult) -> None:
        """Fetch FAERS data for interaction pairs and update the store."""
        interactions = self.store.get_all_interactions()
        if not interactions:
            logger.warning("[FDAEnrichmentAgent] No interactions in DB to enrich")
            return

        # Sort by severity (critical/major first) to prioritize important pairs
        severity_order = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
        interactions.sort(key=lambda i: severity_order.get(i.severity, 4))

        # Limit to max_pairs
        pairs_to_process = interactions[: self.max_pairs]
        result.records_processed = len(pairs_to_process)

        for interaction in pairs_to_process:
            try:
                updated = self._enrich_pair(interaction)
                if updated:
                    result.records_updated += 1
                else:
                    result.records_skipped += 1
            except Exception as e:
                logger.warning(f"[FDAEnrichmentAgent] Error enriching {interaction.id}: {e}")
                result.errors.append(f"{interaction.id}: {e}")
                result.records_skipped += 1

    def _enrich_pair(self, interaction: Interaction) -> bool:
        """
        Enrich a single interaction pair with FAERS data.

        Returns True if the interaction was updated with new evidence.
        """
        # Resolve drug names from IDs
        drug_a = self.store.get_drug_by_id(interaction.drug_a_id)
        drug_b = self.store.get_drug_by_id(interaction.drug_b_id)
        if not drug_a or not drug_b:
            return False

        # Query OpenFDA for co-reported adverse events
        events = self.client.search_adverse_events(
            [drug_a.name, drug_b.name],
            limit=self.events_per_pair,
        )
        if not events:
            return False

        # Store adverse events with correct drug IDs (not names)
        total_count = 0
        for event in events:
            event.drug_ids = [drug_a.id, drug_b.id]
            self.store.upsert_adverse_event(event)
            total_count += event.count

        # Update interaction evidence_count if FAERS has more evidence
        if total_count > interaction.evidence_count:
            interaction.evidence_count = total_count
            self.store.upsert_interaction(interaction)
            logger.info(
                f"[FDAEnrichmentAgent] {drug_a.name}+{drug_b.name}: "
                f"{len(events)} events, {total_count} total FAERS reports"
            )
            return True

        return False
