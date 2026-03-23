import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AppShell } from "@/layout/app-shell";
import { ErrorBoundary } from "@/components/error-boundary";
import { AnalysisSkeleton } from "@/components/loading-skeleton";
import { HomePage } from "@/pages/home";
import { CheckerPage } from "@/pages/checker";
import { DrugInfoPage } from "@/pages/drug-info";
import { AboutPage } from "@/pages/about";

const ResultsPage = lazy(() =>
  import("@/pages/results").then((m) => ({ default: m.ResultsPage }))
);

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Routes>
            <Route element={<AppShell />}>
              <Route path="/" element={<HomePage />} />
              <Route
                path="/checker"
                element={
                  <ErrorBoundary>
                    <CheckerPage />
                  </ErrorBoundary>
                }
              />
              <Route
                path="/results"
                element={
                  <ErrorBoundary>
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <ResultsPage />
                    </Suspense>
                  </ErrorBoundary>
                }
              />
              <Route
                path="/drugs/:id"
                element={
                  <ErrorBoundary>
                    <DrugInfoPage />
                  </ErrorBoundary>
                }
              />
              <Route path="/about" element={<AboutPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
