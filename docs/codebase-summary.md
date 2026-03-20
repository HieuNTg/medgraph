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
│   ├── models.py            — Pydantic V2 request/response models (CheckRequest, CheckResponse, …)
│   ├── search.py            — DrugSearcher: fuzzy name → Drug lookup with optional RxNorm fallback
│   └── server.py            — FastAPI app factory, all route handlers, lifespan startup
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
drugs               (id PK, name, brand_names JSON, description, drug_class, rxnorm_cui)
enzymes             (id PK, name, gene)
interactions        (id PK, drug_a_id, drug_b_id, severity, description, mechanism,
                     source, evidence_count)
drug_enzyme_relations (drug_id, enzyme_id, relation_type, strength)  -- composite PK
adverse_events      (id PK, drug_ids JSON, reaction, count, seriousness, source_url)
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check with DB record counts and graph node count |
| GET | `/api/stats` | Aggregate counts (drugs, interactions, enzymes, adverse events) |
| GET | `/api/drugs/search?q=&limit=` | Fuzzy drug name search; returns up to 50 results |
| GET | `/api/drugs/{drug_id}` | Single drug detail with enzyme relations |
| POST | `/api/check` | Main analysis: accepts 2–10 drug names, returns full cascade report |
| GET | `/api/interactions/{id}/evidence` | FAERS evidence records for a specific interaction |
