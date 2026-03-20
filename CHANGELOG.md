# Changelog

All notable changes to MEDGRAPH are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-03-20

### Added

- Initial release of MEDGRAPH — Drug Interaction Cascade Analyzer
- **Knowledge graph** built with NetworkX 3.x, persisted to SQLite
- **Cascade analysis engine** tracing multi-hop CYP450 enzyme interaction chains
- **89 drugs** seeded from DrugBank open subset with full enzyme relation data
- **28 direct drug interactions** with severity classifications (minor / moderate / major / critical)
- **8 CYP450 enzymes** modelled: CYP3A4, CYP2D6, CYP2C9, CYP2C19, CYP1A2, CYP2B6, CYP2E1, CYP2C8
- **OpenFDA FAERS integration** for real-world adverse event evidence counts (optional, skip flag available)
- **RxNorm API integration** for drug name normalisation and brand-name resolution
- **FastAPI REST API** with 6 endpoints and OpenAPI/Swagger documentation
- **Risk scoring** (0–100) with severity aggregation across all drug pairs
- **React 19 frontend** with TypeScript and Tailwind CSS v4
  - Autocomplete drug search (powered by `/api/drugs/search`)
  - Cascade path visualisation per drug pair
  - Evidence trail with FAERS adverse event counts
  - Light and dark theme
  - Mobile-responsive layout
- **Medical disclaimer** displayed prominently on every page and in every API response
- **pytest test suite** covering data layer, cascade engine, and API endpoints
- **CLI commands**: `seed`, `serve`
- **Makefile** for common development tasks
