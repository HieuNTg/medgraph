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
    ) -> float:
        """
        Compute risk score for a drug pair interaction result.

        Args:
            result: DrugInteractionResult with direct interaction and cascade paths
            store: Optional GraphStore for additional evidence lookup

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
