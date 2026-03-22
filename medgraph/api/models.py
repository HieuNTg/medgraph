"""
FastAPI request/response models for MEDGRAPH API.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class CheckRequest(BaseModel):
    drugs: list[str]
    include_evidence: bool = True


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


class InteractionResponse(BaseModel):
    drug_a: DrugResponse
    drug_b: DrugResponse
    severity: str
    risk_score: float
    description: str
    mechanism: Optional[str]
    cascade_paths: list[CascadePathResponse]
    evidence: list[EvidenceResponse]


class CheckResponse(BaseModel):
    drugs: list[DrugResponse]
    interactions: list[InteractionResponse]
    overall_risk: str
    overall_score: float
    drug_count: int
    interaction_count: int
    timestamp: str
    disclaimer: str


class StatsResponse(BaseModel):
    drug_count: int
    interaction_count: int
    enzyme_count: int
    adverse_event_count: int


class SearchResult(BaseModel):
    id: str
    name: str
    brand_names: list[str]
    drug_class: Optional[str]


class HealthResponse(BaseModel):
    status: str
    db_size: int
    graph_nodes: int


class PDFReportRequest(BaseModel):
    check_result: dict
    graph_png_b64: Optional[str] = None
