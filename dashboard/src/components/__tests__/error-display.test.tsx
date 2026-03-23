import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErrorDisplay } from "@/components/error-display";

describe("ErrorDisplay", () => {
  it("renders default error message", () => {
    render(<ErrorDisplay />);
    expect(
      screen.getByText("Something went wrong. Please try again.")
    ).toBeInTheDocument();
  });

  it("renders custom message", () => {
    render(<ErrorDisplay message="Network timeout" />);
    expect(screen.getByText("Network timeout")).toBeInTheDocument();
  });

  it("shows retry button when onRetry provided", () => {
    render(<ErrorDisplay onRetry={() => {}} />);
    expect(screen.getByText("Try Again")).toBeInTheDocument();
  });

  it("hides retry button when no onRetry", () => {
    render(<ErrorDisplay />);
    expect(screen.queryByText("Try Again")).not.toBeInTheDocument();
  });

  it("calls onRetry when retry clicked", async () => {
    const onRetry = vi.fn();
    const user = userEvent.setup();
    render(<ErrorDisplay onRetry={onRetry} />);
    await user.click(screen.getByText("Try Again"));
    expect(onRetry).toHaveBeenCalledOnce();
  });

  it("has alert role for accessibility", () => {
    render(<ErrorDisplay />);
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });
});
