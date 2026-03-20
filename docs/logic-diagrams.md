# MEDGRAPH — Logic Diagrams

## 1. System Flow (End-to-End)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER (Browser)                              │
│  1. Type drug name ──→ autocomplete dropdown ──→ select drug        │
│  2. Repeat for 2-10 drugs                                           │
│  3. Click "Check Interactions"                                      │
└───────────────────────────┬─────────────────────────────────────────┘
                            │  POST /api/check
                            │  { "drugs": ["Warfarin", "Aspirin"] }
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     FastAPI Server (:8000)                           │
│                                                                     │
│  ┌──────────────┐    ┌──────────────┐    ┌────────────────────┐    │
│  │  Validation   │───→│ Drug Search  │───→│ Cascade Analyzer   │    │
│  │ • empty? 400  │    │ • fuzzy match│    │ • direct lookup    │    │
│  │ • <2? 400     │    │ • name→ID    │    │ • enzyme cascades  │    │
│  │ • >10? 400    │    │ • not found? │    │ • BFS paths        │    │
│  │ • DB empty?503│    │   400+suggest│    │ • risk scoring     │    │
│  └──────────────┘    └──────────────┘    └────────┬───────────┘    │
│                                                    │                │
│                                          ┌─────────▼──────────┐    │
│                                          │  Build Response     │    │
│                                          │ • DrugResponse[]    │    │
│                                          │ • InteractionResp[] │    │
│                                          │ • overall_risk      │    │
│                                          │ • disclaimer        │    │
│                                          └─────────┬──────────┘    │
└────────────────────────────────────────────────────┬────────────────┘
                                                     │ JSON Response
                                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      React Frontend                                 │
│                                                                     │
│  ┌──────────────┐  ┌─────────────────┐  ┌──────────────────────┐   │
│  │ RiskSummary  │  │ InteractionCard │  │ CascadePath          │   │
│  │ • donut chart│  │ • severity badge│  │ • animated flow      │   │
│  │ • overall    │  │ • risk score bar│  │ • Drug→Enzyme→Drug   │   │
│  │   risk level │  │ • description   │  │ • color-coded edges  │   │
│  │ • export PNG │  │ • expand toggle │  │ • human explanation  │   │
│  └──────────────┘  └─────────────────┘  └──────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Medical Disclaimer (always visible on every page)           │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Cascade Analysis Algorithm

```
                    analyze(drug_ids, graph, store)
                              │
                              ▼
                    ┌─────────────────┐
                    │ Resolve drug IDs │
                    │ to Drug objects  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Generate pairs   │  C(n,2) combinations
                    │ (A,B), (A,C)... │  max 45 for 10 drugs
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌────────────┐  ┌──────────────┐  ┌───────────┐
     │ Batch load │  │ Batch load   │  │ Find ALL  │
     │ interactions│  │ adverse      │  │ cascade   │
     │ from SQLite│  │ events (FAERS│  │ paths via │
     └─────┬──────┘  └──────┬───────┘  │ PathFinder│
           │                │          └─────┬─────┘
           ▼                ▼                ▼
     ┌─────────────────────────────────────────┐
     │         For each pair (Drug A, Drug B):  │
     │                                          │
     │  1. Check interaction_lookup[A,B]        │
     │     → direct interaction? (severity,     │
     │       mechanism, description)            │
     │                                          │
     │  2. Filter cascade_paths for this pair   │
     │     → enzyme-mediated cascades           │
     │                                          │
     │  3. Collect evidence from adverse_events │
     │     → FAERS case counts                  │
     │                                          │
     │  4. Build DrugInteractionResult          │
     └──────────────────┬──────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │   RiskScorer    │
              │  score each     │
              │  interaction    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Sort by score   │  highest risk first
              │ Classify overall│  max(scores) → tier
              │ Attach disclaimer│
              └────────┬────────┘
                       │
                       ▼
                InteractionReport
```

---

## 3. Cascade Detection (PathFinder)

### 3a. Enzyme Cascade Detection (2-hop, O(drugs × enzymes))

