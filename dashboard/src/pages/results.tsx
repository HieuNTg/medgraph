import { useLocation, useNavigate, Link } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { ArrowLeft, RotateCcw, Network } from "lucide-react";
import { Button } from "@/components/ui/button";
import { RiskSummary } from "@/components/risk-summary";
import { InteractionCard } from "@/components/interaction-card";
import { InteractionGraph } from "@/components/interaction-graph";
import type { CheckResponse, InteractionResult } from "@/lib/types";

const SEVERITY_ORDER: Record<string, number> = {
  critical: 0,
  major: 1,
  moderate: 2,
  minor: 3,
};

function sortBySeverity(interactions: InteractionResult[]): InteractionResult[] {
  return [...interactions].sort(
    (a, b) =>
      (SEVERITY_ORDER[a.severity] ?? 99) - (SEVERITY_ORDER[b.severity] ?? 99)
  );
}

interface ResultsState {
  result: CheckResponse;
}

export function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as ResultsState | null;
  const [showGraph, setShowGraph] = useState(true);
  const graphContainerRef = useRef<HTMLDivElement>(null);
  const [graphWidth, setGraphWidth] = useState(700);

  useEffect(() => {
    if (!state?.result) {
      navigate("/checker", { replace: true });
    }
  }, [state, navigate]);

  // Responsive graph width
  useEffect(() => {
    const el = graphContainerRef.current;
    if (!el) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        setGraphWidth(Math.max(300, entry.contentRect.width));
      }
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  if (!state?.result) return null;

  const { result } = state;
  const sorted = sortBySeverity(result.interactions);

  // Check if graph has meaningful data to show
  const hasGraphData =
    result.drugs.some((d) => d.enzyme_relations.length > 0) ||
    result.interactions.some((i) => i.cascade_paths.length > 0);

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Breadcrumb */}
      <div className="flex items-center gap-3">
        <Button asChild variant="ghost" size="sm">
          <Link to="/checker" className="flex items-center gap-2">
            <ArrowLeft className="h-4 w-4" />
            Back to Checker
          </Link>
        </Button>
      </div>

      {/* Risk summary */}
      <RiskSummary response={result} />

      {/* Knowledge Graph Visualization */}
      {hasGraphData && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="font-semibold text-[var(--foreground)] flex items-center gap-2">
              <Network className="h-5 w-5 text-[var(--primary)]" />
              Interaction Network
            </h2>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setShowGraph((p) => !p)}
            >
              {showGraph ? "Hide" : "Show"} Graph
            </Button>
          </div>
          {showGraph && (
            <div ref={graphContainerRef}>
              <InteractionGraph
                data={result}
                width={graphWidth}
                height={450}
              />
              <p className="text-xs text-[var(--muted-foreground)] mt-2">
                Drag nodes to rearrange. Scroll to zoom. Blue circles = drugs,
                amber rectangles = enzymes.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Drug list */}
      <div className="space-y-1">
        <h2 className="text-sm font-medium text-[var(--muted-foreground)]">
          Medications analyzed:
        </h2>
        <div className="flex flex-wrap gap-2">
          {result.drugs.map((drug) => (
            <span
              key={drug.id}
              className="rounded-full border border-[var(--border)] bg-[var(--secondary)] px-3 py-1 text-sm text-[var(--foreground)]"
            >
              {drug.name}
            </span>
          ))}
        </div>
      </div>

      {/* Interaction cards */}
      {sorted.length > 0 ? (
        <div className="space-y-4">
          <h2 className="font-semibold text-[var(--foreground)]">
            {sorted.length} Interaction{sorted.length !== 1 ? "s" : ""} Found
          </h2>
          {sorted.map((interaction, i) => (
            <InteractionCard key={i} interaction={interaction} />
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-green-200 bg-green-50 p-8 text-center dark:border-green-800 dark:bg-green-950">
          <div className="text-green-600 dark:text-green-400 text-4xl mb-3">✓</div>
          <h3 className="font-semibold text-green-800 dark:text-green-300 text-lg">
            No Significant Interactions Found
          </h3>
          <p className="text-sm text-green-700 dark:text-green-400 mt-1">
            No clinically significant drug interactions were detected between
            your medications.
          </p>
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        <Button asChild variant="outline">
          <Link to="/checker" className="flex items-center gap-2">
            <RotateCcw className="h-4 w-4" />
            Check Another Combination
          </Link>
        </Button>
      </div>
    </div>
  );
}
