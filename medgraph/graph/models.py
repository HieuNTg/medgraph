"""
Pydantic data models for MEDGRAPH knowledge graph entities.

MEDICAL DISCLAIMER: Data in this system is for informational and research
purposes only. It does not constitute medical advice. Always consult a licensed
healthcare professional before making any medical decisions.
"""

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

MEDICAL_DISCLAIMER = (
    "DISCLAIMER: This tool is for informational and research purposes only. "
    "It does not constitute medical advice. Drug interaction data may be incomplete. "
    "Always consult a licensed healthcare professional or pharmacist before making "
    "any medication decisions."
)


class Drug(BaseModel):
    """Represents a pharmaceutical drug."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # DrugBank ID, e.g. "DB00001"
    name: str  # Generic/INN name
    brand_names: list[str] = Field(default_factory=list)
    description: str = ""
    drug_class: Optional[str] = None
    rxnorm_cui: Optional[str] = None  # RxNorm concept ID for normalization


class ActiveIngredient(BaseModel):
    """Active ingredient within a drug (for combination products)."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    drug_id: str


class Enzyme(BaseModel):
    """Metabolic enzyme, primarily CYP450 isoforms."""

    model_config = ConfigDict(from_attributes=True)

    id: str  # e.g. "CYP3A4"
    name: str  # Human-readable name
    gene: Optional[str] = None  # Gene symbol


class Interaction(BaseModel):
    """Pairwise drug-drug interaction record."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    drug_a_id: str
    drug_b_id: str
    severity: str  # "critical" | "major" | "moderate" | "minor"
    description: str
    mechanism: Optional[str] = None
    source: str  # "drugbank" | "openfda" | "seed"
    evidence_count: int = 0  # FDA FAERS report count


class DrugEnzymeRelation(BaseModel):
    """Relationship between a drug and a metabolic enzyme."""

    model_config = ConfigDict(from_attributes=True)

    drug_id: str
    enzyme_id: str
    relation_type: str  # "metabolized_by" | "inhibits" | "induces"
    strength: str = "moderate"  # "strong" | "moderate" | "weak"


class AdverseEvent(BaseModel):
    """Adverse event report from FDA FAERS or similar sources."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    drug_ids: list[str]  # Drugs involved
    reaction: str  # Reaction term
    count: int = 0  # FAERS report count
    seriousness: str = "unknown"  # "serious" | "non-serious" | "fatal" | "unknown"
    source_url: Optional[str] = None


class GeneticGuideline(BaseModel):
    """CPIC pharmacogenomics guideline for drug-gene pair."""
    model_config = ConfigDict(from_attributes=True)

    drug_id: str
    gene_id: str  # e.g. "CYP2D6", "CYP2C19"
    phenotype: str  # "poor" | "intermediate" | "normal" | "ultrarapid"
    recommendation: str  # Clinical recommendation text
    severity_multiplier: float = 1.0  # Multiplier for risk score adjustment
