# MEDGRAPH — Project Roadmap

## v2.0.0 — All 5 Phases Complete (2026-03-23)
**Status**: COMPLETE - All phases implemented and documented

All 5 planned roadmap phases have been completed:
- Phase 1: Data Expansion + Evidence Quality (2,500+ drugs, 1,500+ interactions with evidence levels)
- Phase 2: Graph-Powered Features (alternatives, pathways, contraindication networks, deprescribing)
- Phase 3: User Experience + Profiles (authentication, saved profiles, history, shareable results)
- Phase 4: Clinical Integration (FHIR R4, CDS Hooks, Smart on FHIR, enterprise adoption)
- Phase 5: Mobile + Advanced Features (PWA, offline, pill ID, voice input, polypharmacy optimizer)

---

## v0.1.0 — MVP + Phase 2-3 Hardening & Observability
**Status**: Released

**Phase 1 — Core**:
- 89 built-in drugs across major therapeutic classes
- 28 curated drug-drug interactions with severity ratings
- 8 CYP450 enzymes with metabolizer / inhibitor / inducer relationships
- Cascade path detection via NetworkX graph traversal
- Risk scoring: critical / major / moderate / minor
- FastAPI REST backend with Pydantic V2 models
- React 19 + TypeScript + Vite frontend
- Drug search with fuzzy matching
- Medical disclaimer, WCAG AA target
- Docker + docker-compose support
- GitHub Actions CI (lint, test, build)

**Phase 2 — API Hardening**:
- RFC 7807 Problem Details error format
- Request ID tracing (X-Request-ID header)
- Paginated search endpoints
- API key verification + rate limiting
- Security headers (CSP, HSTS, X-Frame-Options)
- OpenAPI metadata (tags, contact, license info)
- 17 new hardening tests

**Phase 3 — Observability & Monitoring**:
- Prometheus metrics (/metrics endpoint)
- Custom app metrics: analysis duration, graph size
- Structured JSON logging with request_id injection
- Health check split (liveness /health/live, readiness /health/ready)
- Optional Sentry error tracking (SENTRY_DSN gated)
- K8s-compatible health checks (Docker + docker-compose updated)
- 14 new observability tests

**Phase 4 — Database & Data Scale**:
- Alembic migration framework (SQLite baseline + versioning)
- Data expansion: 507 drugs (5.7x from 89), 179 interactions, 469 enzyme relations
- Backup/restore CLI commands (`db backup`, `db restore`)
- Schema version tracking via metadata table
- Health endpoint includes schema_version
- 20 new tests (266 total passing)
- All code review fixes applied (H1-H2, M1-M3, L1-L3)

---

## v0.2.0 — DrugBank Integration
**Target**: Q2 2026

- Full DrugBank CSV import (2,700+ drugs)
- Improved search: brand name aliases, prefix ranking
- Paginated drug browse UI
- Interaction count: scale from 28 to 500+
- Performance: graph load time budget < 5 s for full dataset

---

## v0.3.0 — Evidence Enrichment
**Target**: Q3 2026

- OpenFDA FAERS enrichment pipeline (case counts per interaction pair)
- Evidence scoring: weight interactions by FAERS case volume
- Evidence panel UI with source links
- Severity confidence indicator based on evidence strength

---

## v0.4.0 — User Accounts
**Target**: Q4 2026

- OAuth2 / email login (no PHI stored)
- Saved medication lists ("My Drugs")
- Analysis history with shareable report links
- Email alert when a saved drug gets a new interaction entry

---

## v0.5.0 — Mobile
**Target**: Q1 2027

- Progressive Web App (PWA) with offline drug list cache
- Evaluate React Native for App Store / Play Store distribution
- QR code sharing of analysis results

---

## v1.0.0 — Clinical Validation
**Target**: Q3 2027

- Independent pharmacist review of interaction dataset
- Formal accessibility audit (third-party WCAG AA certification)
- HIPAA gap analysis (if user health data stored)
- Performance SLA: p99 < 500 ms for 10-drug check
- Documented data update cadence (quarterly DrugBank + FAERS refresh)

---

## Future / Backlog
- AI agent for automated PubMed literature enrichment
- Multi-language UI (Spanish, French priority)
- Genomic pharmacogenomics layer (CYP2D6 poor-metabolizer flag)
- Public REST API with rate-limiting and API keys for third-party integrators
- Interaction network graph visualization (D3 / Cytoscape)
