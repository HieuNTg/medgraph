# PGx Genetic Data Privacy Framework

**Security Design Document**
**Status**: Design Phase
**Author**: Security Lead (Đức)
**Target**: Q3–Q4 2026
**Related**: `docs/design-pgx-scoring.md`, `medgraph/engine/pgx_scorer.py`

---

## Executive Summary

MEDGRAPH's PGx scoring feature (go-live Q4 2026) requires patients to submit metabolizer phenotypes (CYP2D6, CYP2C19, etc.) to personalize drug interaction risk scores. Genetic phenotypes are GDPR Article 9 "special category" data and GINA-protected health information — a breach carries disproportionate harm (genetic discrimination, insurance denial) compared to other PHI categories. This document defines the consent flow, storage architecture, access controls, deletion requirements, and API security standards required before any genetic data can be accepted in production.

---

## Threat Model

### What Data Is Collected

- **Metabolizer phenotypes** only: `poor_metabolizer`, `intermediate_metabolizer`, `normal_metabolizer`, `rapid_metabolizer`, `ultrarapid_metabolizer` per gene (CYP2D6, CYP2C19, CYP2C9, CYP3A4, DPYD, TPMT, UGT1A1, HLA-B)
- **NOT raw DNA** — no nucleotide sequences, no VCF files, no SNP arrays
- Optionally: allele pairs (e.g., `*1/*4`) submitted for phenotype prediction via `predict_phenotype_from_alleles()`
- Optionally: self-reported ancestry (affects population frequency lookup)
- `patient_id` (hashed, never plaintext), timestamp of submission, provider name

### Threat Actors

| Actor | Vector | Motivation |
|-------|--------|-----------|
| External attacker | SQL injection, API auth bypass, misconfigured S3/storage | Data theft for sale, ransomware |
| Insider threat (employee/contractor) | Direct DB access, log scraping, bulk export | Curiosity, financial gain |
| Compromised provider token | JWT theft via XSS or phishing | Pivot to patient genetic data |
| Third-party library | Dependency compromise (supply chain) | Silent exfiltration |
| Legal compulsion | Subpoena, government request | Law enforcement access to genetic data |

### Impact of Breach

- **Genetic discrimination**: insurers, employers can infer heritable conditions from metabolizer status (GINA violation)
- **Irreversibility**: unlike passwords, genetic data cannot be "changed" after exposure
- **Family exposure**: phenotypes reveal partial heritable information about biological relatives
- **Re-identification risk**: phenotype + ancestry + drug list may be re-identifiable even without name/DOB
- **Regulatory**: GDPR Art. 83 fines up to €20M or 4% global revenue; HIPAA penalties up to $1.9M/year per violation category

---

## Data Classification

### Sensitivity Tier: CRITICAL

Genetic phenotype data is classified at MEDGRAPH's highest sensitivity tier — above standard PII.

| Property | Value |
|----------|-------|
| Data type | Genetic phenotype (metabolizer status) |
| GDPR classification | Article 9 — Special Category (genetic data) |
| GINA classification | Genetic information — protected from discrimination |
| HIPAA classification | PHI if linked to patient identity in covered entity context |
| Retention sensitivity | High — cannot be "reset" if exposed |
| Scope of harm | Individual + biological relatives |

### What Is vs. Is Not Genetic Data Under GDPR Art. 4(13)

- **IS genetic data**: phenotype strings tied to a patient ID, allele pairs, ancestry linked to a patient
- **IS NOT** (aggregate/de-identified): population-level phenotype frequencies used in scoring without patient linkage; CPIC guidelines in `genetic_guidelines` table (reference data, not patient data)

The `GeneticGuideline` records already in the DB (from `seed_pharmacogenomics.py`) are **reference data** — no privacy controls needed. Only **patient-submitted profiles** require the controls in this document.

---

## Architecture Requirements

### Consent Flow

**Requirement**: No genetic data may be accepted via any API endpoint before explicit, informed, recorded consent.

#### Consent Collection

