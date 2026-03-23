import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Loader2, AlertCircle } from "lucide-react";
import { getSharedResult } from "@/lib/api";
import type { CheckResponse } from "@/lib/types";

// Lazy-loaded — dynamic import of ResultsPage internals is complex,
// so we show a minimal summary and redirect to results via state navigation.
export function SharedResultPage() {
  const { token } = useParams<{ token: string }>();
  const [result, setResult] = useState<CheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    getSharedResult(token)
      .then(setResult)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load shared result."))
      .finally(() => setLoading(false));
  }, [token]);

  if (loading) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 flex items-center gap-3 text-[var(--muted-foreground)]">
        <Loader2 className="h-5 w-5 animate-spin" />
        Loading shared result...
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 space-y-4">
        <div role="alert" className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <p className="text-sm">{error ?? "Result not found."}</p>
        </div>
      </div>
    );
  }

  // Redirect to results page with data in state
  return (
    <div className="mx-auto max-w-3xl px-4 py-16 space-y-4">
      <h1 className="text-2xl font-bold text-[var(--foreground)]">Shared Analysis</h1>
      <p className="text-[var(--muted-foreground)]">
        Overall risk: <span className="font-semibold text-[var(--foreground)] capitalize">{result.overall_risk}</span>
      </p>
      <p className="text-sm text-[var(--muted-foreground)]">
        {result.drug_count} drug{result.drug_count !== 1 ? "s" : ""} · {result.interaction_count} interaction{result.interaction_count !== 1 ? "s" : ""}
      </p>
      <p className="text-xs text-[var(--muted-foreground)]">
        Drugs: {result.drugs.map((d) => d.name).join(", ")}
      </p>
    </div>
  );
}
