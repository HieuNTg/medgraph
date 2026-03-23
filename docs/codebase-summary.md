# MEDGRAPH — Codebase Summary

## Backend Package: `medgraph/`

```
medgraph/
├── __init__.py              — Package version (__version__)
├── __main__.py              — Entry point: runs CLI
├── cli.py                   — Click CLI: `seed`, `serve`, `analyze`, `enrich`, `expand`, `db` commands
├── logging_config.py        — Structured logging: JSONFormatter for JSON output, configure_logging()
│
├── api/
│   ├── __init__.py
│   ├── audit.py             — Audit logging service: track user actions, exports, shares (HIPAA compliance)
│   ├── auth.py              — API key + JWT verification, rate limiting, user authentication
│   ├── errors.py            — RFC 7807 Problem Details error handlers (application/problem+json)
│   ├── metrics.py           — Prometheus metrics: ANALYSIS_DURATION, GRAPH_NODES, GRAPH_EDGES; setup_metrics()
│   ├── middleware.py        — RequestIDMiddleware: X-Request-ID header (UUID4 if missing); request_id in logs
│   ├── models.py            — Pydantic V2 request/response models incl. PaginatedResponse[T], HealthResponse w/ schema_version
│   ├── search.py            — DrugSearcher: fuzzy name → Drug lookup with optional RxNorm fallback
│   ├── security.py          — SecurityHeadersMiddleware: CORS, CSP, HSTS, X-Frame-Options, etc.
│   ├── server.py            — FastAPI app factory; setup_metrics(), _init_sentry(); /health/live, /health/ready endpoints
│   └── user_auth.py         — User account registration, login, JWT issuance, token refresh
│
├── fhir/
│   ├── __init__.py
│   ├── capability.py        — FHIR CapabilityStatement endpoint for conformance
│   ├── cds_hooks.py         — CDS Hooks service implementation (order-select, order-sign)
│   ├── models.py            — Pydantic models for FHIR R4 resources (MedicationRequest, Bundle, etc.)
│   ├── parser.py            — Extract drug data from FHIR MedicationRequest/Statement resources
│   └── smart_launch.py      — Smart on FHIR OAuth2 launch and app embedding
│
├── engine/
│   ├── __init__.py
│   ├── alternatives.py      — AlternativesFinder: drug alternative suggestions via shared enzyme paths
│   ├── analyzer.py          — CascadeAnalyzer: orchestrates full interaction report for a drug set
│   ├── centrality.py        — CentralityAnalyzer: hub drug identification via betweenness/PageRank
│   ├── contraindication.py  — Contraindication network builder for regimen-level conflict analysis
│   ├── deprescriber.py      — DeprescribingEngine: safe drug removal ordering with cascade analysis
│   ├── models.py            — Internal engine models (InteractionResult, AnalysisReport, CascadePath, …)
│   ├── optimizer.py         — PolypharmacyOptimizer: minimum vertex cover for regimen optimization
│   ├── pathfinder.py        — PathFinder: finds enzyme-mediated multi-hop paths in NetworkX graph
│   └── scorer.py            — RiskScorer: assigns numeric risk score + severity label per interaction
│
├── graph/
│   ├── __init__.py
│   ├── builder.py           — GraphBuilder: constructs NetworkX DiGraph from GraphStore data
│   ├── models.py            — Domain models: Drug, Enzyme, Interaction, DrugEnzymeRelation, AdverseEvent
│   └── store.py             — GraphStore: SQLite CRUD + schema version tracking; WAL mode; online backup/restore
│
├── data/
│   ├── __init__.py
│   ├── drugbank.py          — DrugBank CSV importer (optional enrichment)
│   ├── evidence_classifier.py — Evidence level classification (A-D) for interactions
│   ├── openfda.py           — OpenFDA FAERS API client (optional enrichment)
│   ├── refresh_pipeline.py  — Orchestrator for periodic data updates from external sources
│   ├── rxnorm.py            — RxNorm API client for CUI lookup / drug name normalization
│   ├── seed.py              — Seeding orchestrator: base seed_data + expanded datasets (297 drugs, 182 enzymes)
│   ├── seed_data.py         — Base dataset: 89 drugs, 28 interactions, 8 enzymes
│   ├── seed_drugs_extended.py       — Extended drugs (297 additional drugs from Flockhart CYP450 + DDInter)
│   ├── seed_interactions_extended.py — Extended interactions (61 direct + 182 enzyme pathway relations)
│   └── supplement_provider.py — NIH DSLD supplement/herbal drug interactions integration
│
└── migrations/
    ├── __init__.py
    ├── env.py               — Alembic environment config (SQLite online mode)
    ├── runner.py            — Migration runner: upgrade(), downgrade(), current()
    └── versions/
        └── 001_baseline_schema.py — Baseline migration (captures all Phase 1-3 tables + schema_metadata)
```