1. **Opt-in trigger**: User initiates PGx profile creation in frontend
2. **Consent modal** (mandatory, not pre-checked):
   - What is collected: metabolizer phenotypes for listed genes
   - Why: personalize drug interaction risk scores
   - Storage: encrypted, 90-day default retention, deletable on demand
   - Sharing: not shared with third parties; not used for research without separate consent
   - Legal basis: GDPR Art. 9(2)(a) — explicit consent
3. **Consent record stored** before any data accepted:
   ```
   consent_id, patient_id_hash, consent_version, timestamp_utc,
   ip_address_hash, user_agent_hash, consent_text_sha256
   ```
4. **Withdrawal**: account settings page → "Delete my genetic data" → triggers hard delete cascade (see Deletion section)
5. **Consent versioning**: if consent text changes (new data uses, retention change), existing users must re-consent before next PGx API call; version mismatch → 403 with `consent_required` error code

#### Consent Version Table

```sql
CREATE TABLE pgx_consent_versions (
    version     TEXT PRIMARY KEY,  -- e.g. "v1.0", "v1.1"
    text_sha256 TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE pgx_patient_consent (
    id               TEXT PRIMARY KEY,
    patient_id_hash  TEXT NOT NULL,
    consent_version  TEXT NOT NULL REFERENCES pgx_consent_versions(version),
    timestamp_utc    TEXT NOT NULL,
    ip_address_hash  TEXT NOT NULL,  -- SHA-256 of IP, not raw IP
    user_agent_hash  TEXT NOT NULL,
    withdrawn_at     TEXT,           -- NULL = active
    UNIQUE(patient_id_hash, consent_version)
);
```

---

### Data Storage

#### Schema

Genetic profiles stored in a **separate table**, never joined into main drug/interaction queries.

```sql
CREATE TABLE pgx_genetic_profiles (
    id               TEXT PRIMARY KEY,          -- e.g. "pgx_abc123def456"
    patient_id_hash  TEXT NOT NULL,             -- SHA-256(patient_id + HASH_SALT)
    consent_id       TEXT NOT NULL REFERENCES pgx_patient_consent(id),
    encrypted_data   BLOB NOT NULL,             -- AES-256-GCM ciphertext
    data_key_id      TEXT NOT NULL,             -- Key rotation reference
    created_at       TEXT NOT NULL,
    expires_at       TEXT NOT NULL,             -- Default: created_at + 90 days
    last_accessed_at TEXT,
    INDEX(patient_id_hash),
    INDEX(expires_at)
);

-- Separate table for derived phenotype results (lower sensitivity — no raw alleles)
CREATE TABLE pgx_phenotype_cache (
    id              TEXT PRIMARY KEY,
    profile_id      TEXT NOT NULL REFERENCES pgx_genetic_profiles(id) ON DELETE CASCADE,
    gene_id         TEXT NOT NULL,
    phenotype       TEXT NOT NULL,
    confidence      REAL NOT NULL,
    created_at      TEXT NOT NULL
);
```

#### Encryption

- **Algorithm**: AES-256-GCM (authenticated encryption — detects tampering)
- **Key management**: encryption key stored in env var `PGX_ENCRYPTION_KEY` (32 bytes, base64); never in source code or DB
- **Key rotation**: `data_key_id` field allows tracking which key version encrypted each record; rotation process re-encrypts rows in batches
- **In-memory**: decrypt phenotypes only for the duration of a scoring request; call `del phenotypes` and clear references immediately after use
- **No column-level DB encryption dependency**: application-layer encryption so SQLite → PostgreSQL migration does not lose protection

```python
# medgraph/security/genetic_vault.py
import os, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from base64 import b64decode, b64encode

class GeneticVault:
    """AES-256-GCM encryption for genetic profile data."""

    def __init__(self) -> None:
        raw_key = b64decode(os.environ["PGX_ENCRYPTION_KEY"])
        if len(raw_key) != 32:
            raise ValueError("PGX_ENCRYPTION_KEY must be 32 bytes (256-bit)")
        self._aesgcm = AESGCM(raw_key)

    def encrypt(self, plaintext_dict: dict) -> tuple[bytes, bytes]:
        """Returns (nonce, ciphertext). Store both."""
        nonce = os.urandom(12)  # 96-bit nonce for GCM
        plaintext = json.dumps(plaintext_dict, separators=(",", ":")).encode()
        ciphertext = self._aesgcm.encrypt(nonce, plaintext, None)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> dict:
        plaintext = self._aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(plaintext.decode())
```

