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
│   ├── auth.py              — API key verification + rate limiting (check_rate_limit, verify_api_key)
│   ├── errors.py            — RFC 7807 Problem Details error handlers (application/problem+json)
│   ├── metrics.py           — Prometheus metrics: ANALYSIS_DURATION, GRAPH_NODES, GRAPH_EDGES; setup_metrics()
│   ├── middleware.py        — RequestIDMiddleware: X-Request-ID header (UUID4 if missing); request_id in logs
│   ├── models.py            — Pydantic V2 request/response models incl. PaginatedResponse[T], HealthResponse w/ schema_version
│   ├── search.py            — DrugSearcher: fuzzy name → Drug lookup with optional RxNorm fallback
│   ├── security.py          — SecurityHeadersMiddleware: CORS, CSP, HSTS, X-Frame-Options, etc.
│   └── server.py            — FastAPI app factory; setup_metrics(), _init_sentry(); /health/live, /health/ready endpoints
│
├── engine/
│   ├── __init__.py
│   ├── analyzer.py          — CascadeAnalyzer: orchestrates full interaction report for a drug set
│   ├── models.py            — Internal engine models (InteractionResult, AnalysisReport, CascadePath, …)
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
│   ├── openfda.py           — OpenFDA FAERS API client (optional enrichment)
│   ├── rxnorm.py            — RxNorm API client for CUI lookup / drug name normalization
│   ├── seed.py              — Seeding orchestrator: base seed_data + expanded datasets (297 drugs, 182 enzymes)
│   ├── seed_data.py         — Base dataset: 89 drugs, 28 interactions, 8 enzymes
│   ├── seed_drugs_extended.py       — Extended drugs (297 additional drugs from Flockhart CYP450 + DDInter)
│   └── seed_interactions_extended.py — Extended interactions (61 direct + 182 enzyme pathway relations)
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
├── App.tsx                  — Root router configuration
├── index.css                — Tailwind v4 directives + CSS variable theme definitions
├── App.css                  — Global resets
│
├── layout/
│   └── app-shell.tsx        — Top nav, medical disclaimer banner, <Outlet> wrapper
│
├── pages/
│   ├── home.tsx             — Landing page with feature highlights
│   ├── checker.tsx          — Main drug entry form + submit flow
│   ├── results.tsx          — Results page: renders interactions from /api/check response
│   ├── drug-info.tsx        — Single drug detail page (/drugs/:id)
│   └── about.tsx            — Project info, data sources, methodology
│
├── components/
│   ├── drug-input.tsx       — Multi-drug search input with typeahead suggestions
│   ├── interaction-card.tsx — Card showing a single drug pair interaction + severity badge
│   ├── cascade-path.tsx     — Visual step-by-step cascade path (enzyme chain)
│   ├── risk-summary.tsx     — Overall risk score banner + breakdown bar
│   ├── evidence-panel.tsx   — Collapsible FAERS evidence list for an interaction
│   ├── medical-disclaimer.tsx — Amber disclaimer banner (always visible)
│   └── ui/                  — Shared primitives (Badge, Card, Progress, Separator, …)
│
└── lib/
    ├── api.ts               — Typed fetch wrappers for all API endpoints
    ├── query-client.ts      — TanStack QueryClient singleton configuration
    ├── types.ts             — TypeScript interfaces mirroring API response shapes
    └── utils.ts             — cn() helper, severity colour maps, formatting utilities
```

## Key Classes

| Class | Module | Responsibility |
|-------|--------|---------------|
| `GraphStore` | `graph/store.py` | SQLite persistence: upsert + query for all entity types |
| `GraphBuilder` | `graph/builder.py` | Converts `GraphStore` data into NetworkX `DiGraph` |
| `CascadeAnalyzer` | `engine/analyzer.py` | Runs full analysis; coordinates PathFinder + RiskScorer |
| `RiskScorer` | `engine/scorer.py` | Scores interactions; maps to critical/major/moderate/minor |
| `PathFinder` | `engine/pathfinder.py` | Finds enzyme-mediated paths via NetworkX graph traversal |
| `DrugSearcher` | `api/search.py` | Resolves user input strings to `Drug` objects |

## Database Schema

```sql
drugs                   (id PK, name, brand_names JSON, description, drug_class, rxnorm_cui)
enzymes                 (id PK, name, gene)
interactions            (id PK, drug_a_id, drug_b_id, severity, description, mechanism,
                         source, evidence_count)
drug_enzyme_relations   (drug_id, enzyme_id, relation_type, strength)  -- composite PK
adverse_events          (id PK, drug_ids JSON, reaction, count, seriousness, source_url)
genetic_guidelines      (id PK, drug_id, gene_id, phenotype, recommendation, severity_multiplier)
schema_metadata         (key PK, value TEXT) -- Phase 4: schema version tracking
```

**Key Features**:
- **Phase 2**: WAL mode enabled for concurrent reads; foreign keys enforced; LIKE ESCAPE for safe wildcards
- **Phase 4**: schema_metadata table for version tracking; all tables created by Alembic migration 001_baseline_schema

## API Endpoints

All endpoints accessible at `/api/v1/*` (canonical) and `/api/*` (backward compat).

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

**Phase 2 Features**:
- All errors return RFC 7807 Problem Details (application/problem+json)
- Every response includes X-Request-ID header (generated by middleware)
- Search endpoint returns paginated results with offset/limit/total/has_more

**Phase 3 Features**:
- `/health/live` + `/health/ready` split for Kubernetes liveness/readiness probes
- `/metrics` exposes Prometheus-format metrics (auto-instrumented + custom app metrics)
- Request IDs included in structured JSON logs when MEDGRAPH_LOG_FORMAT=json
- Optional Sentry error tracking when SENTRY_DSN is set

## Testing (Phase 2 + Phase 3 + Phase 4)

**test_api_hardening.py** (17 tests, Phase 2):
- API v1 prefix routing (/api/v1/* + /api/*)
- RFC 7807 error format validation (400, 422, 404, 503 responses)
- Pagination with offset/limit/total/has_more
- X-Request-ID header presence on all responses
- OpenAPI metadata (tags, contact, license)
- Unresolved drug suggestions with validation

**test_observability.py** (14 tests, Phase 3):
- Prometheus metrics endpoint (/metrics) returns 200 with Prometheus text format
- Custom metrics present: medgraph_analysis_duration_seconds, medgraph_graph_nodes_total, medgraph_graph_edges_total
- Health endpoint split: /health/live (liveness), /health/ready (readiness), /health (backward compat)
- Structured JSON logging with request_id field
- JSONFormatter produces valid JSON with timestamp, level, logger, message fields
- Sentry initialization when SENTRY_DSN is set
- Sentry skipped (with warning) when sentry-sdk not installed but SENTRY_DSN set

**test_database.py** (20 tests, Phase 4):
- Schema version tracking: get_schema_version(), set_schema_version()
- Schema metadata table created on store init
- Backup/restore roundtrip: data integrity across backup → restore cycles
- Online backup API using sqlite3.backup()
- Expanded seed data: 297 new drugs, 61 new interactions loaded via seed_expanded()
- Migration runner: upgrade, downgrade, current revision tracking
- Alembic baseline migration (001) captures full schema

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
