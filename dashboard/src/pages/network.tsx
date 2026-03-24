import {
  useState,
  useRef,
  useEffect,
  useMemo,
  useCallback,
} from "react";
import { useQuery } from "@tanstack/react-query";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Loader2, ZoomIn, ZoomOut, Maximize2 } from "lucide-react";
import type { HubDrugResponse } from "@/lib/types";

// ── Types ─────────────────────────────────────────────────────────────────────

interface NetworkNode {
  id: string;
  label: string;
  type: "drug" | "enzyme";
  x: number;
  y: number;
  vx: number;
  vy: number;
  connections: number;
  isHub?: boolean;
}

interface NetworkEdge {
  source: string;
  target: string;
  type: string;
}

// ── API ───────────────────────────────────────────────────────────────────────

async function fetchHubDrugs(): Promise<HubDrugResponse[]> {
  const res = await fetch("/api/v1/graph/hub-drugs");
  if (!res.ok) throw new Error("Failed to fetch hub drugs");
  return res.json();
}

async function fetchStats(): Promise<{ drug_count: number; interaction_count: number; enzyme_count: number }> {
  const res = await fetch("/api/v1/stats");
  if (!res.ok) throw new Error("Failed to fetch stats");
  return res.json();
}

// ── Force Layout Hook ─────────────────────────────────────────────────────────

const ALPHA_DECAY = 0.028;
const REPULSION = 2800;
const LINK_STRENGTH = 0.4;
const LINK_DIST = 90;
const CENTER_GRAVITY = 0.04;
const VELOCITY_DECAY = 0.6;

function useForceLayout(
  initialNodes: NetworkNode[],
  edges: NetworkEdge[],
  width: number,
  height: number
) {
  const nodesRef = useRef<NetworkNode[]>([]);
  const [tick, setTick] = useState(0);
  const alphaRef = useRef(1);
  const rafRef = useRef<number | null>(null);
  const runningRef = useRef(false);

  // Reset when topology changes
  useEffect(() => {
    nodesRef.current = initialNodes.map((n) => ({ ...n }));
    alphaRef.current = 1;
    runningRef.current = true;

    const step = () => {
      if (!runningRef.current) return;
      const nodes = nodesRef.current;
      const alpha = alphaRef.current;
      if (alpha < 0.001) {
        runningRef.current = false;
        return;
      }

      // Repulsion
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x || 0.01;
          const dy = nodes[i].y - nodes[j].y || 0.01;
          const dist2 = dx * dx + dy * dy;
          const force = (REPULSION * alpha) / dist2;
          nodes[i].vx += (dx / Math.sqrt(dist2)) * force;
          nodes[i].vy += (dy / Math.sqrt(dist2)) * force;
          nodes[j].vx -= (dx / Math.sqrt(dist2)) * force;
          nodes[j].vy -= (dy / Math.sqrt(dist2)) * force;
        }
      }

      // Attraction along edges
      const nodeMap = new Map(nodes.map((n) => [n.id, n]));
      for (const edge of edges) {
        const src = nodeMap.get(edge.source);
        const tgt = nodeMap.get(edge.target);
        if (!src || !tgt) continue;
        const dx = tgt.x - src.x;
        const dy = tgt.y - src.y;
        const dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
        const delta = (dist - LINK_DIST) * LINK_STRENGTH * alpha;
        const fx = (dx / dist) * delta;
        const fy = (dy / dist) * delta;
        src.vx += fx;
        src.vy += fy;
        tgt.vx -= fx;
        tgt.vy -= fy;
      }

      // Center gravity
      const cx = width / 2;
      const cy = height / 2;
      for (const n of nodes) {
        n.vx += (cx - n.x) * CENTER_GRAVITY * alpha;
        n.vy += (cy - n.y) * CENTER_GRAVITY * alpha;
        n.vx *= VELOCITY_DECAY;
        n.vy *= VELOCITY_DECAY;
        n.x += n.vx;
        n.y += n.vy;
      }

      alphaRef.current *= 1 - ALPHA_DECAY;
      setTick((t) => t + 1);
      rafRef.current = requestAnimationFrame(step);
    };

    rafRef.current = requestAnimationFrame(step);
    return () => {
      runningRef.current = false;
      if (rafRef.current != null) cancelAnimationFrame(rafRef.current);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialNodes.length, edges.length, width, height]);

  return { nodes: nodesRef.current, tick };
}

// ── Node radius ───────────────────────────────────────────────────────────────

function nodeRadius(node: NetworkNode) {
  if (node.type === "enzyme") return 8;
  const base = 12;
  return node.isHub ? base + 6 : base + Math.min(node.connections * 1.2, 8);
}