#### Logging Rules

- **NEVER** log phenotype values, allele strings, or patient_id in plaintext
- **NEVER** include genetic data in exception messages (wrap before raising)
- Log only: `profile_id`, `action`, `timestamp`, `patient_id_hash` (already hashed)
- Audit log is separate from application log (different file/destination)
- Log level for genetic access events: always `INFO`; never suppressed by log level config

---

### Data Access Control

#### Roles

| Role | Can Read Genetic Profiles | Can Write | Can Delete | Notes |
|------|--------------------------|-----------|-----------|-------|
| `pgx_service` | Yes — own patient only | Yes | Yes — own only | FastAPI dependency injection |
| `admin` | No direct access | No | Via compliance workflow only | Use break-glass procedure |
| `analytics` | No | No | No | Aggregate stats only, no row-level |
| `drug_check_service` | No | No | No | Receives adjusted scores, not phenotypes |

The `PGxScorer` class (`medgraph/engine/pgx_scorer.py`) is already stateless — it accepts phenotypes per-call and stores nothing. This is the correct pattern. Phenotypes must be decrypted, passed to `PGxScorer.adjust_interaction_score()`, then cleared from memory.

#### Ownership Enforcement

Every genetic data API call must verify `patient_id_hash` ownership:

```python
# medgraph/api/pgx_routes.py
def _assert_profile_ownership(profile: GeneticProfile, jwt_patient_id: str) -> None:
    expected_hash = hash_patient_id(jwt_patient_id)  # SHA-256(id + HASH_SALT)
    if not hmac.compare_digest(profile.patient_id_hash, expected_hash):
        raise HTTPException(status_code=403, detail="Forbidden")
```

Use `hmac.compare_digest` (constant-time comparison) — not `==` — to prevent timing attacks.

#### API Scope

All `/api/pgx/*` endpoints require JWT with explicit `genetic_data` scope:

```python
# In JWT payload
{"sub": "patient_12345", "scopes": ["drug_check", "genetic_data"], "exp": ...}
```

Drug check endpoints (`/api/check`, `/api/interactions`) do NOT receive or return genetic data — they receive a `pgx_profile_id` reference and the scoring layer resolves it internally, returning only the adjusted score. Raw phenotypes never leave the PGx service boundary.

#### Audit Trail

```sql
CREATE TABLE pgx_audit_log (
    id               TEXT PRIMARY KEY,
    patient_id_hash  TEXT NOT NULL,
    action           TEXT NOT NULL,   -- "profile_created", "profile_read", "check_with_pgx", "profile_deleted", "consent_withdrawn"
    profile_id       TEXT,
    request_id       TEXT,            -- correlation with application log
    ip_address_hash  TEXT NOT NULL,
    user_agent_hash  TEXT NOT NULL,
    timestamp_utc    TEXT NOT NULL,
    INDEX(patient_id_hash),
    INDEX(timestamp_utc)
);
```

- Audit log is **append-only** — no UPDATE or DELETE on this table
- Retained minimum 7 years (HIPAA audit trail requirement)
- Separate from `pgx_genetic_profiles` TTL — audit log outlives the data it describes
- Export for compliance review: admin CLI only, not via API

---

### Data Retention and Deletion

#### Retention Modes

| Mode | Behavior | Who Controls |
|------|----------|-------------|
| Process-and-discard (default) | Phenotypes computed in-memory, never written to DB | System default |
| Session storage | Stored for duration of session (max 24h), auto-deleted | User opt-in per session |
| Persistent storage | Stored with configurable TTL (default 90 days, max 365 days) | User explicit opt-in |

