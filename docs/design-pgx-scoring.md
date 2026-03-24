# Patient Pharmacogenomics Scoring Design

**Phase 5.4 Design Document**
**Status**: Design Phase
**Target Release**: v0.4.0 (Q4 2026)

---

## Executive Summary

Design for personalized drug interaction risk scoring based on patient genetic profile. Integrates CPIC pharmacogenomics guidelines to adjust interaction severity scores based on metabolizer phenotypes (CYP2D6, CYP2C19, CYP2C9, DPYD, TPMT, etc.). Enables precision medicine risk stratification.

---

## Problem Statement

**Current State**:
- `seed_cpic_guidelines.py` + `seed_pharmacogenomics.py`: Static CPIC data loaded into DB
- `GeneticGuideline` model: stores recommendations + severity_multiplier per drug-gene-phenotype
- No patient-level input; no risk score adjustment based on genotype

**Gaps**:
1. No API to accept patient genetic data
2. No personalized risk scoring logic
3. No phenotype inference from genotype
4. Privacy considerations not addressed (genetic data handling)
5. No audit trail for genetic data access

---

## Proposed Architecture

### High-Level Flow

```
┌─ Patient Genetic Profile Input ───┐
│ ├─ Gene: CYP2D6, CYP2C19, etc.    │
│ ├─ Phenotype: "poor", "normal",   │
│ │   "ultrarapid", "intermediate"  │
│ └─ Optional ancestry info         │
│                                    │
├─ CPIC Guideline Lookup            │
│ ├─ Match drug × gene × phenotype  │
│ ├─ Retrieve: recommendation +     │
│ │   severity_multiplier           │
│ └─ Handle missing guidelines      │
│   (population frequencies)         │
│                                    │
├─ Risk Score Modulation            │
│ ├─ Base interaction score         │
│ ├─ × CPIC severity_multiplier     │
│ ├─ Account for phenotype-specific │
│ │   effect (e.g., poor met →      │
│ │   higher levels)                │
│ └─ Update severity tier           │
│                                    │
├─ Phenotype Prediction (Optional)  │
│ ├─ If allele data provided        │
│ ├─ Call allele → phenotype mapper │
│ └─ Infer phenotype categories     │
│                                    │
├─ Report Generation                │
│ ├─ Personalized recommendations   │
│ ├─ Confidence based on phenotype  │
│ └─ Actionable dosing guidance     │
│                                    │
└─ Privacy & Audit                  │
    ├─ Encrypt genetic data at rest │
    ├─ HIPAA-compliant storage      │
    ├─ Audit log: who accessed when │
    └─ Auto-delete after 30 days    │
```

---

## Data Model

### Patient Genetic Profile

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime, timezone

class GeneticMarker(BaseModel):
    """Single genetic marker (gene allele pair)."""
    gene_id: str  # e.g., "CYP2D6", "CYP2C19", "HLA-B"
    allele_1: str  # e.g., "*1", "*4", "*2A"
    allele_2: str  # e.g., "*1", "*4", "*2A"

    @property
    def predicted_phenotype(self) -> str:
        """Infer phenotype from alleles using lookup table."""
        return ALLELE_PHENOTYPE_MAP.get(
            (self.gene_id, tuple(sorted([self.allele_1, self.allele_2]))),
            "unknown"
        )

class PatientGeneticProfile(BaseModel):
    """Complete genetic profile for a patient."""
    patient_id: str  # FHIR Patient.id (not PHI stored; hashed)
    markers: list[GeneticMarker]
    ancestry: Optional[Literal[
        "european", "east_asian", "african",
        "south_asian", "hispanic", "middle_eastern"
    ]] = None
    test_date: Optional[datetime] = None
    test_provider: Optional[str] = None  # e.g., "Myriad", "GeneSight"

class PhenotypePrediction(BaseModel):
    """Predicted metabolizer status."""
    gene_id: str
    phenotype: str  # "poor", "intermediate", "normal", "ultrarapid"
    confidence: float  # 0.0–1.0 based on allele interpretation
    recommendation: str  # Clinical recommendation text