```
For each enzyme node in graph:

    ┌─────────┐         ┌──────────┐         ┌─────────┐
    │ Drug A  │──inhibits──→│ CYP3A4  │←──metabolized_by──│ Drug B  │
    └─────────┘         └──────────┘         └─────────┘

    Pattern 1: INHIBITION CASCADE
    ─────────────────────────────
    Drug A inhibits CYP3A4
    Drug B needs CYP3A4 for metabolism
    → Drug B ACCUMULATES → TOXICITY
    → Severity: major (strong) / moderate (weak)

    Example: Ketoconazole ──inhibits──→ CYP3A4 ←──metabolized_by── Simvastatin
             Result: Simvastatin levels ↑↑↑ → rhabdomyolysis risk


    ┌─────────┐         ┌──────────┐         ┌─────────┐
    │ Drug C  │──induces───→│ CYP2D6  │←──metabolized_by──│ Drug D  │
    └─────────┘         └──────────┘         └─────────┘

    Pattern 2: INDUCTION CASCADE
    ─────────────────────────────
    Drug C induces CYP2D6
    Drug D metabolized faster via CYP2D6
    → Drug D DEPLETED → LOSS OF EFFICACY
    → Severity: major (strong) / moderate (weak)

    Example: Rifampin ──induces──→ CYP3A4 ←──metabolized_by── Warfarin
             Result: Warfarin levels ↓↓↓ → blood clot risk
```

### 3b. Multi-Hop BFS (3-hop, max depth 3)

```
Only when ≤5 drugs (performance guard):

    BFS from each drug node:

    Drug A ──inhibits──→ CYP3A4 ──metabolized_by──→ Drug B ──inhibits──→ CYP2D6
                                                                           │
                                                                    metabolized_by
                                                                           │
                                                                        Drug C

    3-DRUG CASCADE EXAMPLE:
    ───────────────────────
    Rifampin ──induces──→ CYP enzymes
    → Warfarin metabolized faster (less effective anticoagulant)
    → BUT Aspirin still increases bleeding independently
    → Compound risk: reduced warfarin + aspirin bleeding = UNPREDICTABLE

    Queue: deque[(current_node, path, edges)]
    Stop:  when target drug reached OR depth > max_depth
    Skip:  cycles, non-pharmacokinetic edges
    Output: CascadePath with steps, severity, description
```

### 3c. Deduplication & Ranking

```
    All paths from enzyme cascade + BFS
              │
              ▼
    ┌─────────────────────┐
    │ Deduplicate by key:  │
    │ "{drugA}:{drugB}:    │
    │  {description[:60]}" │
    │ Also check reverse   │
    └─────────┬───────────┘
              │
              ▼
    ┌─────────────────────┐
    │ Sort by severity:    │
    │ critical(4) > major  │
    │ (3) > moderate(2)    │
    │ > minor(1)           │
    └─────────────────────┘
```

---

## 4. Risk Scoring Formula

```
┌─────────────────────────────────────────────────────────────────────┐
│                     RISK SCORE COMPUTATION                          │
│                                                                     │
│  final_score = min(100, base + cascade_bonus × strength + evidence) │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  base_score = severity_weight(direct_interaction.severity)  │    │
│  │                                                             │    │
│  │    critical  ───→ 90                                        │    │
│  │    major     ───→ 70                                        │    │
│  │    moderate  ───→ 40                                        │    │
│  │    minor     ───→ 15                                        │    │
│  │    none      ───→  0                                        │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  cascade_bonus = Σ severity_weight(path.severity) × 0.5    │    │
│  │                                                             │    │
│  │    Each cascade path adds half its severity weight          │    │
│  │    Example: 1 major cascade = 70 × 0.5 = +35               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  enzyme_strength = max strength across all cascade steps    │    │
│  │                                                             │    │
│  │    strong    ───→ 1.0                                       │    │
│  │    moderate  ───→ 0.6                                       │    │
│  │    weak      ───→ 0.3                                       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  evidence_modifier = log₁₀(FAERS_case_count + 1) × 5       │    │
│  │                                                             │    │
│  │    100 cases    ───→ log₁₀(101) × 5 ≈ 10.0                 │    │
│  │    1,000 cases  ───→ log₁₀(1001) × 5 ≈ 15.0                │    │
│  │    10,000 cases ───→ log₁₀(10001) × 5 ≈ 20.0               │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  SEVERITY CLASSIFICATION:                                           │
│  ┌──────────────────────────────────┐                               │
│  │  score ≥ 80  ──→  CRITICAL 🔴   │                               │
│  │  score ≥ 60  ──→  MAJOR    🟠   │                               │
│  │  score ≥ 35  ──→  MODERATE 🟡   │                               │
│  │  score <  35 ──→  MINOR    🔵   │                               │
│  └──────────────────────────────────┘                               │
│                                                                     │
│  OVERALL REPORT SCORE = max(all interaction scores)                 │
│  (worst-case drives the overall risk level)                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Scoring Example: Ketoconazole + Simvastatin

```
  base_score     = 90   (direct interaction = critical)
  cascade_bonus  = 70 × 0.5 = 35   (1 major cascade via CYP3A4)
  enzyme_strength = 1.0  (strong inhibitor)
  evidence       = log₁₀(15001) × 5 ≈ 20.9  (15,000 FAERS cases)

  final = min(100, 90 + 35 × 1.0 + 20.9) = min(100, 145.9) = 100.0
  classification = CRITICAL 🔴