Default is process-and-discard. Persistent storage requires a second opt-in confirmation beyond the base consent.

#### TTL Enforcement

```python
# medgraph/tasks/pgx_cleanup.py — runs daily via APScheduler or cron
def purge_expired_pgx_profiles(store: GraphStore) -> int:
    """Hard-delete profiles past expires_at. Returns count deleted."""
    deleted = store.execute("""
        DELETE FROM pgx_genetic_profiles
        WHERE expires_at < datetime('now')
    """)
    # CASCADE deletes pgx_phenotype_cache rows automatically
    audit_system_action("purge_expired_profiles", count=deleted.rowcount)
    return deleted.rowcount
```

Schedule: daily at 03:00 UTC (1 hour after FAERS refresh, avoid contention).

#### Right to Erasure (GDPR Art. 17)

Hard delete — not soft delete (`deleted_at` flag is insufficient for genetic data).

```python
# DELETE /api/pgx/profile/{profile_id}
async def delete_genetic_profile(profile_id: str, current_user: JWTUser):
    profile = store.get_pgx_profile(profile_id)
    _assert_profile_ownership(profile, current_user.patient_id)

    # 1. Delete encrypted data + cascade phenotype cache
    store.execute("DELETE FROM pgx_genetic_profiles WHERE id = ?", [profile_id])

    # 2. Record consent withdrawal
    store.execute("""
        UPDATE pgx_patient_consent SET withdrawn_at = datetime('now')
        WHERE patient_id_hash = ? AND withdrawn_at IS NULL
    """, [hash_patient_id(current_user.patient_id)])

    # 3. Audit log (audit record persists — legally required)
    audit_log(current_user.patient_id, "profile_deleted", profile_id, request)

    return Response(status_code=204)
```

Response time SLA: deletion must complete within 30 days of request (GDPR Art. 12(3)). Immediate deletion is the implementation target.

#### What Cannot Be Deleted

- Audit log entries (legally required for HIPAA/GDPR accountability)
- Drug interaction results that used PGx scoring — stored as adjusted scores only, no phenotype data embedded

---

### API Security

#### Endpoint Group

All PGx endpoints under `/api/pgx/` with dedicated FastAPI router and middleware:

```python
# medgraph/api/pgx_routes.py
router = APIRouter(
    prefix="/api/pgx",
    tags=["pharmacogenomics"],
    dependencies=[
        Depends(require_genetic_data_scope),   # JWT scope check
        Depends(pgx_rate_limiter),             # Stricter rate limit
        Depends(no_cache_headers),             # Prevent CDN/proxy caching
    ]
)
```

#### Rate Limiting

PGx endpoints have stricter limits than general API:

| Endpoint | Limit | Rationale |
|----------|-------|-----------|
| `POST /api/pgx/profile` | 5 req/hour per user | Prevent bulk genetic profile creation |
| `POST /api/check-with-pgx` | 20 req/hour per user | Higher (diagnostic use), still limited |
| `DELETE /api/pgx/profile/*` | 10 req/hour per user | Prevent delete-flood attacks |
| General API (`/api/check`) | 60 req/minute per user | Existing limit |

#### No Caching

```python
# medgraph/api/middleware.py
class NoCachePGxMiddleware:
    """Prevent any proxy/CDN from caching genetic data responses."""
    async def __call__(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/api/pgx"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, private"
            response.headers["Pragma"] = "no-cache"
            response.headers["Surrogate-Control"] = "no-store"
        return response
```

#### Request/Response Rules

- Genetic data in **POST body only** — never in URL path or query parameters (URLs logged by proxies, load balancers, CDN)
- Response `Content-Type: application/json` with `X-Content-Type-Options: nosniff`
- `profile_id` in URL path is acceptable (opaque token, not genetic data)
- TLS 1.2 minimum; TLS 1.3 preferred; HTTP connections rejected for `/api/pgx/*`

#### Input Validation