```

### PGx-Adjusted Interaction

```python
class PGxAdjustedInteraction(BaseModel):
    """
    Drug-drug interaction adjusted for patient pharmacogenomics.
    """
    interaction_id: str  # Base interaction ID
    drug_a_id: str
    drug_b_id: str
    drug_a_name: str
    drug_b_name: str

    # Base scores (unadjusted)
    base_severity: str  # "critical" | "major" | "moderate" | "minor"
    base_risk_score: float  # 0–100

    # PGx adjustments
    pgx_adjustments: list[dict] = Field(
        default_factory=list,
        description=[
            {
                "gene": "CYP3A4",
                "phenotype": "poor_metabolizer",
                "severity_multiplier": 2.0,
                "reason": "Simvastatin levels 2x higher in PM"
            }
        ]
    )

    # Adjusted scores
    adjusted_severity: str
    adjusted_risk_score: float

    # Clinical guidance
    recommendations: list[str]
    dosing_guidance: Optional[str] = None
    monitoring_needed: Optional[str] = None

    # Confidence
    pgx_confidence: float  # 0.0–1.0
```

---

## API Design

### 1. Submit Genetic Profile

```http
POST /api/pgx/profile
Content-Type: application/json
Authorization: Bearer <patient_or_provider_token>

{
  "patient_id": "pt_12345_hash",  # Hashed for privacy
  "markers": [
    {
      "gene_id": "CYP2D6",
      "allele_1": "*1",
      "allele_2": "*4"  # *4 = non-functional
    },
    {
      "gene_id": "CYP2C19",
      "allele_1": "*2",
      "allele_2": "*3"  # Both dysfunctional → poor metabolizer
    }
  ],
  "ancestry": "east_asian",
  "test_provider": "GeneSight"
}

Response: 201 Created
{
  "profile_id": "pgx_profile_20260324_abc123",
  "patient_id": "pt_12345_hash",
  "predicted_phenotypes": [
    {
      "gene_id": "CYP2D6",
      "phenotype": "poor_metabolizer",
      "confidence": 0.98
    },
    {
      "gene_id": "CYP2C19",
      "phenotype": "poor_metabolizer",
      "confidence": 0.99
    }
  ],
  "stored_at": "2026-03-24T17:45:00Z",
  "expires_at": "2026-04-24T17:45:00Z"
}
```

### 2. Check Interaction with PGx Adjustment

```http
POST /api/check-with-pgx
Content-Type: application/json
Authorization: Bearer <patient_or_provider_token>

{
  "drugs": ["Simvastatin", "Ketoconazole", "Paroxetine"],
  "pgx_profile_id": "pgx_profile_20260324_abc123"
}

Response: 200 OK
{
  "drugs": [
    { "id": "DB00641", "name": "Simvastatin", ... },
    { "id": "DB01026", "name": "Ketoconazole", ... },
    { "id": "DB00715", "name": "Paroxetine", ... }
  ],
  "interactions": [
    {
      "interaction_id": "INT_SIM_KETO_001",
      "drug_a_name": "Ketoconazole",
      "drug_b_name": "Simvastatin",
      "base_severity": "critical",
      "base_risk_score": 95,
      "adjusted_severity": "critical",  # No change (not CYP2D6/CYP2C19)
      "adjusted_risk_score": 95,
      "pgx_adjustments": [],
      "recommendations": [
        "Avoid Simvastatin + Ketoconazole combination",
        "Use pravastatin or rosuvastatin instead"
      ]
    },
    {
      "interaction_id": "INT_SSRI_PAROX_001",
      "drug_a_name": "Paroxetine",
      "drug_b_name": "Simvastatin",
      "base_severity": "moderate",
      "base_risk_score": 45,
      "pgx_adjustments": [
        {
          "gene": "CYP2D6",
          "phenotype": "poor_metabolizer",
          "severity_multiplier": 1.5,
          "reason": "Patient is CYP2D6 PM; Paroxetine levels higher"
        }
      ],
      "adjusted_severity": "major",
      "adjusted_risk_score": 67,  # 45 * 1.5
      "recommendations": [
        "CYP2D6 PM: Monitor for paroxetine toxicity",
        "Consider dose reduction to 50%",
        "Monitor for serotonin syndrome with Simvastatin"
      ],
      "monitoring_needed": "EKG baseline + QTc; monitor for tremor, agitation"
    }
  ],
  "overall_risk": "critical",
  "overall_score": 95,
  "pgx_summary": {
    "genes_tested": ["CYP2D6", "CYP2C19"],
    "actionable_findings": 2,
    "confidence": 0.98
  },
  "disclaimer": "DISCLAIMER: ..."
}
```

### 3. View/Update Genetic Profile

```http
GET /api/pgx/profile/{profile_id}
Authorization: Bearer <patient_or_provider_token>

