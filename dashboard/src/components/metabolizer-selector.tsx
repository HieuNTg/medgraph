import { useState } from "react";
import { ChevronDown, ChevronUp, Dna } from "lucide-react";

const CYP_GENES = [
  {
    id: "CYP2D6",
    label: "CYP2D6",
    description:
      "Metabolizes ~25% of drugs (opioids, antidepressants, beta-blockers)",
  },
  {
    id: "CYP2C19",
    label: "CYP2C19",
    description: "Metabolizes PPIs, clopidogrel, some SSRIs",
  },
] as const;

const PHENOTYPES = [
  {
    value: "poor",
    label: "Poor",
    color: "text-red-600 dark:text-red-400",
    bg: "bg-red-100 dark:bg-red-900/30",
  },
  {
    value: "intermediate",
    label: "Intermediate",
    color: "text-amber-600 dark:text-amber-400",
    bg: "bg-amber-100 dark:bg-amber-900/30",
  },
  {
    value: "normal",
    label: "Normal",
    color: "text-green-600 dark:text-green-400",
    bg: "bg-green-100 dark:bg-green-900/30",
  },
  {
    value: "ultrarapid",
    label: "Ultra-rapid",
    color: "text-blue-600 dark:text-blue-400",
    bg: "bg-blue-100 dark:bg-blue-900/30",
  },
] as const;

interface MetabolizerSelectorProps {
  value: Record<string, string>;
  onChange: (value: Record<string, string>) => void;
  disabled?: boolean;
}

export function MetabolizerSelector({
  value,
  onChange,
  disabled,
}: MetabolizerSelectorProps) {
  const [expanded, setExpanded] = useState(false);

  const hasSelections = Object.keys(value).length > 0;

  const handleSelect = (geneId: string, phenotype: string) => {
    const next = { ...value };
    if (next[geneId] === phenotype) {
      delete next[geneId];
    } else {
      next[geneId] = phenotype;
    }
    onChange(next);
  };

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--card)]">
      <button
        type="button"
        onClick={() => setExpanded(!expanded)}
        disabled={disabled}
        className="flex w-full items-center justify-between px-4 py-3 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--accent)] transition-colors rounded-lg disabled:opacity-50"
      >
        <div className="flex items-center gap-2">
          <Dna className="h-4 w-4 text-[var(--primary)]" />
          <span>Pharmacogenomics (Optional)</span>
          {hasSelections && (
            <span className="rounded-full bg-[var(--primary)] px-2 py-0.5 text-xs text-white">
              {Object.keys(value).length} set
            </span>
          )}
        </div>
        {expanded ? (
          <ChevronUp className="h-4 w-4" />
        ) : (
          <ChevronDown className="h-4 w-4" />
        )}
      </button>

      {expanded && (
        <div className="border-t border-[var(--border)] px-4 py-4 space-y-4">
          <p className="text-xs text-[var(--muted-foreground)]">
            If you know your CYP450 metabolizer status from genetic testing,
            select it below to personalize interaction risk scoring.
          </p>
          {CYP_GENES.map((gene) => (
            <div key={gene.id} className="space-y-2">
              <div>
                <span className="text-sm font-medium text-[var(--foreground)]">
                  {gene.label}
                </span>
                <span className="text-xs text-[var(--muted-foreground)] ml-2">
                  {gene.description}
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {PHENOTYPES.map((pt) => (
                  <button
                    key={pt.value}
                    type="button"
                    disabled={disabled}
                    onClick={() => handleSelect(gene.id, pt.value)}
                    className={`rounded-md px-3 py-1.5 text-xs font-medium border transition-colors ${
                      value[gene.id] === pt.value
                        ? `${pt.bg} ${pt.color} border-current`
                        : "border-[var(--border)] text-[var(--muted-foreground)] hover:bg-[var(--accent)]"
                    } disabled:opacity-50`}
                  >
                    {pt.label}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
