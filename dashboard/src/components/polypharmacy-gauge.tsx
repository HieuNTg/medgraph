/**
 * Polypharmacy risk gauge.
 *
 * SVG semicircle gauge from 0–100 with color-coded risk zones:
 *   0–34  → green (low)
 *   35–59 → yellow (moderate)
 *   60–79 → orange (high)
 *   80+   → red (critical)
 */

import type { PolypharmacyResponse } from "@/lib/types";

interface PolypharmacyGaugeProps {
  data: PolypharmacyResponse;
}

const RISK_CONFIG: Record<string, { color: string; label: string }> = {
  low: { color: "#22c55e", label: "Low Risk" },
  moderate: { color: "#eab308", label: "Moderate Risk" },
  high: { color: "#f97316", label: "High Risk" },
  critical: { color: "#ef4444", label: "Critical Risk" },
};

function gaugeColor(score: number): string {
  if (score < 35) return "#22c55e";
  if (score < 60) return "#eab308";
  if (score < 80) return "#f97316";
  return "#ef4444";
}

/** Compute SVG arc path for a semicircle gauge needle track (180°). */
function arcPath(cx: number, cy: number, r: number, startDeg: number, endDeg: number): string {
  const toRad = (d: number) => ((d - 90) * Math.PI) / 180;
  const x1 = cx + r * Math.cos(toRad(startDeg));
  const y1 = cy + r * Math.sin(toRad(startDeg));
  const x2 = cx + r * Math.cos(toRad(endDeg));
  const y2 = cy + r * Math.sin(toRad(endDeg));
  const large = endDeg - startDeg > 180 ? 1 : 0;
  return `M${x1},${y1} A${r},${r} 0 ${large} 1 ${x2},${y2}`;
}

export function PolypharmacyGauge({ data }: PolypharmacyGaugeProps) {
  const score = Math.min(Math.max(data.polypharmacy_score, 0), 100);
  const risk = data.risk_level?.toLowerCase() ?? "low";
  const config = RISK_CONFIG[risk] ?? RISK_CONFIG.low;

  // Semicircle from -180° to 0° (left to right), needle angle in that range
  const W = 260;
  const H = 150;
  const cx = W / 2;
  const cy = H - 10;
  const R = 100;

  // Arc spans 180° (from 180° to 360° in SVG coords, i.e. left to right at bottom)
  // Map score 0→180deg, 100→360deg in standard coords
  const startAngle = 180; // leftmost
  const endAngle = 360;   // rightmost
  const filled = startAngle + (score / 100) * 180;

  const color = gaugeColor(score);

  // Needle
  const needleDeg = startAngle + (score / 100) * 180;
  const needleRad = ((needleDeg - 90) * Math.PI) / 180;
  const nx = cx + (R - 10) * Math.cos(needleRad);
  const ny = cy + (R - 10) * Math.sin(needleRad);

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5 space-y-4">
      <div className="flex flex-col items-center">
        <svg
          width={W}
          height={H}
          role="img"
          aria-label={`Polypharmacy risk gauge: ${score.toFixed(0)} out of 100, ${config.label}`}
        >
          <title>Polypharmacy Risk Assessment</title>
          {/* Background track */}
          <path
            d={arcPath(cx, cy, R, startAngle, endAngle)}
            fill="none"
            stroke="#e5e7eb"
            strokeWidth={16}
            strokeLinecap="round"
          />
          {/* Filled arc */}
          {score > 0 && (
            <path
              d={arcPath(cx, cy, R, startAngle, filled)}
              fill="none"
              stroke={color}
              strokeWidth={16}
              strokeLinecap="round"
            />
          )}
          {/* Needle */}
          <line
            x1={cx}
            y1={cy}
            x2={nx}
            y2={ny}
            stroke={color}
            strokeWidth={2.5}
            strokeLinecap="round"
          />
          <circle cx={cx} cy={cy} r={5} fill={color} />

          {/* Score label */}
          <text x={cx} y={cy - 22} textAnchor="middle" fontSize={28} fontWeight="700" fill={color}>
            {score.toFixed(0)}
          </text>
          <text x={cx} y={cy - 6} textAnchor="middle" fontSize={11} fill="currentColor" className="text-[var(--muted-foreground)]">
            / 100
          </text>

          {/* Zone labels */}
          <text x={12} y={cy + 4} fontSize={9} fill="#22c55e">0</text>
          <text x={W - 18} y={cy + 4} fontSize={9} fill="#ef4444">100</text>
        </svg>

        <div
          className="mt-1 text-sm font-semibold"
          style={{ color }}
        >
          {config.label}
        </div>
        {data.summary && (
          <p className="text-xs text-[var(--muted-foreground)] text-center mt-1 max-w-xs">
            {data.summary}
          </p>
        )}
      </div>

      {/* Risk clusters */}
      {data.risk_clusters.length > 0 && (
        <div className="space-y-1">
          <h4 className="text-xs font-medium text-[var(--muted-foreground)]">
            Risk clusters
          </h4>
          <ul className="space-y-1">
            {data.risk_clusters.map((cluster, i) => (
              <li
                key={i}
                className="rounded-md border border-[var(--border)] bg-[var(--secondary)] px-3 py-2 text-xs text-[var(--foreground)]"
              >
                {typeof cluster.label === "string"
                  ? cluster.label
                  : JSON.stringify(cluster)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
