/**
 * Hub drugs info card — lists top hub drugs with centrality scores.
 */

import type { HubDrugResponse } from "@/lib/types";

interface HubDrugsCardProps {
  hubs: HubDrugResponse[];
  loading?: boolean;
  error?: string | null;
}

export function HubDrugsCard({ hubs, loading, error }: HubDrugsCardProps) {
  if (loading) {
    return (
      <div className="text-sm text-[var(--muted-foreground)] animate-pulse py-4 text-center">
        Loading hub drugs…
      </div>
    );
  }

  if (error) {
    return (
      <p className="text-sm text-red-500 py-4 text-center">{error}</p>
    );
  }

  if (hubs.length === 0) {
    return (
      <p className="text-sm text-[var(--muted-foreground)] py-4 text-center">
        No hub drug data available
      </p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="text-xs w-full border-collapse">
        <thead>
          <tr className="border-b border-[var(--border)]">
            <th className="text-left py-1.5 pr-2 font-medium text-[var(--muted-foreground)]">Drug</th>
            <th className="text-right py-1.5 px-2 font-medium text-[var(--muted-foreground)]">Interactions</th>
            <th className="text-right py-1.5 px-2 font-medium text-[var(--muted-foreground)]">Betweenness</th>
            <th className="text-right py-1.5 pl-2 font-medium text-[var(--muted-foreground)]">PageRank</th>
          </tr>
        </thead>
        <tbody>
          {hubs.map((hub) => (
            <tr
              key={hub.drug_id}
              className="border-b border-[var(--border)] last:border-0 hover:bg-[var(--secondary)] transition-colors"
            >
              <td className="py-1.5 pr-2 font-medium text-[var(--foreground)]">
                {hub.drug_name}
              </td>
              <td className="py-1.5 px-2 text-right text-[var(--muted-foreground)]">
                {hub.interaction_count}
              </td>
              <td className="py-1.5 px-2 text-right text-[var(--muted-foreground)]">
                {hub.betweenness.toFixed(4)}
              </td>
              <td className="py-1.5 pl-2 text-right text-[var(--muted-foreground)]">
                {hub.pagerank.toFixed(4)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-[10px] text-[var(--muted-foreground)] mt-2">
        Hub drugs have many connections and high centrality in the interaction network. Use caution when adding or removing them from a regimen.
      </p>
    </div>
  );
}