## Frontend: `dashboard/src/`

```
dashboard/src/
├── main.tsx                 — React app entry, QueryClientProvider + RouterProvider
├── App.tsx                  — Root router w/ ErrorBoundary; Suspense + AnalysisSkeleton for lazy routes
├── index.css                — Tailwind v4 directives + CSS variable theme definitions
├── App.css                  — Global resets
│
├── layout/
│   └── app-shell.tsx        — Top nav, medical disclaimer banner, <Outlet> wrapper
│
├── pages/
│   ├── home.tsx             — Landing page with feature highlights
│   ├── checker.tsx          — Main drug entry form + submit flow
│   ├── history.tsx          — User analysis history with timeline view
│   ├── login.tsx            — User login/registration forms
│   ├── profiles.tsx         — Saved medication profiles management
│   ├── results.tsx          — Results page: renders interactions from /api/check response
│   ├── shared-result.tsx    — Read-only shared result page (no auth required)
│   ├── drug-info.tsx        — Single drug detail page (/drugs/:id)
│   └── about.tsx            — Project info, data sources, methodology
│
├── components/
│   ├── contraindication-matrix.tsx — Heat-map visualization of drug-drug conflicts
│   ├── deprescribing-panel.tsx — Safe drug removal ordering recommendations
│   ├── drug-input.tsx       — Multi-drug search input w/ aria-controls, role="combobox"
│   ├── error-boundary.tsx   — React error boundary: catches render errors, shows retry UI
│   ├── error-display.tsx    — Standardized error card w/ retry callback, network error icon
│   ├── evidence-badge.tsx   — Evidence level badge (A-D ratings)
│   ├── evidence-panel.tsx   — Collapsible FAERS evidence list for an interaction
│   ├── hub-drugs-card.tsx   — Hub drug information with centrality metrics
│   ├── history-timeline.tsx — User analysis history with date filtering
│   ├── interaction-card.tsx — Card showing a single drug pair interaction + severity badge
│   ├── loading-skeleton.tsx — SearchResultsSkeleton, AnalysisSkeleton (pulse animations, a11y labels)
│   ├── medical-disclaimer.tsx — Amber disclaimer banner (always visible)
│   ├── offline-indicator.tsx — Shows when app is in offline mode
│   ├── pathway-graph.tsx    — Force-directed graph visualization of cascade paths (Cytoscape.js)
│   ├── pill-camera.tsx      — Camera-based pill identification UI with ONNX inference
│   ├── polypharmacy-gauge.tsx — Risk gauge for overall regimen polypharmacy assessment
│   ├── profile-card.tsx     — User profile information display
│   ├── risk-summary.tsx     — Overall risk score banner + breakdown bar
│   ├── cascade-path.tsx     — Visual step-by-step cascade path (enzyme chain)
│   ├── share-button.tsx     — Generate and share result links
│   ├── voice-input.tsx      — Web Speech API microphone input for drug names
│   ├── __tests__/           — Component & integration tests (7 test files, 40 tests)
│   └── ui/                  — Shared primitives (Badge, Card, Progress, Separator, …)
│
├── lib/
│   ├── api.ts               — Typed fetch wrappers for all API endpoints
│   ├── auth-context.ts      — React Context for user auth state + token management
│   ├── offline-checker.ts   — TypeScript port of cascade BFS for offline checking
│   ├── offline-store.ts     — IndexedDB wrapper for offline drug database + sync
│   ├── query-client.ts      — TanStack QueryClient singleton configuration
│   ├── types.ts             — TypeScript interfaces mirroring API response shapes
│   ├── utils.ts             — cn() helper, severity colour maps, formatting utilities
│   └── __tests__/           — API integration tests (api.test.ts)
│
├── test/
│   ├── setup.ts             — Vitest + jest-dom + vitest-axe matchers
│   └── test-utils.tsx       — renderWithProviders() helper wraps QueryClient + MemoryRouter
│
├── sw.js                    — Service Worker: offline cache, IndexedDB sync, push notifications
├── manifest.json            — PWA manifest: app name, icons, display mode, theme colors
└── offline-pill-model.onnx  — Quantized MobileNetV2 for browser-side pill identification
```

