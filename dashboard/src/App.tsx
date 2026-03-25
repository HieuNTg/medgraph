import { lazy, Suspense } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AppShell } from "@/layout/app-shell";
import { ErrorBoundary } from "@/components/error-boundary";
import { AnalysisSkeleton } from "@/components/loading-skeleton";
import { AuthProvider } from "@/lib/auth-context";
import { ProtectedRoute } from "@/components/protected-route";
const HomePage = lazy(() =>
  import("@/pages/home").then((m) => ({ default: m.HomePage }))
);

const CheckerPage = lazy(() =>
  import("@/pages/checker").then((m) => ({ default: m.CheckerPage }))
);

const DrugInfoPage = lazy(() =>
  import("@/pages/drug-info").then((m) => ({ default: m.DrugInfoPage }))
);

const AboutPage = lazy(() =>
  import("@/pages/about").then((m) => ({ default: m.AboutPage }))
);

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
                <Route path="/" element={<Suspense fallback={<AnalysisSkeleton />}><HomePage /></Suspense>} />
                <Route
                  path="/checker"
                  element={
                    <ErrorBoundary>
                      <Suspense fallback={<AnalysisSkeleton />}>
                        <CheckerPage />
                      </Suspense>
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
                      <Suspense fallback={<AnalysisSkeleton />}>
                        <DrugInfoPage />
                      </Suspense>
                    </ErrorBoundary>
                  }
                />
                <Route path="/about" element={<Suspense fallback={<AnalysisSkeleton />}><AboutPage /></Suspense>} />
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
                    <ProtectedRoute>
                      <Suspense fallback={<AnalysisSkeleton />}>
                        <ProfilesPage />
                      </Suspense>
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <ProtectedRoute>
                      <Suspense fallback={<AnalysisSkeleton />}>
                        <HistoryPage />
                      </Suspense>
                    </ProtectedRoute>
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
