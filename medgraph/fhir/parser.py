"""
FHIR R4 resource parser for MEDGRAPH.

Extracts drug identifiers from FHIR resources and resolves them to
MEDGRAPH internal drug IDs. Supports MedicationRequest,
MedicationStatement, and Bundle resources.
"""

from __future__ import annotations

import logging
from typing import Optional

from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# RxNorm system URI (FHIR standard)
_RXNORM_SYSTEM = "http://www.nlm.nih.gov/research/umls/rxnorm"


class FHIRParser:
    """
    Parse FHIR R4 resources and resolve medications to MEDGRAPH drug IDs.

    Resolution priority:
      1. RxNorm CUI (coding.system == RxNorm, match drugs.rxnorm_cui)
      2. Drug display name / text (case-insensitive name match)
      3. None — drug not found, logged as warning
    """

    def __init__(self, store: GraphStore) -> None:
        self.store = store

    def extract_drug_ids(self, fhir_data: dict) -> list[str]:
        """
        Extract MEDGRAPH drug IDs from a FHIR resource dict.

        Handles:
          - MedicationRequest
          - MedicationStatement
          - Bundle (iterates all entries)

        Returns deduplicated list of resolved MEDGRAPH drug IDs.
        """
        resource_type = fhir_data.get("resourceType", "")

        if resource_type == "Bundle":
            return self._extract_from_bundle(fhir_data)
        elif resource_type in ("MedicationRequest", "MedicationStatement"):
            drug_id = self._resolve_medication(fhir_data)
            return [drug_id] if drug_id else []
        else:
            logger.warning("FHIRParser: unsupported resourceType %r", resource_type)
            return []

    def _extract_from_bundle(self, bundle: dict) -> list[str]:
        """Iterate Bundle.entry[] and resolve each medication resource."""
        seen: set[str] = set()
        results: list[str] = []
        for entry in bundle.get("entry", []):
            resource = entry.get("resource", entry)
            resource_type = resource.get("resourceType", "")
            if resource_type in ("MedicationRequest", "MedicationStatement"):
                drug_id = self._resolve_medication(resource)
                if drug_id and drug_id not in seen:
                    seen.add(drug_id)
                    results.append(drug_id)
        return results

    def _resolve_medication(self, medication: dict) -> Optional[str]:
        """
        Resolve a single FHIR medication resource to a MEDGRAPH drug ID.

        Priority: RxNorm CUI -> drug name match -> None
        """
        concept = medication.get("medicationCodeableConcept", {})
        if not concept:
            # Some MedicationRequests use medicationReference — skip (no inline code)
            return None

        # 1. Try RxNorm CUI lookup
        for coding in concept.get("coding", []):
            system = coding.get("system", "")
            code = coding.get("code", "")
            if system == _RXNORM_SYSTEM and code:
                drug = self._find_by_rxnorm_cui(code)
                if drug:
                    return drug.id
                # RxNorm found but not in DB — fall through to name match
                display = coding.get("display", "")
                if display:
                    drug = self.store.get_drug_by_name(display)
                    if drug:
                        return drug.id

        # 2. Try text field
        text = concept.get("text", "")
        if text:
            drug = self.store.get_drug_by_name(text)
            if drug:
                return drug.id

        # 3. Try any coding display name
        for coding in concept.get("coding", []):
            display = coding.get("display", "")
            if display:
                drug = self.store.get_drug_by_name(display)
                if drug:
                    return drug.id

        logger.debug("FHIRParser: could not resolve medication %r", concept.get("text", ""))
        return None

    def _find_by_rxnorm_cui(self, rxnorm_cui: str):
        """Lookup drug by RxNorm CUI in the store."""
        try:
            with self.store._connect() as conn:
                row = conn.execute(
                    "SELECT * FROM drugs WHERE rxnorm_cui = ? LIMIT 1",
                    (rxnorm_cui,),
                ).fetchone()
            if row:
                return self.store._row_to_drug(row)
        except Exception as exc:
            logger.warning("FHIRParser: rxnorm_cui lookup failed for %r: %s", rxnorm_cui, exc)
        return None
