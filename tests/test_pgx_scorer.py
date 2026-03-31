"""
Comprehensive tests for PGxScorer — pharmacogenomics scoring engine (CRITICAL patient safety).

Covers all methods with 30+ test cases:
- PGxScorer.__init__
- adjust_interaction_score with various phenotypes
- compute_pgx_confidence
- build_recommendations
- predict_phenotype_from_alleles
- _get_guidelines_for_drug (caching)
- Edge cases: None inputs, empty lists, boundary scores

Patient safety critical: 0% → 100% coverage target.
"""

from __future__ import annotations

import pytest

from medgraph.engine.pgx_scorer import (
    PGxScorer,
    PGxAdjustmentResult,
    predict_phenotype_from_alleles,
    score_to_severity,
    PHENOTYPE_POOR,
    PHENOTYPE_INTERMEDIATE,
    PHENOTYPE_NORMAL,
    PHENOTYPE_RAPID,
    PHENOTYPE_ULTRARAPID,
)
from medgraph.graph.models import GeneticGuideline


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


class MockGraphStore:
    """Mock GraphStore for PGxScorer testing."""

    def __init__(self, guidelines: list[GeneticGuideline] | None = None):
        self.guidelines = guidelines or []

    def get_all_guidelines(self) -> list[GeneticGuideline]:
        return self.guidelines


@pytest.fixture
def empty_store() -> MockGraphStore:
    """Store with no genetic guidelines."""
    return MockGraphStore([])


@pytest.fixture
def basic_store() -> MockGraphStore:
    """Store with common CPIC guidelines."""
    guidelines = [
        # Codeine + CYP2D6 poor metabolizer
        GeneticGuideline(
            drug_id="DB00521",
            gene_id="CYP2D6",
            phenotype=PHENOTYPE_POOR,
            recommendation="Avoid codeine; consider alternative opioid",
            severity_multiplier=1.5,
        ),
        # Codeine + CYP2D6 ultrarapid metabolizer
        GeneticGuideline(
            drug_id="DB00521",
            gene_id="CYP2D6",
            phenotype=PHENOTYPE_ULTRARAPID,
            recommendation="Avoid codeine; risk of overdose with normal dosing",
            severity_multiplier=1.8,
        ),
        # Citalopram + CYP2C19 poor metabolizer
        GeneticGuideline(
            drug_id="DB00215",
            gene_id="CYP2C19",
            phenotype=PHENOTYPE_POOR,
            recommendation="Consider alternative; reduce dose if needed",
            severity_multiplier=1.3,
        ),
        # Citalopram + CYP2C19 rapid metabolizer
        GeneticGuideline(
            drug_id="DB00215",
            gene_id="CYP2C19",
            phenotype=PHENOTYPE_RAPID,
            recommendation="May require higher dose; monitor efficacy",
            severity_multiplier=0.8,
        ),
        # Warfarin + CYP2C9 poor metabolizer
        GeneticGuideline(
            drug_id="DB00682",
            gene_id="CYP2C9",
            phenotype=PHENOTYPE_POOR,
            recommendation="Use lower starting dose; increase INR monitoring",
            severity_multiplier=1.6,
        ),
        # Simvastatin + CYP3A4 poor metabolizer
        GeneticGuideline(
            drug_id="DB00641",
            gene_id="CYP3A4",
            phenotype=PHENOTYPE_POOR,
            recommendation="Reduce dose; monitor for myopathy",
            severity_multiplier=2.0,
        ),
    ]
    return MockGraphStore(guidelines)


@pytest.fixture
def pgx_scorer(basic_store: MockGraphStore) -> PGxScorer:
    """PGxScorer instance with mock store."""
    return PGxScorer(basic_store)


@pytest.fixture
def pgx_scorer_empty(empty_store: MockGraphStore) -> PGxScorer:
    """PGxScorer instance with empty store (no guidelines)."""
    return PGxScorer(empty_store)


# ---------------------------------------------------------------------------
# Test: PGxScorer.__init__
# ---------------------------------------------------------------------------


