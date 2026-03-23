import { describe, it, expect, vi } from "vitest";
import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { renderWithProviders } from "@/test/test-utils";
import { ErrorBoundary } from "@/components/error-boundary";

// Component that throws on render
function ThrowingComponent({ shouldThrow = true }: { shouldThrow?: boolean }) {
  if (shouldThrow) {
    throw new Error("Test error");
  }
  return <div>No error</div>;
}

describe("ErrorBoundary", () => {
  // Suppress React error boundary console.error noise in tests
  const originalError = console.error;
  beforeEach(() => {
    console.error = vi.fn();
  });
  afterEach(() => {
    console.error = originalError;
  });

  it("renders children when no error occurs", () => {
    renderWithProviders(
      <ErrorBoundary>
        <div>Child content</div>
      </ErrorBoundary>
    );
    expect(screen.getByText("Child content")).toBeInTheDocument();
  });

  it("shows fallback UI when child throws", () => {
    renderWithProviders(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    );
    expect(screen.getByText("Something went wrong")).toBeInTheDocument();
    expect(screen.getByText("Try Again")).toBeInTheDocument();
    expect(screen.getByText("Refresh Page")).toBeInTheDocument();
  });

  it("does NOT expose stack trace to user", () => {
    renderWithProviders(
      <ErrorBoundary>
        <ThrowingComponent />
      </ErrorBoundary>
    );
    // Should not show the actual error message in the UI
    expect(screen.queryByText("Test error")).not.toBeInTheDocument();
  });

  it("recovers after clicking Try Again", async () => {
    let shouldThrow = true;
    function ToggleComponent() {
      if (shouldThrow) throw new Error("Boom");
      return <div>Recovered</div>;
    }

    renderWithProviders(
      <ErrorBoundary>
        <ToggleComponent />
      </ErrorBoundary>
    );

    expect(screen.getByText("Something went wrong")).toBeInTheDocument();

    // Fix the error condition before retry
    shouldThrow = false;
    const user = userEvent.setup();
    await user.click(screen.getByText("Try Again"));

    expect(screen.getByText("Recovered")).toBeInTheDocument();
  });

  it("renders custom fallback when provided", () => {
    renderWithProviders(
      <ErrorBoundary fallback={<div>Custom fallback</div>}>
        <ThrowingComponent />
      </ErrorBoundary>
    );
    expect(screen.getByText("Custom fallback")).toBeInTheDocument();
  });
});
