# GNN-Based Drug-Drug Interaction Prediction Design

**Phase 5.3 Design Document**
**Status**: Design Phase
**Target Release**: v0.5.0–v1.0.0 (Q1–Q2 2027)

---

## Executive Summary

Design for predicting novel drug-drug interactions using Graph Neural Networks. Learns from known interactions encoded as edges in the knowledge graph. Generates candidate predictions with confidence scores for prospective validation. Bridges gap between rule-based cascade detection and data-driven discovery.

---

## Problem Statement

**Current State**:
- MEDGRAPH uses rule-based cascade detection: inhibition chains via CYP450
- Operates on curated 500+ drug × 179 interaction edge set
- No learning mechanism; cannot predict unseen interaction pairs
- Cascade rules miss indirect pharmacological effects (e.g., protein binding competition)

**Gaps**:
1. Hard-coded inhibition/induction/substrate rules → inflexible
2. No representation learning of drug similarity
3. Cannot extrapolate beyond known enzyme pathways
4. New drugs have zero baseline predictions until manually reviewed

---

## Proposed Architecture

### High-Level Flow

```
┌─ Knowledge Graph Construction ────────┐
│ ├─ Drug nodes (features: fingerprint) │
│ ├─ Enzyme nodes (features: gene data) │
│ ├─ Known interaction edges (labels)   │
│ └─ Food/supplement nodes              │
│                                       │
├─ Negative Sampling                    │
│ ├─ Random non-interacting pairs       │
│ ├─ Confidence-based hard negatives    │
│ └─ Ensure class balance (1:10)        │
│                                       │
├─ Feature Engineering                  │
│ ├─ Drug: ECFP fingerprint + DeepChem  │
│ ├─ Enzyme: gene expression (optional) │
│ └─ Graph structure: 1/2-hop neighbors │
│                                       │
├─ GNN Model Training                   │
│ ├─ Architecture: GAT / GraphSAGE      │
│ ├─ Loss: Binary cross-entropy + L2    │
│ ├─ Validation: 80/10/10 split         │
│ └─ Early stopping on val AUC          │
│                                       │
├─ Inference & Scoring                  │
│ ├─ Generate predictions for all       │
│ │   unseen drug pairs                 │
│ ├─ Confidence = model output logit    │
│ ├─ Rank by descending score           │
│ └─ Filter: confidence > threshold     │
│                                       │
├─ Human Validation Workflow            │
│ ├─ Pharmacist reviews top candidates  │
│ ├─ Approved → add to interaction DB   │
│ └─ Rejected → log as hard negative    │
│                                       │
└─ Continuous Improvement               │
    ├─ Feedback loop: approved → retrain│
    └─ Quarterly model retraining       │
```

---

## Graph Neural Network Architecture

### Architecture Choice: Graph Attention Network (GAT)

Compared architectures:

| Model | Key Strength | Weakness | Fit for MEDGRAPH |
|-------|--------------|----------|-----------------|
| **GraphSAGE** | Efficient sampling; inductive | Less attention to heterogeneous types | Good for scale-up |
| **GAT** | Multi-head attention; interpretable | Quadratic complexity O(n²) | **CHOSEN for v0.5.0** |
| **RGCN** | Relation types (5+ edge types) | Higher memory; slower training | Better for multi-relation graphs |
| **GIN** | Simple; universal approximator | Less interpretable | Baseline comparator |

**Why GAT for v0.5.0?**
1. Current graph is small (500 drugs + 8 enzymes + 179 edges) → O(n²) acceptable
2. Attention weights interpretable (which drug neighbors matter for prediction?)
3. Proven effective on biomedical networks (recent benchmarks 2024–2025)
4. Can add relation types later (upgrade to RGCN if needed)

**Upgrade Path**: GraphSAGE for v1.0.0+ if scaling beyond 5K drugs.

### GAT Model Definition

