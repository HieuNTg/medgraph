import { useLocation, useNavigate, Link } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  RotateCcw,
  Network,
  FileDown,
  Loader2,
  Dna,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { RiskSummary } from "@/components/risk-summary";
import { InteractionCard } from "@/components/interaction-card";
import { PGxAlertPanel } from "@/components/pgx-alert";
import { InteractionGraph } from "@/components/interaction-graph";
import { PathwayGraph } from "@/components/pathway-graph";
import { ContraindicationMatrix } from "@/components/contraindication-matrix";
import { DeprescribingPanel } from "@/components/deprescribing-panel";
import { PolypharmacyGauge } from "@/components/polypharmacy-gauge";
import type {
  CheckResponse,
  ContraindicationResponse,
  DeprescribingResponse,
  InteractionResult,
  PathwayResponse,
  PolypharmacyResponse,
  PGxAlert,
} from "@/lib/types";
import {
  exportPdfReport,
  getPathways,
  getContraindications,
  getDeprescribingRecs,
} from "@/lib/api";

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
  metabolizerPhenotypes?: Record<string, string>;
  pgxAlerts?: PGxAlert[];
  ancestry?: string | null;
}

/** Collapsible section wrapper. */
function CollapsibleSection({
  title,
  icon,
  defaultOpen = false,
  children,
}: {
  title: string;
  icon?: React.ReactNode;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden">
      <button
        onClick={() => setOpen((p) => !p)}
        className="w-full flex items-center justify-between px-5 py-3 text-left hover:bg-[var(--secondary)] transition-colors"
        aria-expanded={open}
      >
        <span className="font-semibold text-[var(--foreground)] flex items-center gap-2 text-sm">
          {icon}
          {title}
        </span>
        {open ? (
          <ChevronUp className="h-4 w-4 text-[var(--muted-foreground)]" />
        ) : (
          <ChevronDown className="h-4 w-4 text-[var(--muted-foreground)]" />
        )}
      </button>
      {open && <div className="px-5 pb-5 pt-2">{children}</div>}
    </div>
  );
}

/** Derive a naive polypharmacy score from the check response. */
function derivePolypharmacyData(result: CheckResponse): PolypharmacyResponse {
  const score = Math.min(result.overall_score * 100, 100);
  const risk_level =
    score < 35 ? "low" : score < 60 ? "moderate" : score < 80 ? "high" : "critical";
  return {
    polypharmacy_score: score,
    risk_level,
    risk_clusters: [],
    summary: result.interaction_count > 0
      ? `${result.interaction_count} interaction${result.interaction_count !== 1 ? "s" : ""} detected across ${result.drug_count} drug${result.drug_count !== 1 ? "s" : ""}.`
      : "No significant interactions detected.",
  };
}

