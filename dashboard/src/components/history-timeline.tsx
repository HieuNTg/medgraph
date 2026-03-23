import type { AnalysisHistoryEntry } from "@/lib/types";

const RISK_STYLES: Record<string, string> = {
  critical: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
  moderate: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
  low: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
  minimal: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
};

interface HistoryTimelineProps {
  entries: AnalysisHistoryEntry[];
  onSelect: (entry: AnalysisHistoryEntry) => void;
}

export function HistoryTimeline({ entries, onSelect }: HistoryTimelineProps) {
  return (
    <ol className="relative border-l border-[var(--border)] space-y-6 ml-3">
      {entries.map((entry) => {
        const date = new Date(entry.created_at);
        const riskKey = entry.overall_risk.toLowerCase();
        const badgeClass =
          RISK_STYLES[riskKey] ??
          "bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300";

        return (
          <li key={entry.id} className="ml-6">
            {/* Timeline dot */}
            <span className="absolute -left-[7px] flex h-3.5 w-3.5 items-center justify-center rounded-full border-2 border-[var(--primary)] bg-[var(--background)]" />

            <button
              type="button"
              onClick={() => onSelect(entry)}
              className="w-full text-left rounded-xl border border-[var(--border)] bg-[var(--card)] p-4 space-y-2 hover:border-[var(--primary)] transition-colors"
            >
              <div className="flex items-center justify-between gap-2">
                <time
                  dateTime={entry.created_at}
                  className="text-xs text-[var(--muted-foreground)]"
                >
                  {date.toLocaleString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </time>
                <span
                  className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize ${badgeClass}`}
                >
                  {entry.overall_risk}
                </span>
              </div>
              <p className="text-sm text-[var(--foreground)]">
                {entry.drug_ids.length} drug{entry.drug_ids.length !== 1 ? "s" : ""} checked
              </p>
              <p className="text-xs text-[var(--muted-foreground)] truncate">
                {entry.drug_ids.join(", ")}
              </p>
            </button>
          </li>
        );
      })}
    </ol>
  );
}