```python
import torch
import torch.nn as nn
from torch_geometric.nn import GATConv, global_mean_pool

class DrugInteractionGAT(nn.Module):
    """
    Graph Attention Network for DDI prediction.
    Input: Drug nodes + enzyme nodes with features.
    Output: Probability of interaction for drug pairs.
    """

    def __init__(self, input_dim: int, hidden_dim: int, num_heads: int = 8):
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads

        # Layer 1: Multi-head attention
        self.gat1 = GATConv(
            input_dim,
            hidden_dim,
            heads=num_heads,
            dropout=0.2,
            concat=False  # Average heads, not concatenate
        )

        # Layer 2: Deeper attention
        self.gat2 = GATConv(
            hidden_dim,
            hidden_dim,
            heads=num_heads,
            dropout=0.2,
            concat=False
        )

        # Output layer: pairwise edge prediction
        self.edge_mlp = nn.Sequential(
            nn.Linear(2 * hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 1),  # Logit for binary classification
        )

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Node features (n_nodes, input_dim)
            edge_index: Graph connectivity (2, n_edges)

        Returns:
            node_embeddings: (n_nodes, hidden_dim)
        """
        # GAT layers with activation
        x = self.gat1(x, edge_index)
        x = nn.functional.relu(x)
        x = self.gat2(x, edge_index)
        return x

    def predict_interaction(
        self,
        node_embeddings: torch.Tensor,
        drug_a_idx: int,
        drug_b_idx: int
    ) -> torch.Tensor:
        """Predict interaction probability between two drugs."""
        # Concatenate embeddings
        pair_embedding = torch.cat([
            node_embeddings[drug_a_idx],
            node_embeddings[drug_b_idx]
        ])
        logit = self.edge_mlp(pair_embedding)
        probability = torch.sigmoid(logit)
        return probability
```

---

## Training Data Preparation

### Known Interactions (Positive Examples)

**Source**: `store.get_all_interactions()`
- ~179 known interaction edges from seed data + OpenFDA
- Split: 80% train, 10% val, 10% test

```python
def load_positive_edges(store: GraphStore) -> torch.Tensor:
    """Load known interactions as positive training edges."""
    interactions = store.get_all_interactions()
    edge_pairs = []
    for interaction in interactions:
        drug_a_idx = drug_id_to_index[interaction.drug_a_id]
        drug_b_idx = drug_id_to_index[interaction.drug_b_id]
        edge_pairs.append([drug_a_idx, drug_b_idx])
        # Bidirectional assumption (DDI is symmetric)
        edge_pairs.append([drug_b_idx, drug_a_idx])
    return torch.tensor(edge_pairs).t().contiguous()
```

### Negative Sampling Strategy

**Problem**: Only 179 known interactions among ~500 drugs → 25,000 possible pairs. Class imbalance 1:140.

**Solution**: Hard negative sampling (higher learning signal)

```python
class NegativeSampler:
    def __init__(self, store: GraphStore, ratio: int = 10):
        self.store = store
        self.ratio = ratio  # 10 negatives per positive

    def sample_hard_negatives(self, known_edges: torch.Tensor) -> torch.Tensor:
        """
        Sample negatives with moderate confidence (0.3–0.7).
        Easy negatives (confidence << 0.1) are uninformative.
        """
        # Get all drug pairs
        n_drugs = len(self.drug_index_map)
        all_pairs = []
        for i in range(n_drugs):
            for j in range(i+1, n_drugs):
                all_pairs.append((i, j))

        known_set = set((e[0].item(), e[1].item()) for e in known_edges.t())

        # Sample candidates with moderate rule-based interaction confidence
        negatives = []
        for i, j in all_pairs:
            if (i, j) in known_set or (j, i) in known_set:
                continue
            # Compute rule-based confidence (enzyme overlap, etc.)
            rule_confidence = self._compute_rule_confidence(i, j)
            if 0.3 <= rule_confidence <= 0.7:  # Hard negatives
                negatives.append([i, j])
            if len(negatives) >= len(known_edges.t()) * self.ratio:
                break

        return torch.tensor(negatives).t().contiguous()

    def _compute_rule_confidence(self, drug_i: int, drug_j: int) -> float:
        """
        Existing rule-based interaction confidence
        (enzyme overlap + inhibition strength, etc.).
        """
        # Placeholder — use MEDGRAPH cascade analyzer
        from medgraph.engine.analyzer import CascadeAnalyzer
        analyzer = CascadeAnalyzer(self.store)
        result = analyzer.analyze([self.index_to_drug[drug_i], self.index_to_drug[drug_j]])
        return result.overall_score / 100.0
```

