"""
Severity Classification Agent — re-classifies interaction severity using
NLP pattern matching on real pharmacological data.

This agent analyzes interaction descriptions, mechanism text, and enzyme
relationship data to refine severity classifications. It uses evidence-based
rules derived from pharmacological principles:

1. CYP3A4 strong inhibition + narrow therapeutic index drug → critical
2. Multiple enzyme pathway involvement → escalate severity
3. FDA FAERS case count thresholds → evidence-based classification
4. Pharmacological keyword analysis → severity inference

This agent:
- Re-evaluates severity for all interactions using multi-factor analysis
- Uses enzyme relationship data (strength, relation_type) from the graph
- Incorporates FAERS evidence counts for evidence-based classification
- Updates Interaction.severity when the computed severity is higher
- Runs as a background job, not user-facing
"""

from __future__ import annotations

import logging

from medgraph.agents.base import AgentResult, BaseAgent
from medgraph.graph.models import Drug, DrugEnzymeRelation, Interaction
from medgraph.graph.store import GraphStore

logger = logging.getLogger(__name__)

# Narrow therapeutic index drugs — toxicity risk is especially high
_NARROW_THERAPEUTIC_INDEX = {
    "warfarin",
    "lithium",
    "digoxin",
    "theophylline",
    "phenytoin",
    "carbamazepine",
    "cyclosporine",
    "tacrolimus",
    "methotrexate",
    "aminophylline",
    "valproic acid",
}

# High-risk CYP enzymes (most clinically significant)
_HIGH_RISK_ENZYMES = {"CYP3A4", "CYP2D6", "CYP2C9", "CYP2C19"}

# FAERS case count thresholds for evidence-based severity adjustment
_FAERS_CRITICAL_THRESHOLD = 1000  # >1000 FAERS reports → strong evidence
_FAERS_MAJOR_THRESHOLD = 100  # >100 reports → moderate evidence

# Severity ordering for comparison
_SEVERITY_RANK = {"critical": 4, "major": 3, "moderate": 2, "minor": 1, "none": 0}

# Pharmacological keywords that indicate severity in descriptions
_CRITICAL_KEYWORDS = [
    "rhabdomyolysis",
    "serotonin syndrome",
    "torsades de pointes",
    "hemorrhage",
    "bleeding",
    "qc prolongation",
    "qt prolongation",
    "hepatotoxicity",
    "liver failure",
    "nephrotoxicity",
    "renal failure",
    "respiratory depression",
    "cardiac arrest",
    "anaphylaxis",
    "stevens-johnson",
    "agranulocytosis",
    "aplastic anemia",
]
_MAJOR_KEYWORDS = [
    "toxicity",
    "accumulation",
    "elevated levels",
    "increased risk",
    "significantly",
    "substantially",
    "marked increase",
    "potentiate",
    "hypotension",
    "hypertension",
    "arrhythmia",
    "seizure",
    "hypoglycemia",
    "hyperkalemia",
]


