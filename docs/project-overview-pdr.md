# MEDGRAPH — Product Development Requirements

## Product
**MEDGRAPH** — Drug Interaction Cascade Analyzer
Version: 0.1.0 (MVP)

## Problem Statement
125,000+ US deaths per year are attributable to adverse drug interactions. Existing consumer
tools (Drugs.com checker, pharmacy software) only evaluate **pairwise** interactions.
Polypharmacy patients taking 5–10 drugs face **cascade risks** that pairwise checks miss:

> Drug A inhibits enzyme → Drug B accumulates → Drug B toxicity reaches Drug C threshold

MEDGRAPH detects these multi-drug cascade effects through shared CYP450 enzyme pathways.

## Target Users
| User | Primary Need |
|------|-------------|
| Patients / caregivers | Quick safety check before adding a new drug |
| Pharmacists | Second-opinion cascade tool for complex regimens |
| Healthcare researchers | Exploratory analysis of interaction networks |

## Core Value Proposition
Cascade analysis that simple checkers miss:
- **Ketoconazole + Simvastatin** via CYP3A4 inhibition → rhabdomyolysis risk
- **Fluoxetine + Codeine** via CYP2D6 inhibition → reduced analgesia / toxicity
- Multi-hop paths: Drug A → enzyme inhibition → Drug B accumulation → shared target with Drug C

## MVP Scope
- 89+ built-in drugs across major therapeutic classes
- 28+ curated drug-drug interactions with severity ratings
- 8 CYP450 enzymes (CYP1A2, CYP2C9, CYP2C19, CYP2D6, CYP3A4, CYP2B6, CYP2E1, CYP2C8)
- CPIC pharmacogenomics guidelines for CYP2D6, CYP2C9, CYP2C19, CYP3A4
- Expandable via DrugBank CSV import and OpenFDA enrichment pipeline
- React 19 + TypeScript UI with cascade path visualization
- REST API with RFC 7807 error standardization and request tracing

## Success Metrics
- Correctly detects all seeded known cascade interactions
- API response < 2 seconds for a 10-drug analysis
- Zero false-negative misses on curated Ketoconazole/Simvastatin and Fluoxetine/Codeine pairs

## Non-Goals (MVP)
- User accounts or saved medication lists
- Prescription management or EHR integration
- Clinical decision support certification (FDA Class II)
- Native mobile application
- Multi-language UI
