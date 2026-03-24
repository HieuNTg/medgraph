"""
PGx Scoring Engine for MEDGRAPH.

Adjusts drug interaction risk scores based on patient metabolizer phenotypes
using CPIC pharmacogenomics guidelines stored in the database.

Usage:
    scorer = PGxScorer(store)
    result = scorer.score_regimen(drug_names, phenotypes, graph, ancestry)
"""

from __future__ import annotations

import logging
from typing import Optional

from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Phenotype constants
# ---------------------------------------------------------------------------

PHENOTYPE_POOR = "poor_metabolizer"
PHENOTYPE_INTERMEDIATE = "intermediate_metabolizer"
PHENOTYPE_NORMAL = "normal_metabolizer"
PHENOTYPE_RAPID = "rapid_metabolizer"
PHENOTYPE_ULTRARAPID = "ultrarapid_metabolizer"

VALID_PHENOTYPES = {
    PHENOTYPE_POOR,
    PHENOTYPE_INTERMEDIATE,
    PHENOTYPE_NORMAL,
    PHENOTYPE_RAPID,
    PHENOTYPE_ULTRARAPID,
}

# ---------------------------------------------------------------------------
# Allele-to-phenotype mapping (major CYP genes — based on CPIC definitions)
# ---------------------------------------------------------------------------