export function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as ResultsState | null;
  const [showGraph, setShowGraph] = useState(true);
  const graphContainerRef = useRef<HTMLDivElement>(null);
  const [graphWidth, setGraphWidth] = useState(700);
  const [exporting, setExporting] = useState(false);

  const drugIds = state?.result?.drugs?.map((d) => d.id) ?? [];

  const {
    data: pathwayData,
    isLoading: pathwayLoading,
    error: pathwayQueryError,
  } = useQuery<PathwayResponse>({
    queryKey: ["pathways", drugIds],
    queryFn: () => getPathways(drugIds),
    enabled: drugIds.length > 0,
  });

  const {
    data: contraindicationData,
    isLoading: contraindicationLoading,
    error: contraindicationQueryError,
  } = useQuery<ContraindicationResponse>({
    queryKey: ["contraindications", drugIds],
    queryFn: () => getContraindications(drugIds),
    enabled: drugIds.length > 0,
  });

  const {
    data: deprescribingData,
    isLoading: deprescribingLoading,
    error: deprescribingQueryError,
  } = useQuery<DeprescribingResponse[]>({
    queryKey: ["deprescribing", drugIds],
    queryFn: () => getDeprescribingRecs(drugIds),
    enabled: drugIds.length > 0,
  });

  const pathwayError = pathwayQueryError
    ? pathwayQueryError instanceof Error
      ? pathwayQueryError.message
      : "Failed to load pathways"
    : null;
  const contraindicationError = contraindicationQueryError
    ? contraindicationQueryError instanceof Error
      ? contraindicationQueryError.message
      : "Failed to load contraindications"
    : null;
  const deprescribingError = deprescribingQueryError
    ? deprescribingQueryError instanceof Error
      ? deprescribingQueryError.message
      : "Failed to load deprescribing data"
    : null;

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

  const { result, metabolizerPhenotypes, pgxAlerts, ancestry } = state;

  const handleExportPdf = async () => {
    setExporting(true);
    try {
      let graphPng: string | undefined;
      const canvas = graphContainerRef.current?.querySelector("canvas");
      if (canvas && showGraph) {
        graphPng = canvas.toDataURL("image/png").replace("data:image/png;base64,", "");
      }
      const blob = await exportPdfReport(result, graphPng);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `medgraph-report-${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF export failed:", err);
    } finally {
      setExporting(false);
    }
  };

  const sorted = sortBySeverity(result.interactions);
  const hasGraphData =
    result.drugs.some((d) => d.enzyme_relations.length > 0) ||
    result.interactions.some((i) => i.cascade_paths.length > 0);

  const polypharmacyData = derivePolypharmacyData(result);

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

      {/* Polypharmacy gauge */}
      <PolypharmacyGauge data={polypharmacyData} />

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
              <InteractionGraph data={result} width={graphWidth} height={450} />
              <p className="text-xs text-[var(--muted-foreground)] mt-2">
                Drag nodes to rearrange. Scroll to zoom. Blue circles = drugs,
                amber rectangles = enzymes.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Metabolic Pathway Graph */}
      {(pathwayData || pathwayLoading) && (
        <CollapsibleSection
          title="Metabolic Pathway Graph"
          icon={<Network className="h-4 w-4 text-[var(--primary)]" />}
          defaultOpen={false}
        >
          {pathwayLoading && (
            <p className="text-sm text-[var(--muted-foreground)] animate-pulse py-4 text-center">
              Loading pathway data…
            </p>
          )}
          {pathwayError && (
            <p className="text-sm text-red-500 py-4 text-center">{pathwayError}</p>
          )}
          {pathwayData && !pathwayLoading && (
            <PathwayGraph data={pathwayData} width={graphWidth || 600} height={380} />
          )}
        </CollapsibleSection>
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

      {/* Pharmacogenomics context */}
      {metabolizerPhenotypes && Object.keys(metabolizerPhenotypes).length > 0 && (
        <div className="flex flex-wrap items-center gap-2 rounded-lg border border-[var(--border)] bg-[var(--card)] px-4 py-3">
          <Dna className="h-4 w-4 shrink-0 text-[var(--primary)]" />
          <span className="text-xs font-medium text-[var(--muted-foreground)]">
            Pharmacogenomics applied:
          </span>
          {Object.entries(metabolizerPhenotypes).map(([gene, phenotype]) => (
            <span
              key={gene}
              className="rounded-full border border-[var(--border)] bg-[var(--secondary)] px-2.5 py-0.5 text-xs text-[var(--foreground)]"
            >
              {gene}: {phenotype}
            </span>
          ))}
        </div>
      )}

      {/* PGx Alerts */}
      {pgxAlerts && pgxAlerts.length > 0 && (
        <PGxAlertPanel alerts={pgxAlerts} ancestry={ancestry} />
      )}

      {/* Contraindication Matrix */}
      <CollapsibleSection
        title="Contraindication Matrix"
        defaultOpen={false}
      >
        {contraindicationLoading && (
          <p className="text-sm text-[var(--muted-foreground)] animate-pulse py-4 text-center">
            Loading contraindication data…
          </p>
        )}
        {contraindicationError && (
          <p className="text-sm text-red-500 py-4 text-center">{contraindicationError}</p>
        )}
        {contraindicationData && !contraindicationLoading && (
          <ContraindicationMatrix data={contraindicationData} />
        )}
        {!contraindicationData && !contraindicationLoading && !contraindicationError && (
          <p className="text-sm text-[var(--muted-foreground)] py-4 text-center">
            No contraindication data available
          </p>
        )}
      </CollapsibleSection>

      {/* Interaction cards */}
      {sorted.length > 0 ? (
        <div className="space-y-4">
          <h2 className="font-semibold text-[var(--foreground)]">
            {sorted.length} Interaction{sorted.length !== 1 ? "s" : ""} Found
          </h2>
          {sorted.map((interaction) => (
            <InteractionCard
              key={`${interaction.drug_a.id}-${interaction.drug_b.id}`}
              interaction={interaction}
            />
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

      {/* Deprescribing Panel */}
      <CollapsibleSection
        title="Deprescribing Recommendations"
        defaultOpen={false}
      >
        <DeprescribingPanel
          recommendations={deprescribingData ?? []}
          loading={deprescribingLoading}
          error={deprescribingError}
        />
      </CollapsibleSection>

      {/* Actions */}
      <div className="flex gap-3">
        <Button asChild variant="outline">
          <Link to="/checker" className="flex items-center gap-2">
            <RotateCcw className="h-4 w-4" />
            Check Another Combination
          </Link>
        </Button>
        <Button
          variant="default"
          onClick={handleExportPdf}
          disabled={exporting}
          className="flex items-center gap-2"
        >
          {exporting ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Generating PDF…
            </>
          ) : (
            <>
              <FileDown className="h-4 w-4" />
              Export PDF Report
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