### Node Features

**Drug Node Features** (ECFP fingerprint):

```python
from rdkit import Chem
from rdkit.Chem import AllChem

def compute_drug_features(drug: Drug) -> np.ndarray:
    """
    Compute ECFP (Extended Connectivity Fingerprint) for drug.
    SMILES must be resolved from DrugBank or PubChem.
    """
    smiles = resolve_smiles(drug.id)  # DrugBank/PubChem lookup
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        # Fallback: random feature vector if SMILES unavailable
        return np.random.randn(2048).astype(np.float32)

    # ECFP4: radius=2, n_bits=2048
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048)
    return np.array(fp, dtype=np.float32)  # Sparse binary vector

def build_node_features(store: GraphStore) -> torch.Tensor:
    """Build feature matrix for all drugs + enzymes."""
    features = []
    for drug in store.get_all_drugs():
        fp = compute_drug_features(drug)
        features.append(fp)

    # Enzyme features: one-hot encoding (8 enzymes)
    n_enzymes = len(store.get_all_enzymes())
    for i, enzyme in enumerate(store.get_all_enzymes()):
        one_hot = np.zeros(2048)  # Pad to match ECFP dimension
        one_hot[:n_enzymes][i] = 1.0
        features.append(one_hot)

    return torch.tensor(np.array(features), dtype=torch.float32)
```

**Enzyme Node Features** (optional; simpler: one-hot):

```python
# Enzyme features: one-hot + gene expression (if available)
enzyme_features = torch.eye(n_enzymes, dtype=torch.float32)
# Optionally: append normalized expression levels from GTEx (future)
```

---

## Model Training

### Training Loop

```python
import torch.optim as optim
from torch_geometric.data import Data
from sklearn.metrics import roc_auc_score, precision_recall_curve

class DDITrainer:
    def __init__(self, model: DrugInteractionGAT, learning_rate: float = 1e-3):
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.criterion = nn.BCEWithLogitsLoss()

    def train_epoch(self, data: Data, pos_edges: torch.Tensor, neg_edges: torch.Tensor) -> float:
        """Train for one epoch."""
        self.model.train()

        # Forward pass
        node_embeddings = self.model(data.x, data.edge_index)

        # Positive edges
        pos_preds = []
        for drug_a_idx, drug_b_idx in pos_edges.t():
            pred = self.model.predict_interaction(node_embeddings, drug_a_idx, drug_b_idx)
            pos_preds.append(pred)
        pos_labels = torch.ones(len(pos_preds), dtype=torch.float32)

        # Negative edges
        neg_preds = []
        for drug_a_idx, drug_b_idx in neg_edges.t():
            pred = self.model.predict_interaction(node_embeddings, drug_a_idx, drug_b_idx)
            neg_preds.append(pred)
        neg_labels = torch.zeros(len(neg_preds), dtype=torch.float32)

        # Combine
        all_preds = torch.cat(pos_preds + neg_preds)
        all_labels = torch.cat([pos_labels, neg_labels])

        # Loss + backprop
        loss = self.criterion(all_preds, all_labels)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()

        return loss.item()

    def evaluate(self, node_embeddings: torch.Tensor, edges: torch.Tensor, labels: torch.Tensor) -> dict:
        """Compute metrics on validation/test set."""
        self.model.eval()
        with torch.no_grad():
            preds = []
            for drug_a_idx, drug_b_idx in edges.t():
                pred = self.model.predict_interaction(node_embeddings, drug_a_idx, drug_b_idx)
                preds.append(pred.item())

            preds = np.array(preds)
            labels = labels.cpu().numpy()

            auc = roc_auc_score(labels, preds)
            precision, recall, _ = precision_recall_curve(labels, preds)
            pr_auc = -np.trapz(precision, recall)

        return {
            'auc': auc,
            'pr_auc': pr_auc,
            'predictions': preds
        }

# Training loop
def train(model, store, epochs=50, patience=10):
    # Build graph data
    node_features = build_node_features(store)
    all_edges = get_graph_edges(store)
    positive_edges = load_positive_edges(store)
    negative_edges = NegativeSampler(store, ratio=10).sample_hard_negatives(positive_edges)

    # Split data
    n_pos = positive_edges.shape[1]
    train_pos, val_pos, test_pos = train_test_split(positive_edges.t(), test_size=0.2)
    train_neg, val_neg, test_neg = train_test_split(negative_edges.t(), test_size=0.2)

    trainer = DDITrainer(model)
    best_val_auc = 0.0
    patience_counter = 0

    for epoch in range(epochs):
        loss = trainer.train_epoch(data, positive_edges, negative_edges)

        # Evaluate on validation set
        val_edges = torch.cat([val_pos, val_neg], dim=0)
        val_labels = torch.cat([torch.ones(len(val_pos)), torch.zeros(len(val_neg))])
        node_embeddings = model(data.x, data.edge_index)
        metrics = trainer.evaluate(node_embeddings, val_edges.t(), val_labels)

        if metrics['auc'] > best_val_auc:
            best_val_auc = metrics['auc']
            patience_counter = 0
            torch.save(model.state_dict(), 'best_gnn_model.pt')
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

        if epoch % 5 == 0:
            print(f"Epoch {epoch}: loss={loss:.4f}, val_auc={metrics['auc']:.4f}")

    # Evaluate on test set
    test_edges = torch.cat([test_pos, test_neg], dim=0)
    test_labels = torch.cat([torch.ones(len(test_pos)), torch.zeros(len(test_neg))])
    model.load_state_dict(torch.load('best_gnn_model.pt'))
    test_metrics = trainer.evaluate(node_embeddings, test_edges.t(), test_labels)
    print(f"Test AUC: {test_metrics['auc']:.4f}, PR-AUC: {test_metrics['pr_auc']:.4f}")
```