```python
# Validate phenotype values against allowlist before processing
VALID_GENES = {"CYP2D6", "CYP2C19", "CYP2C9", "CYP3A4", "DPYD", "TPMT", "UGT1A1", "HLA-B"}
VALID_PHENOTYPES = {"poor_metabolizer", "intermediate_metabolizer", "normal_metabolizer",
                    "rapid_metabolizer", "ultrarapid_metabolizer"}

class PGxProfileRequest(BaseModel):
    phenotypes: dict[str, str]  # gene_id -> phenotype

    @model_validator(mode="after")
    def validate_phenotypes(self) -> "PGxProfileRequest":
        for gene, phenotype in self.phenotypes.items():
            if gene not in VALID_GENES:
                raise ValueError(f"Unknown gene: {gene}")
            if phenotype not in VALID_PHENOTYPES and not phenotype.startswith("HLA-B"):
                raise ValueError(f"Invalid phenotype: {phenotype}")
        if len(self.phenotypes) > 20:
            raise ValueError("Too many genes in one profile (max 20)")
        return self
```

---

## Implementation Plan

### Phase 1 — Consent UI + API Scaffolding (Q3 2026, ~3 weeks)

- [ ] `pgx_consent_versions` + `pgx_patient_consent` tables + migrations
- [ ] `POST /api/pgx/consent` — record consent
- [ ] `GET /api/pgx/consent/status` — check current consent version
- [ ] Frontend consent modal (blocks PGx profile creation if not consented)
- [ ] `require_genetic_data_scope` JWT middleware
- [ ] `NoCachePGxMiddleware` registration
- [ ] PGx rate limiter configuration

### Phase 2 — Encrypted Storage + Audit (Q3 2026, ~4 weeks)

- [ ] `pgx_genetic_profiles` + `pgx_phenotype_cache` tables + migrations
- [ ] `pgx_audit_log` table + migrations
- [ ] `GeneticVault` class (`medgraph/security/genetic_vault.py`)
- [ ] `POST /api/pgx/profile` — store encrypted profile
- [ ] `POST /api/check-with-pgx` — decrypt in-flight, call `PGxScorer`, clear from memory
- [ ] `GET /api/pgx/profile/{id}` — return phenotype metadata (not raw ciphertext)
- [ ] Audit log middleware — hook all genetic data read/write paths
- [ ] Patient-ID hashing utility (`hash_patient_id()`) with `HASH_SALT` env var
- [ ] Integration test: encrypt → store → retrieve → decrypt round-trip

### Phase 3 — Deletion + Compliance Testing (Q4 2026, ~3 weeks)

- [ ] `DELETE /api/pgx/profile/{id}` — hard delete + consent withdrawal
- [ ] `pgx_cleanup.py` daily purge task — register with APScheduler
- [ ] Break-glass admin procedure for compliance deletion (documented, CLI-only)
- [ ] Privacy Impact Assessment (PIA) — complete template in `docs/pia-pgx.md`
- [ ] Data breach notification procedure — runbook in `docs/runbooks/genetic-data-breach.md`
- [ ] GDPR Art. 9 consent mechanism review by legal/DPO
- [ ] GINA non-discrimination notice in consent modal text
- [ ] Load test: 1000 profiles stored, bulk deletion < 5 seconds
- [ ] Penetration test: genetic data endpoints (scope: auth bypass, injection, insecure direct object reference)

---

## Compliance Checklist

### GDPR (EU General Data Protection Regulation)

- [ ] Art. 9(2)(a): Explicit consent mechanism implemented and recorded
- [ ] Art. 9: Special category data processing documented in DPA register
- [ ] Art. 12–14: Privacy notice updated to include genetic data processing
- [ ] Art. 17: Right to erasure — hard delete implemented, SLA documented (30 days)
- [ ] Art. 20: Data portability — `GET /api/pgx/profile/{id}` returns exportable JSON
- [ ] Art. 25: Data minimization — phenotypes only (no raw DNA), process-and-discard default
- [ ] Art. 30: Records of processing activities (ROPA) — entry for PGx feature added
- [ ] Art. 32: Encryption at rest (AES-256-GCM) + in transit (TLS 1.3) implemented
- [ ] Art. 35: Data Protection Impact Assessment (DPIA) completed before go-live
- [ ] Art. 83: Fines awareness — breach notification procedure tested

