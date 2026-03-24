import { describe, it, expect, vi } from "vitest";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { renderWithProviders } from "@/test/test-utils";
import { DrugInput } from "@/components/drug-input";

// Mock the API module
vi.mock("@/lib/api", () => ({
  searchDrugs: vi.fn().mockResolvedValue([
    { id: "DB00682", name: "Warfarin", brand_names: ["Coumadin"], drug_class: "Anticoagulant" },
    { id: "DB00945", name: "Aspirin", brand_names: ["Bayer"], drug_class: "NSAID" },
  ]),
}));

describe("DrugInput", () => {
  it("renders search input", () => {
    renderWithProviders(<DrugInput onSubmit={() => {}} />);
    expect(
      screen.getByLabelText("common.search")
    ).toBeInTheDocument();
  });

  it("shows hint text for no selection", () => {
    renderWithProviders(<DrugInput onSubmit={() => {}} />);
    expect(
      screen.getByText("checker.add_hint_0")
    ).toBeInTheDocument();
  });

  it("disables submit button with fewer than 2 drugs", () => {
    renderWithProviders(<DrugInput onSubmit={() => {}} />);
    expect(screen.getByText("checker.check_button")).toBeDisabled();
  });

  it("shows loading state when loading prop is true", () => {
    renderWithProviders(<DrugInput onSubmit={() => {}} loading />);
    expect(screen.getByText("checker.analyzing")).toBeInTheDocument();
  });

  it("has correct aria attributes on input", () => {
    renderWithProviders(<DrugInput onSubmit={() => {}} />);
    const input = screen.getByLabelText("common.search");
    expect(input).toHaveAttribute("aria-autocomplete", "list");
  });

  it("shows dropdown when typing 2+ chars", async () => {
    const user = userEvent.setup();
    renderWithProviders(<DrugInput onSubmit={() => {}} />);

    const input = screen.getByLabelText("common.search");
    await user.type(input, "war");

    // Wait for debounce + query
    await waitFor(
      () => {
        expect(screen.getByRole("listbox")).toBeInTheDocument();
      },
      { timeout: 2000 }
    );
  });

  it("adds drug when clicked in dropdown", async () => {
    const user = userEvent.setup();
    renderWithProviders(<DrugInput onSubmit={() => {}} />);

    const input = screen.getByLabelText("common.search");
    await user.type(input, "war");

    await waitFor(
      () => {
        expect(screen.getByRole("listbox")).toBeInTheDocument();
      },
      { timeout: 2000 }
    );

    // Click first result
    const options = screen.getAllByRole("option");
    await user.click(options[0]);

    // Drug should appear as badge
    expect(screen.getByText("Warfarin")).toBeInTheDocument();
  });
});
