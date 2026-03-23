"""
FHIR R4 Pydantic models for MEDGRAPH.

Simplified subset of FHIR R4 spec covering resources needed for
drug interaction checking via MedicationRequest / MedicationStatement.
Full FHIR R4 spec: https://hl7.org/fhir/R4/
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


# ── Core FHIR datatypes ───────────────────────────────────────────────────────


class FHIRCoding(BaseModel):
    system: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None


class FHIRCodeableConcept(BaseModel):
    coding: list[FHIRCoding] = []
    text: Optional[str] = None


class FHIRReference(BaseModel):
    reference: Optional[str] = None
    display: Optional[str] = None


# ── FHIR R4 Resources ─────────────────────────────────────────────────────────


class MedicationRequest(BaseModel):
    resourceType: str = "MedicationRequest"
    id: Optional[str] = None
    status: Optional[str] = None
    medicationCodeableConcept: Optional[FHIRCodeableConcept] = None
    medicationReference: Optional[FHIRReference] = None


class MedicationStatement(BaseModel):
    resourceType: str = "MedicationStatement"
    id: Optional[str] = None
    status: Optional[str] = None
    medicationCodeableConcept: Optional[FHIRCodeableConcept] = None


class FHIRBundle(BaseModel):
    resourceType: str = "Bundle"
    type: str = "collection"
    entry: list[dict] = []


class OperationOutcome(BaseModel):
    resourceType: str = "OperationOutcome"
    issue: list[dict] = []


# ── CDS Hooks models ──────────────────────────────────────────────────────────


class CDSRequest(BaseModel):
    hook: str
    hookInstance: Optional[str] = None
    context: dict = {}
    prefetch: dict = {}


class CDSCard(BaseModel):
    uuid: Optional[str] = None
    summary: str
    detail: Optional[str] = None
    indicator: str  # "info" | "warning" | "critical"
    source: dict
    suggestions: list[dict] = []


class CDSResponse(BaseModel):
    cards: list[CDSCard] = []


class CDSServiceDefinition(BaseModel):
    hook: str
    title: str
    description: str
    id: str
    prefetch: dict = {}
