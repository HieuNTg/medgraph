/**
 * Interactive knowledge graph visualization for drug interactions.
 *
 * Renders a force-directed graph showing drugs (circles) and enzymes (diamonds)
 * with typed edges (inhibits=red, induces=green, metabolized_by=blue).
 * Users can hover nodes for details and drag to rearrange.
 */

import { useMemo, useRef, useCallback, useEffect } from "react";
import ForceGraph2D, {
  type ForceGraphMethods,
  type NodeObject,
  type LinkObject,
} from "react-force-graph-2d";
import type { CheckResponse } from "@/lib/types";

interface InteractionGraphProps {
  data: CheckResponse;
  width?: number;
  height?: number;
}

interface GraphNode extends NodeObject {
  id: string;
  label: string;
  type: "drug" | "enzyme";
  severity?: string;
}

interface GraphLink extends LinkObject {
  source: string;
  target: string;
  relation: string;
  label: string;
}

// Color scheme for node types
const NODE_COLORS: Record<string, string> = {
  drug: "#3b82f6",      // blue-500
  enzyme: "#f59e0b",    // amber-500
};

const NODE_COLORS_DARK: Record<string, string> = {
  drug: "#60a5fa",      // blue-400
  enzyme: "#fbbf24",    // amber-400
};

// Color scheme for edge relation types
const EDGE_COLORS: Record<string, string> = {
  inhibits: "#ef4444",       // red-500
  induces: "#22c55e",        // green-500
  metabolized_by: "#3b82f6", // blue-500
  interacts_with: "#a855f7", // purple-500
};

/**
 * Build graph data from CheckResponse API response.
 * Extracts unique drugs and enzymes from cascade paths,
 * creating nodes and edges for the force-directed layout.
 */
function buildGraphData(data: CheckResponse) {
  const nodes = new Map<string, GraphNode>();
  const links: GraphLink[] = [];

  // Add drug nodes from the response
  for (const drug of data.drugs) {
    nodes.set(drug.name, {
      id: drug.name,
      label: drug.name,
      type: "drug",
    });

    // Add enzyme nodes from drug's enzyme_relations
    for (const rel of drug.enzyme_relations) {
      if (!nodes.has(rel.enzyme_name)) {
        nodes.set(rel.enzyme_name, {
          id: rel.enzyme_name,
          label: rel.enzyme_name,
          type: "enzyme",
        });
      }

      // Add drug-enzyme edge
      links.push({
        source: drug.name,
        target: rel.enzyme_name,
        relation: rel.relation_type,
        label: `${rel.relation_type} (${rel.strength})`,
      });
    }
  }

  // Add edges from cascade paths for interaction context
  for (const interaction of data.interactions) {
    for (const cascade of interaction.cascade_paths) {
      for (const step of cascade.steps) {
        // Ensure nodes exist
        if (!nodes.has(step.source)) {
          nodes.set(step.source, {
            id: step.source,
            label: step.source,
            type: step.source.startsWith("CYP") ? "enzyme" : "drug",
          });
        }
        if (!nodes.has(step.target)) {
          nodes.set(step.target, {
            id: step.target,
            label: step.target,
            type: step.target.startsWith("CYP") ? "enzyme" : "drug",
          });
        }
      }
    }

    // Add direct interaction edge between drug pairs
    if (interaction.description) {
      const exists = links.some(
        (l) =>
          (l.source === interaction.drug_a.name &&
            l.target === interaction.drug_b.name &&
            l.relation === "interacts_with") ||
          (l.source === interaction.drug_b.name &&
            l.target === interaction.drug_a.name &&
            l.relation === "interacts_with")
      );
      if (!exists && interaction.risk_score > 0) {
        links.push({
          source: interaction.drug_a.name,
          target: interaction.drug_b.name,
          relation: "interacts_with",
          label: `${interaction.severity} interaction`,
        });
      }
    }
  }

  // Deduplicate links (keep unique source-target-relation combos)
  const seen = new Set<string>();
  const uniqueLinks = links.filter((link) => {
    const key = `${link.source}-${link.target}-${link.relation}`;
    const revKey = `${link.target}-${link.source}-${link.relation}`;
    if (seen.has(key) || seen.has(revKey)) return false;
    seen.add(key);
    return true;
  });

  return {
    nodes: Array.from(nodes.values()),
    links: uniqueLinks,
  };
}

