import { ExternalLink, FileText, AlertCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { Evidence } from "@/lib/types";

interface EvidencePanelProps {
  evidence: Evidence[];
}

const SOURCE_VARIANT: Record<string, "default" | "secondary" | "outline"> = {
  FDA: "default",
  DrugBank: "secondary",
  RxNorm: "outline",
  OpenFDA: "default",
};

export function EvidencePanel({ evidence }: EvidencePanelProps) {
  if (evidence.length === 0) {
    return (
      <div className="flex items-center gap-2 text-sm text-[var(--muted-foreground)]">
        <AlertCircle className="h-4 w-4" />
        No evidence records available.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {evidence.map((item, index) => (
        <div
          key={index}
          className="rounded-md border border-[var(--border)] bg-[var(--background)] p-3"
        >
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-2 flex-1">
              <FileText className="mt-0.5 h-4 w-4 shrink-0 text-[var(--muted-foreground)]" />
              <div className="space-y-1 flex-1">
                <div className="flex items-center gap-2">
                  <Badge
                    variant={SOURCE_VARIANT[item.source] ?? "outline"}
                    className="text-xs"
                  >
                    {item.source}
                  </Badge>
                  {item.case_count !== null && (
                    <span className="text-xs text-[var(--muted-foreground)]">
                      {item.case_count.toLocaleString()} cases reported
                    </span>
                  )}
                </div>
                <p className="text-sm text-[var(--foreground)]">
                  {item.description}
                </p>
              </div>
            </div>
            {item.url && (
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="shrink-0 text-[var(--primary)] hover:underline"
                aria-label={`View source from ${item.source}`}
              >
                <ExternalLink className="h-4 w-4" />
              </a>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