```

### Scoring Example: Warfarin + Aspirin

```
  base_score     = 70   (direct interaction = major)
  cascade_bonus  = 0    (no enzyme cascade - direct pharmacodynamic)
  enzyme_strength = 1.0  (no cascades, default)
  evidence       = log₁₀(15001) × 5 ≈ 20.9  (15,000 FAERS cases)

  final = min(100, 70 + 0 × 1.0 + 20.9) = min(100, 90.9) = 90.9
  classification = CRITICAL 🔴
```

---

## 5. Knowledge Graph Structure

```
                         KNOWLEDGE GRAPH (NetworkX DiGraph)

  NODES                              EDGES
  ─────                              ─────
  drug:DB00682 (Warfarin)            metabolized_by (+ strength)
  drug:DB00945 (Aspirin)             inhibits       (+ strength)
  drug:DB01026 (Ketoconazole)        induces        (+ strength)
  drug:DB00641 (Simvastatin)         interacts_with (+ severity)
  ...89 drug nodes

  enzyme:CYP3A4
  enzyme:CYP2D6
  enzyme:CYP2C9
  enzyme:CYP2C19
  enzyme:CYP1A2
  ...8 enzyme nodes


  Example subgraph:

  ┌──────────────┐  metabolized_by   ┌───────────┐  metabolized_by   ┌──────────────┐
  │   Warfarin   │─────(strong)─────→│  CYP2C9   │←────(strong)─────│  Diclofenac  │
  │  DB00682     │                   │           │                   │  DB00586     │
  └──────┬───────┘                   └───────────┘                   └──────────────┘
         │                                 ▲
         │ metabolized_by (weak)           │ inhibits (strong)
         │                                 │
         ▼                           ┌─────┴──────┐
  ┌──────────────┐                   │ Fluconazole │
  │   CYP3A4     │                   │  DB00196    │
  └──────────────┘                   └─────────────┘
         ▲
         │ inhibits (strong)
         │
  ┌──────┴───────┐  interacts_with   ┌──────────────┐
  │ Ketoconazole │───(critical)─────→│ Simvastatin  │
  │  DB01026     │                   │  DB00641     │
  └──────────────┘                   └──────────────┘
         │                                  │
         │ inhibits (strong)               │ metabolized_by (strong)
         │                                  │
         └───────────→ CYP3A4 ←─────────────┘
                    (CASCADE PATH!)
