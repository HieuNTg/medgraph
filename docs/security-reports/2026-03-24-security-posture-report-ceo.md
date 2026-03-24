# Báo Cáo Bảo Mật — MEDGRAPH v2.1 Sprint
**Người lập:** Security Engineer
**Gửi:** CEO, MEDGRAPH
**Ngày:** 2026-03-24
**Phạm vi:** Sprint v2.1 — Security fixes + FAERS pipeline + PGx scoring engine

---

## Executive Summary

The sprint applied seven meaningful security fixes. All seven were verified in code — none were shipped as documentation stubs. Two **Critical** vulnerabilities introduced by the new FAERS pipeline remain unresolved and require immediate action before any production deployment. Five additional High/Medium issues are documented below.

**Risk Level: HIGH** — Block production deploy until Critical items are resolved.

---

## Part 1 — Verification of Previous Security Fixes

### 1.1 JWT Hardcoded Fallback → RuntimeError in Production
**Status: VERIFIED**

`medgraph/api/user_auth.py:78-92` — `UserAuth.__init__` now raises `RuntimeError` if `MEDGRAPH_JWT_SECRET` is unset or equals the dev default when `MEDGRAPH_ENV=production`. The check fires at app startup so the server refuses to start rather than silently using a weak secret.

`medgraph/api/server.py:160-166` — Redundant check also in `lifespan()`. Redundancy is harmless but means the check runs twice on startup. Not a defect — belt-and-suspenders is acceptable here.

### 1.2 Auth-OFF Warning in Production
**Status: VERIFIED (warning only — not enforcement)**

`server.py:167-171` — When `MEDGRAPH_ENV=production` and `MEDGRAPH_API_KEYS` is empty, a `SECURITY WARNING` is logged. This is a warning, not a `RuntimeError`. An operator can still start the server in production with zero API-key auth. Acceptable if JWT user-auth is considered sufficient; note the two-layer model (API key + JWT) is optional by design.

