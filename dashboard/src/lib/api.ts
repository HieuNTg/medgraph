import type { CheckResponse, Drug, SearchResult } from "./types";

const API_BASE = "";

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
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

export function checkInteractions(drugs: string[]): Promise<CheckResponse> {
  return apiFetch("/api/check", {
    method: "POST",
    body: JSON.stringify({ drugs }),
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

export async function exportPdfReport(
  checkResult: CheckResponse,
  graphPngB64?: string
): Promise<Blob> {
  const res = await fetch("/api/report/pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
