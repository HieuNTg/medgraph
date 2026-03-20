"""
FDA Label Parser Agent — extracts interaction warnings from FDA drug labels.

Parses the "drug_interactions" section of FDA-approved drug labels via the
OpenFDA drug label API. Discovers new interactions not in the seed data by
matching mentioned drug names against the knowledge graph.

This agent:
- Fetches drug label interaction sections from OpenFDA label API
- Extracts mentioned drug names from interaction text using NLP patterns
- Creates new Interaction records for discovered drug-drug interactions
- Updates existing interaction descriptions with FDA label text
- Runs as a background job, not user-facing

Data source: https://api.fda.gov/drug/label.json
"""

from __future__ import annotations

import hashlib
import logging
import re
from typing import Optional

from medgraph.agents.base import AgentResult, BaseAgent
from medgraph.data.openfda import OpenFDAClient
from medgraph.graph.models import Drug, Interaction
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Patterns to extract drug names and interaction signals from label text
_INTERACTION_SIGNALS = [
    r"(?:concomitant|concurrent|co-?administration)\s+(?:use\s+)?(?:of|with)\s+(\w+)",
    r"(\w+)\s+(?:may|can|will)\s+(?:increase|decrease|alter|affect|reduce|enhance|potentiate)",
    r"(?:avoid|contraindicated)\s+(?:with|in combination with)\s+(\w+)",
    r"(?:inhibit|induce)s?\s+(?:the\s+)?(?:metabolism|clearance)\s+of\s+(\w+)",
    r"(\w+)\s+(?:is|are)\s+(?:a\s+)?(?:strong|moderate|weak)\s+(?:inhibitor|inducer)",
    r"plasma\s+(?:levels?|concentrations?)\s+of\s+(\w+)\s+(?:may|can|will)\s+(?:increase|decrease)",
]
_COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _INTERACTION_SIGNALS]

# Minimum drug name length to avoid false positives
_MIN_DRUG_NAME_LEN = 4


