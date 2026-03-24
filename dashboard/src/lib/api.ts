import type {
  AlternativeResponse,
  AnalysisHistoryEntry,
  CheckResponse,
  ContraindicationResponse,
  DeprescribingResponse,
  Drug,
  HubDrugResponse,
  MedicationProfile,
  OptimizationResult,
  PathwayResponse,
  ScheduleResponse,
  SearchResult,
  TokenResponse,
  User,
} from "./types";
import { setOfflineAuthToken } from "./offline-store";

const API_BASE = "";

// ── Auth token management ─────────────────────────────────────────────────────
let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
  setOfflineAuthToken(token);
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;
  const res = await fetch(`${API_BASE}${path}`, {
    headers,
    ...options,
  });
  if (!res.ok) {
    const msg = await res.text().catch(() => res.statusText);
    throw new Error(`API error ${res.status}: ${msg}`);
  }
  return res.json() as Promise<T>;
}

export function searchDrugs(query: string): Promise<SearchResult[]> {
  return apiFetch(`/api/drugs/search?q=${encodeURIComponent(query)}`);
}

export function checkInteractions(
  drugs: string[],
  metabolizerPhenotypes?: Record<string, string>
): Promise<CheckResponse> {
  return apiFetch("/api/check", {
    method: "POST",
    body: JSON.stringify({
      drugs,
      metabolizer_phenotypes: metabolizerPhenotypes ?? null,
    }),
  });
}

export function getDrug(id: string): Promise<Drug> {
  return apiFetch(`/api/drugs/${id}`);
}

export function getStats(): Promise<{
  drug_count: number;
  interaction_count: number;
  enzyme_count: number;
}> {
  return apiFetch("/api/stats");
}

export function getAlternatives(
  drugId: string,
  regimen: string[]
): Promise<AlternativeResponse[]> {
  return apiFetch("/api/alternatives", {
    method: "POST",
    body: JSON.stringify({ drug_id: drugId, regimen }),
  });
}

export function getPathways(drugIds: string[]): Promise<PathwayResponse> {
  return apiFetch(
    `/api/v1/graph/pathways?drugs=${drugIds.map(encodeURIComponent).join(",")}`
  );
}

export function getHubDrugs(topN = 20): Promise<HubDrugResponse[]> {
  return apiFetch(`/api/v1/graph/hub-drugs?top_n=${topN}`);
}

export function getContraindications(
  drugIds: string[]
): Promise<ContraindicationResponse> {
  return apiFetch(
    `/api/v1/graph/contraindications?drugs=${drugIds.map(encodeURIComponent).join(",")}`
  );
}

export function getDeprescribingRecs(
  drugs: string[]
): Promise<DeprescribingResponse[]> {
  return apiFetch("/api/deprescribe", {
    method: "POST",
    body: JSON.stringify({ drugs }),
  });
}

export function optimizeRegimen(
  drugs: string[],
  mustKeep: string[] = []
): Promise<OptimizationResult> {
  return apiFetch("/api/v1/optimize", {
    method: "POST",
    body: JSON.stringify({ drugs, must_keep: mustKeep }),
  });
}

// ── Auth functions ────────────────────────────────────────────────────────────

export function register(
  email: string,
  password: string,
  displayName?: string
): Promise<TokenResponse> {
  return apiFetch("/api/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password, display_name: displayName ?? null }),
  });
}

export function login(email: string, password: string): Promise<TokenResponse> {
  return apiFetch("/api/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export function refreshToken(token: string): Promise<TokenResponse> {
  return apiFetch("/api/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token: token }),
  });
}

export function getMe(): Promise<User> {
  return apiFetch("/api/auth/me");
}

// ── Profile functions ─────────────────────────────────────────────────────────

export function createProfile(
  name: string,
  drugIds: string[],
  notes?: string
): Promise<MedicationProfile> {
  return apiFetch("/api/profiles", {
    method: "POST",
    body: JSON.stringify({ name, drug_ids: drugIds, notes: notes ?? null }),
  });
}

export function getProfiles(): Promise<MedicationProfile[]> {
  return apiFetch("/api/profiles");
}

export function updateProfile(
  id: string,
  data: Partial<MedicationProfile>
): Promise<MedicationProfile> {
  return apiFetch(`/api/profiles/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export function deleteProfile(id: string): Promise<void> {
  return apiFetch(`/api/profiles/${id}`, { method: "DELETE" });
}

// ── History functions ─────────────────────────────────────────────────────────

export function getHistory(
  limit = 20,
  offset = 0
): Promise<AnalysisHistoryEntry[]> {
  return apiFetch(`/api/history?limit=${limit}&offset=${offset}`);
}

// ── Sharing functions ─────────────────────────────────────────────────────────

export function shareResult(
  analysisId: string
): Promise<{ id: string; url: string }> {
  return apiFetch("/api/share", {
    method: "POST",
    body: JSON.stringify({ analysis_id: analysisId }),
  });
}

export function getSharedResult(token: string): Promise<CheckResponse> {
  return apiFetch(`/api/share/${token}`);
}

export function getSchedule(
  drugs: { name: string; frequency: number }[]
): Promise<ScheduleResponse> {
  return apiFetch("/api/v1/schedule", {
    method: "POST",
    body: JSON.stringify({ drugs }),
  });
}

export async function exportPdfReport(
  checkResult: CheckResponse,
  graphPngB64?: string
): Promise<Blob> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (authToken) headers["Authorization"] = `Bearer ${authToken}`;
  const res = await fetch("/api/report/pdf", {
    method: "POST",
    headers,
    body: JSON.stringify({
      check_result: checkResult,
      graph_png_b64: graphPngB64 ?? null,
    }),
  });
  if (!res.ok) {
    throw new Error(`PDF export failed: ${res.status}`);
  }
  return res.blob();
}
