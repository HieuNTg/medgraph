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

export interface CheckResponse {
  drugs: Drug[];
  interactions: InteractionResult[];
  overall_risk: string;
  overall_score: number;
  drug_count: number;
  interaction_count: number;
  timestamp: string;
  disclaimer: string;
}

export interface SearchResult {
  id: string;
  name: string;
  brand_names: string[];
  drug_class: string | null;
}