class LabelParserAgent(BaseAgent):
    """
    Extracts drug interaction warnings from FDA drug labels.

    For each drug in the knowledge graph, fetches the FDA label's
    drug_interactions section and parses it for mentioned drug names.
    Creates new Interaction records for any discovered pairs.

    Args:
        store: GraphStore for reading/writing data
        max_drugs: Maximum drugs to process (for rate limiting)
    """

    def __init__(self, store: GraphStore, max_drugs: int = 50) -> None:
        super().__init__(store, name="LabelParserAgent")
        self.max_drugs = max_drugs
        self.client = OpenFDAClient()
        # Pre-build drug name lookup for fast matching
        self._drug_name_map: dict[str, Drug] = {}

    def _execute(self, result: AgentResult) -> None:
        """Fetch and parse FDA labels for all drugs."""
        drugs = self.store.get_all_drugs()
        if not drugs:
            logger.warning("[LabelParserAgent] No drugs in DB")
            return

        # Build lowercase drug name -> Drug lookup
        self._drug_name_map = {d.name.lower(): d for d in drugs}

        # Process up to max_drugs
        to_process = drugs[: self.max_drugs]
        result.records_processed = len(to_process)

        for drug in to_process:
            try:
                found = self._parse_label_for_drug(drug)
                if found > 0:
                    result.records_updated += found
                else:
                    result.records_skipped += 1
            except Exception as e:
                logger.warning(f"[LabelParserAgent] Error parsing label for {drug.name}: {e}")
                result.errors.append(f"{drug.name}: {e}")
                result.records_skipped += 1

    def _parse_label_for_drug(self, drug: Drug) -> int:
        """
        Fetch FDA label for a drug and extract interaction mentions.

        Returns number of new interactions discovered.
        """
        label_text = self.client.get_drug_label_interactions(drug.name)
        if not label_text:
            return 0

        # Extract mentioned drug names from label text
        mentioned_names = self._extract_drug_mentions(label_text)
        if not mentioned_names:
            return 0

        new_count = 0
        for mentioned_name in mentioned_names:
            mentioned_drug = self._drug_name_map.get(mentioned_name.lower())
            if not mentioned_drug or mentioned_drug.id == drug.id:
                continue

            # Check if interaction already exists
            existing = self.store.get_direct_interaction(drug.id, mentioned_drug.id)
            if existing:
                # Update description if label provides better info
                if len(label_text) > len(existing.description) and existing.source == "seed":
                    # Extract the relevant sentence from label text
                    snippet = self._extract_relevant_snippet(label_text, mentioned_name)
                    if snippet:
                        existing.description = snippet
                        existing.source = "fda_label"
                        self.store.upsert_interaction(existing)
                        new_count += 1
                continue

            # Create new interaction from label data
            snippet = self._extract_relevant_snippet(label_text, mentioned_name)
            severity = self._infer_severity_from_text(label_text, mentioned_name)

            interaction_id = hashlib.md5(
                f"label:{drug.id}:{mentioned_drug.id}".encode()
            ).hexdigest()[:12]

            interaction = Interaction(
                id=f"FDA-LABEL-{interaction_id}",
                drug_a_id=drug.id,
                drug_b_id=mentioned_drug.id,
                severity=severity,
                description=snippet
                or f"FDA label warning: {drug.name} interacts with {mentioned_name}",
                mechanism=None,
                source="fda_label",
                evidence_count=0,
            )
            self.store.upsert_interaction(interaction)
            new_count += 1
            logger.info(
                f"[LabelParserAgent] Discovered: {drug.name} + {mentioned_name} ({severity})"
            )

        return new_count

    def _extract_drug_mentions(self, text: str) -> list[str]:
        """
        Extract drug names mentioned in FDA label interaction text.

        Uses regex patterns to find drug names in context of interaction warnings,
        then cross-references against known drugs in the knowledge graph.
        """
        candidates: set[str] = set()

        # Pattern-based extraction
        for pattern in _COMPILED_PATTERNS:
            for match in pattern.finditer(text):
                name = match.group(1).strip()
                if len(name) >= _MIN_DRUG_NAME_LEN:
                    candidates.add(name)

        # Also do direct name matching against known drugs
        text_lower = text.lower()
        for drug_name in self._drug_name_map:
            if len(drug_name) >= _MIN_DRUG_NAME_LEN and drug_name in text_lower:
                candidates.add(drug_name)

        return list(candidates)

    def _extract_relevant_snippet(self, full_text: str, drug_name: str) -> Optional[str]:
        """Extract the sentence(s) mentioning a specific drug from label text."""
        sentences = re.split(r"[.!?]\s+", full_text)
        relevant = []
        for sentence in sentences:
            if drug_name.lower() in sentence.lower():
                clean = sentence.strip()
                if clean:
                    relevant.append(clean)

        if relevant:
            # Return up to 2 relevant sentences, capped at 500 chars
            snippet = ". ".join(relevant[:2])
            return snippet[:500]
        return None

    def _infer_severity_from_text(self, text: str, drug_name: str) -> str:
        """Infer interaction severity from FDA label language."""
        # Find context around the drug mention
        text_lower = text.lower()
        idx = text_lower.find(drug_name.lower())
        if idx < 0:
            return "moderate"

        # Extract surrounding context (200 chars before and after)
        start = max(0, idx - 200)
        end = min(len(text), idx + len(drug_name) + 200)
        context = text_lower[start:end]

        # Check for severity indicators
        critical_words = ["contraindicated", "fatal", "life-threatening", "do not use", "never"]
        major_words = ["serious", "severe", "significant", "avoid", "strongly", "dangerous"]
        moderate_words = ["caution", "monitor", "adjust", "careful", "closely"]

        for word in critical_words:
            if word in context:
                return "critical"
        for word in major_words:
            if word in context:
                return "major"
        for word in moderate_words:
            if word in context:
                return "moderate"

        return "moderate"  # Default for FDA-labeled interactions
