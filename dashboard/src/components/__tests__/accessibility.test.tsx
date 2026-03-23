import { describe, it, expect, vi } from "vitest";
import { render } from "@testing-library/react";
import { axe } from "vitest-axe";
import { ErrorDisplay } from "@/components/error-display";
import { SearchResultsSkeleton, AnalysisSkeleton } from "@/components/loading-skeleton";
import { renderWithProviders } from "@/test/test-utils";
import { DrugInput } from "@/components/drug-input";

// Mock API for DrugInput
vi.mock("@/lib/api", () => ({
  searchDrugs: vi.fn().mockResolvedValue([]),
}));

describe("Accessibility (axe-core)", () => {
  it("ErrorDisplay has no a11y violations", async () => {
    const { container } = render(
      <ErrorDisplay message="Test error" onRetry={() => {}} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("SearchResultsSkeleton has no a11y violations", async () => {
    const { container } = render(<SearchResultsSkeleton />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("AnalysisSkeleton has no a11y violations", async () => {
    const { container } = render(<AnalysisSkeleton />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("DrugInput has no a11y violations", async () => {
    const { container } = renderWithProviders(
      <DrugInput onSubmit={() => {}} />
    );
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