## Key Classes

| Class | Module | Responsibility |
|-------|--------|---------------|
| `AlternativesFinder` | `engine/alternatives.py` | Drug alternative suggestions via shared enzyme paths |
| `CascadeAnalyzer` | `engine/analyzer.py` | Runs full analysis; coordinates PathFinder + RiskScorer |
| `CentralityAnalyzer` | `engine/centrality.py` | Hub drug identification via betweenness/PageRank |
| `ContraindicationNetwork` | `engine/contraindication.py` | Builds conflict network for regimen-level analysis |
| `DeprescribingEngine` | `engine/deprescriber.py` | Safe drug removal ordering with cascade effects |
| `DrugSearcher` | `api/search.py` | Resolves user input strings to `Drug` objects |
| `GraphBuilder` | `graph/builder.py` | Converts `GraphStore` data into NetworkX `DiGraph` |
| `GraphStore` | `graph/store.py` | SQLite persistence: upsert + query for all entity types |
| `PathFinder` | `engine/pathfinder.py` | Finds enzyme-mediated paths via NetworkX graph traversal |
| `PolypharmacyOptimizer` | `engine/optimizer.py` | Minimum vertex cover for regimen optimization |
| `RiskScorer` | `engine/scorer.py` | Scores interactions; maps to critical/major/moderate/minor |

## Database Schema

```sql
-- Core domain tables
drugs                   (id PK, name, brand_names JSON, description, drug_class, rxnorm_cui,
                         category, atc_code, last_updated)  -- Phase 1: category + atc_code
enzymes                 (id PK, name, gene)
interactions            (id PK, drug_a_id, drug_b_id, severity, description, mechanism,
                         source, evidence_count, evidence_level, source_citation, last_updated)
drug_enzyme_relations   (drug_id, enzyme_id, relation_type, strength)  -- composite PK
adverse_events          (id PK, drug_ids JSON, reaction, count, seriousness, source_url)
genetic_guidelines      (id PK, drug_id, gene_id, phenotype, recommendation, severity_multiplier)
schema_metadata         (key PK, value TEXT)  -- schema version tracking

-- Phase 3: User data tables
users                   (id PK, email UNIQUE, password_hash, display_name, created_at, last_login)
medication_profiles     (id PK, user_id FK, name, drug_ids JSON, notes, created_at, updated_at)
analysis_history        (id PK, user_id FK, drug_ids JSON, result_json, overall_risk, created_at)
shared_results          (id PK, analysis_id FK, expires_at, created_at)  -- shareable result links
audit_log               (id PK, user_id FK, action, resource_type, resource_id, ip_address, user_agent, created_at)
```

