"""
Risk scoring module for MEDGRAPH.

Implements the scoring formula from the product specification:
    base_score = severity_weight(direct_interaction.severity)
    cascade_bonus = sum(cascade_severity * 0.5 for each cascade_path)
    evidence_modifier = log10(fda_adverse_event_count + 1) * 5
    enzyme_strength = inhibitor_strength_weight (strong=1.0, moderate=0.6, weak=0.3)
    final_score = min(100, base_score + cascade_bonus * enzyme_strength + evidence_modifier)

Severity classification:
    >= 80: critical
    >= 60: major
    >= 35: moderate
    <  35: minor
"""

from __future__ import annotations

import math
from typing import Optional

from medgraph.engine.models import CascadePath, DrugInteractionResult, InteractionReport
from medgraph.graph.store import GraphStore

# Base scores by severity level
_SEVERITY_WEIGHTS: dict[str, float] = {
    "critical": 90.0,
    "major": 70.0,
    "moderate": 40.0,
    "minor": 15.0,
    "none": 0.0,
}

# Enzyme inhibitor/inducer strength multipliers
_STRENGTH_WEIGHTS: dict[str, float] = {
    "strong": 1.0,
    "moderate": 0.6,
    "weak": 0.3,
}

# Score thresholds for classification
_THRESHOLDS = [
    (80.0, "critical"),
    (60.0, "major"),
    (35.0, "moderate"),
    (0.0, "minor"),
]

# Maps external severity codes (e.g. DrugBank A-X) to internal severity levels
_SEVERITY_CODE_MAP: dict[str, str] = {
    "A": "critical",  # contraindicated
    "B": "major",
    "C": "moderate",
    "D": "minor",
    "X": "critical",  # avoid combination
}


