"""
Natural language explanation generator for drug interaction cascades.

Produces human-readable explanations of cascade paths, interaction risks,
and pharmacogenomic impacts without requiring external LLM APIs.
Uses template-based generation with pharmacological domain knowledge.
"""

from __future__ import annotations

from medgraph.engine.models import CascadePath, DrugInteractionResult, InteractionReport
from medgraph.graph.models import GeneticGuideline


# ---------------------------------------------------------------------------
# Severity descriptors
# ---------------------------------------------------------------------------

_SEVERITY_DESC = {
    "critical": "potentially life-threatening",
    "major": "clinically significant",
    "moderate": "may require monitoring",
    "minor": "generally well-tolerated",
}

_RELATION_VERB = {
    "inhibits": "inhibits",
    "induces": "induces",
    "metabolized_by": "is metabolized by",
    "interacts_with": "interacts with",
}

_STRENGTH_ADV = {
    "strong": "strongly",
    "moderate": "moderately",
    "weak": "weakly",
}

_PHENOTYPE_DESC = {
    "poor": "significantly reduced",
    "intermediate": "partially reduced",
    "normal": "normal",
    "rapid": "increased",
    "ultrarapid": "significantly increased",
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def explain_interaction(result: DrugInteractionResult) -> str:
    """
    Generate a plain-English explanation of a drug interaction.

    Covers: direct interaction, cascade paths, risk score context.
    """
    parts: list[str] = []

    drug_a = result.drug_a.name
    drug_b = result.drug_b.name
    severity_desc = _SEVERITY_DESC.get(result.severity, result.severity)

    # Opening summary
    parts.append(
        f"{drug_a} and {drug_b} have a {severity_desc} interaction "
        f"(risk score: {result.risk_score:.0f}/100)."
    )

    # Direct interaction
    if result.direct_interaction:
        desc = result.direct_interaction.description
        if desc:
            parts.append(f"Direct interaction: {desc}")
        mech = result.direct_interaction.mechanism
        if mech:
            parts.append(f"Mechanism: {mech}")

    # Cascade paths
    for cp in result.cascade_paths:
        cascade_text = explain_cascade_path(cp)
        if cascade_text:
            parts.append(cascade_text)

    # Evidence
    if result.evidence:
        total = sum(e.evidence_count for e in result.evidence if e.evidence_count > 0)
        if total > 0:
            parts.append(
                f"This interaction is supported by {total:,} FDA adverse event reports."
            )

    return " ".join(parts)


def explain_cascade_path(path: CascadePath) -> str:
    """Generate a readable explanation of a single cascade pathway."""
    if not path.steps:
        return ""

    step_descriptions = []
    for step in path.steps:
        verb = _RELATION_VERB.get(step.relation, step.relation)
        adv = _STRENGTH_ADV.get(step.strength, "")
        prefix = f"{adv} " if adv else ""

        if step.target_type == "enzyme":
            step_descriptions.append(
                f"{step.source_drug} {prefix}{verb} {step.target}"
            )
        else:
            step_descriptions.append(
                f"{step.target} {step.effect}"
            )

    chain = ", which ".join(step_descriptions) if step_descriptions else ""
    severity = _SEVERITY_DESC.get(path.net_severity, path.net_severity)

    return f"Enzyme cascade ({severity}): {chain}."


def explain_pgx_impact(
    drug_name: str,
    gene: str,
    phenotype: str,
    guideline: GeneticGuideline,
) -> str:
    """
    Explain how a patient's genetic profile affects a specific drug.

    Args:
        drug_name: Drug name for display.
        gene: Gene ID (e.g. CYP2D6).
        phenotype: Patient's phenotype (e.g. "poor").
        guideline: Matching CPIC guideline.
    """
    enzyme_activity = _PHENOTYPE_DESC.get(phenotype, phenotype)
    multiplier = guideline.severity_multiplier

    if multiplier > 1.0:
        impact = "increases"
        pct = f"{(multiplier - 1) * 100:.0f}%"
    elif multiplier < 1.0:
        impact = "decreases"
        pct = f"{(1 - multiplier) * 100:.0f}%"
    else:
        return (
            f"Patient has {phenotype} metabolizer status for {gene}. "
            f"No significant impact on {drug_name} risk expected."
        )

    parts = [
        f"Patient has {phenotype} metabolizer status for {gene} "
        f"({enzyme_activity} enzyme activity).",
        f"This {impact} the interaction risk for {drug_name} by {pct}.",
    ]

    if guideline.recommendation:
        parts.append(f"CPIC recommendation: {guideline.recommendation}")

    return " ".join(parts)


def explain_report(report: InteractionReport) -> str:
    """Generate a summary explanation for a full interaction report."""
    if not report.interactions:
        return "No drug interactions were detected among the analyzed medications."

    drug_names = [d.name for d in report.drugs]
    severity_desc = _SEVERITY_DESC.get(report.overall_risk, report.overall_risk)
    n_interactions = len(report.interactions)
    n_cascades = sum(len(r.cascade_paths) for r in report.interactions)

    parts = [
        f"Analysis of {len(drug_names)} medications "
        f"({', '.join(drug_names)}) found {n_interactions} interaction(s) "
        f"with an overall {severity_desc} risk level "
        f"(score: {report.overall_score:.0f}/100).",
    ]

    if n_cascades > 0:
        parts.append(
            f"{n_cascades} enzyme-mediated cascade pathway(s) were identified, "
            f"where drugs affect each other indirectly through shared CYP450 enzymes."
        )

    # Highlight critical/major interactions
    critical = [r for r in report.interactions if r.severity in ("critical", "major")]
    if critical:
        names = [
            f"{r.drug_a.name} + {r.drug_b.name} ({r.severity})"
            for r in critical
        ]
        parts.append(f"Key concerns: {'; '.join(names)}.")

    return " ".join(parts)
