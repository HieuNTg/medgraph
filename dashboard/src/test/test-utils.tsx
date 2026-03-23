import type { ReactNode } from "react";
import { render, type RenderOptions } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { MemoryRouter } from "react-router-dom";

/**
 * Create a fresh QueryClient for each test — prevents shared state.
 */
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, staleTime: 0 },
      mutations: { retry: false },
    },
  });
}

interface WrapperProps {
  children: ReactNode;
}

/**
 * Render helper that wraps components with required providers.
 */
export function renderWithProviders(
  ui: React.ReactElement,
  options?: Omit<RenderOptions, "wrapper"> & { route?: string }
) {
  const queryClient = createTestQueryClient();
  const { route = "/", ...renderOptions } = options ?? {};

  function Wrapper({ children }: WrapperProps) {
    return (
      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[route]}>{children}</MemoryRouter>
      </QueryClientProvider>
    );
  }

  return { ...render(ui, { wrapper: Wrapper, ...renderOptions }), queryClient };
}