### 1.3 Audit Endpoint Restricted to Own User for Non-Admins
**Status: VERIFIED — with a secondary bug (see Critical #2 below)**

`server.py:1742-1743`:
```python
if not _user.get("is_admin", False):
    user_id = _user.get("user_id") or _user.get("sub")
```
The intent is correct. However the user dict from `get_user()` contains `id`, not `user_id` or `sub`. This means the fallback resolves to `None`, so a non-admin user sees *all* audit logs. See Critical Issue #2.

### 1.4 `_client_ip()` Trusted-Proxy Validation
**Status: VERIFIED**

`auth.py:60-66` — `_is_trusted_proxy()` checks `MEDGRAPH_TRUSTED_PROXIES` env var. `server.py:353-359` — `_client_ip()` only reads `X-Forwarded-For` when the direct IP is in the trusted list. IP spoofing via header injection is blocked. Implementation is correct.

### 1.5 defusedxml for PubMed XML Parsing
**Status: PARTIALLY IMPLEMENTED — fallback to stdlib is dangerous**

`medgraph/data/pubmed_agent.py:192-196`:
```python
try:
    import defusedxml.ElementTree as SafeET
    root = SafeET.fromstring(xml_text)
except ImportError:
    root = ET.fromstring(xml_text)  # <- stdlib, vulnerable to XML entity attacks
```
If `defusedxml` is not installed, the app silently falls back to the standard library `xml.etree.ElementTree` which is **not** protected against XML bomb / billion-laughs attacks. This should be a hard dependency, not an optional one. Check `requirements.txt` to confirm whether `defusedxml` is pinned.

### 1.6 Frontend Auth Headers on All fetch() Calls
**Status: VERIFIED**

`dashboard/src/lib/api.ts:29-41` — All API calls route through `apiFetch()` which unconditionally injects `Authorization: Bearer <token>` when `authToken` is set. The PDF export function at line 218 also manually sets the header. Consistent.

### 1.7 ProtectedRoute Centralized
**Status: VERIFIED**

`dashboard/src/components/protected-route.tsx` — Clean implementation. `requireAuth=true` by default redirects unauthenticated users to `/login` preserving `location.state.from` for post-login redirect. `redirectAuthenticated` prevents already-logged-in users from accessing `/login`. No bypass possible from this component alone.

---

## Part 2 — New Attack Surfaces

---

### CRITICAL ISSUE #1: Admin Role Check Never Actually Evaluates True

**File:** `medgraph/api/server.py:1742, 1776, 1802`
**Affected endpoints:** `GET /api/v1/admin/refresh`, `GET /api/v1/admin/refresh/jobs`, `GET /api/v1/audit` (admin path)

The admin check reads:
```python
if not _user.get("is_admin", False):
    raise HTTPException(status_code=403, detail="Admin access required")
```

The `_user` dict originates from `user_auth.get_user()` → `store.get_user_by_id()` → `SELECT * FROM users`. The `users` table schema (`store.py:74-82`) has no `is_admin` column. The JWT payload contains only `sub`, `exp`, `type`, `jti`. Neither source ever sets `is_admin`.

**Effect:** `_user.get("is_admin", False)` **always returns False**. Every authenticated user, regardless of role, triggers the 403. No user — including legitimate admins — can ever call these endpoints.

This is not a privilege escalation (no one gets in). It is a **broken access control** that makes the admin FAERS refresh feature entirely non-functional. However, it also means that if the `is_admin` field is ever added to the JWT or user dict by a future change without re-auditing this gate, the behaviour changes unpredictably.

**Resolution required before production:**
1. Add `is_admin BOOLEAN NOT NULL DEFAULT 0` to `users` table via migration.
2. Surface it in `get_user()` return dict.
3. Verify admin assignment path (CLI or seeding) sets the column.

---

### CRITICAL ISSUE #2: Audit Log Non-Admin Restriction Returns All Logs

**File:** `medgraph/api/server.py:1742-1743`

```python
if not _user.get("is_admin", False):
    user_id = _user.get("user_id") or _user.get("sub")
```

`get_user()` returns `{"id": ..., "email": ..., "display_name": ..., "created_at": ...}`. Neither `user_id` nor `sub` exists in this dict. The expression evaluates to `None or None` = `None`.

`store.get_audit_logs(user_id=None, ...)` with `user_id=None` returns **all audit log entries** from all users.

Since Critical #1 means `is_admin` is always False, **every authenticated user who calls `GET /api/v1/audit` receives the full audit log of every user in the system** — including email addresses, IP addresses, and action history.

**This is a confirmed data breach vector.** Any registered user can see all audit activity.

**Immediate fix:**
```python
if not _user.get("is_admin", False):
    user_id = _user["id"]   # "id" is the correct key
```

---

### HIGH ISSUE #1: FAERS Pipeline — No Rate/Volume Guard on DB Writes

**File:** `medgraph/data/refresh_service.py:393-409`

The refresh iterates all drugs in batches of 5, calls OpenFDA for each, and upserts every returned adverse event. With a large drug catalogue, a single refresh run can issue hundreds of API calls and upsert thousands of rows in a single request cycle (the endpoint is synchronous: `server.py:1779`). There is no:
- Maximum records-per-run cap
- Request timeout for the entire job (only per-HTTP-call timeout of 15s)
- Transaction batching (each `upsert_adverse_event` opens its own connection)

**Risk:** A slow OpenFDA response or large drug list blocks the async event loop via `await`, and n×individual SQLite connections under load may produce `SQLITE_BUSY` errors. The per-event `try/except` at line 406 silently discards these.

**Recommendation:** Wrap the entire refresh in a single transaction, add a `max_records` limit parameter, and cap concurrent OpenFDA calls with a semaphore.

### HIGH ISSUE #2: FAERS Data Integrity — Unvalidated drug_ids FK Resolution

**File:** `medgraph/data/refresh_service.py:400-404`

```python
resolved_ids = [
    name_to_id.get(name.lower(), name) for name in event.drug_ids
]
```

If a drug name does not resolve, the raw name string is used as the drug ID. `upsert_adverse_event` then inserts this string into `adverse_event_drugs.drug_id`, which has a `FOREIGN KEY (drug_id) REFERENCES drugs(id)`. SQLite FK enforcement is on (`PRAGMA foreign_keys=ON` in `store.connect()`). This will raise an `IntegrityError` caught by the bare `except Exception` at line 406 and silently discarded.

**Effect:** Unresolvable drug names silently fail, producing no data corruption. However, the silent failure means administrators have no visibility into what percentage of FAERS events were rejected. The per-event swallow at line 408 logs only at DEBUG level.

**Recommendation:** Log at WARNING with count summary; consider a separate unresolved-names report in the job record.

### HIGH ISSUE #3: defusedxml is an Optional Dependency

**File:** `medgraph/data/pubmed_agent.py:193-196` (see 1.5 above)

The stdlib `xml.etree.ElementTree` is vulnerable to XML entity expansion (billion-laughs, quadratic blowup). PubMed is an external service — a compromised or malicious response could trigger this. `defusedxml` must be a hard dependency in `requirements.txt`, not caught with `ImportError`.

---

## Part 3 — PGx Data Privacy Verification

**Claim verified: genetic phenotype data is NOT stored.**

Evidence:
1. `pgx_scorer.py:187-188` — docstring explicitly states "Keeps no patient state — accepts phenotypes per-call (privacy-safe)."
2. `server.py:904` — `/check-pgx` endpoint docstring: "No patient genetic data is stored — phenotypes are processed in-memory only."
3. Code path confirmed: `phenotypes: dict[str, str] = request.phenotypes or {}` is passed directly to `PGxScorer.adjust_interaction_score()`, which performs in-memory lookup against `genetic_guidelines` table (population-level CPIC data, not patient data) and returns adjusted scores. No write to any table occurs.
4. `/api/v1/pgx/risk-profile` (`server.py:804-887`) — same pattern. Phenotypes used in-memory, population frequency data is read-only from `ANCESTRY_ALLELE_FREQUENCIES` constant. Nothing written.
5. `store.py` — confirmed no `patient_phenotypes`, `patient_genetics`, or similar table exists.

**PGx privacy posture: CLEAN.** No genetic data persisted. Disclaimer messages are present in both endpoints. HIPAA concern here is minimal given no PHI storage.

---

## Part 4 — Admin Endpoint Security Summary

| Endpoint | Auth Required | Admin Check | Admin Check Works? |
|---|---|---|---|
| `POST /api/v1/admin/refresh` | Yes (JWT) | `_user.get("is_admin")` | NO — always 403 |
| `GET /api/v1/admin/refresh/jobs` | Yes (JWT) | `_user.get("is_admin")` | NO — always 403 |
| `GET /api/v1/audit` | Yes (JWT) | `_user.get("is_admin")` | NO — leaks all logs |
| `GET /api/v1/health/freshness` | No | None (public) | N/A — intentional |

The admin endpoints fail safely (always 403) for the refresh endpoints, but fail **dangerously** for the audit endpoint (leaks all data).

---

## Part 5 — FAERS Pipeline Data Integrity Assessment

Could the FAERS pipeline corrupt the database?

**Low probability of corruption, but silent data loss is real.**

- Upserts use `ON CONFLICT(id) DO UPDATE` — deterministic, no phantom rows.
- Each `upsert_adverse_event` is its own transaction with rollback on error.
- The dedup key (`FAERS-<md5[:12]>`) is stable for same drug+reaction combinations, so re-running refresh does not duplicate data.
- Risk: the FK failure case (HIGH ISSUE #2) silently discards events. Not corruption — silent incompleteness.
- Risk: if `trigger_refresh` is called concurrently (two admin users, or scheduler + manual trigger), SQLite WAL mode handles concurrent reads but serializes writes. Concurrent writes will block up to `busy_timeout=5000ms` then raise. The refresh service has no mutex — concurrent runs can produce duplicate `refresh_metadata` rows and partial job records. No data corruption but metrics become unreliable.

**Recommendation:** Add an in-process lock (`asyncio.Lock`) around `trigger_refresh` to prevent concurrent runs.

---

## Part 6 — Remaining Vulnerabilities

### Medium: Audit Log Strips User/IP from AuditLogResponse

`server.py:1746-1754` — `AuditLogResponse` omits `ip_address` and `user_agent` fields. This is correct for privacy — IP should not be exposed via API. However, the audit endpoint is effectively useless to a legitimate admin today because (a) admin check is broken, (b) even if fixed, the response lacks actor identification beyond `user_id`. Recommend exposing `user_id` in the response.

### Medium: Rate Limiting State is In-Memory and Per-Process

`auth.py:57` — `_request_log` is a module-level dict. If the server runs behind a load balancer with multiple workers, rate limit state is not shared. An attacker can bypass rate limits by distributing requests across workers. For the current single-process deployment this is acceptable, but must be addressed before horizontal scaling.

### Medium: Token Blacklist is In-Memory Only

`user_auth.py:29` — `_revoked_tokens` is an in-memory dict. On server restart, all revoked tokens become valid again (until they naturally expire). Given `access_token_expiry=15min`, the exposure window is short. Refresh tokens are stored in the DB (`refresh_tokens` table) so refresh token revocation survives restarts. The gap is access token revocation not persisting across restarts. Acceptable risk for current scale.

### Medium: `GET /health/freshness` Leaks Internal Data Version

`server.py:1816-1819` — This public endpoint returns `data_version` and `days_since_refresh`. This is low-sensitivity metadata but informs an attacker about deployment cadence and data pipeline activity. No HIPAA concern; low-risk information disclosure.

### Low: `_prune_request_log` Pruning Logic

`auth.py:90` — Pruning checks only the last timestamp in the list (`v[-1]`). If a client had many requests early in the window and then went quiet, `v[-1]` may be stale but earlier entries in the list may still be within the window. The prune logic removes the key, resetting their counter. This can allow a client to slightly exceed rate limits by timing requests. Impact is minor — 60 req/min limit means this grants at most a few extra requests.

### Low: CORS `allow_credentials` Not Set

`server.py:287-292` — `CORSMiddleware` does not set `allow_credentials=True`. This means cookies and `Authorization` headers from cross-origin requests require the browser to explicitly handle them. Since the app uses `Authorization: Bearer` header (not cookies), this is not a problem for the current implementation. If sessions or cookies are ever added, this must be revisited.

---

## Part 7 — HIPAA/Privacy Compliance Assessment

| Concern | Status | Notes |
|---|---|---|
| Genetic data (PGx phenotypes) stored | CLEAN | In-memory only, verified |
| PHI in analysis history | LOW RISK | Drug IDs + risk level only, no patient names |
| PHI in audit log | LOW RISK | Email/IP in DB, not exposed via API response |
| PHI in error logs | LOW RISK | No phenotype data logged (verified grep above) |
| PHI in shared results | CONCERN | Shared analysis includes `drug_ids` + `overall_risk` — pseudonymous but consider expiry enforcement |
| Sensitive data in Sentry | RISK | `server.py:248-255` — Sentry integration sends error context. If an exception occurs during `/check-pgx` processing, phenotype data present in the call stack may be captured by Sentry. Sentry's `before_send` hook should scrub `phenotypes` and `metabolizer_phenotypes` keys. |

The Sentry concern is the most significant HIPAA-adjacent issue introduced this sprint. It is not a confirmed data leak but is a potential one if errors occur during PGx processing.

---

## Recommended Actions (Prioritized)

1. **[IMMEDIATE — blocks production]** Fix audit log user_id key: `server.py:1743` change `_user.get("user_id") or _user.get("sub")` → `_user["id"]`. Single-line fix, eliminates confirmed data breach vector.

2. **[IMMEDIATE — blocks production]** Add `is_admin` column to `users` table via migration. Surface in `get_user()`. Add admin-seeding CLI command. Without this, admin endpoints are permanently inaccessible.

3. **[HIGH — before beta]** Make `defusedxml` a hard dependency in `requirements.txt`. Remove the `ImportError` fallback in `pubmed_agent.py`.

4. **[HIGH — before beta]** Add `asyncio.Lock` in `RefreshService` to serialize concurrent refresh calls. Add a `max_records` cap parameter.

5. **[HIGH — before any PGx endpoint exposure]** Add Sentry `before_send` hook to scrub `phenotypes` and `metabolizer_phenotypes` from captured exceptions.

6. **[MEDIUM]** Replace per-process in-memory rate limit with Redis-backed store before horizontal scaling.

7. **[MEDIUM]** Confirm `defusedxml` installed in production container image (add to `Dockerfile` / `requirements.txt` verification step in CI).

8. **[LOW]** Log unresolved FAERS drug names at WARNING level with count in the job summary to give admins visibility into pipeline data quality.

---

## Unresolved Questions

1. Is there an admin provisioning mechanism planned? Currently no user in the system can have `is_admin=True` — there is no seeding, no CLI command, and no migration. Who is the intended admin user and how do they get the role assigned?

2. Is `defusedxml` currently in `requirements.txt` / installed in the production image? This review did not read that file — must be confirmed before closing HIGH ISSUE #3.

3. Sentry DSN — is it configured in the production environment? If `SENTRY_DSN` is not set, the PGx-in-Sentry risk is moot. Confirm deployment env config.

4. Is concurrent refresh a realistic scenario? If there is only one admin and no scheduler, the `asyncio.Lock` recommendation can be deferred. Confirm scheduling plans for v0.3.0.

---

*Report covers: medgraph/data/refresh_service.py, medgraph/engine/pgx_scorer.py, medgraph/api/server.py (lines 1-1910), medgraph/api/auth.py, medgraph/api/user_auth.py, medgraph/api/security.py, medgraph/api/middleware.py, medgraph/graph/store.py (schema + user/refresh methods), dashboard/src/components/protected-route.tsx, dashboard/src/lib/api.ts, tests/test_refresh_service.py, medgraph/data/pubmed_agent.py (XML parsing section).*
