import { useState } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  AlertCircle,
  Info,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { CascadePath } from "@/components/cascade-path";
import { EvidencePanel } from "@/components/evidence-panel";
import type { InteractionResult } from "@/lib/types";

interface InteractionCardProps {
  interaction: InteractionResult;
}

const SEVERITY_CONFIG = {
  critical: {
    label: "Critical",
    icon: AlertOctagon,
    badge: "critical" as const,
    progressClass: "bg-[var(--color-critical)]",
    borderClass: "border-l-4 border-l-[var(--color-critical)]",
  },
  major: {
    label: "Major",
    icon: AlertTriangle,
    badge: "major" as const,
    progressClass: "bg-[var(--color-major)]",
    borderClass: "border-l-4 border-l-[var(--color-major)]",
  },
  moderate: {
    label: "Moderate",
    icon: AlertCircle,
    badge: "moderate" as const,
    progressClass: "bg-[var(--color-moderate)]",
    borderClass: "border-l-4 border-l-[var(--color-moderate)]",
  },
  minor: {
    label: "Minor",
    icon: Info,
    badge: "minor" as const,
    progressClass: "bg-[var(--color-minor)]",
    borderClass: "border-l-4 border-l-[var(--color-minor)]",
  },
};

export function InteractionCard({ interaction }: InteractionCardProps) {
  const [showCascade, setShowCascade] = useState(false);
  const [showEvidence, setShowEvidence] = useState(false);

  const config = SEVERITY_CONFIG[interaction.severity] ?? SEVERITY_CONFIG.minor;
  const Icon = config.icon;

  return (
    <Card className={config.borderClass}>
      <CardContent className="pt-6 space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-3">
            <Icon
              className={`h-5 w-5 shrink-0 severity-${interaction.severity}`}
            />
            <div>
              <h3 className="font-semibold text-[var(--foreground)]">
                {interaction.drug_a.name} + {interaction.drug_b.name}
              </h3>
              {interaction.mechanism && (
                <p className="text-xs text-[var(--muted-foreground)] mt-0.5">
                  {interaction.mechanism}
                </p>
              )}
            </div>
          </div>
          <Badge variant={config.badge} className="shrink-0">
            {config.label}
          </Badge>
        </div>

        {/* Risk score */}
        <div className="space-y-1">
          <div className="flex justify-between text-xs text-[var(--muted-foreground)]">
            <span>Risk Score</span>
            <span className="font-medium">
              {Math.round(interaction.risk_score)}%
            </span>
          </div>
          <Progress
            value={interaction.risk_score}
            indicatorClassName={config.progressClass}
            className="h-2"
          />
        </div>

        {/* Description */}
        <p className="text-sm text-[var(--foreground)] leading-relaxed">
          {interaction.description}
        </p>

        {/* Toggles */}
        {(interaction.cascade_paths.length > 0 ||
          interaction.evidence.length > 0) && (
          <div className="flex gap-2 flex-wrap">
            {interaction.cascade_paths.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowCascade((p) => !p)}
                className="flex items-center gap-1.5"
              >
                {showCascade ? (
                  <ChevronUp className="h-3.5 w-3.5" />
                ) : (
                  <ChevronDown className="h-3.5 w-3.5" />
                )}
                {showCascade ? "Hide" : "View"} Cascade Path
              </Button>
            )}
            {interaction.evidence.length > 0 && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowEvidence((p) => !p)}
                className="flex items-center gap-1.5"
              >
                {showEvidence ? (
                  <ChevronUp className="h-3.5 w-3.5" />
                ) : (
                  <ChevronDown className="h-3.5 w-3.5" />
                )}
                {showEvidence ? "Hide" : "View"} Evidence (
                {interaction.evidence.length})
              </Button>
            )}
          </div>
        )}

        {/* Expandable: Cascade */}
        {showCascade && interaction.cascade_paths.length > 0 && (
          <>
            <Separator />
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-[var(--foreground)]">
                Cascade Pathway
              </h4>
              {interaction.cascade_paths.map((path, i) => (
                <CascadePath key={i} path={path} />
              ))}
            </div>
          </>
        )}

        {/* Expandable: Evidence */}
        {showEvidence && interaction.evidence.length > 0 && (
          <>
            <Separator />
            <div className="space-y-3">
              <h4 className="text-sm font-semibold text-[var(--foreground)]">
                Evidence Sources
              </h4>
              <EvidencePanel evidence={interaction.evidence} />
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