**Key Features**:
- **Phase 1**: Evidence fields on interactions; category/atc_code on drugs; last_updated timestamps
- **Phase 2**: WAL mode enabled for concurrent reads; foreign keys enforced; LIKE ESCAPE for safe wildcards
- **Phase 3**: User authentication + profile/history/audit logging for feature rich experience
- **Phase 4**: schema_metadata for version tracking; all tables created by Alembic migration 001_baseline_schema

## API Endpoints

All endpoints accessible at `/api/v1/*` (canonical) and `/api/*` (backward compat).

**Core Analysis**:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health/live` | Liveness probe (no DB check); no auth required |
| GET | `/health/ready` | Readiness probe (DB check); no auth required |
| GET | `/health` | Backward-compat alias for `/health/ready`; no auth required |
| GET | `/metrics` | Prometheus metrics (Prometheus text format); no auth required |
| GET | `/api/v1/stats` | Aggregate counts (cached 1 hour); requires API key |
| GET | `/api/v1/drugs/search?q=&limit=&offset=` | Paginated search; returns PaginatedResponse with total/has_more |
| GET | `/api/v1/drugs/{drug_id}` | Single drug detail with enzyme relations |
| POST | `/api/v1/check` | Main analysis; accepts 2–10 drugs, returns CheckResponse + PGx annotations |
| GET | `/api/v1/interactions/{id}/evidence` | FAERS evidence for an interaction |
| POST | `/api/v1/report/{pdf,json,csv}` | Export analysis results in target format |
| GET | `/api/v1/pgx/guidelines` | CPIC pharmacogenomics guidelines for a drug |

**Phase 2 — Graph Features**:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/alternatives` | Drug alternative suggestions for interaction avoidance |
| GET | `/api/v1/graph/pathways?drugs=...` | Interactive cascade pathway visualization data |
| GET | `/api/v1/graph/contraindications?drugs=...` | Contraindication network for regimen |
| GET | `/api/v1/graph/hub-drugs` | Hub drugs with highest interaction potential |
| POST | `/api/v1/deprescribe` | Safe drug removal ordering recommendations |
| POST | `/api/v1/optimize` | Polypharmacy regimen optimization (minimum vertex cover) |

**Phase 3 — User Features**:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | User account registration |
| POST | `/auth/login` | User login, returns JWT access + refresh tokens |
| POST | `/auth/refresh` | Token refresh |
| GET | `/auth/me` | Current user profile |
| POST/GET/PUT/DELETE | `/api/v1/profiles` | Medication profile CRUD |
| GET | `/api/v1/history` | User analysis history (paginated, filterable) |
| POST | `/api/v1/share` | Create shareable result link |
| GET | `/api/v1/shared/{token}` | Retrieve shared result (no auth) |
| GET | `/api/v1/audit` | Audit log (admin only) |

