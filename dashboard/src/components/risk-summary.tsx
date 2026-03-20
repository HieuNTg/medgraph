import { useRef } from "react";
import {
  AlertOctagon,
  AlertTriangle,
  AlertCircle,
  Info,
  Download,
  Clock,
} from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { CheckResponse } from "@/lib/types";

interface RiskSummaryProps {
  response: CheckResponse;
}

const RISK_CONFIG: Record<
  string,
  { label: string; color: string; icon: React.ElementType }
> = {
  critical: { label: "Critical Risk", color: "#dc2626", icon: AlertOctagon },
  major: { label: "Major Risk", color: "#ea580c", icon: AlertTriangle },
  moderate: { label: "Moderate Risk", color: "#ca8a04", icon: AlertCircle },
  minor: { label: "Minor Risk", color: "#2563eb", icon: Info },
  safe: { label: "No Significant Risk", color: "#16a34a", icon: Info },
};

const SEVERITY_ORDER = ["critical", "major", "moderate", "minor"];

export function RiskSummary({ response }: RiskSummaryProps) {
  const summaryRef = useRef<HTMLDivElement>(null);

  const risk = response.overall_risk?.toLowerCase() ?? "safe";
  const config = RISK_CONFIG[risk] ?? RISK_CONFIG.safe;
  const Icon = config.icon;

  // Build severity distribution data for donut
  const severityCounts = SEVERITY_ORDER.reduce(
    (acc, sev) => {
      acc[sev] = response.interactions.filter((i) => i.severity === sev).length;
      return acc;
    },
    {} as Record<string, number>
  );

  const pieData = SEVERITY_ORDER.filter((sev) => severityCounts[sev] > 0).map(
    (sev) => ({
      name: sev,
      value: severityCounts[sev],
      color: RISK_CONFIG[sev]?.color ?? "#6b7280",
    })
  );

  const handleExport = async () => {
    if (!summaryRef.current) return;
    try {
      const { default: html2canvas } = await import("html2canvas");
      const canvas = await html2canvas(summaryRef.current, {
        backgroundColor: "#ffffff",
        scale: 2,
      });
      const link = document.createElement("a");
      link.download = `medgraph-report-${Date.now()}.png`;
      link.href = canvas.toDataURL("image/png");
      link.click();
    } catch (err) {
      console.error("Export failed:", err);
    }
  };

  const timestamp = new Date(response.timestamp).toLocaleString();

  return (
    <Card ref={summaryRef}>
      <CardHeader>
        <div className="flex items-start justify-between gap-4">
          <div className="flex items-center gap-4">
            <div
              className="flex h-16 w-16 items-center justify-center rounded-full"
              style={{ backgroundColor: config.color + "20" }}
            >
              <Icon
                className="h-8 w-8"
                style={{ color: config.color }}
              />
            </div>
            <div>
              <CardTitle
                className="text-2xl"
                style={{ color: config.color }}
              >
                {config.label}
              </CardTitle>
              <p className="text-sm text-[var(--muted-foreground)] mt-1">
                {response.drug_count} medications analyzed ·{" "}
                {response.interaction_count} interaction
                {response.interaction_count !== 1 ? "s" : ""} found
              </p>
            </div>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleExport}
            className="flex items-center gap-2 shrink-0"
          >
            <Download className="h-4 w-4" />
            Export PNG
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Severity distribution */}
        {pieData.length > 0 && (
          <div className="flex items-center gap-6">
            <div className="h-32 w-32 shrink-0">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius="55%"
                    outerRadius="80%"
                    dataKey="value"
                    strokeWidth={0}
                  >
                    {pieData.map((entry, i) => (
                      <Cell key={i} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value, name) => [
                      `${value} interaction${Number(value) !== 1 ? "s" : ""}`,
                      (name as string).charAt(0).toUpperCase() +
                        (name as string).slice(1),
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-2">
              {SEVERITY_ORDER.filter((sev) => severityCounts[sev] > 0).map(
                (sev) => (
                  <div key={sev} className="flex items-center gap-2 text-sm">
                    <div
                      className="h-3 w-3 rounded-full shrink-0"
                      style={{ backgroundColor: RISK_CONFIG[sev]?.color }}
                    />
                    <span className="capitalize text-[var(--foreground)]">
                      {sev}
                    </span>
                    <span className="font-medium text-[var(--foreground)]">
                      {severityCounts[sev]}
                    </span>
                  </div>
                )
              )}
            </div>
          </div>
        )}

        {/* Timestamp */}
        <div className="flex items-center gap-2 text-xs text-[var(--muted-foreground)]">
          <Clock className="h-3.5 w-3.5" />
          Analysis performed: {timestamp}
        </div>
      </CardContent>
    </Card>
  );
}
