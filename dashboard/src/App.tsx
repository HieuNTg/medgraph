import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AppShell } from "@/layout/app-shell";
import { HomePage } from "@/pages/home";
import { CheckerPage } from "@/pages/checker";
import { DrugInfoPage } from "@/pages/drug-info";
import { AboutPage } from "@/pages/about";

const ResultsPage = lazy(() =>
  import("@/pages/results").then((m) => ({ default: m.ResultsPage }))
);

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/checker" element={<CheckerPage />} />
            <Route
              path="/results"
              element={
                <Suspense
                  fallback={
                    <div className="flex items-center justify-center min-h-[50vh]">
                      <div className="h-8 w-8 animate-spin rounded-full border-4 border-[var(--primary)] border-t-transparent" />
                    </div>
                  }
                >
                  <ResultsPage />
                </Suspense>
              }
            />
            <Route path="/drugs/:id" element={<DrugInfoPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
