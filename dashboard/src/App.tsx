import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AppShell } from "@/layout/app-shell";
import { ErrorBoundary } from "@/components/error-boundary";
import { AnalysisSkeleton } from "@/components/loading-skeleton";
import { AuthProvider } from "@/lib/auth-context";
import { HomePage } from "@/pages/home";
import { CheckerPage } from "@/pages/checker";
import { DrugInfoPage } from "@/pages/drug-info";
import { AboutPage } from "@/pages/about";

const ResultsPage = lazy(() =>
  import("@/pages/results").then((m) => ({ default: m.ResultsPage }))
);

const LoginPage = lazy(() =>
  import("@/pages/login").then((m) => ({ default: m.LoginPage }))
);

const ProfilesPage = lazy(() =>
  import("@/pages/profiles").then((m) => ({ default: m.ProfilesPage }))
);

const HistoryPage = lazy(() =>
  import("@/pages/history").then((m) => ({ default: m.HistoryPage }))
);

const SharedResultPage = lazy(() =>
  import("@/pages/shared-result").then((m) => ({ default: m.SharedResultPage }))
);

const NetworkPage = lazy(() =>
  import("@/pages/network").then((m) => ({ default: m.NetworkPage }))
);

const PharmacogenomicsPage = lazy(() =>
  import("@/pages/pharmacogenomics").then((m) => ({ default: m.PharmacogenomicsPage }))
);

const SchedulePage = lazy(() =>
  import("@/pages/schedule").then((m) => ({ default: m.SchedulePage }))
);

function App() {
  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
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
                <Route
                  path="/login"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <LoginPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/profiles"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <ProfilesPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <HistoryPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/shared/:token"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <SharedResultPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/network"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <NetworkPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/pharmacogenomics"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <PharmacogenomicsPage />
                    </Suspense>
                  }
                />
                <Route
                  path="/schedule"
                  element={
                    <Suspense fallback={<AnalysisSkeleton />}>
                      <SchedulePage />
                    </Suspense>
                  }
                />
              </Route>
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

export default App;
