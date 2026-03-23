import { describe, it, expect, vi, beforeEach } from "vitest";
import { searchDrugs, checkInteractions, getDrug, getStats } from "@/lib/api";

// Mock global fetch
const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

function mockOk(data: unknown) {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve(data),
  } as Response);
}

function mockError(status: number, body = "Error") {
  mockFetch.mockResolvedValueOnce({
    ok: false,
    status,
    statusText: "Server Error",
    text: () => Promise.resolve(body),
  } as unknown as Response);
}

beforeEach(() => {
  mockFetch.mockReset();
});

describe("searchDrugs", () => {
  it("calls correct URL with encoded query", async () => {
    mockOk([{ id: "DB1", name: "Aspirin" }]);
    await searchDrugs("asp irin");
    expect(mockFetch).toHaveBeenCalledWith(
      "/api/drugs/search?q=asp%20irin",
      expect.objectContaining({
        headers: { "Content-Type": "application/json" },
      })
    );
  });

  it("returns search results", async () => {
    const data = [{ id: "DB1", name: "Aspirin", brand_names: [], drug_class: null }];
    mockOk(data);
    const result = await searchDrugs("asp");
    expect(result).toEqual(data);
  });
});

describe("checkInteractions", () => {
  it("sends POST with drug names", async () => {
    mockOk({ drugs: [], interactions: [] });
    await checkInteractions(["Warfarin", "Aspirin"]);
    expect(mockFetch).toHaveBeenCalledWith(
      "/api/check",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          drugs: ["Warfarin", "Aspirin"],
          metabolizer_phenotypes: null,
        }),
      })
    );
  });

  it("includes metabolizer phenotypes when provided", async () => {
    mockOk({ drugs: [], interactions: [] });
    await checkInteractions(["Warfarin"], { CYP2D6: "poor" });
    const body = JSON.parse(mockFetch.mock.calls[0][1].body);
    expect(body.metabolizer_phenotypes).toEqual({ CYP2D6: "poor" });
  });
});

describe("getDrug", () => {
  it("fetches drug by ID", async () => {
    const drug = { id: "DB00682", name: "Warfarin" };
    mockOk(drug);
    const result = await getDrug("DB00682");
    expect(result).toEqual(drug);
    expect(mockFetch).toHaveBeenCalledWith(
      "/api/drugs/DB00682",
      expect.any(Object)
    );
  });
});

describe("getStats", () => {
  it("returns stats object", async () => {
    const stats = { drug_count: 507, interaction_count: 179, enzyme_count: 8 };
    mockOk(stats);
    const result = await getStats();
    expect(result).toEqual(stats);
  });
});

describe("API error handling", () => {
  it("throws on non-ok response", async () => {
    mockError(500, "Internal Server Error");
    await expect(searchDrugs("test")).rejects.toThrow("API error 500");
  });

  it("includes response body in error message", async () => {
    mockError(404, "Drug not found");
    await expect(getDrug("INVALID")).rejects.toThrow("Drug not found");
  });
});