class TestPGxScorerInit:
    def test_init_with_store(self, basic_store: MockGraphStore):
        """Initialization should accept a GraphStore."""
        scorer = PGxScorer(basic_store)
        assert scorer.store is basic_store

    def test_init_cache_starts_empty(self, basic_store: MockGraphStore):
        """Cache should initialize as None."""
        scorer = PGxScorer(basic_store)
        assert scorer._guidelines_cache is None

    def test_init_creates_instance(self, basic_store: MockGraphStore):
        """Should create valid PGxScorer instance."""
        scorer = PGxScorer(basic_store)
        assert isinstance(scorer, PGxScorer)


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Normal Metabolizer
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreNormalMetabolizer:
    def test_normal_metabolizer_no_adjustment(self, pgx_scorer: PGxScorer):
        """Normal metabolizer should not adjust score."""
        phenotypes = {"CYP2D6": PHENOTYPE_NORMAL}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 40.0
        assert severity == "moderate"
        assert adjustments == []

    def test_normal_metabolizer_both_drugs(self, pgx_scorer: PGxScorer):
        """Normal metabolizer with multiple drugs should still have no adjustment."""
        phenotypes = {"CYP2D6": PHENOTYPE_NORMAL, "CYP2C19": PHENOTYPE_NORMAL}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=30.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 30.0
        assert adjustments == []


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Poor Metabolizer
# ---------------------------------------------------------------------------


class TestAdjustInteractionScorePoorMetabolizer:
    def test_poor_metabolizer_increases_score(self, pgx_scorer: PGxScorer):
        """Poor metabolizer should increase risk score."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        expected_score = 40.0 * 1.5  # 1.5 multiplier
        assert score == expected_score
        assert len(adjustments) == 1
        assert adjustments[0].severity_multiplier == 1.5
        assert adjustments[0].phenotype == PHENOTYPE_POOR

    def test_poor_metabolizer_citalopram(self, pgx_scorer: PGxScorer):
        """Poor metabolizer for CYP2C19 with citalopram."""
        phenotypes = {"CYP2C19": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00215",
            drug_a_name="Citalopram",
            drug_b_id="DB00521",
            drug_b_name="Codeine",
            base_score=35.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        expected_score = 35.0 * 1.3
        assert score == expected_score
        assert len(adjustments) == 1
        assert adjustments[0].gene == "CYP2C19"

    def test_poor_metabolizer_severity_escalation(self, pgx_scorer: PGxScorer):
        """Poor metabolizer should escalate severity tier."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=25.0,
            base_severity="minor",
            phenotypes=phenotypes,
        )
        # 25 * 1.5 = 37.5 → moderate (threshold >= 35)
        assert score == 37.5
        assert severity == "moderate"


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Ultrarapid Metabolizer
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreUltrarapidMetabolizer:
    def test_ultrarapid_metabolizer_increases_score(self, pgx_scorer: PGxScorer):
        """Ultrarapid metabolizer should increase risk score."""
        phenotypes = {"CYP2D6": PHENOTYPE_ULTRARAPID}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=50.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        expected_score = 50.0 * 1.8
        assert score == expected_score
        assert adjustments[0].severity_multiplier == 1.8
        assert adjustments[0].phenotype == PHENOTYPE_ULTRARAPID


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Multiple Phenotypes
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreMultiplePhenotypes:
    def test_multiple_phenotypes_combined_multiplier(self, pgx_scorer: PGxScorer):
        """Multiple matching phenotypes should multiply all multipliers."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR, "CYP2C19": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        # 1.5 * 1.3 = 1.95
        expected_score = 40.0 * 1.95
        assert score == expected_score
        assert len(adjustments) == 2

    def test_multiple_phenotypes_cap_at_100(self, pgx_scorer: PGxScorer):
        """Score should cap at 100."""
        phenotypes = {"CYP2D6": PHENOTYPE_ULTRARAPID, "CYP2C19": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=80.0,
            base_severity="critical",
            phenotypes=phenotypes,
        )
        # 80 * 1.8 * 1.3 = 187.2 → capped at 100
        assert score == 100.0
        assert severity == "critical"


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — No Matching Guidelines
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreNoGuidelines:
    def test_no_matching_guidelines_no_adjustment(self, pgx_scorer: PGxScorer):
        """Phenotypes without guidelines should not adjust score."""
        phenotypes = {"CYP1A2": "normal_metabolizer"}  # No guideline for this gene
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=50.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 50.0
        assert adjustments == []

    def test_unmatched_drug_no_adjustment(self, pgx_scorer: PGxScorer):
        """Drug not in guidelines should not be adjusted."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB99999",  # Unknown drug
            drug_a_name="UnknownDrug",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=45.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 45.0
        assert adjustments == []


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Empty Phenotypes
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreEmptyPhenotypes:
    def test_empty_phenotypes_dict_no_adjustment(self, pgx_scorer: PGxScorer):
        """Empty phenotypes dict should not adjust score."""
        phenotypes = {}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 40.0
        assert severity == "moderate"
        assert adjustments == []