class RiskScorer:
    """
    Computes risk scores for drug interaction results and reports.

    All scoring is deterministic and based on severity weights,
    cascade complexity, and FDA adverse event evidence counts.
    """

    def score_interaction(
        self,
        result: DrugInteractionResult,
        store: Optional[GraphStore] = None,
        metabolizer_phenotypes: Optional[dict[str, str]] = None,
    ) -> float:
        """
        Compute risk score for a drug pair interaction result.

        Args:
            result: DrugInteractionResult with direct interaction and cascade paths
            store: Optional GraphStore for additional evidence lookup
            metabolizer_phenotypes: Optional dict mapping gene ID to phenotype,
                e.g. {"CYP2D6": "poor", "CYP2C19": "normal"}

        Returns:
            Float score in range [0, 100]
        """
        # Base score from direct interaction severity
        direct_severity = "none"
        if result.direct_interaction:
            direct_severity = result.direct_interaction.severity
        base_score = _SEVERITY_WEIGHTS.get(direct_severity, 0.0)

        # Cascade bonus
        cascade_bonus = self._compute_cascade_bonus(result.cascade_paths)

        # Enzyme strength modifier — use max strength from cascade paths
        enzyme_strength = self._get_max_enzyme_strength(result.cascade_paths)

        # Evidence modifier from FAERS counts
        evidence_count = 0
        if result.direct_interaction:
            evidence_count = result.direct_interaction.evidence_count
        # Also include evidence from EvidenceItems
        for ev in result.evidence:
            evidence_count = max(evidence_count, ev.evidence_count)

        evidence_modifier = math.log10(evidence_count + 1) * 5.0

        # Final score
        final = base_score + (cascade_bonus * enzyme_strength) + evidence_modifier

        # Pharmacogenomics adjustment
        pgx_multiplier = 1.0
        if metabolizer_phenotypes and store:
            for gene_id, phenotype in metabolizer_phenotypes.items():
                # Check if either drug has a guideline for this gene+phenotype
                for drug in [result.drug_a, result.drug_b]:
                    guidelines = store.get_genetic_guidelines(drug.id, gene_id)
                    for gl in guidelines:
                        if gl.phenotype == phenotype:
                            pgx_multiplier = max(pgx_multiplier, gl.severity_multiplier)

        final = final * pgx_multiplier
        return min(100.0, final)

    def score_report(self, report: InteractionReport) -> float:
        """
        Compute overall score for a full interaction report.

        Uses worst-case (maximum) individual score as overall risk.

        Args:
            report: Complete InteractionReport

        Returns:
            Float score in range [0, 100]
        """
        if not report.interactions:
            return 0.0
        return max(r.risk_score for r in report.interactions)

    def classify_severity(self, score: float) -> str:
        """
        Map a numeric score to a severity classification string.

        Args:
            score: Float in range [0, 100]

        Returns:
            "critical" | "major" | "moderate" | "minor"
        """
        for threshold, label in _THRESHOLDS:
            if score >= threshold:
                return label
        return "minor"

    def rescore_report(
        self, report: InteractionReport, store: Optional[GraphStore] = None
    ) -> InteractionReport:
        """
        Recompute all scores in a report in-place.

        Updates each DrugInteractionResult.risk_score and severity,
        then updates report.overall_score and overall_risk.
        """
        for result in report.interactions:
            result.risk_score = self.score_interaction(result, store)
            result.severity = self.classify_severity(result.risk_score)

        report.overall_score = self.score_report(report)
        report.overall_risk = self.classify_severity(report.overall_score)
        return report

    @staticmethod
    def standardize_severity(code: str) -> str:
        """
        Map an external severity code to an internal severity level.

        Supports DrugBank-style letter codes (A, B, C, D, X):
            A / X → critical
            B     → major
            C     → moderate
            D     → minor

        Unknown codes are returned unchanged (lowercased) so callers can
        still pass already-normalized strings without double-mapping.

        Args:
            code: Severity code string (case-insensitive)

        Returns:
            Normalized severity string: "critical" | "major" | "moderate" | "minor"
        """
        normalized = code.strip().upper()
        return _SEVERITY_CODE_MAP.get(normalized, code.strip().lower())

    def score_polypharmacy(
        self,
        interactions: list,
        cascades: list,
    ) -> dict:
        """
        Score entire regimen topology for polypharmacy risk.

        Args:
            interactions: List of DrugInteractionResult objects from the analyzer.
            cascades: List of CascadePath objects across all drug pairs.

        Returns:
            {
                polypharmacy_score: float (0–100),
                risk_level: str,
                risk_clusters: list[dict],  # groups of drugs sharing enzyme conflicts
                summary: str,
            }
        """
        if not interactions:
            return {
                "polypharmacy_score": 0.0,
                "risk_level": "minor",
                "risk_clusters": [],
                "summary": "No interactions to score.",
            }

        # --- Component 1: Interaction burden ---
        total_interaction_count = len(interactions)
        max_individual_score = max((r.risk_score for r in interactions), default=0.0)

        # Burden penalty: each additional interaction adds diminishing risk
        burden_score = min(30.0, total_interaction_count * 3.0)

        # --- Component 2: Cascade depth ---
        all_cascade_depths = [len(c.steps) for c in cascades]
        max_cascade_depth = max(all_cascade_depths, default=0)
        # Each additional hop = +5 pts, capped at 20
        cascade_depth_score = min(20.0, max_cascade_depth * 5.0)

        # --- Component 3: Shared enzyme count ---
        all_enzymes: set[str] = set()
        for c in cascades:
            all_enzymes.update(c.enzyme_ids)
        shared_enzyme_score = min(20.0, len(all_enzymes) * 4.0)

        # --- Component 4: Severity amplifier ---
        # Boost based on max individual score (most dangerous pair dominates)
        severity_amplifier = max_individual_score * 0.3  # 30% of worst pair score

        raw_score = burden_score + cascade_depth_score + shared_enzyme_score + severity_amplifier
        polypharmacy_score = min(100.0, raw_score)
        risk_level = self.classify_severity(polypharmacy_score)

        # --- Risk clusters: groups of 3+ drugs sharing the same enzyme ---
        enzyme_to_drugs: dict[str, set[str]] = {}
        for c in cascades:
            pair = frozenset([c.drug_a_name, c.drug_b_name])
            for eid in c.enzyme_ids:
                enzyme_to_drugs.setdefault(eid, set()).update(pair)

        risk_clusters: list[dict] = []
        for enzyme_id, drug_names in enzyme_to_drugs.items():
            if len(drug_names) >= 3:
                risk_clusters.append(
                    {
                        "enzyme": enzyme_id,
                        "drugs": sorted(drug_names),
                        "drug_count": len(drug_names),
                    }
                )
        risk_clusters.sort(key=lambda c: c["drug_count"], reverse=True)

        # --- Summary ---
        summary = (
            f"Regimen contains {total_interaction_count} interaction pair(s) "
            f"across {len(all_enzymes)} shared enzyme(s). "
            f"Maximum cascade depth: {max_cascade_depth} hop(s). "
            f"Overall polypharmacy risk: {risk_level} ({polypharmacy_score:.1f}/100)."
        )

        return {
            "polypharmacy_score": round(polypharmacy_score, 2),
            "risk_level": risk_level,
            "risk_clusters": risk_clusters,
            "summary": summary,
        }

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _compute_cascade_bonus(self, paths: list[CascadePath]) -> float:
        """Sum cascade severity weights * 0.5 discount factor."""
        total = 0.0
        for path in paths:
            severity_weight = _SEVERITY_WEIGHTS.get(path.net_severity, 0.0)
            total += severity_weight * 0.5
        return total

    def _get_max_enzyme_strength(self, paths: list[CascadePath]) -> float:
        """Return the maximum enzyme strength weight across all cascade steps."""
        max_strength = 0.0
        for path in paths:
            for step in path.steps:
                weight = _STRENGTH_WEIGHTS.get(step.strength, 0.3)
                max_strength = max(max_strength, weight)
        return max_strength if max_strength > 0 else 1.0