Response: 200 OK
{
  "profile_id": "pgx_profile_20260324_abc123",
  "predicted_phenotypes": [...],
  "created_at": "2026-03-24T17:45:00Z",
  "expires_at": "2026-04-24T17:45:00Z",
  "last_used": "2026-03-24T18:00:00Z"
}
```

### 4. Delete Genetic Profile (GDPR/Privacy)

```http
DELETE /api/pgx/profile/{profile_id}
Authorization: Bearer <patient_or_provider_token>

Response: 204 No Content
```

---

## Implementation Details

### 1. Phenotype Prediction Engine

**File**: `medgraph/pgx/phenotype_predictor.py`

```python
# Allele-to-phenotype mappings (simplified)
ALLELE_PHENOTYPE_MAP = {
    ("CYP2D6", ("*1", "*1")): "normal_metabolizer",
    ("CYP2D6", ("*1", "*4")): "intermediate_metabolizer",
    ("CYP2D6", ("*4", "*4")): "poor_metabolizer",
    ("CYP2D6", ("*1", "*2")): "intermediate_metabolizer",
    ("CYP2D6", ("*1", "*41")): "intermediate_metabolizer",
    # ... extensive mapping based on CPIC
    ("CYP2C19", ("*1", "*1")): "normal_metabolizer",
    ("CYP2C19", ("*2", "*2")): "poor_metabolizer",
    ("CYP2C19", ("*1", "*2")): "intermediate_metabolizer",
    # ... etc
}

class PhenotypePredictionEngine:
    def __init__(self, store: GraphStore):
        self.store = store
        self.allele_map = ALLELE_PHENOTYPE_MAP

    def predict_phenotypes(
        self,
        markers: list[GeneticMarker]
    ) -> list[PhenotypePrediction]:
        """Predict metabolizer status from allele pairs."""
        predictions = []
        for marker in markers:
            key = (marker.gene_id, tuple(sorted([marker.allele_1, marker.allele_2])))
            phenotype = self.allele_map.get(key, "unknown")
            confidence = 0.95 if phenotype != "unknown" else 0.0

            predictions.append(PhenotypePrediction(
                gene_id=marker.gene_id,
                phenotype=phenotype,
                confidence=confidence,
                recommendation=self._get_recommendation(marker.gene_id, phenotype)
            ))
        return predictions

    def _get_recommendation(self, gene_id: str, phenotype: str) -> str:
        """Generic recommendation."""
        if phenotype == "poor_metabolizer":
            return f"{gene_id} poor metabolizer: may accumulate drugs slowly metabolized by this enzyme"
        elif phenotype == "ultrarapid_metabolizer":
            return f"{gene_id} ultrarapid metabolizer: may have reduced drug efficacy"
        return f"{gene_id} {phenotype}: standard dosing expected"
