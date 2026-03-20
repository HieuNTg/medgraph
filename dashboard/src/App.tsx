import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "@/lib/query-client";
import { AppShell } from "@/layout/app-shell";
import { HomePage } from "@/pages/home";
import { CheckerPage } from "@/pages/checker";
import { ResultsPage } from "@/pages/results";
import { DrugInfoPage } from "@/pages/drug-info";
import { AboutPage } from "@/pages/about";

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<AppShell />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/checker" element={<CheckerPage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/drugs/:id" element={<DrugInfoPage />} />
            <Route path="/about" element={<AboutPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