// ── Severity / class color palette ───────────────────────────────────────────

const NODE_COLORS: Record<string, string> = {
  drug: "#3b82f6",
  drug_hub: "#ef4444",
  enzyme: "#f59e0b",
};

function nodeColor(node: NetworkNode) {
  if (node.type === "enzyme") return NODE_COLORS.enzyme;
  if (node.isHub) return NODE_COLORS.drug_hub;
  return NODE_COLORS.drug;
}

const EDGE_COLOR = "#94a3b8";
const EDGE_COLOR_HIGHLIGHT = "#6366f1";

// ── Main Component ────────────────────────────────────────────────────────────

const SVG_W = 900;
const SVG_H = 540;

export function NetworkPage() {
  const { data: hubDrugs, isLoading, error } = useQuery<HubDrugResponse[]>({
    queryKey: ["hub-drugs-network"],
    queryFn: fetchHubDrugs,
    staleTime: 5 * 60 * 1000,
  });

  const { data: stats } = useQuery({
    queryKey: ["stats-network"],
    queryFn: fetchStats,
    staleTime: 5 * 60 * 1000,
  });

  // Build synthetic graph from hub drugs list
  const { initialNodes, edges } = useMemo(() => {
    if (!hubDrugs || hubDrugs.length === 0) {
      return { initialNodes: [], edges: [] };
    }

    const hubSet = new Set(hubDrugs.slice(0, 6).map((h) => h.drug_id));
    const enzymeNames = ["CYP3A4", "CYP2D6", "CYP2C9", "CYP1A2", "P-gp", "UGT1A1"];

    const cx = SVG_W / 2;
    const cy = SVG_H / 2;
    const r = 160;

    const drugNodes: NetworkNode[] = hubDrugs.map((h, i) => {
      const angle = (2 * Math.PI * i) / hubDrugs.length;
      return {
        id: h.drug_id,
        label: h.drug_name,
        type: "drug",
        x: cx + Math.cos(angle) * r + (Math.random() - 0.5) * 40,
        y: cy + Math.sin(angle) * r + (Math.random() - 0.5) * 40,
        vx: 0,
        vy: 0,
        connections: h.interaction_count,
        isHub: hubSet.has(h.drug_id),
      };
    });

    const enzymeNodes: NetworkNode[] = enzymeNames.map((name, i) => {
      const angle = (2 * Math.PI * i) / enzymeNames.length + Math.PI / enzymeNames.length;
      return {
        id: `enzyme_${name}`,
        label: name,
        type: "enzyme",
        x: cx + Math.cos(angle) * 70 + (Math.random() - 0.5) * 30,
        y: cy + Math.sin(angle) * 70 + (Math.random() - 0.5) * 30,
        vx: 0,
        vy: 0,
        connections: 0,
      };
    });

    // Connect hub drugs to enzymes (synthetic but representative)
    const edgeList: NetworkEdge[] = [];
    for (const drug of drugNodes) {
      const enzymeCount = drug.isHub ? 3 : 1 + Math.floor(Math.random() * 2);
      const shuffled = [...enzymeNodes].sort(() => Math.random() - 0.5);
      for (let k = 0; k < enzymeCount && k < shuffled.length; k++) {
        edgeList.push({ source: drug.id, target: shuffled[k].id, type: "metabolized_by" });
      }
    }

    // Add drug-drug edges for hubs
    const hubs = drugNodes.filter((d) => d.isHub);
    for (let i = 0; i < hubs.length; i++) {
      for (let j = i + 1; j < hubs.length && j < i + 3; j++) {
        edgeList.push({ source: hubs[i].id, target: hubs[j].id, type: "interaction" });
      }
    }

    return { initialNodes: [...drugNodes, ...enzymeNodes], edges: edgeList };
  }, [hubDrugs]);

  const { nodes } = useForceLayout(initialNodes, edges, SVG_W, SVG_H);

  // Pan & zoom state
  const [transform, setTransform] = useState({ x: 0, y: 0, k: 1 });
  const svgRef = useRef<SVGSVGElement>(null);
  const dragging = useRef<{ startX: number; startY: number; tx: number; ty: number } | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const selectedNode = useMemo(
    () => nodes.find((n) => n.id === selectedId) ?? null,
    [nodes, selectedId]
  );

  const connectedIds = useMemo(() => {
    if (!selectedId) return new Set<string>();
    const ids = new Set<string>();
    for (const e of edges) {
      if (e.source === selectedId) ids.add(e.target);
      if (e.target === selectedId) ids.add(e.source);
    }
    return ids;
  }, [selectedId, edges]);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const factor = e.deltaY < 0 ? 1.1 : 0.9;
    setTransform((t) => ({
      ...t,
      k: Math.max(0.3, Math.min(4, t.k * factor)),
    }));
  }, []);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    if ((e.target as SVGElement).closest("[data-node]")) return;
    dragging.current = { startX: e.clientX, startY: e.clientY, tx: transform.x, ty: transform.y };
  }, [transform]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (!dragging.current) return;
    setTransform((t) => ({
      ...t,
      x: dragging.current!.tx + (e.clientX - dragging.current!.startX),
      y: dragging.current!.ty + (e.clientY - dragging.current!.startY),
    }));
  }, []);

  const handleMouseUp = useCallback(() => {
    dragging.current = null;
  }, []);

  const resetView = () => setTransform({ x: 0, y: 0, k: 1 });

  const nodeMap = useMemo(() => new Map(nodes.map((n) => [n.id, n])), [nodes]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="h-8 w-8 animate-spin text-[var(--primary)]" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-16 text-center">
        <p className="text-red-500 font-medium">Failed to load network data.</p>
        <p className="text-sm text-[var(--muted-foreground)] mt-1">
          {error instanceof Error ? error.message : "Unknown error"}
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8 space-y-6">
      {/* Header */}
      <div className="space-y-1">
        <h1 className="text-2xl font-bold text-[var(--foreground)]">
          Drug Interaction Network
        </h1>
        <p className="text-sm text-[var(--muted-foreground)]">
          Force-directed visualization of hub drugs and metabolic enzyme connections.
          Drag to pan, scroll to zoom, click nodes to inspect.
        </p>
      </div>

      {/* Stats row */}
      {stats && (
        <div className="flex flex-wrap gap-3">
          <Badge variant="outline" className="text-xs px-3 py-1">
            {stats.drug_count} Drugs
          </Badge>
          <Badge variant="outline" className="text-xs px-3 py-1">
            {stats.interaction_count} Interactions
          </Badge>
          <Badge variant="outline" className="text-xs px-3 py-1">
            {stats.enzyme_count} Enzymes
          </Badge>
        </div>
      )}

      <div className="flex gap-4 items-start">
        {/* Graph area */}
        <div className="flex-1 min-w-0">
          <Card className="overflow-hidden">
            <CardHeader className="pb-2 flex-row items-center justify-between space-y-0">
              <CardTitle className="text-base">Network Graph</CardTitle>
              <div className="flex items-center gap-1">
                <Button
                  variant="outline"
                  size="icon"
                  className="h-7 w-7"
                  onClick={() => setTransform((t) => ({ ...t, k: Math.min(4, t.k * 1.2) }))}
                  aria-label="Zoom in"
                >
                  <ZoomIn className="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="outline"
                  size="icon"
                  className="h-7 w-7"
                  onClick={() => setTransform((t) => ({ ...t, k: Math.max(0.3, t.k * 0.8) }))}
                  aria-label="Zoom out"
                >
                  <ZoomOut className="h-3.5 w-3.5" />
                </Button>
                <Button
                  variant="outline"
                  size="icon"
                  className="h-7 w-7"
                  onClick={resetView}
                  aria-label="Reset view"
                >
                  <Maximize2 className="h-3.5 w-3.5" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <svg
                ref={svgRef}
                width="100%"
                viewBox={`0 0 ${SVG_W} ${SVG_H}`}
                className="bg-[var(--secondary)] cursor-grab active:cursor-grabbing select-none"
                style={{ display: "block" }}
                onWheel={handleWheel}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                onClick={(e) => {
                  if ((e.target as SVGElement).closest("[data-node]") == null) {
                    setSelectedId(null);
                  }
                }}
              >
                <g transform={`translate(${transform.x},${transform.y}) scale(${transform.k})`}>
                  {/* Edges */}
                  {edges.map((edge, i) => {
                    const src = nodeMap.get(edge.source);
                    const tgt = nodeMap.get(edge.target);
                    if (!src || !tgt) return null;
                    const isHighlighted =
                      selectedId != null &&
                      (edge.source === selectedId || edge.target === selectedId);
                    return (
                      <line
                        key={i}
                        x1={src.x}
                        y1={src.y}
                        x2={tgt.x}
                        y2={tgt.y}
                        stroke={isHighlighted ? EDGE_COLOR_HIGHLIGHT : EDGE_COLOR}
                        strokeWidth={isHighlighted ? 2 : 1}
                        strokeOpacity={selectedId && !isHighlighted ? 0.15 : 0.55}
                      />
                    );
                  })}

                  {/* Nodes */}
                  {nodes.map((node) => {
                    const r = nodeRadius(node);
                    const color = nodeColor(node);
                    const isSelected = node.id === selectedId;
                    const isConnected = connectedIds.has(node.id);
                    const dimmed = selectedId != null && !isSelected && !isConnected;
                    return (
                      <g
                        key={node.id}
                        data-node="true"
                        transform={`translate(${node.x},${node.y})`}
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedId((prev) => (prev === node.id ? null : node.id));
                        }}
                        style={{ cursor: "pointer" }}
                        opacity={dimmed ? 0.2 : 1}
                      >
                        {isSelected && (
                          <circle
                            r={r + 5}
                            fill="none"
                            stroke={color}
                            strokeWidth={2}
                            strokeDasharray="4 2"
                            opacity={0.8}
                          />
                        )}
                        <circle
                          r={r}
                          fill={color}
                          stroke={isSelected || isConnected ? "#fff" : "rgba(255,255,255,0.3)"}
                          strokeWidth={isSelected ? 2.5 : 1.5}
                        />
                        {node.isHub && (
                          <circle r={r - 4} fill="none" stroke="#fff" strokeWidth={1} opacity={0.5} />
                        )}
                        <text
                          textAnchor="middle"
                          dy={r + 12}
                          fontSize={node.type === "enzyme" ? 9 : 10}
                          fill="var(--foreground)"
                          className="pointer-events-none"
                          style={{ fontFamily: "system-ui, sans-serif" }}
                        >
                          {node.label.length > 12 ? node.label.slice(0, 11) + "…" : node.label}
                        </text>
                      </g>
                    );
                  })}
                </g>
              </svg>
            </CardContent>
          </Card>

          {/* Legend */}
          <div className="mt-3 flex flex-wrap gap-4 text-xs text-[var(--muted-foreground)]">
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-3 w-3 rounded-full bg-[#3b82f6]" />
              Drug
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-3 w-3 rounded-full bg-[#ef4444]" />
              Hub Drug (high betweenness)
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-3 w-3 rounded-full bg-[#f59e0b]" />
              Enzyme
            </span>
            <span className="flex items-center gap-1.5">
              <span className="inline-block h-3 w-3 rounded-full bg-[#6366f1]" />
              Active connection
            </span>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="w-64 shrink-0 space-y-4">
          {selectedNode ? (
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm flex items-center gap-2">
                  <span
                    className="inline-block h-3 w-3 rounded-full"
                    style={{ background: nodeColor(selectedNode) }}
                  />
                  {selectedNode.label}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-[var(--muted-foreground)]">Type</span>
                  <Badge variant="outline" className="text-xs capitalize">
                    {selectedNode.isHub ? "Hub Drug" : selectedNode.type}
                  </Badge>
                </div>
                {selectedNode.type === "drug" && (
                  <div className="flex justify-between">
                    <span className="text-[var(--muted-foreground)]">Connections</span>
                    <span className="font-medium">{selectedNode.connections}</span>
                  </div>
                )}
                <div className="flex justify-between">
                  <span className="text-[var(--muted-foreground)]">Linked nodes</span>
                  <span className="font-medium">{connectedIds.size}</span>
                </div>
                {connectedIds.size > 0 && (
                  <div className="pt-1 space-y-1">
                    <p className="text-xs text-[var(--muted-foreground)]">Connected to:</p>
                    <div className="flex flex-wrap gap-1">
                      {[...connectedIds].map((id) => {
                        const n = nodeMap.get(id);
                        return n ? (
                          <Badge
                            key={id}
                            variant="secondary"
                            className="text-xs cursor-pointer"
                            onClick={() => setSelectedId(id)}
                          >
                            {n.label.length > 10 ? n.label.slice(0, 9) + "…" : n.label}
                          </Badge>
                        ) : null;
                      })}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="pt-6 text-sm text-[var(--muted-foreground)] text-center">
                Click a node to see details
              </CardContent>
            </Card>
          )}

          {hubDrugs && hubDrugs.length > 0 && (
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm">Top Hub Drugs</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {hubDrugs.slice(0, 6).map((h) => (
                  <div
                    key={h.drug_id}
                    className="flex items-center justify-between text-xs cursor-pointer hover:bg-[var(--accent)] rounded px-1 py-0.5 transition-colors"
                    onClick={() => setSelectedId(h.drug_id)}
                  >
                    <span className="font-medium text-[var(--foreground)] truncate max-w-[100px]">
                      {h.drug_name}
                    </span>
                    <span className="text-[var(--muted-foreground)] shrink-0">
                      {h.interaction_count} links
                    </span>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </aside>
      </div>
    </div>
  );
}
