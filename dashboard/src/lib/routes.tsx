import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import { AppShell } from "@/layout/app-shell";
import { ErrorBoundary } from "@/components/error-boundary";
import { AnalysisSkeleton } from "@/components/loading-skeleton";
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

function Lazy({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<AnalysisSkeleton />}>{children}</Suspense>;
}

function LazyProtected({ children }: { children: React.ReactNode }) {
  return (
    <ProtectedRoute>
      <Suspense fallback={<AnalysisSkeleton />}>{children}</Suspense>
    </ProtectedRoute>
  );
}

function LazyBounded({ children }: { children: React.ReactNode }) {
  return (
    <ErrorBoundary>
      <Suspense fallback={<AnalysisSkeleton />}>{children}</Suspense>
    </ErrorBoundary>
  );
}

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<Lazy><HomePage /></Lazy>} />
        <Route path="/checker" element={<LazyBounded><CheckerPage /></LazyBounded>} />
        <Route path="/results" element={<LazyBounded><ResultsPage /></LazyBounded>} />
        <Route path="/drugs/:id" element={<LazyBounded><DrugInfoPage /></LazyBounded>} />
        <Route path="/about" element={<Lazy><AboutPage /></Lazy>} />
        <Route path="/login" element={<Lazy><LoginPage /></Lazy>} />
        <Route path="/profiles" element={<LazyProtected><ProfilesPage /></LazyProtected>} />
        <Route path="/history" element={<LazyProtected><HistoryPage /></LazyProtected>} />
        <Route path="/shared/:token" element={<Lazy><SharedResultPage /></Lazy>} />
        <Route path="/network" element={<Lazy><NetworkPage /></Lazy>} />
        <Route path="/pharmacogenomics" element={<Lazy><PharmacogenomicsPage /></Lazy>} />
        <Route path="/schedule" element={<Lazy><SchedulePage /></Lazy>} />
      </Route>
    </Routes>
  );
}
