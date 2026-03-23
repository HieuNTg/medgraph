"""
FastAPI request/response models for MEDGRAPH API.
"""

from __future__ import annotations

import re
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, field_validator

T = TypeVar("T")

# Only allow alphanumeric, spaces, hyphens, apostrophes, and parentheses in drug names
_DRUG_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9\s\-'(),.]+$")
_VALID_PHENOTYPES = {"poor", "intermediate", "normal", "rapid", "ultrarapid"}
_MAX_DRUGS = 20
# Max base64-encoded PNG size for PDF reports (5 MB)
_MAX_PNG_B64_LEN = 5 * 1024 * 1024


class CheckRequest(BaseModel):
    drugs: list[str]
    include_evidence: bool = True
    metabolizer_phenotypes: Optional[dict[str, str]] = None

    @field_validator("drugs")
    @classmethod
    def validate_drugs(cls, v: list[str]) -> list[str]:
        sanitized = []
        for name in v:
            stripped = name.strip()
            if not stripped:
                continue
            if len(stripped) > 100:
                raise ValueError(f"Drug name too long (max 100 chars): '{stripped[:20]}...'")
            if not _DRUG_NAME_PATTERN.match(stripped):
                raise ValueError(f"Drug name contains invalid characters: '{stripped}'")
            sanitized.append(stripped)
        if not sanitized:
            raise ValueError("At least one valid drug name is required")
        if len(sanitized) > _MAX_DRUGS:
            raise ValueError(f"Too many drugs (max {_MAX_DRUGS})")
        return sanitized

    @field_validator("metabolizer_phenotypes")
    @classmethod
    def validate_phenotypes(cls, v: Optional[dict[str, str]]) -> Optional[dict[str, str]]:
        if v is None:
            return v
        for gene, phenotype in v.items():
            if phenotype.lower() not in _VALID_PHENOTYPES:
                raise ValueError(
                    f"Invalid phenotype '{phenotype}' for {gene}. "
                    f"Must be one of: {', '.join(sorted(_VALID_PHENOTYPES))}"
                )
        return v


class EnzymeRelationResponse(BaseModel):
    enzyme_name: str
    relation_type: str
    strength: str


class DrugResponse(BaseModel):
    id: str
    name: str
    brand_names: list[str]
    drug_class: Optional[str]
    enzyme_relations: list[EnzymeRelationResponse] = []


class CascadeStepResponse(BaseModel):
    source: str
    target: str
    relation: str
    effect: str


class CascadePathResponse(BaseModel):
    steps: list[CascadeStepResponse]
    description: str
    net_severity: str


class EvidenceResponse(BaseModel):
    source: str
    description: str
    case_count: Optional[int]
    url: Optional[str]


class PGxAnnotation(BaseModel):
    gene: str
    phenotype: str
    drug_name: str
    recommendation: str
    severity_multiplier: float


class InteractionResponse(BaseModel):
    drug_a: DrugResponse
    drug_b: DrugResponse
    severity: str
    risk_score: float
    description: str
    mechanism: Optional[str]
    cascade_paths: list[CascadePathResponse]
    evidence: list[EvidenceResponse]
    pgx_annotations: list[PGxAnnotation] = []
    explanation: str = ""


class CheckResponse(BaseModel):
    drugs: list[DrugResponse]
    interactions: list[InteractionResponse]
    overall_risk: str
    overall_score: float
    drug_count: int
    interaction_count: int
    timestamp: str
    disclaimer: str
    summary: str = ""


class StatsResponse(BaseModel):
    drug_count: int
    interaction_count: int
    enzyme_count: int
    adverse_event_count: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Offset-based paginated response wrapper."""

    items: list[T]
    total: int
    offset: int
    limit: int
    has_more: bool


class SearchResult(BaseModel):
    id: str
    name: str
    brand_names: list[str]
    drug_class: Optional[str]


class LivenessResponse(BaseModel):
    status: str


class HealthResponse(BaseModel):
    status: str
    db_size: int
    graph_nodes: int


class PDFReportRequest(BaseModel):
    check_result: dict
    graph_png_b64: Optional[str] = None

    @field_validator("graph_png_b64")
    @classmethod
    def validate_png_size(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > _MAX_PNG_B64_LEN:
            raise ValueError(f"Graph image too large (max {_MAX_PNG_B64_LEN // (1024 * 1024)} MB)")
        return v


class JSONReportRequest(BaseModel):
    check_result: CheckResponse
    pretty: bool = True


class CSVReportRequest(BaseModel):
    check_result: CheckResponse