---

## Inference & Prediction Generation

### Batch Prediction

```python
def predict_novel_interactions(
    model: DrugInteractionGAT,
    store: GraphStore,
    confidence_threshold: float = 0.6,
    top_k: int = 100
) -> list[InteractionPrediction]:
    """
    Generate predictions for all unseen drug pairs.
    Returns ranked list of novel interaction candidates.
    """
    model.eval()
    all_drugs = store.get_all_drugs()
    known_pairs = {
        (i.drug_a_id, i.drug_b_id)
        for i in store.get_all_interactions()
    }

    predictions = []

    with torch.no_grad():
        node_embeddings = model(data.x, data.edge_index)

        for i, drug_a in enumerate(all_drugs):
            for j, drug_b in enumerate(all_drugs):
                if i >= j:
                    continue
                if (drug_a.id, drug_b.id) in known_pairs:
                    continue

                pred_prob = model.predict_interaction(
                    node_embeddings, i, j
                ).item()

                if pred_prob >= confidence_threshold:
                    predictions.append(InteractionPrediction(
                        drug_a_id=drug_a.id,
                        drug_b_id=drug_b.id,
                        drug_a_name=drug_a.name,
                        drug_b_name=drug_b.name,
                        predicted_probability=pred_prob,
                        model_version="gat-v0.5.0",
                        confidence_score=pred_prob,
                        reasoning="GAT model learned from known interactions"
                    ))

    # Sort by descending confidence
    predictions.sort(key=lambda x: x.predicted_probability, reverse=True)
    return predictions[:top_k]
```

---

## API Design

### 1. Generate Predictions
```http
POST /api/admin/gnn/predict
Content-Type: application/json
X-API-Key: <admin_key>

{
  "confidence_threshold": 0.65,
  "top_k": 200,
  "model_version": "gat-v0.5.0"
}

Response: 200 OK
{
  "total_candidates": 347,
  "predictions": [
    {
      "id": "PRED_20260324_001",
      "drug_a_id": "DB00641",
      "drug_a_name": "Simvastatin",
      "drug_b_id": "DB00758",
      "drug_b_name": "Clopidogrel",
      "predicted_probability": 0.82,
      "confidence_score": 0.82,
      "reasoning": "GAT attention identified shared CYP3A4 + platelet effect overlap",
      "status": "pending_review"
    },
    ...
  ],
  "model_info": {
    "version": "gat-v0.5.0",
    "train_auc": 0.91,
    "test_auc": 0.88,
    "trained_at": "2026-03-20T00:00:00Z"
  }
}
```