class SeverityAgent(BaseAgent):
    """
    Re-classifies interaction severity using multi-factor NLP analysis.

    Factors considered:
    1. Description text — pharmacological keywords
    2. Enzyme relationships — strength and type of CYP450 involvement
    3. Narrow therapeutic index — drugs where small changes matter
    4. FAERS evidence counts — real-world adverse event frequency
    5. Multi-enzyme involvement — multiple pathway disruption

    Only escalates severity (never downgrades). This is a safety-first approach:
    false positives (over-warning) are preferable to false negatives.

    Args:
        store: GraphStore for reading/writing data
    """

    def __init__(self, store: GraphStore) -> None:
        super().__init__(store, name="SeverityAgent")

    def _execute(self, result: AgentResult) -> None:
        """Re-classify severity for all interactions."""
        interactions = self.store.get_all_interactions()
        if not interactions:
            return

        # Pre-load all enzyme relations for batch processing
        all_relations = self.store.get_all_drug_enzyme_relations()
        drug_relations: dict[str, list[DrugEnzymeRelation]] = {}
        for rel in all_relations:
            drug_relations.setdefault(rel.drug_id, []).append(rel)

        # Pre-load all drugs to avoid N+1 queries in _classify()
        all_drugs = self.store.get_all_drugs()
        drug_map: dict[str, Drug] = {d.id: d for d in all_drugs}

        result.records_processed = len(interactions)

        for interaction in interactions:
            try:
                new_severity = self._classify(interaction, drug_relations, drug_map)
                current_rank = _SEVERITY_RANK.get(interaction.severity, 0)
                new_rank = _SEVERITY_RANK.get(new_severity, 0)

                # Only escalate, never downgrade (safety-first)
                if new_rank > current_rank:
                    logger.info(
                        f"[SeverityAgent] Escalating {interaction.id}: "
                        f"{interaction.severity} → {new_severity}"
                    )
                    interaction.severity = new_severity
                    self.store.upsert_interaction(interaction)
                    result.records_updated += 1
                else:
                    result.records_skipped += 1
            except Exception as e:
                logger.warning(f"[SeverityAgent] Error on {interaction.id}: {e}")
                result.errors.append(f"{interaction.id}: {e}")
                result.records_skipped += 1

    def _classify(
        self,
        interaction: Interaction,
        drug_relations: dict[str, list[DrugEnzymeRelation]],
        drug_map: dict[str, Drug],
    ) -> str:
        """
        Compute severity for an interaction using multi-factor analysis.

        Returns the computed severity string.
        """
        scores: list[int] = []

        # Factor 1: Description keyword analysis
        scores.append(self._score_description(interaction.description))

        # Factor 2: Mechanism keyword analysis
        if interaction.mechanism:
            scores.append(self._score_description(interaction.mechanism))

        # Factor 3: Narrow therapeutic index check
        drug_a = drug_map.get(interaction.drug_a_id)
        drug_b = drug_map.get(interaction.drug_b_id)
        if drug_a and drug_a.name.lower() in _NARROW_THERAPEUTIC_INDEX:
            scores.append(3)  # major baseline for NTI drugs
        if drug_b and drug_b.name.lower() in _NARROW_THERAPEUTIC_INDEX:
            scores.append(3)  # major baseline for NTI drugs

        # Factor 4: Enzyme relationship analysis
        enzyme_score = self._score_enzyme_involvement(
            interaction.drug_a_id,
            interaction.drug_b_id,
            drug_relations,
        )
        if enzyme_score > 0:
            scores.append(enzyme_score)

        # Factor 5: FAERS evidence count
        if interaction.evidence_count >= _FAERS_CRITICAL_THRESHOLD:
            scores.append(4)
        elif interaction.evidence_count >= _FAERS_MAJOR_THRESHOLD:
            scores.append(3)

        if not scores:
            return "minor"

        max_score = max(scores)
        if max_score >= 4:
            return "critical"
        elif max_score >= 3:
            return "major"
        elif max_score >= 2:
            return "moderate"
        return "minor"

    def _score_description(self, text: str) -> int:
        """Score severity from description/mechanism text keywords."""
        if not text:
            return 0

        text_lower = text.lower()

        for keyword in _CRITICAL_KEYWORDS:
            if keyword in text_lower:
                return 4

        for keyword in _MAJOR_KEYWORDS:
            if keyword in text_lower:
                return 3

        return 0

    def _score_enzyme_involvement(
        self,
        drug_a_id: str,
        drug_b_id: str,
        drug_relations: dict[str, list[DrugEnzymeRelation]],
    ) -> int:
        """
        Score severity based on enzyme relationship analysis.

        High-risk patterns:
        - Drug A strongly inhibits high-risk enzyme + Drug B metabolized by same enzyme
        - Multiple shared enzymes affected
        - Strong inhibition of any CYP enzyme used by NTI drug
        """
        rels_a = drug_relations.get(drug_a_id, [])
        rels_b = drug_relations.get(drug_b_id, [])

        if not rels_a or not rels_b:
            return 0

        # Find shared enzymes
        enzymes_a = {r.enzyme_id: r for r in rels_a}
        enzymes_b = {r.enzyme_id: r for r in rels_b}
        shared = set(enzymes_a.keys()) & set(enzymes_b.keys())

        if not shared:
            return 0

        max_score = 0

        for enzyme_id in shared:
            rel_a = enzymes_a[enzyme_id]
            rel_b = enzymes_b[enzyme_id]

            # Pattern: Drug A inhibits enzyme + Drug B metabolized by enzyme
            if rel_a.relation_type == "inhibits" and rel_b.relation_type == "metabolized_by":
                if rel_a.strength == "strong" and enzyme_id in _HIGH_RISK_ENZYMES:
                    max_score = max(max_score, 4)  # critical
                elif rel_a.strength == "strong":
                    max_score = max(max_score, 3)  # major
                else:
                    max_score = max(max_score, 2)  # moderate

            # Reverse: Drug B inhibits enzyme + Drug A metabolized by enzyme
            if rel_b.relation_type == "inhibits" and rel_a.relation_type == "metabolized_by":
                if rel_b.strength == "strong" and enzyme_id in _HIGH_RISK_ENZYMES:
                    max_score = max(max_score, 4)
                elif rel_b.strength == "strong":
                    max_score = max(max_score, 3)
                else:
                    max_score = max(max_score, 2)

            # Pattern: Both drugs compete for same enzyme (substrate competition)
            if rel_a.relation_type == "metabolized_by" and rel_b.relation_type == "metabolized_by":
                max_score = max(max_score, 2)  # moderate

        # Multi-enzyme involvement escalation
        if len(shared) >= 3:
            max_score = max(max_score, 3)  # major if 3+ shared enzymes
        elif len(shared) >= 2:
            max_score = max(max_score, 2)  # escalate to moderate for 2+ shared enzymes

        return max_score
