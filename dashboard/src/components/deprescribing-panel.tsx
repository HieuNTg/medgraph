/**
 * Deprescribing recommendations panel.
 *
 * Shows ordered suggestions for which drugs could be safely removed from a
 * regimen to reduce interaction burden. Includes a mandatory medical disclaimer.
 */

import { AlertTriangle } from "lucide-react";
import type { DeprescribingResponse } from "@/lib/types";

interface DeprescribingPanelProps {
  recommendations: DeprescribingResponse[];
  loading?: boolean;
  error?: string | null;
}

function BenefitBar({ value }: { value: number }) {
  // value is 0–1 scale
  const pct = Math.min(Math.max(value * 100, 0), 100);
  const color =
    pct >= 66 ? "bg-green-500" : pct >= 33 ? "bg-yellow-400" : "bg-blue-400";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 rounded-full bg-[var(--border)] overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-[10px] text-[var(--muted-foreground)] w-8 text-right">
        {pct.toFixed(0)}%
      </span>
    </div>
  );
}

export function DeprescribingPanel({
  recommendations,
  loading,
  error,
}: DeprescribingPanelProps) {
  return (
    <div className="space-y-4">
      {/* Mandatory medical disclaimer */}
      <div className="flex gap-2.5 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 dark:border-amber-700 dark:bg-amber-950">
        <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
        <p className="text-xs text-amber-800 dark:text-amber-300">
          <strong>Medical disclaimer:</strong> These suggestions are algorithmic
          and for informational purposes only. Never stop or change medications
          without consulting your prescribing clinician. Abrupt discontinuation
          can be dangerous.
        </p>
      </div>

      {loading && (
        <p className="text-sm text-[var(--muted-foreground)] animate-pulse text-center py-4">
          Calculating deprescribing recommendations…
        </p>
      )}

      {error && (
        <p className="text-sm text-red-500 text-center py-4">{error}</p>
      )}

      {!loading && !error && recommendations.length === 0 && (
        <p className="text-sm text-[var(--muted-foreground)] text-center py-4">
          No deprescribing recommendations available for this regimen.
        </p>
      )}

      {!loading && !error && recommendations.length > 0 && (
        <ol className="space-y-3">
          {recommendations.map((rec) => (
            <li
              key={rec.drug_id}
              className="rounded-lg border border-[var(--border)] bg-[var(--card)] p-4 space-y-2"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[var(--primary)] text-xs font-bold text-white">
                    {rec.order}
                  </span>
                  <span className="font-medium text-sm text-[var(--foreground)]">
                    {rec.drug_name}
                  </span>
                </div>
                <span className="text-xs text-[var(--muted-foreground)] shrink-0">
                  {rec.interactions_resolved} interaction{rec.interactions_resolved !== 1 ? "s" : ""} resolved
                </span>
              </div>
              <BenefitBar value={rec.removal_benefit} />
              <p className="text-xs text-[var(--muted-foreground)]">{rec.rationale}</p>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