### 2. Review Prediction
```http
PATCH /api/admin/gnn/predictions/{prediction_id}
Content-Type: application/json
X-API-Key: <admin_key>

{
  "action": "approve",
  "adjusted_severity": "major",
  "mechanism": "Clopidogrel inhibits CYP3A4; Simvastatin substrate",
  "notes": "Confirmed mechanism; high clinical relevance"
}

Response: 200 OK
{
  "id": "PRED_20260324_001",
  "status": "approved",
  "promoted_to_interaction_id": "INT_SIM_CLOP_001",
  "timestamp": "2026-03-24T18:15:00Z"
}
```

### 3. Model Training Job
```http
POST /api/admin/gnn/train
Content-Type: application/json
X-API-Key: <admin_key>

{
  "epochs": 50,
  "learning_rate": 0.001,
  "negative_sampling_ratio": 10,
  "async": true
}

Response: 202 Accepted
{
  "job_id": "gnn_train_20260324_1645",
  "status": "queued"
}
```

---

## Estimated Effort

| Component | Effort | Notes |
|-----------|--------|-------|
| GAT model architecture + PyTorch Geometric setup | 10h | Model definition; device handling |
| Feature engineering (ECFP + enzymes) | 8h | SMILES resolution; RDKit integration |
| Negative sampling strategy | 6h | Hard negative sampling; validation |
| Training loop + validation | 6h | Early stopping; hyperparameter tuning |
| Inference + batch prediction | 4h | Top-k ranking; threshold tuning |
| API endpoints (review workflow) | 6h | Admin endpoints; status tracking |
| Tests + baselines | 8h | Unit tests; GAT vs GIN/GraphSAGE comparison |
| Documentation + report | 4h | Architecture docs; results analysis |
| **Total** | **52h** | ~6–7 days dev + 2 days review |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Class imbalance (179 pos vs ~25K neg pairs) | High | Hard negative sampling (0.3–0.7 rule confidence); focal loss (v0.6.0) |
| Cold start (new drugs with no neighbors) | Medium | Use drug fingerprint features; add similarity-based fallback (Tanimoto) |
| Overfitting on small dataset | Medium | L2 regularization; dropout; early stopping; k-fold CV |
| Model drift over time | Low | Quarterly retraining; track test AUC on held-out test set |
| SMILES resolution bottleneck | Medium | Batch RxNorm/PubChem lookup; fallback to random features |
| Computational cost (training) | Low | Train on CPU initially; GPU optional (< 30s/epoch on 500 drugs) |

---

## Testing Strategy

### Benchmarks
- **Baseline 1**: Rule-based MEDGRAPH cascade (current)
- **Baseline 2**: GIN model (simpler architecture)
- **Target**: GAT F1 > 0.80 on test set (vs baselines ~0.65–0.70)

### Validation
- 80/10/10 train/val/test split
- 5-fold cross-validation on full dataset
- Pharmacist review of top 50 predictions (gold standard)

---

## Future Work (v1.0.0+)

1. **RGCN for Multi-Relation Graphs**: Support edge type heterogeneity (inhibition vs induction vs substrate)
2. **GraphSAGE for Inductive Learning**: Predict interactions for new drugs without retraining
3. **Temporal GNN**: Model interaction emergence over time
4. **Explainability**: Attention visualization; LIME/SHAP for prediction rationale
5. **Ensemble**: Stack GAT + RGCN + similarity-based methods

---

## References

- Recent GNN for DDI: https://www.nature.com/articles/s41598-025-12936-1
- GAT Paper: https://arxiv.org/abs/1710.10903
- PyTorch Geometric: https://pytorch-geometric.readthedocs.io/
- Morgan Fingerprints (ECFP): https://rdkit.org/
- GNN Benchmarks (2024–2025): https://link.springer.com/article/10.1007/s10462-023-10669-z
- DrugBank DDI Dataset: https://go.drugbank.com/
