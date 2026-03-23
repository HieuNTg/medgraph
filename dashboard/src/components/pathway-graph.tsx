/**
 * SVG-based metabolic pathway graph visualization.
 *
 * Renders drug nodes (circles) and enzyme nodes (diamonds) connected by
 * typed edges. Uses a simple circular layout — no external graph library.
 *
 * Edge colors: red=inhibits, green=induces, blue=metabolized_by, gray=other
 */

import { useMemo } from "react";
import type { PathwayResponse } from "@/lib/types";

interface PathwayGraphProps {
  data: PathwayResponse;
  width?: number;
  height?: number;
}

const EDGE_COLOR: Record<string, string> = {
  inhibits: "#ef4444",
  induces: "#22c55e",
  metabolized_by: "#3b82f6",
};

function edgeColor(relation: string): string {
  return EDGE_COLOR[relation] ?? "#94a3b8";
}

/** Place nodes in a circle around the center. */
function circularLayout(
  count: number,
  cx: number,
  cy: number,
  radius: number
): { x: number; y: number }[] {
  if (count === 0) return [];
  return Array.from({ length: count }, (_, i) => {
    const angle = (2 * Math.PI * i) / count - Math.PI / 2;
    return { x: cx + radius * Math.cos(angle), y: cy + radius * Math.sin(angle) };
  });
}

export function PathwayGraph({
  data,
  width = 600,
  height = 400,
}: PathwayGraphProps) {
  const { positions, nodeMap } = useMemo(() => {
    const cx = width / 2;
    const cy = height / 2;
    const radius = Math.min(cx, cy) * 0.7;
    const coords = circularLayout(data.nodes.length, cx, cy, radius);
    const map = new Map<string, { x: number; y: number }>();
    data.nodes.forEach((n, i) => map.set(n.id, coords[i]));
    return { positions: coords, nodeMap: map };
  }, [data.nodes, width, height]);

  if (data.nodes.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-sm text-[var(--muted-foreground)]">
        No pathway data available
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden">
      {/* Legend */}
      <div className="flex flex-wrap items-center gap-4 px-4 py-2 border-b border-[var(--border)] bg-[var(--secondary)]">
        <span className="text-xs font-medium text-[var(--muted-foreground)]">Legend:</span>
        <LegendItem color="#3b82f6" shape="circle" label="Drug" />
        <LegendItem color="#f59e0b" shape="diamond" label="Enzyme" />
        <LegendItem color="#ef4444" shape="line" label="Inhibits" />
        <LegendItem color="#22c55e" shape="line" label="Induces" />
        <LegendItem color="#3b82f6" shape="line" label="Metabolized by" />
      </div>

      <svg
        width={width}
        height={height}
        aria-label="Metabolic pathway graph"
        className="block"
        style={{ background: "transparent" }}
      >
        <defs>
          {["inhibits", "induces", "metabolized_by", "other"].map((rel) => {
            const col = edgeColor(rel);
            return (
              <marker
                key={rel}
                id={`arrow-${rel}`}
                viewBox="0 -4 8 8"
                refX="8"
                refY="0"
                markerWidth="6"
                markerHeight="6"
                orient="auto"
              >
                <path d="M0,-4L8,0L0,4" fill={col} />
              </marker>
            );
          })}
        </defs>

        {/* Edges */}
        {data.edges.map((edge, i) => {
          const s = nodeMap.get(edge.source);
          const t = nodeMap.get(edge.target);
          if (!s || !t) return null;
          const col = edgeColor(edge.relation);
          const markerId = EDGE_COLOR[edge.relation] ? `arrow-${edge.relation}` : "arrow-other";
          return (
            <line
              key={i}
              x1={s.x}
              y1={s.y}
              x2={t.x}
              y2={t.y}
              stroke={col}
              strokeWidth={1.5}
              strokeOpacity={0.65}
              markerEnd={`url(#${markerId})`}
            />
          );
        })}

        {/* Nodes */}
        {data.nodes.map((node) => {
          const pos = nodeMap.get(node.id);
          if (!pos) return null;
          return node.type === "enzyme" ? (
            <EnzymNode key={node.id} x={pos.x} y={pos.y} label={node.label} />
          ) : (
            <DrugNode key={node.id} x={pos.x} y={pos.y} label={node.label} />
          );
        })}
      </svg>
    </div>
  );
}

function DrugNode({ x, y, label }: { x: number; y: number; label: string }) {
  return (
    <g>
      <circle cx={x} cy={y} r={10} fill="#3b82f6" stroke="#ffffff" strokeWidth={1.5} />
      <text
        x={x}
        y={y + 18}
        textAnchor="middle"
        fontSize={10}
        fill="currentColor"
        className="text-[var(--foreground)]"
      >
        {label.length > 12 ? `${label.slice(0, 11)}…` : label}
      </text>
    </g>
  );
}

function EnzymNode({ x, y, label }: { x: number; y: number; label: string }) {
  const s = 10;
  const points = `${x},${y - s} ${x + s},${y} ${x},${y + s} ${x - s},${y}`;
  return (
    <g>
      <polygon points={points} fill="#f59e0b" stroke="#ffffff" strokeWidth={1.5} />
      <text
        x={x}
        y={y + s + 8}
        textAnchor="middle"
        fontSize={10}
        fill="currentColor"
        className="text-[var(--foreground)]"
      >
        {label.length > 12 ? `${label.slice(0, 11)}…` : label}
      </text>
    </g>
  );
}

function LegendItem({
  color,
  shape,
  label,
}: {
  color: string;
  shape: "circle" | "diamond" | "line";
  label: string;
}) {
  return (
    <div className="flex items-center gap-1.5">
      {shape === "circle" && (
        <span
          className="inline-block h-3 w-3 rounded-full shrink-0"
          style={{ background: color }}
        />
      )}
      {shape === "diamond" && (
        <svg width={12} height={12} className="shrink-0">
          <polygon points="6,0 12,6 6,12 0,6" fill={color} />
        </svg>
      )}
      {shape === "line" && (
        <span
          className="inline-block h-0.5 w-4 rounded-full shrink-0"
          style={{ background: color }}
        />
      )}
      <span className="text-xs text-[var(--muted-foreground)]">{label}</span>
    </div>
  );
}
