# FDA Label NLP Mining Design

**Phase 5.2 Design Document**
**Status**: Design Phase
**Target Release**: v0.3.0–v0.4.0 (Q3–Q4 2026)

---

## Executive Summary

Design for automated extraction of drug-drug interaction candidates from FDA drug labels via NLP. Converts unstructured SPL XML (Structured Product Labeling) text into structured interaction records with confidence scoring. Bridges gap between manual curation and FAERS signal detection.

---

## Problem Statement

**Current State**:
- `openfda.py`: Fetches raw drug label text via OpenFDA API
- Labels contain unstructured "Drug Interactions" sections (prose, tables, fragments)
- Human extraction: manual review of 500+ drug labels → ~50–100 novel interactions (effort-intensive)
- No automated screening for interaction candidates

**Gaps**:
1. Drug interaction text not parsed structurally (entity extraction missing)
2. No confidence scoring; all interactions treated equally
3. Manual workflow doesn't scale beyond small drug sets
4. False positives not filtered (e.g., "no interaction" statements misclassified)

---

## Proposed Architecture

### High-Level Flow

```
┌─ Fetch Drug Label (SPL XML) via OpenFDA ─┐
│                                          │
├─> Parse SPL + Extract Interactions Text  │
│   ├─ Identify <interactions> section     │
│   └─ Clean formatting (remove markup)    │
│                                          │
├─> NLP Pipeline (Rule + Transformer)      │
│   ├─ Named Entity Recognition (NER)      │
│   │   └─ BioBERT / SciBERT for drug/gene │
│   │                                      │
│   ├─ Relation Extraction (RE)            │
│   │   ├─ Rule-based: regex patterns      │
│   │   └─ BioBERT directional DDI model   │
│   │                                      │
│   └─ Negative Detection (filter)         │
│       └─ "no interaction" / "unlikely"   │
│                                          │
├─> Interaction Candidate Scoring          │
│   ├─ Confidence = NER + RE score         │
│   ├─ Severity = mechanism mention        │
│   └─ Filter: confidence < 0.6 → discard  │
│                                          │
├─> Human Review Workflow                  │
│   ├─ Candidates rank by confidence       │
│   ├─ Pharmacist review (Accept/Reject)   │
│   └─ Approved → Upsert interaction DB    │
│                                          │
└─> Monitoring + Feedback Loop             │
    ├─ Log extraction metrics              │
    └─ Reject rates → retrain signals      │
```

### NLP Approach: Hybrid Rule + Transformer

**Why Hybrid?**
- Rule-based: Fast, interpretable, low resource cost; good for common patterns
- Transformer: High accuracy on nuanced text; few-shot learning
- Hybrid: Rule filter → Transformer refinement (2-stage pipeline)

---

## Technical Approach

### Stage 1: SPL XML Parsing

**Data Source**: OpenFDA `/drug/label.json` endpoint

**SPL Sections of Interest**:
- `<section classCode="INTERACTIONS">` (standard)
- `<highlight>` elements within interactions section
- `<paragraph>` structures containing drug names + mechanism descriptions

**Implementation**:
```python
from lxml import etree

def extract_interactions_section(spl_xml: str) -> str:
    """Extract interactions section from SPL."""
    try:
        root = etree.fromstring(spl_xml.encode('utf-8'))
        # Query for section with INTERACTIONS code
        sections = root.xpath(
            '//section[@classCode="INTERACTIONS"]//paragraph/text()',
            namespaces={...}
        )
        return "\n".join(sections)
    except Exception as e:
        logger.error(f"SPL parse error: {e}")
        return ""
```

### Stage 2: Named Entity Recognition (NER)

**Task**: Identify drug names and gene/enzyme mentions in label text.

**Models Compared**:

| Model | Training | Latency | Accuracy | Cost |
|-------|----------|---------|----------|------|
| BioBERT | PubMed + SQuAD | ~100ms/doc | ~88% F1 | Low (4GB VRAM) |
| SciBERT | arXiv + ScienceParse | ~100ms/doc | ~85% F1 | Low (4GB VRAM) |
| PubMedBERT | PubMed + PMC | ~150ms/doc | ~89% F1 | Medium (6GB VRAM) |
| LLaMA 2 70B | General domain | ~500ms/doc | ~92% F1 | High (need GPU) |

