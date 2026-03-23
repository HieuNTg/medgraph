import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { RiskSummary } from "@/components/risk-summary";
import type { CheckResponse } from "@/lib/types";

// Mock recharts to avoid canvas rendering issues in jsdom
vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="responsive-container">{children}</div>
  ),
  PieChart: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="pie-chart">{children}</div>
  ),
  Pie: () => <div data-testid="pie" />,
  Cell: () => <div />,
  Tooltip: () => <div />,
}));

function makeResponse(overrides?: Partial<CheckResponse>): CheckResponse {
  return {
    drugs: [],
    interactions: [
      {
        drug_a: { id: "DB1", name: "DrugA", brand_names: [], drug_class: null, enzyme_relations: [] },
        drug_b: { id: "DB2", name: "DrugB", brand_names: [], drug_class: null, enzyme_relations: [] },
        severity: "major",
        risk_score: 75,
        description: "Major interaction",
        mechanism: null,
        cascade_paths: [],
        evidence: [],
      },
    ],
    overall_risk: "major",
    overall_score: 75,
    drug_count: 2,
    interaction_count: 1,
    timestamp: "2026-03-23T12:00:00Z",
    disclaimer: "Test disclaimer",
    ...overrides,
  };
}

describe("RiskSummary", () => {
  it("displays the correct risk label", () => {
    render(<RiskSummary response={makeResponse()} />);
    expect(screen.getByText("Major Risk")).toBeInTheDocument();
  });

  it("shows drug count and interaction count", () => {
    render(<RiskSummary response={makeResponse()} />);
    expect(
      screen.getByText(/2 medications analyzed/)
    ).toBeInTheDocument();
    expect(screen.getByText(/1 interaction found/)).toBeInTheDocument();
  });

  it("pluralizes interactions correctly", () => {
    render(
      <RiskSummary
        response={makeResponse({ interaction_count: 3 })}
      />
    );
    expect(screen.getByText(/3 interactions found/)).toBeInTheDocument();
  });

  it("shows safe label for no risk", () => {
    render(
      <RiskSummary
        response={makeResponse({
          overall_risk: "safe",
          interactions: [],
          interaction_count: 0,
        })}
      />
    );
    expect(screen.getByText("No Significant Risk")).toBeInTheDocument();
  });

  it("renders export button", () => {
    render(<RiskSummary response={makeResponse()} />);
    expect(screen.getByText("Export PNG")).toBeInTheDocument();
  });

  it("shows severity distribution for interactions", () => {
    render(<RiskSummary response={makeResponse()} />);
    // Should show "major" in the severity legend
    expect(screen.getByText("major")).toBeInTheDocument();
  });
});
