export interface Drug {
  id: string;
  name: string;
  brand_names: string[];
  drug_class: string | null;
  enzyme_relations: EnzymeRelation[];
  category?: string;
}

export interface EnzymeRelation {
  enzyme_name: string;
  relation_type: "metabolized_by" | "inhibits" | "induces";
  strength: "strong" | "moderate" | "weak";
}

export interface InteractionResult {
  drug_a: Drug;
  drug_b: Drug;
  severity: "critical" | "major" | "moderate" | "minor";
  risk_score: number;
  description: string;
  mechanism: string | null;
  cascade_paths: CascadePath[];
  evidence: Evidence[];
  evidence_level?: string;
  source_citation?: string;
  confidence_score?: number;
  confidence_level?: string;
  confidence_factors?: string[];
}

export interface CascadePath {
  steps: CascadeStep[];
  description: string;
  net_severity: string;
}

export interface CascadeStep {
  source: string;
  target: string;
  relation: string;
  effect: string;
}

export interface Evidence {
  source: string;
  description: string;
  case_count: number | null;
  url: string | null;
}

export interface FoodInteractionResponse {
  food_name: string;
  food_category: string;
  drug_id: string;
  severity: string;
  description: string;
  mechanism: string | null;
  evidence_level: string;
}

export interface CheckResponse {
  drugs: Drug[];
  interactions: InteractionResult[];
  overall_risk: string;
  overall_score: number;
  drug_count: number;
  interaction_count: number;
  timestamp: string;
  disclaimer: string;
  food_interactions?: FoodInteractionResponse[];
}

export interface SearchResult {
  id: string;
  name: string;
  brand_names: string[];
  drug_class: string | null;
}

// ── Graph / Advanced Analysis Types ──────────────────────────────────────────

export interface PathwayNode {
  id: string;
  type: "drug" | "enzyme";
  label: string;
}

export interface PathwayEdge {
  source: string;
  target: string;
  relation: string;
  strength: string | null;
}

export interface PathwayResponse {
  nodes: PathwayNode[];
  edges: PathwayEdge[];
  cascades: Record<string, unknown>[];
}

export interface AlternativeResponse {
  drug_id: string;
  drug_name: string;
  reason: string;
  enzyme_overlap_count: number;
}

export interface HubDrugResponse {
  drug_id: string;
  drug_name: string;
  betweenness: number;
  pagerank: number;
  interaction_count: number;
}

export interface DeprescribingResponse {
  drug_id: string;
  drug_name: string;
  removal_benefit: number;
  interactions_resolved: number;
  rationale: string;
  order: number;
}

export interface PolypharmacyResponse {
  polypharmacy_score: number;
  risk_level: string;
  risk_clusters: Record<string, unknown>[];
  summary: string;
}

export interface ContraindicationNode {
  id: string;
  label: string;
}

export interface ContraindicationEdge {
  source: string;
  target: string;
  severity: string;
  label?: string;
}

export interface ContraindicationResponse {
  nodes: ContraindicationNode[];
  edges: ContraindicationEdge[];
  clusters: Record<string, unknown>[];
}

// ── Auth / Profile / History Types ───────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  display_name: string | null;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface MedicationProfile {
  id: string;
  name: string;
  drug_ids: string[];
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface AnalysisHistoryEntry {
  id: string;
  drug_ids: string[];
  overall_risk: string;
  created_at: string;
}

export interface OptimizationResult {
  original_risk: number;
  optimized_risk: number;
  drugs_to_remove: string[];
  alternative_regimens: Record<string, unknown>[];
  rationale: string;
  disclaimer: string;
}

// ── PGx / Confidence Types ────────────────────────────────────────────────────

export interface PGxAlert {
  drug_name: string;
  gene: string;
  phenotype: string;
  recommendation: string;
  severity_multiplier: number;
  population_frequency: number | null;
}

export interface ConfidenceInfo {
  score: number;
  level: string;
  factors: string[];
}

// ── Schedule Types ────────────────────────────────────────────────────────────

export interface ScheduleSlot {
  time: string;
  label: string;
  drugs: string[];
}

export interface ScheduleResponse {
  slots: ScheduleSlot[];
  warnings: string[];
}