**Chosen**: BioBERT (balance accuracy/cost) + RxNorm normalization.

**Implementation**:
```python
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

class DrugNER:
    def __init__(self):
        self.nlp = pipeline(
            "ner",
            model="dmis-lab/biobert-base-cased-v1.2",
            device=0 if torch.cuda.is_available() else -1
        )
        self.rxnorm = RxNormClient()

    def extract_entities(self, text: str) -> list[dict]:
        """Extract drug + enzyme entities."""
        entities = self.nlp(text)
        # Merge tokens (B-DRUG + I-DRUG)
        merged = self._merge_tokens(entities)

        # Normalize drug names via RxNorm API
        for ent in merged:
            if ent['entity_type'] == 'DRUG':
                ent['normalized_name'] = self.rxnorm.search(ent['text'])

        return merged

    def _merge_tokens(self, entities):
        """Merge subword tokens (##) into complete entities."""
        # e.g., ["Simva", "##statin"] → "Simvastatin"
        merged = []
        current = None
        for ent in entities:
            if ent['word'].startswith('##'):
                if current:
                    current['text'] += ent['word'][2:]
            else:
                if current:
                    merged.append(current)
                current = {
                    'text': ent['word'],
                    'entity_type': ent['entity'].split('-')[1],
                    'score': ent['score']
                }
        if current:
            merged.append(current)
        return merged
```

### Stage 3: Relation Extraction (RE)

**Task**: Classify interaction type (inhibition, induction, substrate, etc.) + extract mechanism.

**Two-Step Approach**:

#### 3a: Rule-Based Relation Extraction (Fast Filter)

Common patterns in FDA labels:
```regex
Precipitant: {drug1}
Object:      {drug2}
Mechanism:   {drug1} (inhibits|induces|is_substrate|is_metabolized_by) (CYP|UGT|NAT)(\d+[A-Z]*)
Effect:      {effect_description}
```

```python
class RuleBasedRE:
    PATTERNS = [
        r"({drug})\s+(inhibits?|inhibition\s+of)\s+(CYP\d+[A-Z]*)",
        r"({drug})\s+(induces?|induction\s+of)\s+(CYP\d+[A-Z]*)",
        r"({drug})\s+is\s+(a\s+)?substrate\s+of\s+(CYP\d+[A-Z]*)",
        r"increase[sd]?\s+(in\s+)?levels?\s+of\s+({drug})",
        r"decreased?\s+(in\s+)?levels?\s+of\s+({drug})",
    ]

    def extract_relations(self, text: str, entities: list) -> list[dict]:
        relations = []
        for pattern in self.PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                relation = self._parse_match(match, pattern)
                if relation:
                    relations.append(relation)
        return relations
```

#### 3b: Transformer-Based RE (BioBERT DDI)

Pre-trained model: BioBERT directional DDI (tuned on DrugBank + BioCreative corpus)

```python
from transformers import pipeline

class TransformerRE:
    def __init__(self):
        # Fine-tuned model on DDI extraction
        self.ner_model = pipeline(
            "token-classification",
            model="dmis-lab/biobert-base-cased-v1.2",
            aggregation_strategy="simple"
        )
        # DDI-specific relation classifier (custom fine-tune)
        self.relation_model = AutoModelForSequenceClassification.from_pretrained(
            "custom/biobert-ddi-relations"
        )

    def extract_directional_relations(self, text: str) -> list[dict]:
        """Extract precipitant -> object interactions."""
        # Sentence-level classification
        sentences = sent_tokenize(text)
        relations = []

        for sent in sentences:
            # Check if sentence contains DDI
            ddi_pred = self._classify_ddi_sentence(sent)
            if ddi_pred['label'] == 'contains_ddi' and ddi_pred['score'] > 0.7:
                # Extract entities + relations
                entities = self.ner_model(sent)
                if len(entities) >= 2:
                    rel = self._build_relation(sent, entities)
                    relations.append(rel)

        return relations

    def _classify_ddi_sentence(self, sentence: str) -> dict:
        """Does sentence describe a DDI?"""
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            truncation=True,
            max_length=128
        )
        outputs = self.relation_model(**inputs)
        return {
            'label': ['no_ddi', 'contains_ddi'][outputs.logits.argmax()],
            'score': outputs.logits.softmax(-1).max().item()
        }
```