```

### 2. PGx Risk Score Adjustment

**File**: `medgraph/pgx/risk_modulator.py`

```python
class PGxRiskModulator:
    def __init__(self, store: GraphStore):
        self.store = store
        self.cpic_guidelines = self._load_cpic_guidelines()

    def adjust_interaction_risk(
        self,
        interaction: Interaction,
        phenotypes: list[PhenotypePrediction]
    ) -> PGxAdjustedInteraction:
        """
        Adjust base interaction risk based on patient phenotypes.
        """
        adjusted = PGxAdjustedInteraction(
            interaction_id=interaction.id,
            drug_a_id=interaction.drug_a_id,
            drug_b_id=interaction.drug_b_id,
            drug_a_name=self.store.get_drug(interaction.drug_a_id).name,
            drug_b_name=self.store.get_drug(interaction.drug_b_id).name,
            base_severity=interaction.severity,
            base_risk_score=self._compute_risk_score(interaction.severity),
            adjusted_severity=interaction.severity,
            adjusted_risk_score=self._compute_risk_score(interaction.severity),
        )

        total_multiplier = 1.0
        adjustments = []

        # Check each drug against each patient phenotype
        for drug_id, drug_name in [
            (interaction.drug_a_id, adjusted.drug_a_name),
            (interaction.drug_b_id, adjusted.drug_b_name)
        ]:
            for phenotype in phenotypes:
                # Lookup CPIC guideline
                guideline = self._find_guideline(drug_id, phenotype.gene_id, phenotype.phenotype)
                if guideline:
                    total_multiplier *= guideline.severity_multiplier
                    adjustments.append({
                        "drug": drug_name,
                        "gene": phenotype.gene_id,
                        "phenotype": phenotype.phenotype,
                        "severity_multiplier": guideline.severity_multiplier,
                        "reason": guideline.recommendation
                    })

        # Update adjusted scores
        adjusted.pgx_adjustments = adjustments
        adjusted.adjusted_risk_score = min(100, adjusted.base_risk_score * total_multiplier)
        adjusted.adjusted_severity = self._score_to_severity(adjusted.adjusted_risk_score)
        adjusted.pgx_confidence = 0.98 if adjustments else 0.5

        return adjusted

    def _find_guideline(
        self,
        drug_id: str,
        gene_id: str,
        phenotype: str
    ) -> Optional[GeneticGuideline]:
        """Lookup CPIC guideline for drug-gene-phenotype."""
        # Query store
        guidelines = self.store.query_genetic_guidelines(
            drug_id=drug_id,
            gene_id=gene_id,
            phenotype=phenotype
        )
        return guidelines[0] if guidelines else None

    def _compute_risk_score(self, severity: str) -> float:
        """Convert severity string to 0–100 score."""
        severity_to_score = {
            "critical": 90,
            "major": 70,
            "moderate": 50,
            "minor": 25
        }
        return severity_to_score.get(severity, 0)

    def _score_to_severity(self, score: float) -> str:
        """Convert 0–100 score back to severity tier."""
        if score >= 80:
            return "critical"
        elif score >= 60:
            return "major"
        elif score >= 40:
            return "moderate"
        else:
            return "minor"
```

### 3. FastAPI Integration

**File**: `medgraph/api/pgx_routes.py`

```python
from fastapi import APIRouter, Depends, HTTPException, Header
from medgraph.pgx.phenotype_predictor import PhenotypePredictionEngine
from medgraph.pgx.risk_modulator import PGxRiskModulator

router = APIRouter(prefix="/api/pgx", tags=["pharmacogenomics"])

@router.post("/profile")
async def submit_genetic_profile(
    request: PatientGeneticProfile,
    authorization: str = Header(None)
) -> dict:
    """Accept genetic profile; return phenotype predictions."""
    # Verify patient authentication (provider token)
    patient_id = verify_jwt_and_extract_patient_id(authorization)

    # Encrypt patient_id for storage
    encrypted_pid = encrypt_aes_256(patient_id, settings.ENCRYPTION_KEY)

    # Predict phenotypes
    engine = PhenotypePredictionEngine(get_store())
    phenotypes = engine.predict_phenotypes(request.markers)

    # Store in database with encryption
    profile_id = store_genetic_profile(encrypted_pid, phenotypes, request)

    # Log access for audit trail
    audit_log(patient_id, "genetic_profile_submitted", profile_id)

    return {
        "profile_id": profile_id,
        "predicted_phenotypes": phenotypes,
        "expires_at": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    }

