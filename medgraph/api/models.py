"""
FastAPI request/response models for MEDGRAPH API.
"""

import re
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator

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
    confidence_score: float | None = None
    confidence_level: str | None = None
    confidence_factors: list[str] = Field(default_factory=list)


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
    password: str = Field(min_length=8, max_length=128)
    display_name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str = Field(max_length=128)


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


# ── Pharmacogenomics Risk Profile Models ─────────────────────────────────────


class PGxRiskRequest(BaseModel):
    drugs: list[str] = Field(..., min_length=1, max_length=10)
    ancestry: str | None = Field(
        None,
        description=("e.g., european, east_asian, african, south_asian, hispanic, middle_eastern"),
    )
    known_phenotypes: dict[str, str] | None = Field(
        None, description="e.g., {'CYP2D6': 'poor_metabolizer'}"
    )


class PGxDrugAlert(BaseModel):
    drug_name: str
    gene: str
    phenotype: str
    recommendation: str
    severity_multiplier: float
    population_frequency: float | None = None


class PGxRiskResponse(BaseModel):
    alerts: list[PGxDrugAlert]
    ancestry: str | None
    population_risk_factors: list[str]
    disclaimer: str


# ── Schedule Optimizer Models ─────────────────────────────────────────────────


class ScheduleDrugInput(BaseModel):
    """A drug with its dosing frequency for schedule optimization."""

    drug_name: str = Field(..., description="Drug name to search")
    frequency: int = Field(1, ge=1, le=3, description="Doses per day (1, 2, or 3)")


class ScheduledDrugResponse(BaseModel):
    """A drug assigned to a time slot."""

    drug_id: str
    drug_name: str
    frequency: int


class ScheduleRequest(BaseModel):
    """Request body for POST /api/v1/schedule."""

    drugs: list[ScheduleDrugInput] = Field(..., min_length=2, max_length=10)


class ScheduleResponse(BaseModel):
    """Optimised medication schedule response."""

    schedule: dict[str, list[ScheduledDrugResponse]]  # time_slot → drugs
    warnings: list[str]
    disclaimer: str


# ── PGx Check Models (POST /api/v1/check-pgx) ────────────────────────────────

_VALID_FULL_PHENOTYPES = {
    "poor_metabolizer",
    "intermediate_metabolizer",
    "normal_metabolizer",
    "rapid_metabolizer",
    "ultrarapid_metabolizer",
}

_VALID_ANCESTRY = {
    "european",
    "east_asian",
    "african",
    "south_asian",
    "hispanic",
    "middle_eastern",
}


class PGxCheckRequest(BaseModel):
    """Request body for POST /api/v1/check-pgx."""

    drugs: list[str] = Field(..., min_length=2, max_length=10)
    phenotypes: dict[str, str] = Field(
        default_factory=dict,
        description="Gene ID → phenotype string, e.g. {'CYP2D6': 'poor_metabolizer'}",
    )
    ancestry: str | None = Field(
        None,
        description="Self-reported ancestry for population frequency context",
    )

    @field_validator("drugs")
    @classmethod
    def validate_pgx_drugs(cls, v: list[str]) -> list[str]:
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
        if len(sanitized) < 2:
            raise ValueError("At least 2 valid drug names are required")
        if len(sanitized) > _MAX_DRUGS:
            raise ValueError(f"Too many drugs (max {_MAX_DRUGS})")
        return sanitized

    @field_validator("phenotypes")
    @classmethod
    def validate_full_phenotypes(cls, v: dict[str, str]) -> dict[str, str]:
        for gene, phenotype in v.items():
            if phenotype.lower() not in _VALID_FULL_PHENOTYPES:
                raise ValueError(
                    f"Invalid phenotype '{phenotype}' for {gene}. "
                    f"Must be one of: {', '.join(sorted(_VALID_FULL_PHENOTYPES))}"
                )
        return v

    @field_validator("ancestry")
    @classmethod
    def validate_ancestry(cls, v: str | None) -> str | None:
        if v is not None and v.lower() not in _VALID_ANCESTRY:
            raise ValueError(
                f"Invalid ancestry '{v}'. Must be one of: {', '.join(sorted(_VALID_ANCESTRY))}"
            )
        return v


class PGxAdjustment(BaseModel):
    """A single pharmacogenomics adjustment applied to an interaction."""

    drug_name: str
    gene: str
    phenotype: str
    severity_multiplier: float
    reason: str


class PGxInteractionResponse(BaseModel):
    """Interaction response enriched with PGx adjustments."""

    drug_a: DrugResponse
    drug_b: DrugResponse
    base_severity: str
    base_risk_score: float
    adjusted_severity: str
    adjusted_risk_score: float
    description: str
    mechanism: str | None = None
    pgx_adjustments: list[PGxAdjustment] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    pgx_confidence: float = 0.0
    cascade_paths: list[CascadePathResponse] = Field(default_factory=list)
    evidence: list[EvidenceResponse] = Field(default_factory=list)


class PGxSummary(BaseModel):
    """Summary of PGx findings across the full regimen."""

    genes_tested: list[str]
    actionable_findings: int
    confidence: float


class PGxCheckResponse(BaseModel):
    """Response for POST /api/v1/check-pgx."""

    drugs: list[DrugResponse]
    interactions: list[PGxInteractionResponse]
    overall_risk: str
    overall_score: float
    drug_count: int
    interaction_count: int
    pgx_summary: PGxSummary
    timestamp: str
    disclaimer: str
    food_interactions: list[FoodInteractionResponse] = Field(default_factory=list)


# ── Evidence Confidence Fields (added to InteractionResponse) ─────────────────
# These fields are appended to InteractionResponse via model extension pattern.