### Stage 4: Confidence Scoring

**Confidence Metric** (0–1 scale):
```
confidence = (NER_score * 0.4) + (RE_score * 0.4) + (mechanism_score * 0.2)

Where:
  - NER_score = average BioBERT entity scores
  - RE_score = transformer relation confidence
  - mechanism_score = 1.0 if enzyme/pathway mentioned, 0.5 otherwise
```

**Severity Inference**:
- If text contains: "serious", "life-threatening", "fatal" → severity = "critical"
- Else if: "inhibits CYP3A4" or strong enzyme mentioned → severity = "major"
- Else: severity = "moderate"

### Stage 5: Negative Detection Filter

**Problem**: False positives like "Drug A does not interact with Drug B"

**Solution**: Negative marker detection
```python
NEGATIVE_MARKERS = [
    r"no\s+(known\s+)?interaction",
    r"does\s+not\s+interact",
    r"unlikely\s+to\s+interact",
    r"no\s+clinical\s+significance",
    r"no\s+dose\s+adjustment",
]

def has_negative_marker(text: str) -> bool:
    for marker in NEGATIVE_MARKERS:
        if re.search(marker, text, re.IGNORECASE):
            return True
    return False
```

---

## Data Requirements

### Input
- **OpenFDA Label Endpoint**: `GET /drug/label.json?search=generic_name:{drug_name}`
- **SPL XML Structure**: HL7 standard; interactions section varies (tables, prose, lists)
- **Volume**: ~5,000 active drugs; ~3,000 have interaction sections

### Output Schema

```python
class InteractionCandidate(BaseModel):
    id: str
    source: Literal["fda_label"] = "fda_label"
    drug_a_id: str          # Normalized RxNorm CUI
    drug_a_name: str
    drug_b_id: str
    drug_b_name: str
    mechanism: str          # E.g., "CYP3A4 inhibition"
    effect: str            # E.g., "increased Simvastatin levels"
    confidence: float      # 0.0–1.0
    severity_estimate: str # "critical" | "major" | "moderate" | "minor"
    source_url: str        # Link to label
    human_review_status: Literal["pending", "approved", "rejected"] = "pending"
    review_notes: str = ""
    extracted_at: datetime
```

---

## API Design

### 1. Extract Interactions from Label
```http
POST /api/admin/nlp/extract
Content-Type: application/json
X-API-Key: <admin_key>

{
  "drug_name": "Simvastatin",
  "source": "fda_label",
  "confidence_threshold": 0.6
}

Response: 200 OK
{
  "drug_name": "Simvastatin",
  "candidates": [
    {
      "id": "CANDIDATE_20260324_001",
      "drug_a_name": "Ketoconazole",
      "drug_b_name": "Simvastatin",
      "mechanism": "CYP3A4 inhibition",
      "effect": "increased Simvastatin levels 10-20x",
      "confidence": 0.88,
      "severity_estimate": "critical",
      "human_review_status": "pending"
    },
    ...
  ],
  "extraction_time_ms": 245,
  "model_used": "biobert-ddi-v1"
}
```

### 2. Bulk Extract (All Drugs)
```http
POST /api/admin/nlp/extract-batch
Content-Type: application/json
X-API-Key: <admin_key>

{
  "drug_ids": ["DB00641", "DB00682", ...],
  "confidence_threshold": 0.65,
  "async": true
}

Response: 202 Accepted
{
  "job_id": "nlp_extract_20260324_1430",
  "status": "queued",
  "estimated_drugs": 500
}
```

### 3. Review Candidate
```http
PATCH /api/admin/nlp/candidates/{candidate_id}
Content-Type: application/json
X-API-Key: <admin_key>

{
  "action": "approve",
  "notes": "Confirmed in DrugBank; matches known CYP3A4 interaction",
  "adjusted_confidence": 0.95
}

Response: 200 OK
{
  "id": "CANDIDATE_20260324_001",
  "status": "approved",
  "promoted_to_interaction_id": "INT_SIM_KETO_001",
  "timestamp": "2026-03-24T17:30:00Z"
}
```