### GINA (Genetic Information Nondiscrimination Act, US)

- [ ] Non-discrimination notice displayed in consent flow
- [ ] Genetic data not shared with health insurers, employers, or affiliated entities
- [ ] BAA (Business Associate Agreement) reviewed for GINA applicability with any sub-processors
- [ ] Staff training on GINA prohibitions for any team with DB access

### HIPAA (if applicable — covered entity or BA context)

- [ ] PHI determination: is MEDGRAPH operating as covered entity or business associate?
- [ ] Audit controls: `pgx_audit_log` satisfies 45 CFR §164.312(b)
- [ ] Minimum necessary standard: `drug_check_service` role excluded from genetic data access
- [ ] Breach notification procedure: 60-day notification window (45 CFR §164.404)
- [ ] BAA in place with any cloud storage provider holding encrypted profiles

### Data Breach Notification

- [ ] Incident response runbook created: `docs/runbooks/genetic-data-breach.md`
- [ ] Detection: alerting on anomalous bulk reads from `pgx_genetic_profiles` (> 100 rows/hour by single token)
- [ ] Containment: ability to revoke all `genetic_data`-scoped JWTs immediately
- [ ] Notification timeline: GDPR Art. 33 — supervisory authority within 72 hours; Art. 34 — data subjects without undue delay
- [ ] Post-incident: mandatory re-consent for affected patients

### Privacy Impact Assessment (PIA/DPIA)

- [ ] Document created: `docs/pia-pgx.md`
- [ ] Necessity and proportionality test: is genetic data necessary for stated purpose?
- [ ] Risk assessment: likelihood × impact for each threat actor
- [ ] DPO review completed and signed off
- [ ] Review schedule: annually or when processing purpose changes

---

## Risks and Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|-----------|-----------|
| Encryption key exposure via env var leak | Critical | Medium | Use secrets manager (AWS Secrets Manager / HashiCorp Vault) in production; rotate key on any suspected exposure |
| JWT with genetic_data scope stolen via XSS | High | Medium | Short JWT expiry (15 min); HttpOnly cookies for web; re-auth for PGx operations |
| Insider bulk export via admin DB access | Critical | Low | No SELECT on `pgx_genetic_profiles` for admin role; all access via `pgx_service` role only; audit log alert on > 10 rows/query |
| SQLite → PostgreSQL migration exposes data | High | Low | Application-layer encryption is DB-agnostic; verify encryption round-trip in migration smoke test |
| Process-and-discard default bypassed by future dev | High | Medium | Linting rule: any write to `pgx_genetic_profiles` outside `pgx_routes.py` requires security review comment |
| Legal compulsion (subpoena) | High | Low | Minimize stored data; process-and-discard default; legal hold procedure documented |
| Phenotype re-identification | Medium | Low | Phenotype alone is insufficient for re-ID; do not store alongside name/DOB in same query; separate table enforces this |

---

## References

- GDPR Article 9 — Special Category Data: https://gdpr-info.eu/art-9-gdpr/
- GDPR Article 4(13) — Definition of Genetic Data: https://gdpr-info.eu/art-4-gdpr/
- GINA (42 U.S.C. § 2000ff): https://www.eeoc.gov/statutes/genetic-information-nondiscrimination-act-2008
- HIPAA Genetic Information Rule (45 CFR §164.514(f)): https://www.hhs.gov/hipaa/for-professionals/faq/354/does-hipaa-protect-genetic-information/
- CPIC Guidelines (phenotype definitions used in pgx_scorer.py): https://cpicpgx.org/guidelines/
- NIST SP 800-111 — Storage Encryption for End User Devices: https://csrc.nist.gov/publications/detail/sp/800-111/final
- Python `cryptography` AESGCM: https://cryptography.io/en/latest/hazmat/primitives/aead/#cryptography.hazmat.primitives.ciphers.aead.AESGCM

---

*Last updated: 2026-03-26 — Đức (Security Lead)*