export function InteractionGraph({
  data,
  width = 700,
  height = 450,
}: InteractionGraphProps) {
  const graphRef = useRef<ForceGraphMethods<GraphNode, GraphLink>>(undefined);
  const isDark = document.documentElement.classList.contains("dark");

  const graphData = useMemo(() => buildGraphData(data), [data]);

  // Configure forces and zoom to fit on mount
  useEffect(() => {
    const fg = graphRef.current;
    if (fg) {
      // Increase repulsion to spread nodes apart
      fg.d3Force("charge")?.strength(-300);
      fg.d3Force("link")?.distance(100);
    }
    const timer = setTimeout(() => {
      fg?.zoomToFit(400, 50);
    }, 800);
    return () => clearTimeout(timer);
  }, [graphData]);

  // Custom node rendering: circles for drugs, rounded rects for enzymes
  const drawNode = useCallback(
    (node: GraphNode, ctx: CanvasRenderingContext2D, globalScale: number) => {
      const x = node.x ?? 0;
      const y = node.y ?? 0;
      const fontSize = Math.max(11 / globalScale, 3);
      const nodeSize = node.type === "drug" ? 8 : 6;
      const colors = isDark ? NODE_COLORS_DARK : NODE_COLORS;
      const color = colors[node.type] || colors.drug;

      // Draw node shape
      ctx.beginPath();
      if (node.type === "enzyme") {
        // Rounded rectangle for enzymes
        const w = nodeSize * 2.5;
        const h = nodeSize * 1.5;
        const r = 3;
        ctx.moveTo(x - w / 2 + r, y - h / 2);
        ctx.lineTo(x + w / 2 - r, y - h / 2);
        ctx.quadraticCurveTo(x + w / 2, y - h / 2, x + w / 2, y - h / 2 + r);
        ctx.lineTo(x + w / 2, y + h / 2 - r);
        ctx.quadraticCurveTo(x + w / 2, y + h / 2, x + w / 2 - r, y + h / 2);
        ctx.lineTo(x - w / 2 + r, y + h / 2);
        ctx.quadraticCurveTo(x - w / 2, y + h / 2, x - w / 2, y + h / 2 - r);
        ctx.lineTo(x - w / 2, y - h / 2 + r);
        ctx.quadraticCurveTo(x - w / 2, y - h / 2, x - w / 2 + r, y - h / 2);
      } else {
        // Circle for drugs
        ctx.arc(x, y, nodeSize, 0, 2 * Math.PI);
      }
      ctx.fillStyle = color;
      ctx.fill();
      ctx.strokeStyle = isDark ? "#1e293b" : "#ffffff";
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Draw label
      ctx.font = `${fontSize}px Inter, system-ui, sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "top";
      ctx.fillStyle = isDark ? "#e2e8f0" : "#1e293b";
      ctx.fillText(node.label, x, y + nodeSize + 2);
    },
    [isDark]
  );

  // Custom link rendering with color by relation type
  const drawLink = useCallback(
    (
      link: GraphLink,
      ctx: CanvasRenderingContext2D,
      globalScale: number
    ) => {
      const source = link.source as unknown as GraphNode;
      const target = link.target as unknown as GraphNode;
      if (!source.x || !source.y || !target.x || !target.y) return;

      const color = EDGE_COLORS[link.relation] || "#94a3b8";

      // Draw edge line
      ctx.beginPath();
      ctx.moveTo(source.x, source.y);
      ctx.lineTo(target.x, target.y);
      ctx.strokeStyle = color;
      ctx.lineWidth = 1.5 / globalScale;
      ctx.globalAlpha = 0.6;
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Draw arrowhead
      const dx = target.x - source.x;
      const dy = target.y - source.y;
      const angle = Math.atan2(dy, dx);
      const arrowLen = 6 / globalScale;
      const targetR = 10;
      const ax = target.x - Math.cos(angle) * targetR;
      const ay = target.y - Math.sin(angle) * targetR;

      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(
        ax - arrowLen * Math.cos(angle - Math.PI / 6),
        ay - arrowLen * Math.sin(angle - Math.PI / 6)
      );
      ctx.lineTo(
        ax - arrowLen * Math.cos(angle + Math.PI / 6),
        ay - arrowLen * Math.sin(angle + Math.PI / 6)
      );
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();

      // Draw relation label on edge (only when zoomed in enough)
      if (globalScale > 1.2) {
        const midX = (source.x + target.x) / 2;
        const midY = (source.y + target.y) / 2;
        const fontSize = Math.max(8 / globalScale, 3);
        ctx.font = `${fontSize}px Inter, system-ui, sans-serif`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.8;
        ctx.fillText(link.relation, midX, midY - 4 / globalScale);
        ctx.globalAlpha = 1;
      }
    },
    []
  );

  if (graphData.nodes.length === 0) {
    return null;
  }

  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] overflow-hidden">
      {/* Legend */}
      <div className="flex flex-wrap items-center gap-4 px-4 py-2 border-b border-[var(--border)] bg-[var(--secondary)]">
        <span className="text-xs font-medium text-[var(--muted-foreground)]">
          Legend:
        </span>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-3 w-3 rounded-full bg-blue-500" />
          <span className="text-xs text-[var(--muted-foreground)]">Drug</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-3 w-3 rounded bg-amber-500" />
          <span className="text-xs text-[var(--muted-foreground)]">Enzyme</span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-2 w-4 bg-red-500 rounded-full" />
          <span className="text-xs text-[var(--muted-foreground)]">
            Inhibits
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-2 w-4 bg-green-500 rounded-full" />
          <span className="text-xs text-[var(--muted-foreground)]">
            Induces
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-2 w-4 bg-blue-500 rounded-full" />
          <span className="text-xs text-[var(--muted-foreground)]">
            Metabolized by
          </span>
        </div>
        <div className="flex items-center gap-1.5">
          <span className="inline-block h-2 w-4 bg-purple-500 rounded-full" />
          <span className="text-xs text-[var(--muted-foreground)]">
            Interacts
          </span>
        </div>
      </div>

      {/* Graph canvas */}
      <ForceGraph2D
        ref={graphRef}
        graphData={graphData}
        width={width}
        height={height}
        backgroundColor="transparent"
        nodeCanvasObject={drawNode}
        linkCanvasObject={drawLink}
        nodePointerAreaPaint={(node: GraphNode, color, ctx) => {
          const x = node.x ?? 0;
          const y = node.y ?? 0;
          ctx.beginPath();
          ctx.arc(x, y, 10, 0, 2 * Math.PI);
          ctx.fillStyle = color;
          ctx.fill();
        }}
        linkDirectionalArrowLength={0}
        cooldownTicks={150}
        d3AlphaDecay={0.03}
        d3VelocityDecay={0.25}
        enableZoomInteraction={true}
        enablePanInteraction={true}
        enableNodeDrag={true}
      />
    </div>
  );
}