**Phase 4 — Clinical Integration**:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/cds-services` | CDS Hooks discovery endpoint |
| POST | `/cds-services/medgraph-order-select` | CDS Hooks order-select hook |
| POST | `/cds-services/medgraph-order-sign` | CDS Hooks order-sign hook |
| GET | `/fhir/metadata` | FHIR CapabilityStatement |
| POST | `/smart/launch` | Smart on FHIR OAuth2 launch |
| POST | `/smart/callback` | Smart on FHIR authorization callback |

**Response Features**:
- **Phase 2**: RFC 7807 Problem Details; X-Request-ID headers; pagination support
- **Phase 3**: Split health checks; Prometheus metrics; structured JSON logging; optional Sentry
- **Phase 4**: FHIR R4 resource support; CDS Hooks cards; RxNorm resolution

## Testing (Phase 1–5)

**Backend Tests** (pytest, ~266 combined tests):

**test_database.py** (20 tests, Phase 1+4):
- Schema version tracking: get_schema_version(), set_schema_version()
- Schema metadata table created on store init
- Backup/restore roundtrip: data integrity across backup → restore cycles
- Online backup API using sqlite3.backup()
- Expanded seed data: 507 drugs, 243 interactions loaded
- Migration runner: upgrade, downgrade, current revision tracking
- Alembic baseline migration (001) captures full schema
- Evidence level fields (A-D) validation
- Supplement/herbal drug category support

**test_api_hardening.py** (17 tests, Phase 2):
- API v1 prefix routing (/api/v1/* + /api/*)
- RFC 7807 error format validation (400, 422, 404, 503 responses)
- Pagination with offset/limit/total/has_more
- X-Request-ID header presence on all responses
- OpenAPI metadata (tags, contact, license)
- Unresolved drug suggestions with validation

**test_observability.py** (14 tests, Phase 3):
- Prometheus metrics endpoint (/metrics) returns 200 with Prometheus text format
- Custom metrics: medgraph_analysis_duration_seconds, medgraph_graph_nodes_total, medgraph_graph_edges_total
- Health endpoint split: /health/live (liveness), /health/ready (readiness), /health (backward compat)
- Structured JSON logging with request_id field
- JSONFormatter produces valid JSON with timestamp, level, logger, message fields
- Sentry initialization when SENTRY_DSN is set

**Phase 2 Graph Features Tests**:
- AlternativesFinder: drug suggestions avoid cascade conflicts
- CentralityAnalyzer: betweenness/PageRank hub identification
- ContraindicationNetwork: regimen-level conflict analysis
- DeprescribingEngine: safe removal ordering with cascade effects
- PolypharmacyOptimizer: minimum vertex cover algorithm validation

**Phase 3 User Features Tests**:
- User registration/login with JWT tokens
- Medication profile CRUD operations
- Analysis history with filtering/comparison
- Shareable result links with optional expiry
- Audit logging for all actions

**Phase 4 Clinical Integration Tests**:
- FHIR R4 resource parsing (MedicationRequest, Bundle, etc.)
- CDS Hooks discovery and hook implementations
- Smart on FHIR OAuth2 launch flow
- RxNorm CUI to MEDGRAPH drug_id resolution
- CapabilityStatement FHIR conformance

**Phase 5 Mobile Tests**:
- PWA service worker caching strategy
- IndexedDB offline drug database sync
- Pill ID model inference accuracy (top-5)
- Barcode scanning NDC -> drug lookup
- Polypharmacy optimizer alternative suggestions

**Frontend Tests** (Vitest + React Testing Library + axe-core, 40+ tests, Phase 1-5):
- **Test Setup** (`src/test/setup.ts`): jest-dom + vitest-axe matchers auto-extended for toHaveNoViolations()
- **Render Helper** (`src/test/test-utils.tsx`): renderWithProviders() wraps components w/ QueryClient + MemoryRouter
- **Component Tests**:
  - Error handling: ErrorBoundary, ErrorDisplay with retry
  - Loading states: AnalysisSkeleton, SearchResultsSkeleton with a11y
  - Drug input: fuzzy search, keyboard nav, voice input
  - Results display: interactions, cascade paths, evidence panels
  - User features: profiles, history timeline, sharing
  - Graph visualization: pathway graph, contraindication matrix
  - Mobile: offline indicator, pill camera, voice input
- **Coverage** (`@vitest/coverage-v8`): v8 instrumentation for coverage reports
- **TypeScript** (`tsconfig.app.json`): Strict mode, vitest/globals types, path aliases (@/)

## CI/CD Pipeline

**GitHub Actions** (`.github/workflows/ci.yml`):
1. **Lint** — ruff check & format validation (Python 3.11)
2. **Test Backend** — pytest with coverage matrix (Python 3.11 & 3.12; includes test_api_hardening.py)
3. **Test Frontend** — TypeScript type check & production build (Node 20)
4. **Docker Build** — Image build + smoke test (container health check on startup)

**Dependabot** (`.github/dependabot.yml`):
- Weekly updates for pip, npm, and GitHub Actions
- Major version bumps ignored for FastAPI, Pydantic, NetworkX, React, React DOM
- Max 5 open PRs per ecosystem
