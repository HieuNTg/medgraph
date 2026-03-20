import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Shield, AlertCircle } from "lucide-react";
import { DrugInput } from "@/components/drug-input";
import { Progress } from "@/components/ui/progress";
import { checkInteractions } from "@/lib/api";

const LOADING_MESSAGES = [
  "Searching drug database...",
  "Mapping enzyme pathways...",
  "Analyzing CYP450 interactions...",
  "Detecting cascade conflicts...",
  "Compiling evidence...",
  "Building your report...",
];

export function CheckerPage() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);
  const [loadingMsg, setLoadingMsg] = useState(LOADING_MESSAGES[0]);

  const handleSubmit = async (drugIds: string[]) => {
    setError(null);
    setLoading(true);
    setProgress(0);

    // Animate progress messages
    let msgIndex = 0;
    const msgInterval = setInterval(() => {
      msgIndex = (msgIndex + 1) % LOADING_MESSAGES.length;
      setLoadingMsg(LOADING_MESSAGES[msgIndex]);
      setProgress((p) => Math.min(p + 15, 90));
    }, 700);

    try {
      const result = await checkInteractions(drugIds);
      clearInterval(msgInterval);
      setProgress(100);
      setTimeout(() => {
        navigate("/results", { state: { result } });
      }, 300);
    } catch (err) {
      clearInterval(msgInterval);
      setLoading(false);
      setProgress(0);
      setError(
        err instanceof Error ? err.message : "An unexpected error occurred."
      );
    }
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[var(--primary)]">
            <Shield className="h-5 w-5 text-white" />
          </div>
          <h1 className="text-2xl font-bold text-[var(--foreground)]">
            Interaction Checker
          </h1>
        </div>
        <p className="text-[var(--muted-foreground)]">
          Enter 2 to 10 medications to analyze drug interactions and enzyme
          pathway cascades.
        </p>
      </div>

      {/* Input */}
      <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-6 space-y-6">
        <DrugInput onSubmit={handleSubmit} loading={loading} />
      </div>

      {/* Loading state */}
      {loading && (
        <div className="space-y-3">
          <div className="flex items-center gap-3 text-sm text-[var(--muted-foreground)]">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-[var(--primary)] border-t-transparent" />
            {loadingMsg}
          </div>
          <Progress value={progress} className="h-2" />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="flex items-start gap-3 rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 dark:border-red-800 dark:bg-red-950 dark:text-red-300">
          <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
          <div className="space-y-1">
            <p className="font-semibold text-sm">Analysis Failed</p>
            <p className="text-sm">{error}</p>
          </div>
        </div>
      )}
    </div>
  );
}
