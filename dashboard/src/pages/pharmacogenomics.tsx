/**
 * Pharmacogenomics Patient Genotype Page
 *
 * Allows clinicians / patients to enter their CYP450 genotype profile
 * and immediately check a drug list with personalised risk adjustments.
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Dna, AlertTriangle, Info } from "lucide-react";
import { CYP_GENES, PHENOTYPES } from "@/components/metabolizer-selector";
import { DrugInput } from "@/components/drug-input";
import { checkInteractions } from "@/lib/api";
import type { CheckResponse } from "@/lib/types";

// Phenotype → human-readable risk note
const PHENOTYPE_NOTES: Record<string, string> = {
  poor: "Reduced enzyme activity — drugs metabolised by this enzyme may accumulate, increasing toxicity risk.",
  intermediate: "Moderately reduced enzyme activity — some accumulation possible.",
  normal: "Normal enzyme activity — standard dosing typically appropriate.",
  ultrarapid: "Increased enzyme activity — drugs may be metabolised too quickly, reducing efficacy.",
};

// Phenotype → risk badge colour
const PHENOTYPE_BADGE: Record<string, string> = {
  poor: "bg-red-100 text-red-700 border-red-300 dark:bg-red-900/30 dark:text-red-300",
  intermediate:
    "bg-amber-100 text-amber-700 border-amber-300 dark:bg-amber-900/30 dark:text-amber-300",
  normal: "bg-green-100 text-green-700 border-green-300 dark:bg-green-900/30 dark:text-green-300",
  ultrarapid:
    "bg-blue-100 text-blue-700 border-blue-300 dark:bg-blue-900/30 dark:text-blue-300",
};

function PhenotypeDropdown({
  geneId,
  value,
  onChange,
}: {
  geneId: string;
  value: string;
  onChange: (v: string) => void;
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full rounded-md border border-[var(--border)] bg-[var(--background)] px-3 py-2 text-sm text-[var(--foreground)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)]"
      aria-label={`Phenotype for ${geneId}`}
    >
      <option value="">-- Not set --</option>
      {PHENOTYPES.map((pt) => (
        <option key={pt.value} value={pt.value}>
          {pt.label} Metabolizer
        </option>
      ))}
    </select>
  );
}

export function PharmacogenomicsPage() {
  const navigate = useNavigate();
  const [genotype, setGenotype] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenotypeChange = (geneId: string, phenotype: string) => {
    setGenotype((prev) => {
      const next = { ...prev };
      if (!phenotype) {
        delete next[geneId];
      } else {
        next[geneId] = phenotype;
      }
      return next;
    });
  };

  const handleDrugSubmit = async (drugList: string[]) => {
    setError(null);
    setLoading(true);
    try {
      const result: CheckResponse = await checkInteractions(
        drugList,
        Object.keys(genotype).length > 0 ? genotype : undefined
      );
      navigate("/results", {
        state: {
          result,
          metabolizerPhenotypes: genotype,
        },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const activeGenes = Object.entries(genotype).filter(([, v]) => v);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8 space-y-8">
      {/* Header */}
      <div className="space-y-2">
        <div className="flex items-center gap-3">
          <div className="rounded-lg bg-[var(--primary)]/10 p-2">
            <Dna className="h-6 w-6 text-[var(--primary)]" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-[var(--foreground)]">
              Pharmacogenomics Checker
            </h1>
            <p className="text-sm text-[var(--muted-foreground)]">
              Enter your CYP450 genotype for personalised drug interaction risk
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-6">
        {/* Genotype Input */}
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden">
          <div className="border-b border-[var(--border)] px-5 py-3">
            <h2 className="font-semibold text-[var(--foreground)] flex items-center gap-2 text-sm">
              <Dna className="h-4 w-4 text-[var(--primary)]" />
              Patient CYP450 Genotype
            </h2>
            <p className="text-xs text-[var(--muted-foreground)] mt-0.5">
              Select metaboliser status from genetic testing (e.g. Genomind, GeneSight, 23andMe).
            </p>
          </div>
          <div className="px-5 py-4 space-y-5">
            {CYP_GENES.map((gene) => {
              const selected = genotype[gene.id] || "";
              return (
                <div key={gene.id} className="space-y-1.5">
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <span className="text-sm font-medium text-[var(--foreground)]">
                        {gene.label}
                      </span>
                      <span className="text-xs text-[var(--muted-foreground)] ml-2">
                        {gene.description}
                      </span>
                    </div>
                    {selected && (
                      <span
                        className={`shrink-0 rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                          PHENOTYPE_BADGE[selected] ?? ""
                        }`}
                      >
                        {PHENOTYPES.find((p) => p.value === selected)?.label}
                      </span>
                    )}
                  </div>
                  <PhenotypeDropdown
                    geneId={gene.id}
                    value={selected}
                    onChange={(v) => handleGenotypeChange(gene.id, v)}
                  />
                  {selected && PHENOTYPE_NOTES[selected] && (
                    <p className="text-xs text-[var(--muted-foreground)] flex items-start gap-1">
                      <Info className="h-3 w-3 shrink-0 mt-0.5" />
                      {PHENOTYPE_NOTES[selected]}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Active genotype summary */}
        {activeGenes.length > 0 && (
          <div className="rounded-lg border border-[var(--border)] bg-[var(--secondary)] px-4 py-3">
            <p className="text-xs font-medium text-[var(--muted-foreground)] mb-2">
              Active genotype profile ({activeGenes.length} gene{activeGenes.length !== 1 ? "s" : ""} set):
            </p>
            <div className="flex flex-wrap gap-2">
              {activeGenes.map(([gene, phenotype]) => (
                <span
                  key={gene}
                  className={`rounded-full border px-2.5 py-0.5 text-xs font-medium ${
                    PHENOTYPE_BADGE[phenotype] ?? ""
                  }`}
                >
                  {gene}: {PHENOTYPES.find((p) => p.value === phenotype)?.label}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Drug list input */}
        <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden">
          <div className="border-b border-[var(--border)] px-5 py-3">
            <h2 className="font-semibold text-[var(--foreground)] text-sm">
              Medications to Check
            </h2>
            <p className="text-xs text-[var(--muted-foreground)] mt-0.5">
              Search and add 2–10 drugs to check with your genotype profile.
            </p>
          </div>
          <div className="px-5 py-4">
            <DrugInput onSubmit={handleDrugSubmit} loading={loading} />
          </div>
        </div>

        {/* Risk adjustment note */}
        {activeGenes.some(([, v]) => v === "poor") && (
          <div className="flex items-start gap-3 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 dark:border-amber-800 dark:bg-amber-950/30">
            <AlertTriangle className="h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
            <p className="text-xs text-amber-800 dark:text-amber-300">
              <strong>Poor metaboliser detected.</strong> Drugs metabolised by the affected enzyme(s)
              will have their risk scores increased to reflect potential accumulation and toxicity.
              Always verify dosing with a clinical pharmacist.
            </p>
          </div>
        )}

        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-800 dark:bg-red-950/30 dark:text-red-300">
            {error}
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <p className="text-xs text-center text-[var(--muted-foreground)]">
        Pharmacogenomic risk adjustments are informational only. Always consult a licensed
        pharmacist or physician before changing any medication.
      </p>
    </div>
  );
}
