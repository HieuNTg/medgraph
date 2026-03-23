import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { History, AlertCircle, Loader2, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { HistoryTimeline } from "@/components/history-timeline";
import { useAuth } from "@/lib/auth-context";
import { getHistory, checkInteractions } from "@/lib/api";
import type { AnalysisHistoryEntry } from "@/lib/types";

const PAGE_SIZE = 10;

export function HistoryPage() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [entries, setEntries] = useState<AnalysisHistoryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [replaying, setReplaying] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) return;
    setLoading(true);
    getHistory(PAGE_SIZE, 0)
      .then((data) => {
        setEntries(data);
        setHasMore(data.length === PAGE_SIZE);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load history."))
      .finally(() => setLoading(false));
  }, [isAuthenticated]);

  const loadMore = async () => {
    setLoadingMore(true);
    try {
      const data = await getHistory(PAGE_SIZE, entries.length);
      setEntries((prev) => [...prev, ...data]);
      setHasMore(data.length === PAGE_SIZE);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load more.");
    } finally {
      setLoadingMore(false);
    }
  };

  const handleSelect = async (entry: AnalysisHistoryEntry) => {
    setReplaying(true);
    try {
      const result = await checkInteractions(entry.drug_ids);
      navigate("/results", { state: { result } });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to replay analysis.");
      setReplaying(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6 text-center space-y-4">
        <History className="mx-auto h-12 w-12 text-[var(--muted-foreground)]" />
        <h1 className="text-2xl font-bold text-[var(--foreground)]">Analysis History</h1>
        <p className="text-[var(--muted-foreground)]">
          Sign in to view your past drug interaction analyses.
        </p>
        <Button onClick={() => navigate("/login")}>Sign in</Button>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--primary)]">
          <History className="h-5 w-5 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-[var(--foreground)]">Analysis History</h1>
          <p className="text-sm text-[var(--muted-foreground)]">Click an entry to re-run the analysis.</p>
        </div>
      </div>

      {error && (
        <div role="alert" className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {replaying && (
        <div className="flex items-center gap-3 text-sm text-[var(--muted-foreground)]" aria-live="polite">
          <Loader2 className="h-4 w-4 animate-spin" />
          Re-running analysis...
        </div>
      )}

      {loading ? (
        <div className="flex items-center gap-3 text-sm text-[var(--muted-foreground)]">
          <Loader2 className="h-4 w-4 animate-spin" />
          Loading history...
        </div>
      ) : entries.length === 0 ? (
        <div className="rounded-xl border border-dashed border-[var(--border)] p-12 text-center space-y-3">
          <History className="mx-auto h-10 w-10 text-[var(--muted-foreground)]" />
          <p className="text-[var(--muted-foreground)]">
            No analyses yet. Run the interaction checker to build your history.
          </p>
          <Button variant="outline" onClick={() => navigate("/checker")}>
            Go to Checker
          </Button>
        </div>
      ) : (
        <div className="space-y-6">
          <HistoryTimeline entries={entries} onSelect={handleSelect} />

          {hasMore && (
            <div className="flex justify-center pt-2">
              <Button
                variant="outline"
                onClick={loadMore}
                disabled={loadingMore}
                className="flex items-center gap-2"
              >
                {loadingMore ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <ChevronDown className="h-4 w-4" />
                )}
                {loadingMore ? "Loading..." : "Load more"}
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
