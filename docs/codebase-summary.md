# MEDGRAPH — Codebase Summary

## Backend Package: `medgraph/`

```
medgraph/
├── __init__.py              — Package version (__version__)
├── __main__.py              — Entry point: runs CLI
├── cli.py                   — Click CLI: `seed` and `serve` commands
│
├── api/
│   ├── __init__.py
│   ├── auth.py              — API key verification + rate limiting (check_rate_limit, verify_api_key)
│   ├── errors.py            — RFC 7807 Problem Details error handlers (application/problem+json)
│   ├── middleware.py        — RequestIDMiddleware: X-Request-ID header (UUID4 if missing)
│   ├── models.py            — Pydantic V2 request/response models incl. PaginatedResponse[T]
│   ├── search.py            — DrugSearcher: fuzzy name → Drug lookup with optional RxNorm fallback
│   ├── security.py          — SecurityHeadersMiddleware: CORS, CSP, HSTS, X-Frame-Options, etc.
│   └── server.py            — FastAPI app factory; mounts routes at /api/v1 + /api; error handlers
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
│   └── store.py             — GraphStore: SQLite CRUD for all entity types; WAL mode; upsert pattern
│
└── data/
    ├── __init__.py
    ├── drugbank.py          — DrugBank CSV importer (optional enrichment)
    ├── openfda.py           — OpenFDA FAERS API client (optional enrichment)
    ├── rxnorm.py            — RxNorm API client for CUI lookup / drug name normalization
    ├── seed.py              — Seeding orchestrator: loads seed_data into GraphStore
    └── seed_data.py         — Hard-coded MVP dataset: 89 drugs, 28 interactions, 8 enzymes
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
```

**Key Features (Phase 2)**:
- WAL mode enabled for concurrent reads
- Foreign keys enforced
- Search queries use LIKE with ESCAPE '\\' to safely handle wildcards in drug names

## API Endpoints

All endpoints accessible at `/api/v1/*` (canonical) and `/api/*` (backward compat).

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check; no auth required |
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

## Testing (Phase 2)

**test_api_hardening.py** (17 new tests):
- API v1 prefix routing (/api/v1/* + /api/*)
- RFC 7807 error format validation (400, 422, 404, 503 responses)
- Pagination with offset/limit/total/has_more
- X-Request-ID header presence on all responses
- OpenAPI metadata (tags, contact, license)
- Unresolved drug suggestions with validation

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
