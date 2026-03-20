# MEDGRAPH — Project Roadmap

## v0.1.0 — MVP (current)
**Status**: Released

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