# Key: (gene_id, sorted_allele_tuple) → phenotype string
ALLELE_PHENOTYPE_MAP: dict[tuple, str] = {
    # CYP2D6 — common allele pairs
    ("CYP2D6", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("CYP2D6", ("*1", "*2")): PHENOTYPE_NORMAL,
    ("CYP2D6", ("*1", "*4")): PHENOTYPE_INTERMEDIATE,
    ("CYP2D6", ("*1", "*5")): PHENOTYPE_INTERMEDIATE,
    ("CYP2D6", ("*1", "*10")): PHENOTYPE_INTERMEDIATE,
    ("CYP2D6", ("*1", "*41")): PHENOTYPE_INTERMEDIATE,
    ("CYP2D6", ("*4", "*4")): PHENOTYPE_POOR,
    ("CYP2D6", ("*4", "*5")): PHENOTYPE_POOR,
    ("CYP2D6", ("*5", "*5")): PHENOTYPE_POOR,
    ("CYP2D6", ("*10", "*10")): PHENOTYPE_POOR,
    ("CYP2D6", ("*2", "*2xN")): PHENOTYPE_ULTRARAPID,
    ("CYP2D6", ("*1", "*1xN")): PHENOTYPE_ULTRARAPID,
    # CYP2C19 — common allele pairs
    ("CYP2C19", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("CYP2C19", ("*1", "*2")): PHENOTYPE_INTERMEDIATE,
    ("CYP2C19", ("*1", "*3")): PHENOTYPE_INTERMEDIATE,
    ("CYP2C19", ("*2", "*2")): PHENOTYPE_POOR,
    ("CYP2C19", ("*2", "*3")): PHENOTYPE_POOR,
    ("CYP2C19", ("*3", "*3")): PHENOTYPE_POOR,
    ("CYP2C19", ("*1", "*17")): PHENOTYPE_RAPID,
    ("CYP2C19", ("*17", "*17")): PHENOTYPE_ULTRARAPID,
    # CYP2C9 — common allele pairs
    ("CYP2C9", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("CYP2C9", ("*1", "*2")): PHENOTYPE_INTERMEDIATE,
    ("CYP2C9", ("*1", "*3")): PHENOTYPE_INTERMEDIATE,
    ("CYP2C9", ("*2", "*2")): PHENOTYPE_INTERMEDIATE,
    ("CYP2C9", ("*2", "*3")): PHENOTYPE_POOR,
    ("CYP2C9", ("*3", "*3")): PHENOTYPE_POOR,
    # CYP3A4 — common allele pairs
    ("CYP3A4", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("CYP3A4", ("*1", "*22")): PHENOTYPE_INTERMEDIATE,
    ("CYP3A4", ("*22", "*22")): PHENOTYPE_POOR,
    # DPYD — common allele pairs
    ("DPYD", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("DPYD", ("*1", "*2A")): PHENOTYPE_INTERMEDIATE,
    ("DPYD", ("*2A", "*2A")): PHENOTYPE_POOR,
    ("DPYD", ("*1", "c.2846A>T")): PHENOTYPE_INTERMEDIATE,
    # TPMT — common allele pairs
    ("TPMT", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("TPMT", ("*1", "*2")): PHENOTYPE_INTERMEDIATE,
    ("TPMT", ("*1", "*3A")): PHENOTYPE_INTERMEDIATE,
    ("TPMT", ("*1", "*3C")): PHENOTYPE_INTERMEDIATE,
    ("TPMT", ("*2", "*3A")): PHENOTYPE_POOR,
    ("TPMT", ("*3A", "*3A")): PHENOTYPE_POOR,
    ("TPMT", ("*3A", "*3C")): PHENOTYPE_POOR,
    # UGT1A1 — common allele pairs
    ("UGT1A1", ("*1", "*1")): PHENOTYPE_NORMAL,
    ("UGT1A1", ("*1", "*28")): PHENOTYPE_INTERMEDIATE,
    ("UGT1A1", ("*28", "*28")): PHENOTYPE_POOR,
    ("UGT1A1", ("*1", "*6")): PHENOTYPE_INTERMEDIATE,
    ("UGT1A1", ("*6", "*28")): PHENOTYPE_POOR,
    # HLA-B — handled differently (presence/absence of allele)
    ("HLA-B", ("*57:01", "*57:01")): "HLA-B*57:01_positive",
    ("HLA-B", ("*15:02", "*15:02")): "HLA-B*15:02_positive",
    ("HLA-B", ("*58:01", "*58:01")): "HLA-B*58:01_positive",
    ("HLA-B", ("*1", "*57:01")): "HLA-B*57:01_positive",
    ("HLA-B", ("*1", "*15:02")): "HLA-B*15:02_positive",
    ("HLA-B", ("*1", "*58:01")): "HLA-B*58:01_positive",
}

# Score-to-severity thresholds (matches scorer.py _THRESHOLDS)
_SCORE_THRESHOLDS = [
    (80.0, "critical"),
    (60.0, "major"),
    (35.0, "moderate"),
    (0.0, "minor"),
]

# Base scores for severity levels (matches scorer.py _SEVERITY_WEIGHTS)
_SEVERITY_BASE_SCORES: dict[str, float] = {
    "critical": 90.0,
    "major": 70.0,
    "moderate": 40.0,
    "minor": 15.0,
    "none": 0.0,
}


def predict_phenotype_from_alleles(
    gene_id: str,
    allele_1: str,
    allele_2: str,
) -> tuple[str, float]:
    """
    Predict metabolizer phenotype from a diplotype (allele pair).

    Returns (phenotype_string, confidence_0_to_1).
    Returns ("unknown", 0.0) if allele pair not in lookup table.
    """
    key = (gene_id, tuple(sorted([allele_1, allele_2])))
    phenotype = ALLELE_PHENOTYPE_MAP.get(key)
    if phenotype:
        return phenotype, 0.95
    return "unknown", 0.0


def score_to_severity(score: float) -> str:
    """Map numeric score [0,100] to severity tier string."""
    for threshold, label in _SCORE_THRESHOLDS:
        if score >= threshold:
            return label
    return "minor"


class PGxAdjustmentResult:
    """
    Holds one PGx adjustment for a drug-gene-phenotype match.
    Returned as part of PGxScoreResult.
    """

    __slots__ = ("drug_name", "gene", "phenotype", "severity_multiplier", "reason")

    def __init__(
        self,
        drug_name: str,
        gene: str,
        phenotype: str,
        severity_multiplier: float,
        reason: str,
    ) -> None:
        self.drug_name = drug_name
        self.gene = gene
        self.phenotype = phenotype
        self.severity_multiplier = severity_multiplier
        self.reason = reason

    def to_dict(self) -> dict:
        return {
            "drug_name": self.drug_name,
            "gene": self.gene,
            "phenotype": self.phenotype,
            "severity_multiplier": self.severity_multiplier,
            "reason": self.reason,
        }


class PGxScorer:
    """
    Adjusts drug interaction risk scores using patient metabolizer phenotypes
    and CPIC guidelines from the database.

    Keeps no patient state — accepts phenotypes per-call (privacy-safe).
    """

    def __init__(self, store: GraphStore) -> None:
        self.store = store
        # Cache all guidelines once per instance to avoid N+1 queries
        self._guidelines_cache: dict[str, list] | None = None

    def _load_all_guidelines(self) -> dict[str, list]:
        """Load all genetic guidelines into (drug_id -> [GeneticGuideline]) map."""
        if self._guidelines_cache is None:
            all_gl = self.store.get_all_guidelines()
            cache: dict[str, list] = {}
            for gl in all_gl:
                cache.setdefault(gl.drug_id, []).append(gl)
            self._guidelines_cache = cache
        return self._guidelines_cache

    def get_adjustments_for_drug(
        self,
        drug_id: str,
        drug_name: str,
        phenotypes: dict[str, str],
    ) -> list[PGxAdjustmentResult]:
        """
        Return all CPIC adjustment results for a drug given patient phenotypes.

        Args:
            drug_id: Drug ID (e.g. "DB00318")
            drug_name: Human-readable drug name for result labelling
            phenotypes: dict mapping gene_id → phenotype string

        Returns:
            List of PGxAdjustmentResult (one per matching guideline)
        """
        all_guidelines = self._load_all_guidelines()
        drug_guidelines = all_guidelines.get(drug_id, [])
        results: list[PGxAdjustmentResult] = []

        for gl in drug_guidelines:
            patient_phenotype = phenotypes.get(gl.gene_id)
            if patient_phenotype and gl.phenotype == patient_phenotype:
                results.append(
                    PGxAdjustmentResult(
                        drug_name=drug_name,
                        gene=gl.gene_id,
                        phenotype=gl.phenotype,
                        severity_multiplier=gl.severity_multiplier,
                        reason=gl.recommendation,
                    )
                )
        return results

    def adjust_interaction_score(
        self,
        drug_a_id: str,
        drug_a_name: str,
        drug_b_id: str,
        drug_b_name: str,
        base_score: float,
        base_severity: str,
        phenotypes: dict[str, str],
    ) -> tuple[float, str, list[PGxAdjustmentResult]]:
        """
        Adjust a single pairwise interaction score using patient phenotypes.

        Args:
            drug_a_id, drug_a_name: First drug
            drug_b_id, drug_b_name: Second drug
            base_score: Original risk score [0, 100]
            base_severity: Original severity tier string
            phenotypes: dict mapping gene_id → phenotype string

        Returns:
            (adjusted_score, adjusted_severity, adjustments_list)
        """
        adjustments: list[PGxAdjustmentResult] = []

        adjustments.extend(self.get_adjustments_for_drug(drug_a_id, drug_a_name, phenotypes))
        adjustments.extend(self.get_adjustments_for_drug(drug_b_id, drug_b_name, phenotypes))

        if not adjustments:
            return base_score, base_severity, []

        # Multiply all severity multipliers together (cap at 100)
        total_multiplier = 1.0
        for adj in adjustments:
            total_multiplier *= adj.severity_multiplier

        adjusted_score = min(100.0, base_score * total_multiplier)
        adjusted_severity = score_to_severity(adjusted_score)

        return adjusted_score, adjusted_severity, adjustments

    def compute_pgx_confidence(
        self,
        adjustments: list[PGxAdjustmentResult],
        phenotypes: dict[str, str],
    ) -> float:
        """
        Compute confidence score for PGx adjustment.

        0.98 when adjustments present (known CPIC guideline).
        0.50 when no adjustments (no known PGx risk).
        0.0  when no phenotypes provided.
        """
        if not phenotypes:
            return 0.0
        return 0.98 if adjustments else 0.50

    def build_recommendations(
        self,
        adjustments: list[PGxAdjustmentResult],
        base_recommendations: Optional[list[str]] = None,
    ) -> list[str]:
        """
        Build merged list of recommendations from PGx adjustments.

        Deduplicates and prepends PGx-specific recommendations.
        """
        recs: list[str] = []
        seen: set[str] = set()

        for adj in adjustments:
            rec = f"{adj.gene} {adj.phenotype.replace('_', ' ')}: {adj.reason}"
            if rec not in seen:
                recs.append(rec)
                seen.add(rec)

        if base_recommendations:
            for r in base_recommendations:
                if r not in seen:
                    recs.append(r)
                    seen.add(r)

        return recs
