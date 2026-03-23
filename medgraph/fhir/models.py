"""
FHIR R4 Pydantic models for MEDGRAPH.

Simplified subset of FHIR R4 spec covering resources needed for
drug interaction checking via MedicationRequest / MedicationStatement.
Full FHIR R4 spec: https://hl7.org/fhir/R4/
"""

from pydantic import BaseModel


# ── Core FHIR datatypes ───────────────────────────────────────────────────────


class FHIRCoding(BaseModel):
    system: str | None = None
    code: str | None = None
    display: str | None = None


class FHIRCodeableConcept(BaseModel):
    coding: list[FHIRCoding] = []
    text: str | None = None


class FHIRReference(BaseModel):
    reference: str | None = None
    display: str | None = None


# ── FHIR R4 Resources ─────────────────────────────────────────────────────────


class MedicationRequest(BaseModel):
    resourceType: str = "MedicationRequest"
    id: str | None = None
    status: str | None = None
    medicationCodeableConcept: FHIRCodeableConcept | None = None
    medicationReference: FHIRReference | None = None


class MedicationStatement(BaseModel):
    resourceType: str = "MedicationStatement"
    id: str | None = None
    status: str | None = None
    medicationCodeableConcept: FHIRCodeableConcept | None = None


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
    hookInstance: str | None = None
    context: dict = {}
    prefetch: dict = {}


class CDSCard(BaseModel):
    uuid: str | None = None
    summary: str
    detail: str | None = None
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