@router.post("/check-with-pgx")
async def check_interactions_with_pgx(
    request: PGxCheckRequest,
    authorization: str = Header(None)
) -> dict:
    """Analyze drug interactions adjusted for patient PGx."""
    patient_id = verify_jwt_and_extract_patient_id(authorization)

    # Retrieve genetic profile (must exist)
    profile = store.get_genetic_profile(request.pgx_profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Verify ownership (patient can only access own profile)
    if profile.patient_id_hash != hash_patient_id(patient_id):
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Decrypt phenotypes (minimal time in memory)
    phenotypes = decrypt_and_load_phenotypes(profile)

    # Analyze interactions (existing logic)
    analyzer = CascadeAnalyzer(get_store())
    base_report = analyzer.analyze(request.drugs)

    # Adjust each interaction for PGx
    modulator = PGxRiskModulator(get_store())
    pgx_interactions = []
    for interaction_result in base_report.interactions:
        adjusted = modulator.adjust_interaction_risk(
            interaction_result.direct_interaction,
            phenotypes
        )
        pgx_interactions.append(adjusted)

    # Clear sensitive data from memory
    del phenotypes

    # Log access
    audit_log(patient_id, "check_with_pgx", request.pgx_profile_id)

    return {
        "drugs": base_report.drugs,
        "interactions": pgx_interactions,
        "overall_risk": base_report.overall_risk,
        "overall_score": base_report.overall_score,
        "pgx_summary": {
            "genes_tested": [p.gene_id for p in phenotypes],
            "actionable_findings": len([i for i in pgx_interactions if i.pgx_adjustments]),
            "confidence": 0.98
        },
        "disclaimer": MEDICAL_DISCLAIMER
    }

@router.delete("/profile/{profile_id}")
async def delete_genetic_profile(
    profile_id: str,
    authorization: str = Header(None)
) -> dict:
    """Delete patient's genetic profile (GDPR right to erasure)."""
    patient_id = verify_jwt_and_extract_patient_id(authorization)

    profile = store.get_genetic_profile(profile_id)
    if not profile or profile.patient_id_hash != hash_patient_id(patient_id):
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Securely delete from database
    store.delete_genetic_profile(profile_id)

    # Audit log
    audit_log(patient_id, "profile_deleted", profile_id)

    return {"status": "deleted"}
```

---

## Privacy & Security Considerations

### Data Handling

**Golden Rules**:
1. **Encrypt at rest**: AES-256 encryption for genetic markers
2. **Minimize retention**: Auto-delete after 30 days (configurable)
3. **Access logs**: Audit trail for HIPAA compliance
4. **Patient consent**: Explicit opt-in for PGx features

### Implementation

```python
import nacl.secret
import nacl.utils
from datetime import datetime, timedelta, timezone

class GeneticDataVault:
    """Securely store + manage genetic data."""

    def __init__(self, encryption_key: bytes):
        self.secret_box = nacl.secret.SecretBox(encryption_key)

    def encrypt_markers(self, markers: list[GeneticMarker]) -> str:
        """Encrypt genetic markers."""
        plaintext = json.dumps([m.model_dump() for m in markers]).encode()
        ciphertext = self.secret_box.encrypt(plaintext)
        return ciphertext.hex()

    def decrypt_markers(self, ciphertext_hex: str) -> list[GeneticMarker]:
        """Decrypt + deserialize markers."""
        ciphertext = bytes.fromhex(ciphertext_hex)
        plaintext = self.secret_box.decrypt(ciphertext).decode()
        data = json.loads(plaintext)
        return [GeneticMarker(**m) for m in data]

class GeneticProfileStore:
    """Database store with auto-expiration."""

    def store_profile(
        self,
        patient_id_hash: str,
        markers: list[GeneticMarker],
        ttl_days: int = 30
    ) -> str:
        """Store encrypted profile with TTL."""
        vault = GeneticDataVault(settings.ENCRYPTION_KEY)
        encrypted_markers = vault.encrypt_markers(markers)

        expires_at = datetime.now(timezone.utc) + timedelta(days=ttl_days)
        profile_id = f"pgx_{uuid4().hex[:16]}"

        self.conn.execute("""
            INSERT INTO genetic_profiles
            (id, patient_id_hash, encrypted_markers, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (profile_id, patient_id_hash, encrypted_markers, expires_at.isoformat(), datetime.now(timezone.utc).isoformat()))

        return profile_id

    def cleanup_expired_profiles(self):
        """Delete expired profiles (called daily via cron)."""
        self.conn.execute("""
            DELETE FROM genetic_profiles
            WHERE expires_at < datetime('now', 'utc')
        """)
        logger.info(f"Deleted {self.conn.total_changes} expired genetic profiles")
```

### Audit Logging

```python
class AuditLog:
    """HIPAA-compliant access logging."""

    def log_access(
        self,
        patient_id_hash: str,
        action: str,
        profile_id: str,
        ip_address: str,
        user_agent: str
    ):
        """Log genetic data access."""
        self.conn.execute("""
            INSERT INTO genetic_audit_log
            (patient_id_hash, action, profile_id, ip_address, user_agent, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (patient_id_hash, action, profile_id, ip_address, user_agent, datetime.now(timezone.utc).isoformat()))
```

---

## Estimated Effort

| Component | Effort | Notes |
|-----------|--------|-------|
| Data models (GeneticProfile, PhenotypePrediction) | 4h | Pydantic schema design |
| Phenotype predictor (allele → phenotype) | 6h | CPIC allele mapping; confidence scoring |
| Risk modulator (interaction adjustment) | 6h | Severity multiplier logic; score recomputation |
| API endpoints (submit, check, delete) | 6h | FastAPI routes; token verification |
| Privacy/encryption (AES-256, audit log) | 8h | Encryption setup; TTL management; audit table |
| Tests (unit + integration + HIPAA) | 8h | Mock genetic data; privacy compliance tests |
| Documentation | 3h | Architecture; privacy policy; consent form |
| **Total** | **41h** | ~5 days dev + 1.5 days review |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Genetic data breach | Critical | AES-256 encryption; minimal retention (30 days); audit logs |
| Phenotype misclassification | Medium | Use standard CPIC allele interpretations; flag "unknown" phenotypes |
| False negatives (missed recommendations) | High | Validate phenotype map against CPIC docs; quarterly review |
| Patient re-identification (privacy) | High | Hash patient_id; store separately from markers; never log plaintext ID |
| Liability (medical decision harm) | Critical | Prominent disclaimer; recommendations are guidance, not medical advice; track non-adherence |
| Regulatory non-compliance (HIPAA/GDPR) | Critical | Legal review; BAA with clinics; privacy impact assessment |

---

## Testing Strategy

### Functional Tests
- Allele → phenotype conversion accuracy (vs CPIC reference)
- Risk score adjustment correctness (multiplier application)
- PGx-adjusted interaction ranking

### Privacy Tests
- Encryption/decryption round-trip
- Audit log completeness
- TTL-based auto-deletion

### Compliance Tests
- HIPAA audit trail requirements
- GDPR right-to-erasure (DELETE works)
- Token-based authorization

### Gold Standard Validation
- Pharmacist review of 50 PGx-adjusted recommendations
- Compare to known CPIC guideline outcomes

---

## Future Work (v0.5.0+)

1. **Allele Genotyping API**: Integrate with external labs (Myriad, GeneSight)
2. **Ancestry-Based Scoring**: Weight phenotype frequencies by self-reported ancestry
3. **Gene-Gene Interactions**: Model CYP2D6 + CYP2C19 epistasis effects
4. **Advanced Phenotyping**: Support copy number variation (CYP2D6 duplications/deletions)
5. **Longitudinal Tracking**: Store phenotype test history; detect phenotype changes

---

## References

- CPIC Guidelines: https://cpicpgx.org/guidelines/
- CPIC Allele Definitions: https://cpicpgx.org/genes/
- HIPAA Genetic Privacy: https://www.hhs.gov/hipaa/for-professionals/faq/354/does-hipaa-protect-genetic-information/
- GDPR Article 4 (Genetic Data): https://gdpr-info.eu/issues/genetic-data/
- Advancing Clinical Pharmacogenomics (2025): https://ascpt.onlinelibrary.wiley.com/doi/10.1002/cpt.70005
- Clinical Pharmacogenetics Implementation Consortium: https://cpicpgx.org/
