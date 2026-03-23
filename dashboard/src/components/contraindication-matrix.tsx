/**
 * Drug-drug contraindication heatmap.
 *
 * Renders an N×N matrix where each cell's color encodes conflict severity:
 *   green=safe / no data, yellow=moderate, orange=major, red=critical
 */

import type { ContraindicationResponse } from "@/lib/types";

interface ContraindicationMatrixProps {
  data: ContraindicationResponse;
}

const SEVERITY_COLOR: Record<string, string> = {
  critical: "bg-red-500 text-white",
  major: "bg-orange-400 text-white",
  moderate: "bg-yellow-400 text-gray-900",
  minor: "bg-yellow-100 text-gray-900 dark:bg-yellow-900 dark:text-yellow-100",
};

function cellClass(severity: string | undefined): string {
  if (!severity) return "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400";
  return SEVERITY_COLOR[severity.toLowerCase()] ?? "bg-[var(--secondary)] text-[var(--foreground)]";
}

export function ContraindicationMatrix({ data }: ContraindicationMatrixProps) {
  const { nodes, edges } = data;

  if (nodes.length === 0) {
    return (
      <p className="text-sm text-[var(--muted-foreground)] py-4 text-center">
        No contraindication data available
      </p>
    );
  }

  // Build a severity lookup: "srcId|tgtId" -> severity
  const severityMap = new Map<string, string>();
  for (const edge of edges) {
    const key = `${edge.source}|${edge.target}`;
    const revKey = `${edge.target}|${edge.source}`;
    severityMap.set(key, edge.severity);
    severityMap.set(revKey, edge.severity);
  }

  return (
    <div className="overflow-x-auto">
      <table className="text-xs border-collapse w-full">
        <thead>
          <tr>
            {/* top-left empty cell */}
            <th className="w-28 min-w-[7rem]" />
            {nodes.map((n) => (
              <th
                key={n.id}
                className="text-center font-medium text-[var(--muted-foreground)] pb-1 px-1"
                title={n.label}
              >
                <span className="block truncate max-w-[5rem]">{n.label}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {nodes.map((row) => (
            <tr key={row.id}>
              <td
                className="pr-2 font-medium text-[var(--muted-foreground)] text-right truncate max-w-[7rem]"
                title={row.label}
              >
                {row.label}
              </td>
              {nodes.map((col) => {
                if (row.id === col.id) {
                  return (
                    <td
                      key={col.id}
                      className="p-1 text-center text-[var(--muted-foreground)]"
                    >
                      —
                    </td>
                  );
                }
                const severity = severityMap.get(`${row.id}|${col.id}`);
                return (
                  <td key={col.id} className="p-0.5">
                    <div
                      className={`rounded text-center py-1 px-0.5 font-medium capitalize ${cellClass(severity)}`}
                      title={severity ?? "No interaction"}
                    >
                      {severity ? severity.slice(0, 3) : "ok"}
                    </div>
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      {/* Legend */}
      <div className="flex flex-wrap gap-3 mt-3 text-xs text-[var(--muted-foreground)]">
        <LegendCell cls="bg-green-100 dark:bg-green-900/30 text-green-700" label="Safe / none" />
        <LegendCell cls="bg-yellow-100 dark:bg-yellow-900 text-gray-900" label="Minor" />
        <LegendCell cls="bg-yellow-400 text-gray-900" label="Moderate" />
        <LegendCell cls="bg-orange-400 text-white" label="Major" />
        <LegendCell cls="bg-red-500 text-white" label="Critical" />
      </div>
    </div>
  );
}

function LegendCell({ cls, label }: { cls: string; label: string }) {
  return (
    <div className="flex items-center gap-1.5">
      <span className={`inline-block h-4 w-6 rounded text-center text-[9px] font-medium ${cls}`} />
      <span>{label}</span>
    </div>
  );
}
