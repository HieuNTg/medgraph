// Lightweight offline interaction checker.
// Uses IndexedDB data — no full cascade BFS, just direct interaction lookup + basic scoring.

import type { OfflineStore } from "./offline-store";

export interface OfflineCheckResult {
  interactions: {
    drug_a: string;
    drug_b: string;
    severity: string;
    description: string;
  }[];
  risk_score: number;
  risk_level: string;
  is_offline: true;
}

// Simple severity → numeric weight mapping (mirrors backend scorer)
const SEVERITY_WEIGHTS: Record<string, number> = {
  critical: 90,
  major: 70,
  moderate: 40,
  minor: 15,
  none: 0,
};

function classifyRisk(score: number): string {
  if (score >= 80) return "critical";
  if (score >= 60) return "major";
  if (score >= 35) return "moderate";
  return "minor";
}

/**
 * Check drug interactions offline using IndexedDB data.
 *
 * @param drugIds - List of drug IDs to check (must have been synced via OfflineStore)
 * @param store   - Initialized OfflineStore instance
 * @returns OfflineCheckResult with interactions and a basic risk score
 */
export async function checkOffline(
  drugIds: string[],
  store: OfflineStore
): Promise<OfflineCheckResult> {
  if (drugIds.length < 2) {
    return {
      interactions: [],
      risk_score: 0,
      risk_level: "minor",
      is_offline: true,
    };
  }

  const rawInteractions = await store.getInteractions(drugIds);

  // Map drug IDs to names for display
  const drugNames: Record<string, string> = {};
  for (const id of drugIds) {
    const results = await store.searchDrugs("");
    const match = results.find((d) => d.id === id);
    if (match) drugNames[id] = match.name;
    else drugNames[id] = id;
  }

  const interactions = rawInteractions.map((i) => ({
    drug_a: drugNames[i.drug_a_id] ?? i.drug_a_id,
    drug_b: drugNames[i.drug_b_id] ?? i.drug_b_id,
    severity: i.severity,
    description: i.description,
  }));

  // Basic scoring: take worst severity as base, add minor burden per interaction
  const severityScores = rawInteractions.map(
    (i) => SEVERITY_WEIGHTS[i.severity] ?? 0
  );
  const maxScore = severityScores.length > 0 ? Math.max(...severityScores) : 0;
  const burdenBonus = Math.min(10, rawInteractions.length * 2);
  const risk_score = Math.min(100, maxScore + burdenBonus);

  return {
    interactions,
    risk_score,
    risk_level: classifyRisk(risk_score),
    is_offline: true,
  };
}
