import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import {
  SearchResultsSkeleton,
  AnalysisSkeleton,
} from "@/components/loading-skeleton";

describe("SearchResultsSkeleton", () => {
  it("renders with status role", () => {
    render(<SearchResultsSkeleton />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("includes sr-only loading text", () => {
    render(<SearchResultsSkeleton />);
    expect(
      screen.getByText("Loading search results...")
    ).toBeInTheDocument();
  });
});

describe("AnalysisSkeleton", () => {
  it("renders with status role", () => {
    render(<AnalysisSkeleton />);
    expect(screen.getByRole("status")).toBeInTheDocument();
  });

  it("includes sr-only loading text", () => {
    render(<AnalysisSkeleton />);
    expect(
      screen.getByText("Loading analysis results...")
    ).toBeInTheDocument();
  });
});