# ---------------------------------------------------------------------------
# Test: adjust_interaction_score — Boundary Scores
# ---------------------------------------------------------------------------


class TestAdjustInteractionScoreBoundaryScores:
    def test_zero_base_score(self, pgx_scorer: PGxScorer):
        """Base score of 0 should remain 0 even with adjustment."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=0.0,
            base_severity="minor",
            phenotypes=phenotypes,
        )
        assert score == 0.0
        assert severity == "minor"

    def test_100_base_score(self, pgx_scorer: PGxScorer):
        """Base score of 100 should remain 100 when capped."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=100.0,
            base_severity="critical",
            phenotypes=phenotypes,
        )
        assert score == 100.0
        assert severity == "critical"

    def test_near_100_with_multiplier_capped(self, pgx_scorer: PGxScorer):
        """High score with multiplier should cap at 100."""
        phenotypes = {"CYP3A4": PHENOTYPE_POOR}  # 2.0 multiplier
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00641",
            drug_a_name="Simvastatin",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=60.0,
            base_severity="major",
            phenotypes=phenotypes,
        )
        # 60 * 2.0 = 120 → capped at 100
        assert score == 100.0
        assert severity == "critical"


# ---------------------------------------------------------------------------
# Test: compute_pgx_confidence
# ---------------------------------------------------------------------------


class TestComputePGxConfidence:
    def test_confidence_with_adjustments(self, pgx_scorer: PGxScorer):
        """With adjustments, confidence should be 0.98."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine",
            )
        ]
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        confidence = pgx_scorer.compute_pgx_confidence(adjustments, phenotypes)
        assert confidence == 0.98

    def test_confidence_without_adjustments(self, pgx_scorer: PGxScorer):
        """Without adjustments but with phenotypes, confidence should be 0.50."""
        adjustments = []
        phenotypes = {"CYP2D6": PHENOTYPE_NORMAL}
        confidence = pgx_scorer.compute_pgx_confidence(adjustments, phenotypes)
        assert confidence == 0.50

    def test_confidence_no_phenotypes(self, pgx_scorer: PGxScorer):
        """Without phenotypes, confidence should be 0.0."""
        adjustments = []
        phenotypes = {}
        confidence = pgx_scorer.compute_pgx_confidence(adjustments, phenotypes)
        assert confidence == 0.0

    def test_confidence_no_phenotypes_even_with_adjustments(self, pgx_scorer: PGxScorer):
        """With adjustments but empty phenotypes dict, confidence should be 0.0."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine",
            )
        ]
        phenotypes = {}
        confidence = pgx_scorer.compute_pgx_confidence(adjustments, phenotypes)
        assert confidence == 0.0

    def test_confidence_multiple_adjustments(self, pgx_scorer: PGxScorer):
        """Multiple adjustments should still give 0.98 confidence."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine",
            ),
            PGxAdjustmentResult(
                drug_name="Citalopram",
                gene="CYP2C19",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.3,
                reason="Reduce dose",
            ),
        ]
        phenotypes = {"CYP2D6": PHENOTYPE_POOR, "CYP2C19": PHENOTYPE_POOR}
        confidence = pgx_scorer.compute_pgx_confidence(adjustments, phenotypes)
        assert confidence == 0.98


# ---------------------------------------------------------------------------
# Test: build_recommendations
# ---------------------------------------------------------------------------


class TestBuildRecommendations:
    def test_build_recommendations_from_adjustments(self, pgx_scorer: PGxScorer):
        """Recommendations should be built from adjustments."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine; consider alternative opioid",
            )
        ]
        recs = pgx_scorer.build_recommendations(adjustments)
        assert len(recs) == 1
        assert "CYP2D6" in recs[0]
        assert "poor metabolizer" in recs[0]
        assert "Avoid codeine" in recs[0]

    def test_build_recommendations_deduplicates(self, pgx_scorer: PGxScorer):
        """Identical recommendations should be deduplicated."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Test reason",
            ),
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Test reason",
            ),
        ]
        recs = pgx_scorer.build_recommendations(adjustments)
        assert len(recs) == 1

    def test_build_recommendations_with_base_recommendations(self, pgx_scorer: PGxScorer):
        """Should merge PGx recommendations with base recommendations."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine",
            )
        ]
        base_recs = ["Monitor blood pressure", "Check liver function"]
        recs = pgx_scorer.build_recommendations(adjustments, base_recs)
        assert len(recs) == 3
        assert any("CYP2D6" in r for r in recs)
        assert "Monitor blood pressure" in recs
        assert "Check liver function" in recs

    def test_build_recommendations_deduplicates_base(self, pgx_scorer: PGxScorer):
        """Should deduplicate base recommendations too."""
        adjustments = []
        base_recs = ["Monitor", "Monitor"]
        recs = pgx_scorer.build_recommendations(adjustments, base_recs)
        assert recs.count("Monitor") == 1

    def test_build_recommendations_empty_adjustments(self, pgx_scorer: PGxScorer):
        """Empty adjustments should only return base recommendations."""
        adjustments = []
        base_recs = ["Check renal function", "Monitor potassium"]
        recs = pgx_scorer.build_recommendations(adjustments, base_recs)
        assert recs == base_recs

    def test_build_recommendations_no_base(self, pgx_scorer: PGxScorer):
        """Should work with None base_recommendations."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid",
            )
        ]
        recs = pgx_scorer.build_recommendations(adjustments, None)
        assert len(recs) == 1
        assert "CYP2D6" in recs[0]

    def test_build_recommendations_underscore_replacement(self, pgx_scorer: PGxScorer):
        """Underscores in phenotype should be replaced with spaces."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_ULTRARAPID,
                severity_multiplier=1.8,
                reason="Reduce dose",
            )
        ]
        recs = pgx_scorer.build_recommendations(adjustments)
        assert "ultrarapid metabolizer" in recs[0]  # underscore replaced


