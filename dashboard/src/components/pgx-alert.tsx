import { AlertTriangle, Dna, Info } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { PGxAlert } from "@/lib/types";

interface PGxAlertProps {
  alerts: PGxAlert[];
  ancestry?: string | null;
}

export function PGxAlertPanel({ alerts, ancestry }: PGxAlertProps) {
  if (!alerts || alerts.length === 0) return null;

  const severityColor = (multiplier: number) => {
    if (multiplier >= 2.5)
      return "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
    if (multiplier >= 1.5)
      return "bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300";
    return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300";
  };

  const severityLabel = (multiplier: number) => {
    if (multiplier >= 2.5) return "Critical";
    if (multiplier >= 1.5) return "Important";
    return "Informational";
  };

  return (
    <Card className="border-purple-200 dark:border-purple-800">
      <CardContent className="pt-6">
        <div className="flex items-center gap-2 mb-4">
          <Dna className="h-5 w-5 text-purple-600 dark:text-purple-400" />
          <h3 className="font-semibold text-[var(--foreground)]">
            Pharmacogenomics Alerts
          </h3>
          {ancestry && (
            <Badge variant="outline" className="text-xs">
              {ancestry}
            </Badge>
          )}
        </div>

        <div className="space-y-3">
          {alerts.map((alert, i) => (
            <div
              key={`${alert.drug_name}-${alert.gene}-${i}`}
              className={`rounded-lg p-3 ${severityColor(alert.severity_multiplier)}`}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <AlertTriangle className="h-4 w-4 shrink-0" />
                  <span className="font-medium text-sm">
                    {alert.drug_name} — {alert.gene}
                  </span>
                </div>
                <Badge variant="outline" className="text-xs shrink-0">
                  {severityLabel(alert.severity_multiplier)}
                </Badge>
              </div>
              <p className="mt-1 text-sm opacity-90">
                <span className="font-medium">Phenotype:</span>{" "}
                {alert.phenotype.replace(/_/g, " ")}
              </p>
              <p className="mt-1 text-sm opacity-80">{alert.recommendation}</p>
              {alert.population_frequency != null && (
                <p className="mt-1 text-xs opacity-70">
                  <Info className="inline h-3 w-3 mr-1" />
                  Population frequency:{" "}
                  {(alert.population_frequency * 100).toFixed(1)}%
                </p>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
