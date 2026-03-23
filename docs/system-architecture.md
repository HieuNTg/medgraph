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

WAL mode enabled; foreign keys enforced.

## API Layer (Phase 2: Hardened)
- **Framework**: FastAPI with Pydantic V2 models
- **Routing**: Endpoints mounted at both `/api/v1/*` (canonical) and `/api/*` (backward compat)
- **Lifespan**: graph + store loaded once at startup via `asynccontextmanager`
- **Error Handling**: RFC 7807 Problem Details format (application/problem+json) for all errors
- **Request Tracing**: `RequestIDMiddleware` adds X-Request-ID header (UUID4 if not provided)
- **CORS**: configurable via `MEDGRAPH_CORS_ORIGINS` env var; exposes X-Request-ID header
- **Stats cache**: 1-hour in-process TTL for `/api/v1/stats`
- **Security Headers**: `SecurityHeadersMiddleware` adds X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, CSP (report-only), and HSTS (production only)
- **Authentication**: API key verification & rate limiting on `/api/*` endpoints
- **OpenAPI**: Metadata includes contact (MEDGRAPH Team), license (MIT), tags (system/drugs/analysis/reports/pharmacogenomics)

## Frontend Architecture
- **Router**: React Router v7 (`BrowserRouter`)
- **Data fetching**: TanStack Query v5 (cache + background refetch)
- **Pages**: `Home`, `Checker`, `Results`, `DrugInfo`, `About`
- **Layout**: `AppShell` with nav + medical disclaimer banner always visible
- **Styling**: Tailwind v4 with CSS variables for light/dark theming