### 4. Pending Reviews Queue
```http
GET /api/admin/nlp/candidates?status=pending&sort=confidence_desc&limit=20

Response: 200 OK
{
  "total": 347,
  "candidates": [...]
}
```

---

## Implementation Details

### File Structure

```
medgraph/nlp/
├── __init__.py
├── ner.py                    # Named entity recognition
├── relation_extraction.py    # Rule + transformer RE
├── confidence_scorer.py      # Scoring pipeline
├── spl_parser.py            # SPL XML parsing
└── candidate_manager.py      # CRUD + review workflow
```

### Integration with FastAPI

```python
from fastapi import APIRouter, Depends, HTTPException
from medgraph.nlp.candidate_manager import CandidateManager

router = APIRouter(prefix="/api/admin/nlp", tags=["nlp"])

@router.post("/extract")
async def extract_interactions(
    request: ExtractRequest,
    admin_key: str = Depends(verify_admin_key)
) -> ExtractResponse:
    manager = CandidateManager(store=get_store())
    label = fetch_openfda_label(request.drug_name)
    candidates = manager.extract_candidates(
        label,
        confidence_threshold=request.confidence_threshold
    )
    return ExtractResponse(candidates=candidates)
```

---

## Estimated Effort

| Component | Effort | Notes |
|-----------|--------|-------|
| SPL parsing + label fetching | 6h | Handle XML variations |
| BioBERT NER pipeline | 4h | Model loading; normalization |
| Rule-based RE patterns | 4h | Regex development + testing |
| Transformer DDI RE (custom fine-tune) | 20h | Dataset prep; training; validation |
| Confidence scoring logic | 3h | Metric design; threshold tuning |
| Negative marker detection | 2h | Pattern development |
| Review workflow API | 6h | CRUD endpoints; candidate management |
| Tests + integration | 8h | Mock OpenFDA; e2e extraction tests |
| **Total** | **53h** | ~6–7 days dev + 2 days review |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| NLP accuracy plateau (< 80% F1) | High | Use ensemble: rule + BioBERT + PubMedBERT; human validation gate |
| Model bias (underrepresented drugs) | Medium | Evaluate on diverse drug classes; track precision-recall by drug class |
| False positives flood review queue | Medium | Aggressively filter by confidence; use negative markers; interactive thresholding |
| Label format variation (non-standard SPL) | Medium | Test on 50+ diverse labels first; fallback to plaintext extraction |
| Computational cost (inference overhead) | Low | Run extraction asynchronously; cache model in memory; batch inference |
| Data privacy (expose proprietary label data) | Low | Never log full label text; only store extracted entities |

---

## Testing Strategy

### Unit Tests
- SPL parsing edge cases (malformed XML, missing sections)
- NER accuracy on curated test set (e.g., BioCreative corpus subset)
- Rule-based RE pattern matching
- Confidence scoring edge cases

### Integration Tests
- E2E extraction on 20 diverse drug labels (manual validation)
- BioBERT vs rule-based accuracy comparison
- Negative marker filtering correctness

### Human Validation
- Pharmacist review of 100 high-confidence candidates (>0.85)
- Precision/recall calculation vs manual gold standard

---

## Future Work (v0.5.0+)

1. **Few-Shot Learning**: Fine-tune models on user-approved candidates (active learning)
2. **Ensemble Methods**: Stack BioBERT + PubMedBERT + rule-based; use voting
3. **Temporal Analysis**: Track extraction confidence over label versions
4. **Feedback Loop**: User rejects → retrain confidence scorer
5. **Cross-Label Synthesis**: Compare interactions across multiple labels for same drug

---

## References

- BioBERT Model: https://github.com/dmis-lab/biobert
- FDA SPL Standard: https://www.fda.gov/drugs/structured-product-labeling
- DailyMed API: https://dailymed.nlm.nih.gov/
- BioCreative DDI Challenge: https://www.biocreative.org/tasks/biocreative-vi/track-5-drug-drug-interaction/
- Hugging Face NLP Pipelines: https://huggingface.co/docs/transformers/tasks/token_classification
- BioBERT DDI Extraction Paper: https://doi.org/10.1038/s41598-025-21782-0
