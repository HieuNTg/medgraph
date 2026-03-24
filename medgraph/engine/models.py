"""
Pydantic models for the MEDGRAPH cascade analysis engine output.

These models represent the structured output of the cascade analyzer.
All reports include a mandatory medical disclaimer.
"""

from __future__ import annotations

from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, Field

from medgraph.graph.models import Drug, Interaction, MEDICAL_DISCLAIMER


class EvidenceItem(BaseModel):
    """A single piece of evidence supporting an interaction claim."""

    source: str  # "drugbank" | "openfda" | "seed" | "faers"
    description: str
    evidence_count: int = 0
    url: Optional[str] = None


class CascadeStep(BaseModel):
    """
    A single step in a pharmacokinetic cascade chain.

    Example:
        Fluoxetine --[inhibits]--> CYP2D6 --[required by]--> Codeine
    """

    source_drug: str  # Drug name initiating this step
    target: str  # Enzyme name or drug name
    target_type: str  # "enzyme" | "drug"
    relation: str  # "inhibits" | "induces" | "metabolized_by" | "interacts_with"
    strength: str = "moderate"  # "strong" | "moderate" | "weak"
    effect: str  # Human-readable effect, e.g. "reduced CYP2D6 activity"


class CascadePath(BaseModel):
    """
    A complete cascade interaction pathway between two drugs.

    A cascade involves one or more enzyme-mediated steps linking
    the pharmacokinetics of two drugs.
    """

    steps: list[CascadeStep]
    net_severity: str  # "critical" | "major" | "moderate" | "minor"
    description: str  # Human-readable explanation of the full cascade
    drug_a_name: str
    drug_b_name: str
    drug_a_id: str = ""  # Drug ID for reliable matching (not name-based)
    drug_b_id: str = ""  # Drug ID for reliable matching (not name-based)
    enzyme_ids: list[str] = Field(default_factory=list)  # Enzymes involved


class DrugInteractionResult(BaseModel):
    """
    Complete interaction analysis between two specific drugs.

    Combines direct database interactions with enzyme-mediated cascade paths.
    """

    drug_a: Drug
    drug_b: Drug
    direct_interaction: Optional[Interaction] = None  # From DB, if exists
    cascade_paths: list[CascadePath] = Field(default_factory=list)
    risk_score: float = 0.0  # 0-100
    severity: str = "minor"  # Overall severity classification
    evidence: list[EvidenceItem] = Field(default_factory=list)


class InteractionReport(BaseModel):
    """
    Complete multi-drug interaction analysis report.

    The top-level output of CascadeAnalyzer.analyze().
    Always includes the medical disclaimer.
    """

    drugs: list[Drug]
    interactions: list[DrugInteractionResult]
    overall_risk: str  # "critical" | "major" | "moderate" | "minor"
    overall_score: float  # 0-100
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    disclaimer: str = MEDICAL_DISCLAIMER
    drug_count: int = 0
    interaction_count: int = 0
    cascade_count: int = 0

    def model_post_init(self, __context) -> None:
        self.drug_count = len(self.drugs)
        self.interaction_count = len(self.interactions)
        self.cascade_count = sum(len(r.cascade_paths) for r in self.interactions)