```

---

## 6. Data Pipeline

```
    ┌─────────────────────────────────────────────────────────────┐
    │                  python -m medgraph.cli seed                 │
    └───────────────────────────┬─────────────────────────────────┘
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
    ┌────────────────┐ ┌──────────────┐ ┌─────────────────┐
    │ Built-in Seed  │ │ DrugBank CSV │ │ OpenFDA FAERS   │
    │ (always runs)  │ │ (if present) │ │ (if --openfda)  │
    │                │ │              │ │                  │
    │ 89 drugs       │ │ 2700+ drugs  │ │ Adverse event   │
    │ 8 enzymes      │ │ More interact│ │ case counts     │
    │ 28 interactions│ │ More enzyme  │ │ for top 50 drugs│
    │ 115 relations  │ │ relations    │ │                  │
    │ 7 adverse evts │ │              │ │ Rate: 5 req/sec │
    └───────┬────────┘ └──────┬───────┘ └────────┬────────┘
            │                 │                   │
            └────────┬────────┘                   │
                     ▼                            │
            ┌────────────────┐                    │
            │   SQLite DB    │←───────────────────┘
            │ medgraph.db    │
            │                │
            │ Tables:        │
            │ • drugs        │
            │ • enzymes      │
            │ • interactions │
            │ • drug_enzyme  │
            │   _relations   │
            │ • adverse      │
            │   _events      │
            └───────┬────────┘
                    │
                    ▼
            ┌────────────────┐
            │ GraphBuilder   │  On server startup (lifespan)
            │                │
            │ SQLite → nx.   │
            │ DiGraph        │
            │                │
            │ ~97 nodes      │
            │ ~143 edges     │
            │ In-memory      │
            └────────────────┘
```

---

## 7. Frontend Component Tree

```
    App (BrowserRouter)
    │
    ├── AppShell (layout: header + footer + disclaimer)
    │   ├── Header
    │   │   ├── Logo "MEDGRAPH"
    │   │   ├── Nav: Home | Check Interactions | About
    │   │   └── ThemeToggle (light/dark)
    │   │
    │   ├── <Outlet /> (page content)
    │   │   │
    │   │   ├── HomePage (/)
    │   │   │   ├── Hero: "Know Your Drug Interactions"
    │   │   │   ├── Stats: {drugs} | {interactions} | {enzymes}  ←── GET /api/stats
    │   │   │   ├── FeatureCards × 3
    │   │   │   ├── HowItWorks: 3-step flow
    │   │   │   └── CTA → /checker
    │   │   │
    │   │   ├── CheckerPage (/checker)
    │   │   │   ├── DrugInput
    │   │   │   │   ├── Input (debounced 300ms)  ←── GET /api/drugs/search?q=
    │   │   │   │   ├── Dropdown (role="listbox")
    │   │   │   │   ├── Selected Badges (removable)
    │   │   │   │   └── "Check Interactions" Button
    │   │   │   ├── Loading: Progress + "Analyzing..."
    │   │   │   └── Error: red alert box
    │   │   │                    │
    │   │   │          POST /api/check ──→ navigate(/results, { state })
    │   │   │                                       │
    │   │   ├── ResultsPage (/results)              │
    │   │   │   ├── RiskSummary  ◄──────────────────┘
    │   │   │   │   ├── Overall risk icon + label
    │   │   │   │   ├── PieChart (Recharts donut)
    │   │   │   │   ├── Timestamp
    │   │   │   │   └── Export PNG (html2canvas)
    │   │   │   ├── Drug badges
    │   │   │   ├── InteractionCard[] (sorted by severity)
    │   │   │   │   ├── Severity badge (Critical/Major/Moderate/Minor)
    │   │   │   │   ├── Risk score Progress bar
    │   │   │   │   ├── Description text
    │   │   │   │   ├── ► CascadePath (expandable, framer-motion)
    │   │   │   │   │   ├── Step: [Drug] ──relation──→ [Enzyme]
    │   │   │   │   │   ├── Step: [Enzyme] ──relation──→ [Drug]
    │   │   │   │   │   └── Human-readable explanation
    │   │   │   │   └── ► EvidencePanel (expandable)
    │   │   │   │       ├── Source badge (seed/faers)
    │   │   │   │       ├── Case count
    │   │   │   │       └── External link
    │   │   │   └── "Check Another Combination" → /checker
    │   │   │
    │   │   ├── DrugInfoPage (/drugs/:id)  ←── GET /api/drugs/{id}
    │   │   │
    │   │   └── AboutPage (/about)
    │   │       ├── Methodology (Knowledge Graph, Cascade, Scoring)
    │   │       ├── Data Sources (DrugBank, OpenFDA, RxNorm)
    │   │       ├── Limitations
    │   │       └── Full Medical Disclaimer
    │   │
    │   └── Footer
    │       ├── MedicalDisclaimer (always)
    │       └── "Data sources: DrugBank · OpenFDA · RxNorm"
    │
    └── QueryClientProvider (TanStack Query, staleTime: 5min)
```
