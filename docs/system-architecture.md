# MEDGRAPH — System Architecture

## Overview
Monorepo with a Python backend package (`medgraph/`) and a React frontend (`dashboard/`).
Backend serves both the REST API and (in production) the compiled frontend static files.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      Browser / Client                    │
│            React 19 + TypeScript + Vite SPA             │
│   DrugInput → TanStack Query → Results / CascadePath    │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP/JSON (REST + RFC 7807)
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI (port 8000)                     │
│  /health  /api/{v1}/drugs/search  /api/{v1}/check       │
│  RequestID middleware, RFC 7807 errors, CORS            │
│  OpenAPI at /docs (tags, contact, license)              │
└──────┬───────────────┬──────────────────────────────────┘
       │               │
┌──────▼──────┐ ┌──────▼──────────────────────────────────┐
│  GraphStore │ │           Analysis Engine                │
│  (SQLite)   │ │  GraphBuilder → NetworkX DiGraph         │
│  + Genetic  │ │  CascadeAnalyzer → PathFinder            │
│  Guidelines │ │  RiskScorer + PGx scoring                │
│             │ └─────────────────────────────────────────┘
│  drugs      │
│  enzymes    │ ┌──────────────────────────────────────────┐
│  enzyme_rel │ │          Data Pipeline (CLI)              │
│  interactions │  seed_data.py → optional DrugBank CSV    │
│  adverse_ev │ │  optional OpenFDA FAERS enrichment        │
│  genetic_gl │ │  CPIC pharmacogenomics guidelines         │
└─────────────┘ └──────────────────────────────────────────┘
```

## Data Flow
1. User enters drug names → `DrugInput` component
2. Frontend calls `POST /api/check` with drug name array
3. `DrugSearcher` resolves names → drug IDs (fuzzy match)
4. `CascadeAnalyzer.analyze()` runs on the in-memory NetworkX graph
5. `PathFinder` finds multi-hop enzyme-mediated paths
6. `RiskScorer` assigns severity score per interaction pair
7. `CheckResponse` JSON returned → `InteractionCard` + `CascadePath` rendered

## Knowledge Graph
- **Type**: `networkx.DiGraph`
- **Node types**: `drug` (id, name, class), `enzyme` (id, name, gene)
- **Edge types**:
  - `metabolized_by`: drug → enzyme
  - `inhibits`: drug → enzyme
  - `induces`: drug → enzyme
- **Built by**: `GraphBuilder` from `GraphStore` at server startup, held in `app.state`

## Database Schema (SQLite)
| Table | Key Columns |
|-------|-------------|
| `drugs` | `id`, `name`, `brand_names` (JSON), `drug_class`, `rxnorm_cui` |
| `enzymes` | `id`, `name`, `gene` |
| `interactions` | `id`, `drug_a_id`, `drug_b_id`, `severity`, `mechanism`, `evidence_count` |
| `drug_enzyme_relations` | `drug_id`, `enzyme_id`, `relation_type`, `strength` |
| `adverse_events` | `id`, `drug_ids` (JSON), `reaction`, `count`, `seriousness` |
| `genetic_guidelines` | `drug_id`, `gene_id`, `phenotype`, `recommendation`, `severity_multiplier` |
| `schema_metadata` | `key` (PK), `value` (TEXT) — *Phase 4* |

WAL mode enabled; foreign keys enforced. All tables managed by Alembic migrations (`medgraph/migrations/`).

## API Layer (Phase 2 + Phase 3: Hardened & Observable)
- **Framework**: FastAPI with Pydantic V2 models
- **Routing**: Endpoints mounted at both `/api/v1/*` (canonical) and `/api/*` (backward compat)
- **Lifespan**: graph + store loaded once at startup via `asynccontextmanager`
- **Error Handling**: RFC 7807 Problem Details format (application/problem+json) for all errors
- **Request Tracing**: `RequestIDMiddleware` adds X-Request-ID header (UUID4 if not provided); injected into structured logs
- **CORS**: configurable via `MEDGRAPH_CORS_ORIGINS` env var; exposes X-Request-ID header
- **Stats cache**: 1-hour in-process TTL for `/api/v1/stats`
- **Security Headers**: `SecurityHeadersMiddleware` adds X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP (report-only), and HSTS (production only)
- **Authentication**: API key verification & rate limiting on `/api/*` endpoints
- **OpenAPI**: Metadata includes contact (MEDGRAPH Team), license (MIT), tags (system/drugs/analysis/reports/pharmacogenomics)
- **Prometheus Metrics** (Phase 3): Auto-instrumentation via `prometheus-fastapi-instrumentator`; custom app metrics for analysis duration, graph size
- **Health Checks** (Phase 3): Split endpoints `/health/live` (liveness, no DB check), `/health/ready` (readiness, includes DB verification), `/health` (backward-compat alias)
- **Structured Logging** (Phase 3): JSONFormatter outputs logs as single-line JSON (MEDGRAPH_LOG_FORMAT=json); includes request_id, timestamp, level, logger, message
- **Error Tracking** (Phase 3): Optional Sentry integration via SENTRY_DSN env var; configurable traces sample rate (SENTRY_TRACES_RATE, default 0.1)

## Frontend Architecture
- **Router**: React Router v7 (`BrowserRouter`)
- **Data fetching**: TanStack Query v5 (cache + background refetch)
- **Pages**: `Home`, `Checker`, `Results`, `DrugInfo`, `About`
- **Layout**: `AppShell` with nav + medical disclaimer banner always visible
- **Styling**: Tailwind v4 with CSS variables for light/dark theming

## Phase 3: Observability & Monitoring

**Prometheus Metrics** — `/metrics` endpoint exposes Prometheus text format:
- `medgraph_analysis_duration_seconds` — histogram of cascade analysis runtime (8 buckets: 0.05–10.0s)
- `medgraph_graph_nodes_total` — gauge of total knowledge graph nodes
- `medgraph_graph_edges_total` — gauge of total knowledge graph edges
- Auto-instrumented request metrics: `http_requests_total`, `http_request_duration_seconds`, `http_request_size_bytes`, `http_response_size_bytes`

**Structured Logging** — JSON output for log aggregation:
- Format: `{"timestamp": ISO8601, "level": str, "logger": str, "message": str, "request_id": uuid, "exception": traceback?}`
- Enabled via `MEDGRAPH_LOG_FORMAT=json` env var
- Log level controlled by `MEDGRAPH_LOG_LEVEL` (default INFO)

**Health Checks** — Kubernetes-compatible probes:
- `GET /health/live` → `{"status": "ok"}` (liveness: process responding, no DB check)
- `GET /health/ready` → `{"status": "ok", "db_size": int, "graph_nodes": int, "schema_version": str}` (readiness: DB accessible, graph loaded, schema version included)
- `GET /health` → alias for `/health/ready` (backward compat)

**Error Tracking** (Optional) — Sentry integration:
- Enabled only if `SENTRY_DSN` env var is set
- Requires `pip install sentry-sdk[fastapi]` (optional dependency in pyproject.toml under `[project.optional-dependencies] sentry`)
- Configurable trace sample rate via `SENTRY_TRACES_RATE` (default 0.1)
- Environment tag set via `MEDGRAPH_ENV` (default "development")

## Phase 4: Database & Data Scale

**Schema Migrations** — Alembic framework (`medgraph/migrations/`):
- `001_baseline_schema.py` — captures all Phase 1–3 tables + schema_metadata for version tracking
- `env.py` — Alembic config with SQLite online mode support
- `runner.py` — Python API for migrations: `upgrade()`, `downgrade()`, `current()`
- Online migrations enabled via SQLAlchemy engine (no downtime for reads)

**Schema Version Tracking**:
- `schema_metadata` table (key-value store) added to all new DBs
- `GraphStore.get_schema_version()` / `set_schema_version(rev)` — managed by migrations
- Health endpoint includes `schema_version` field in readiness response

**Backup & Restore** — Online backup API:
- `GraphStore.backup(dest_path)` — creates snapshot using sqlite3.backup() (no locking)
- `GraphStore.restore(src_path)` — restores from backup file
- CLI commands: `db backup [--output path]` and `db restore <backup_file>`

**Data Scale** — Expanded seeding:
- Base dataset: 89 drugs, 28 interactions, 8 enzymes
- Expanded dataset: 297 additional drugs (Flockhart CYP450 + DDInter), 182 enzyme pathway relations, 61 new interactions
- `seed_expanded()` method loads both datasets; total ~507 drugs in expanded mode
- Extended seed data in `seed_drugs_extended.py` (2984 lines) and `seed_interactions_extended.py` (2155 lines)

**Database Management CLI**:
- `python -m medgraph.cli db upgrade [--revision head]` — apply migrations
- `python -m medgraph.cli db downgrade [--revision -1]` — revert migrations
- `python -m medgraph.cli db status` — show current migration revision
- `python -m medgraph.cli db backup [--output path]` — create backup
- `python -m medgraph.cli db restore <backup_file>` — restore from backup
- `python -m medgraph.cli expand` — load extended drug data (297 drugs, 182 enzyme relations)
