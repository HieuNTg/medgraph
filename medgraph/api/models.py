"""
FastAPI request/response models for MEDGRAPH API.
"""

import re
from typing import Generic, TypeVar

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
    metabolizer_phenotypes: dict[str, str] | None = None

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
    def validate_phenotypes(cls, v: dict[str, str] | None) -> dict[str, str] | None:
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
    drug_class: str | None
    enzyme_relations: list[EnzymeRelationResponse] = []
    category: str | None = None
    last_updated: str | None = None


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
    case_count: int | None
    url: str | None


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
    mechanism: str | None
    cascade_paths: list[CascadePathResponse]
    evidence: list[EvidenceResponse]
    pgx_annotations: list[PGxAnnotation] = []
    explanation: str = ""
    evidence_level: str | None = None
    source_citation: str | None = None
    clinical_significance: str | None = None


class FoodInteractionResponse(BaseModel):
    food_name: str
    food_category: str
    drug_id: str
    severity: str
    description: str
    mechanism: str | None = None
    evidence_level: str = "C"


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
    food_interactions: list[FoodInteractionResponse] = []


class StatsResponse(BaseModel):
    drug_count: int
    interaction_count: int
    enzyme_count: int
    adverse_event_count: int


class DataFreshnessResponse(BaseModel):
    drug_count: int
    interaction_count: int
    enzyme_count: int
    last_updated: str | None
    data_version: str


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
    drug_class: str | None


class LivenessResponse(BaseModel):
    status: str


class HealthResponse(BaseModel):
    status: str
    db_size: int
    graph_nodes: int
    schema_version: str = "unknown"


class PDFReportRequest(BaseModel):
    check_result: dict
    graph_png_b64: str | None = None

    @field_validator("graph_png_b64")
    @classmethod
    def validate_png_size(cls, v: str | None) -> str | None:
        if v is not None and len(v) > _MAX_PNG_B64_LEN:
            raise ValueError(f"Graph image too large (max {_MAX_PNG_B64_LEN // (1024 * 1024)} MB)")
        return v


class JSONReportRequest(BaseModel):
    check_result: CheckResponse
    pretty: bool = True


class CSVReportRequest(BaseModel):
    check_result: CheckResponse


# ── Graph / Advanced Analysis Models ─────────────────────────────────────────


class PathwayNode(BaseModel):
    id: str
    type: str  # "drug" | "enzyme"
    label: str


class PathwayEdge(BaseModel):
    source: str
    target: str
    relation: str
    strength: str | None = None


class PathwayResponse(BaseModel):
    nodes: list[PathwayNode]
    edges: list[PathwayEdge]
    cascades: list[dict]


class AlternativeRequest(BaseModel):
    drug_id: str
    regimen: list[str]


class AlternativeResponse(BaseModel):
    drug_id: str
    drug_name: str
    reason: str
    enzyme_overlap_count: int


class HubDrugResponse(BaseModel):
    drug_id: str
    drug_name: str
    betweenness: float
    pagerank: float
    interaction_count: int


class DeprescribeRequest(BaseModel):
    drugs: list[str]


class DeprescribingResponse(BaseModel):
    drug_id: str
    drug_name: str
    removal_benefit: float
    interactions_resolved: int
    rationale: str
    order: int


class PolypharmacyResponse(BaseModel):
    polypharmacy_score: float
    risk_level: str
    risk_clusters: list[dict]
    summary: str


class ContraindicationResponse(BaseModel):
    nodes: list[dict]
    edges: list[dict]
    clusters: list[dict]


# ── Auth / User Profile Models ────────────────────────────────────────────────


class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str | None
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


class ProfileRequest(BaseModel):
    name: str
    drug_ids: list[str]
    notes: str | None = None


class ProfileResponse(BaseModel):
    id: str
    name: str
    drug_ids: list[str]
    notes: str | None
    created_at: str
    updated_at: str


class AnalysisHistoryResponse(BaseModel):
    id: str
    drug_ids: list[str]
    overall_risk: str
    created_at: str


class SharedResultResponse(BaseModel):
    id: str
    url: str
    expires_at: str | None


class AuditLogResponse(BaseModel):
    id: str
    action: str
    resource_type: str | None
    resource_id: str | None
    created_at: str


class OptimizeRequest(BaseModel):
    drugs: list[str]
    must_keep: list[str] = []


class OptimizeResponse(BaseModel):
    original_risk: float
    optimized_risk: float
    drugs_to_remove: list[str]
    alternative_regimens: list[dict]
    rationale: str
    disclaimer: str