# ---------------------------------------------------------------------------
# Test: predict_phenotype_from_alleles (Module-level function)
# ---------------------------------------------------------------------------


class TestPredictPhenotypeFromAlleles:
    def test_cyp2d6_normal_1_1(self):
        """CYP2D6 *1/*1 should be normal metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2D6", "*1", "*1")
        assert phenotype == PHENOTYPE_NORMAL
        assert confidence == 0.95

    def test_cyp2d6_poor_4_4(self):
        """CYP2D6 *4/*4 should be poor metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2D6", "*4", "*4")
        assert phenotype == PHENOTYPE_POOR
        assert confidence == 0.95

    def test_cyp2d6_intermediate_1_4(self):
        """CYP2D6 *1/*4 should be intermediate metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2D6", "*1", "*4")
        assert phenotype == PHENOTYPE_INTERMEDIATE
        assert confidence == 0.95

    def test_cyp2d6_ultrarapid_2_2xN(self):
        """CYP2D6 *2/*2xN should be ultrarapid metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2D6", "*2", "*2xN")
        assert phenotype == PHENOTYPE_ULTRARAPID
        assert confidence == 0.95

    def test_cyp2c19_normal_1_1(self):
        """CYP2C19 *1/*1 should be normal metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C19", "*1", "*1")
        assert phenotype == PHENOTYPE_NORMAL
        assert confidence == 0.95

    def test_cyp2c19_poor_2_2(self):
        """CYP2C19 *2/*2 should be poor metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C19", "*2", "*2")
        assert phenotype == PHENOTYPE_POOR
        assert confidence == 0.95

    def test_cyp2c19_rapid_1_17(self):
        """CYP2C19 *1/*17 should be rapid metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C19", "*1", "*17")
        assert phenotype == PHENOTYPE_RAPID
        assert confidence == 0.95

    def test_cyp2c19_ultrarapid_17_17(self):
        """CYP2C19 *17/*17 should be ultrarapid metabolizer."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C19", "*17", "*17")
        assert phenotype == PHENOTYPE_ULTRARAPID
        assert confidence == 0.95

    def test_allele_order_independent(self):
        """Allele order should not matter (sorted)."""
        phenotype1, conf1 = predict_phenotype_from_alleles("CYP2C19", "*1", "*17")
        phenotype2, conf2 = predict_phenotype_from_alleles("CYP2C19", "*17", "*1")
        assert phenotype1 == phenotype2
        assert conf1 == conf2

    def test_unknown_allele_pair(self):
        """Unknown allele pair should return 'unknown' with 0.0 confidence."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2D6", "*999", "*888")
        assert phenotype == "unknown"
        assert confidence == 0.0

    def test_unknown_gene(self):
        """Unknown gene should return 'unknown'."""
        phenotype, confidence = predict_phenotype_from_alleles("UNKNOWN_GENE", "*1", "*1")
        assert phenotype == "unknown"
        assert confidence == 0.0

    def test_cyp2c9_intermediate_1_2(self):
        """CYP2C9 *1/*2 should be intermediate."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C9", "*1", "*2")
        assert phenotype == PHENOTYPE_INTERMEDIATE
        assert confidence == 0.95

    def test_cyp2c9_poor_2_3(self):
        """CYP2C9 *2/*3 should be poor."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP2C9", "*2", "*3")
        assert phenotype == PHENOTYPE_POOR
        assert confidence == 0.95

    def test_cyp3a4_normal_1_1(self):
        """CYP3A4 *1/*1 should be normal."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP3A4", "*1", "*1")
        assert phenotype == PHENOTYPE_NORMAL
        assert confidence == 0.95

    def test_cyp3a4_poor_22_22(self):
        """CYP3A4 *22/*22 should be poor."""
        phenotype, confidence = predict_phenotype_from_alleles("CYP3A4", "*22", "*22")
        assert phenotype == PHENOTYPE_POOR
        assert confidence == 0.95

    def test_dpyd_intermediate_1_2a(self):
        """DPYD *1/*2A should be intermediate."""
        phenotype, confidence = predict_phenotype_from_alleles("DPYD", "*1", "*2A")
        assert phenotype == PHENOTYPE_INTERMEDIATE
        assert confidence == 0.95

    def test_tpmt_poor_3a_3a(self):
        """TPMT *3A/*3A should be poor."""
        phenotype, confidence = predict_phenotype_from_alleles("TPMT", "*3A", "*3A")
        assert phenotype == PHENOTYPE_POOR
        assert confidence == 0.95

    def test_ugt1a1_intermediate_1_28(self):
        """UGT1A1 *1/*28 should be intermediate."""
        phenotype, confidence = predict_phenotype_from_alleles("UGT1A1", "*1", "*28")
        assert phenotype == PHENOTYPE_INTERMEDIATE
        assert confidence == 0.95


# ---------------------------------------------------------------------------
# Test: get_adjustments_for_drug (caching behavior)
# ---------------------------------------------------------------------------


class TestGetAdjustmentsForDrug:
    def test_get_adjustments_single_match(self, pgx_scorer: PGxScorer):
        """Should return matching adjustments for a drug."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        adjustments = pgx_scorer.get_adjustments_for_drug(
            drug_id="DB00521",
            drug_name="Codeine",
            phenotypes=phenotypes,
        )
        assert len(adjustments) == 1
        assert adjustments[0].drug_name == "Codeine"
        assert adjustments[0].gene == "CYP2D6"
        assert adjustments[0].phenotype == PHENOTYPE_POOR

    def test_get_adjustments_multiple_matches(self, pgx_scorer: PGxScorer):
        """Drug with multiple phenotype matches should return all."""
        phenotypes = {"CYP2D6": PHENOTYPE_ULTRARAPID}
        adjustments = pgx_scorer.get_adjustments_for_drug(
            drug_id="DB00521",
            drug_name="Codeine",
            phenotypes=phenotypes,
        )
        assert len(adjustments) >= 1

    def test_get_adjustments_no_match_phenotype(self, pgx_scorer: PGxScorer):
        """No phenotype match should return empty."""
        phenotypes = {"CYP2D6": PHENOTYPE_NORMAL}
        adjustments = pgx_scorer.get_adjustments_for_drug(
            drug_id="DB00521",
            drug_name="Codeine",
            phenotypes=phenotypes,
        )
        assert adjustments == []

    def test_get_adjustments_no_match_drug(self, pgx_scorer: PGxScorer):
        """Unknown drug should return empty."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        adjustments = pgx_scorer.get_adjustments_for_drug(
            drug_id="DB99999",
            drug_name="UnknownDrug",
            phenotypes=phenotypes,
        )
        assert adjustments == []

    def test_get_adjustments_empty_phenotypes(self, pgx_scorer: PGxScorer):
        """Empty phenotypes should return empty."""
        adjustments = pgx_scorer.get_adjustments_for_drug(
            drug_id="DB00521",
            drug_name="Codeine",
            phenotypes={},
        )
        assert adjustments == []

    def test_load_all_guidelines_caches(self, basic_store: MockGraphStore):
        """Guidelines should be cached on first call."""
        scorer = PGxScorer(basic_store)
        assert scorer._guidelines_cache is None

        # First call loads cache
        cache1 = scorer._load_all_guidelines()
        assert scorer._guidelines_cache is not None
        assert isinstance(cache1, dict)

        # Second call should return same cached instance
        cache2 = scorer._load_all_guidelines()
        assert cache1 is cache2


# ---------------------------------------------------------------------------
# Test: score_to_severity (Module-level function)
# ---------------------------------------------------------------------------


class TestScoreToSeverity:
    def test_critical_threshold_80(self):
        """Score >= 80 should be critical."""
        assert score_to_severity(80.0) == "critical"
        assert score_to_severity(90.0) == "critical"
        assert score_to_severity(100.0) == "critical"

    def test_major_threshold_60(self):
        """Score [60, 80) should be major."""
        assert score_to_severity(60.0) == "major"
        assert score_to_severity(70.0) == "major"
        assert score_to_severity(79.9) == "major"

    def test_moderate_threshold_35(self):
        """Score [35, 60) should be moderate."""
        assert score_to_severity(35.0) == "moderate"
        assert score_to_severity(50.0) == "moderate"
        assert score_to_severity(59.9) == "moderate"

    def test_minor_threshold_0(self):
        """Score [0, 35) should be minor."""
        assert score_to_severity(0.0) == "minor"
        assert score_to_severity(15.0) == "minor"
        assert score_to_severity(34.9) == "minor"

    def test_boundary_critical_major(self):
        """Exact boundary between critical and major."""
        assert score_to_severity(79.99) == "major"
        assert score_to_severity(80.0) == "critical"

    def test_boundary_major_moderate(self):
        """Exact boundary between major and moderate."""
        assert score_to_severity(59.99) == "moderate"
        assert score_to_severity(60.0) == "major"


# ---------------------------------------------------------------------------
# Test: PGxAdjustmentResult
# ---------------------------------------------------------------------------


class TestPGxAdjustmentResult:
    def test_adjustment_result_creation(self):
        """Should create PGxAdjustmentResult instance."""
        result = PGxAdjustmentResult(
            drug_name="Codeine",
            gene="CYP2D6",
            phenotype=PHENOTYPE_POOR,
            severity_multiplier=1.5,
            reason="Avoid codeine",
        )
        assert result.drug_name == "Codeine"
        assert result.gene == "CYP2D6"
        assert result.phenotype == PHENOTYPE_POOR
        assert result.severity_multiplier == 1.5
        assert result.reason == "Avoid codeine"

    def test_adjustment_result_to_dict(self):
        """Should convert to dictionary."""
        result = PGxAdjustmentResult(
            drug_name="Codeine",
            gene="CYP2D6",
            phenotype=PHENOTYPE_POOR,
            severity_multiplier=1.5,
            reason="Avoid codeine",
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["drug_name"] == "Codeine"
        assert d["gene"] == "CYP2D6"
        assert d["phenotype"] == PHENOTYPE_POOR
        assert d["severity_multiplier"] == 1.5
        assert d["reason"] == "Avoid codeine"


# ---------------------------------------------------------------------------
# Test: Edge Cases & Integration
# ---------------------------------------------------------------------------


class TestEdgeCasesAndIntegration:
    def test_rapid_metabolizer_decreases_score(self, pgx_scorer: PGxScorer):
        """Rapid metabolizer should decrease severity multiplier."""
        phenotypes = {"CYP2C19": PHENOTYPE_RAPID}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00215",
            drug_a_name="Citalopram",
            drug_b_id="DB00521",
            drug_b_name="Codeine",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        # 0.8 multiplier should decrease score
        expected_score = 40.0 * 0.8
        assert score == expected_score
        assert adjustments[0].severity_multiplier == 0.8

    def test_warfarin_cyp2c9_poor(self, pgx_scorer: PGxScorer):
        """Warfarin with CYP2C9 poor should increase risk."""
        phenotypes = {"CYP2C9": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00682",
            drug_a_name="Warfarin",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=50.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        expected_score = 50.0 * 1.6
        assert score == expected_score
        assert adjustments[0].gene == "CYP2C9"

    def test_simvastatin_cyp3a4_critical_risk(self, pgx_scorer: PGxScorer):
        """Simvastatin with CYP3A4 poor = critical risk."""
        phenotypes = {"CYP3A4": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00641",
            drug_a_name="Simvastatin",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        expected_score = 40.0 * 2.0
        assert score == expected_score
        assert severity == "critical"
        assert len(adjustments) == 1

    def test_no_guidelines_store(self, pgx_scorer_empty: PGxScorer):
        """Scorer with empty store should handle gracefully."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer_empty.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 40.0
        assert adjustments == []

    def test_phenotype_mismatch_no_adjustment(self, pgx_scorer: PGxScorer):
        """Phenotype present but not matching guideline should not adjust."""
        phenotypes = {"CYP2D6": PHENOTYPE_INTERMEDIATE}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00521",
            drug_a_name="Codeine",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=40.0,
            base_severity="moderate",
            phenotypes=phenotypes,
        )
        assert score == 40.0
        assert adjustments == []

    def test_high_base_score_adjustment_prevents_overflow(self, pgx_scorer: PGxScorer):
        """Very high score with multiplier should cap at 100."""
        phenotypes = {"CYP3A4": PHENOTYPE_POOR}
        score, severity, adjustments = pgx_scorer.adjust_interaction_score(
            drug_a_id="DB00641",
            drug_a_name="Simvastatin",
            drug_b_id="DB00215",
            drug_b_name="Citalopram",
            base_score=99.0,
            base_severity="critical",
            phenotypes=phenotypes,
        )
        # 99 * 2.0 = 198 → capped at 100
        assert score == 100.0
        assert severity == "critical"


# ---------------------------------------------------------------------------
# Test: Patient Safety Critical Features
# ---------------------------------------------------------------------------


class TestPatientSafetyCritical:
    """
    Critical tests for patient safety:
    - Ensure no false negatives (missing adjustments)
    - Ensure recommendations are clear
    - Ensure caching doesn't stale data
    """

    def test_poor_metabolizer_always_detected(self, pgx_scorer: PGxScorer):
        """Poor metabolizer phenotype must always be detected."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        for base_score in [10.0, 30.0, 50.0, 70.0, 90.0]:
            score, severity, adjustments = pgx_scorer.adjust_interaction_score(
                drug_a_id="DB00521",
                drug_a_name="Codeine",
                drug_b_id="DB00215",
                drug_b_name="Citalopram",
                base_score=base_score,
                base_severity="moderate",
                phenotypes=phenotypes,
            )
            assert len(adjustments) > 0, f"Failed for base_score={base_score}"
            assert adjustments[0].phenotype == PHENOTYPE_POOR

    def test_recommendations_never_empty_with_adjustments(self, pgx_scorer: PGxScorer):
        """Adjustments should always produce non-empty recommendations."""
        adjustments = [
            PGxAdjustmentResult(
                drug_name="Codeine",
                gene="CYP2D6",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.5,
                reason="Avoid codeine; consider alternative opioid",
            ),
            PGxAdjustmentResult(
                drug_name="Warfarin",
                gene="CYP2C9",
                phenotype=PHENOTYPE_POOR,
                severity_multiplier=1.6,
                reason="Use lower starting dose",
            ),
        ]
        recs = pgx_scorer.build_recommendations(adjustments)
        assert len(recs) >= len(adjustments)
        for rec in recs:
            assert len(rec) > 0
            assert ":" in rec  # Gene: phenotype reason format

    def test_multiple_drug_pair_consistency(self, pgx_scorer: PGxScorer):
        """Same drug pair should give consistent results."""
        phenotypes = {"CYP2D6": PHENOTYPE_POOR}
        results = []
        for _ in range(3):
            score, severity, adjustments = pgx_scorer.adjust_interaction_score(
                drug_a_id="DB00521",
                drug_a_name="Codeine",
                drug_b_id="DB00215",
                drug_b_name="Citalopram",
                base_score=40.0,
                base_severity="moderate",
                phenotypes=phenotypes,
            )
            results.append((score, severity, len(adjustments)))

        # All calls should be identical
        assert results[0] == results[1] == results[2]
