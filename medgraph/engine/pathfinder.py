"""
Graph pathfinder for MEDGRAPH cascade analysis.

Implements BFS-based enzyme cascade path detection through the knowledge graph.
Finds pharmacokinetic cascade paths between input drugs mediated by shared enzymes.

Cascade detection principle:
    Drug A --[inhibits]--> CYP3A4 <--[metabolized_by]-- Drug B
    => Drug A inhibits CYP3A4, Drug B needs CYP3A4 for metabolism
    => Drug B accumulates => TOXICITY RISK
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Optional

import networkx as nx

from medgraph.engine.models import CascadePath, CascadeStep

logger = logging.getLogger(__name__)

# Max BFS depth to prevent combinatorial explosion
DEFAULT_MAX_DEPTH = 3

_SEVERITY_ORDER = {"critical": 4, "major": 3, "moderate": 2, "minor": 1, "none": 0}


class PathFinder:
    """
    Finds enzyme-mediated cascade interaction paths between drugs in the knowledge graph.

    All path finding is performed on a pre-built NetworkX DiGraph.
    """

    def find_cascade_paths(
        self,
        graph: nx.DiGraph,
        drug_ids: list[str],
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> list[CascadePath]:
        """
        Find all relevant cascade paths between the input drugs.

        Uses BFS from each drug node through enzyme nodes to reach other input drugs.
        Only paths that START and END at input drugs are returned (relevant cascades).

        Args:
            graph: NetworkX DiGraph from GraphBuilder
            drug_ids: List of drug IDs to analyze
            max_depth: Maximum path length (hops through nodes)

        Returns:
            List of CascadePath objects, deduplicated and sorted by severity
        """
        if len(drug_ids) < 2:
            return []

        drug_nodes = {f"drug:{did}" for did in drug_ids if f"drug:{did}" in graph}
        if len(drug_nodes) < 2:
            return []

        all_paths: list[CascadePath] = []

        # Optimization: pre-compute each drug's enzyme neighborhood once,
        # then do direct enzyme-based cascade detection (O(drugs * enzymes))
        # rather than full BFS from each source (much faster for large drug sets).
        enzyme_cascade_paths = self._find_enzyme_cascades(graph, list(drug_nodes))
        all_paths.extend(enzyme_cascade_paths)

        # For max_depth > 2, also run BFS for multi-hop paths (depth 3)
        # Only do this when drug count is small to keep performance bounded.
        if max_depth > 2 and len(drug_nodes) <= 5:
            for source_node in drug_nodes:
                target_nodes = drug_nodes - {source_node}
                paths = self._bfs_paths(graph, source_node, target_nodes, max_depth)
                all_paths.extend(paths)

        # Deduplicate
        seen: set[str] = set()
        unique_paths: list[CascadePath] = []
        for path in all_paths:
            key = f"{path.drug_a_name}:{path.drug_b_name}:{path.description[:60]}"
            rev_key = f"{path.drug_b_name}:{path.drug_a_name}:{path.description[:60]}"
            if key not in seen and rev_key not in seen:
                seen.add(key)
                unique_paths.append(path)

        # Sort by severity (highest first)
        unique_paths.sort(
            key=lambda p: _SEVERITY_ORDER.get(p.net_severity, 0),
            reverse=True,
        )
        return unique_paths

    def find_shared_enzymes(
        self,
        graph: nx.DiGraph,
        drug_a_id: str,
        drug_b_id: str,
    ) -> list[str]:
        """
        Find enzyme IDs connected to both drugs (shared enzyme pathways).

        Args:
            graph: Knowledge graph
            drug_a_id: First drug ID
            drug_b_id: Second drug ID

        Returns:
            List of enzyme IDs shared between the two drugs
        """
        node_a = f"drug:{drug_a_id}"
        node_b = f"drug:{drug_b_id}"

        if node_a not in graph or node_b not in graph:
            return []

        enzymes_a = {
            n for n in graph.successors(node_a) if graph.nodes[n].get("node_type") == "enzyme"
        }
        enzymes_b = {
            n for n in graph.successors(node_b) if graph.nodes[n].get("node_type") == "enzyme"
        }
        shared = enzymes_a & enzymes_b
        return [n.replace("enzyme:", "") for n in shared]

    def explain_path(self, path: CascadePath) -> str:
        """
        Generate a detailed human-readable explanation of a cascade path.

        Args:
            path: CascadePath to explain

        Returns:
            Multi-sentence explanation string
        """
        if not path.steps:
            return path.description

        parts: list[str] = []
        for step in path.steps:
            verb = {
                "inhibits": "inhibits",
                "induces": "induces/upregulates",
                "metabolized_by": "is metabolized by",
                "interacts_with": "directly interacts with",
            }.get(step.relation, step.relation)

            parts.append(
                f"{step.source_drug} ({step.strength}) {verb} {step.target}. Effect: {step.effect}."
            )

        return " → ".join(parts)

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _find_enzyme_cascades(
        self,
        graph: nx.DiGraph,
        drug_nodes: list[str],
    ) -> list[CascadePath]:
        """
        Fast O(drugs * enzymes) cascade detection via shared enzyme analysis.

        For each enzyme node, find all drugs that inhibit/induce it and all drugs
        that are metabolized by it. Build cascade paths for relevant combinations.
        This replaces the slower BFS for 2-hop (drug -> enzyme -> drug) paths.
        """
        # Build enzyme -> {inhibitors, inducers, substrates} index
        enzyme_data: dict[str, dict[str, list[tuple[str, str]]]] = {}
        # enzyme_id -> {"inhibits": [(drug_node, strength)], "induces": [...], "metabolized_by": [...]}

        for drug_node in drug_nodes:
            if drug_node not in graph:
                continue
            for enzyme_node in graph.successors(drug_node):
                if graph.nodes[enzyme_node].get("node_type") != "enzyme":
                    continue
                edge = graph.edges.get((drug_node, enzyme_node), {})
                relation = edge.get("relation", "")
                strength = edge.get("strength", "moderate")
                if relation not in ("inhibits", "induces", "metabolized_by"):
                    continue
                if enzyme_node not in enzyme_data:
                    enzyme_data[enzyme_node] = {"inhibits": [], "induces": [], "metabolized_by": []}
                enzyme_data[enzyme_node][relation].append((drug_node, strength))

        # Generate cascade paths from enzyme relationships
        paths: list[CascadePath] = []
        drug_node_set = set(drug_nodes)

        for enzyme_node, relations in enzyme_data.items():
            enzyme_name = graph.nodes[enzyme_node].get("name", enzyme_node)
            enzyme_id = graph.nodes[enzyme_node].get(
                "enzyme_id", enzyme_node.replace("enzyme:", "")
            )

            inhibitors = [(d, s) for d, s in relations["inhibits"] if d in drug_node_set]
            inducers = [(d, s) for d, s in relations["induces"] if d in drug_node_set]
            substrates = [(d, s) for d, s in relations["metabolized_by"] if d in drug_node_set]

            # Pattern: Inhibitor -> Enzyme <- Substrate
            for inh_node, inh_str in inhibitors:
                for sub_node, sub_str in substrates:
                    if inh_node == sub_node:
                        continue
                    inh_name = graph.nodes[inh_node].get("name", inh_node)
                    sub_name = graph.nodes[sub_node].get("name", sub_node)

                    step1 = CascadeStep(
                        source_drug=inh_name,
                        target=enzyme_name,
                        target_type="enzyme",
                        relation="inhibits",
                        strength=inh_str,
                        effect=f"{inh_str} reduction in {enzyme_name} activity → {sub_name} accumulates",
                    )
                    step2 = CascadeStep(
                        source_drug=enzyme_name,
                        target=sub_name,
                        target_type="drug",
                        relation="metabolized_by",
                        strength=sub_str,
                        effect=f"{sub_name} requires {enzyme_name} for metabolism → levels increase",
                    )
                    severity = "major" if inh_str == "strong" else "moderate"
                    desc = (
                        f"{inh_name} inhibits {enzyme_id}, which is required to metabolize {sub_name}. "
                        f"Result: {sub_name} plasma levels increase, raising the risk of toxicity."
                    )
                    paths.append(
                        CascadePath(
                            steps=[step1, step2],
                            net_severity=severity,
                            description=desc,
                            drug_a_name=inh_name,
                            drug_b_name=sub_name,
                            enzyme_ids=[enzyme_id],
                        )
                    )

            # Pattern: Inducer -> Enzyme <- Substrate
            for ind_node, ind_str in inducers:
                for sub_node, sub_str in substrates:
                    if ind_node == sub_node:
                        continue
                    ind_name = graph.nodes[ind_node].get("name", ind_node)
                    sub_name = graph.nodes[sub_node].get("name", sub_node)

                    step1 = CascadeStep(
                        source_drug=ind_name,
                        target=enzyme_name,
                        target_type="enzyme",
                        relation="induces",
                        strength=ind_str,
                        effect=f"{ind_str} increase in {enzyme_name} activity → {sub_name} metabolized faster",
                    )
                    step2 = CascadeStep(
                        source_drug=enzyme_name,
                        target=sub_name,
                        target_type="drug",
                        relation="metabolized_by",
                        strength=sub_str,
                        effect=f"{sub_name} levels decrease → reduced efficacy",
                    )
                    severity = "major" if ind_str == "strong" else "moderate"
                    desc = (
                        f"{ind_name} induces {enzyme_id}, accelerating {sub_name} metabolism. "
                        f"Result: {sub_name} plasma levels decrease, potentially reducing efficacy."
                    )
                    paths.append(
                        CascadePath(
                            steps=[step1, step2],
                            net_severity=severity,
                            description=desc,
                            drug_a_name=ind_name,
                            drug_b_name=sub_name,
                            enzyme_ids=[enzyme_id],
                        )
                    )

        return paths

    def _bfs_paths(
        self,
        graph: nx.DiGraph,
        source: str,
        targets: set[str],
        max_depth: int,
    ) -> list[CascadePath]:
        """
        BFS from source drug node to any target drug node, through enzyme intermediaries.

        Returns CascadePath objects for valid pharmacokinetic cascades.
        """
        # BFS state: (current_node, path_of_nodes, path_of_edges)
        queue: deque[tuple[str, list[str], list[dict]]] = deque()
        queue.append((source, [source], []))

        found_paths: list[CascadePath] = []
        visited_states: set[tuple] = set()

        while queue:
            current, node_path, edge_path = queue.popleft()

            depth = len(node_path) - 1
            if depth > max_depth:
                continue

            state = (current, tuple(node_path))
            if state in visited_states:
                continue
            visited_states.add(state)

            # Check if we reached a target drug (not the source)
            if current in targets and current != source and len(node_path) > 1:
                # Build cascade path from this route
                cascade = self._build_cascade_path(graph, node_path, edge_path)
                if cascade:
                    found_paths.append(cascade)
                continue  # Don't expand further from target

            # Only expand if we haven't exceeded depth
            if depth >= max_depth:
                continue

            for neighbor in graph.successors(current):
                if neighbor in node_path:
                    continue  # Avoid cycles

                node_type = graph.nodes[neighbor].get("node_type", "")
                edge_data = graph.edges.get((current, neighbor), {})

                # Filter: only traverse meaningful pharmacokinetic edges
                relation = edge_data.get("relation", "")
                if not self._is_valid_edge(node_type, relation, current, source, targets):
                    continue

                queue.append((neighbor, node_path + [neighbor], edge_path + [edge_data]))

        return found_paths

    def _is_valid_edge(
        self,
        target_node_type: str,
        relation: str,
        current_node: str,
        source_node: str,
        target_nodes: set[str],
    ) -> bool:
        """
        Filter edges to only traverse pharmacokinetically meaningful paths.

        Valid traversal patterns:
        - drug -> enzyme (inhibits, induces, metabolized_by)
        - enzyme -> [other drugs via reverse lookup — handled in BFS via predecessors]

        We do NOT follow drug -> drug edges here (those are direct interactions,
        handled separately by the analyzer).
        """
        current_type = "enzyme" if "enzyme:" in current_node else "drug"

        if current_type == "drug":
            # From drug: only traverse to enzymes
            return target_node_type == "enzyme" and relation in (
                "inhibits",
                "induces",
                "metabolized_by",
            )
        elif current_type == "enzyme":
            # From enzyme: only traverse to drugs (that are targets or intermediate)
            return target_node_type == "drug"
        return False

    def _build_cascade_path(
        self,
        graph: nx.DiGraph,
        node_path: list[str],
        edge_path: list[dict],
    ) -> Optional[CascadePath]:
        """
        Convert a BFS node/edge path into a structured CascadePath.

        Applies pharmacological logic to infer effects:
        - Drug A inhibits enzyme -> Drug B metabolized_by enzyme = Drug B accumulates
        - Drug A induces enzyme -> Drug B metabolized_by enzyme = Drug B depleted
        """
        if len(node_path) < 3:
            return None

        drug_a_node = node_path[0]
        drug_b_node = node_path[-1]

        # Only continue if start and end are drug nodes
        if (
            graph.nodes[drug_a_node].get("node_type") != "drug"
            or graph.nodes[drug_b_node].get("node_type") != "drug"
        ):
            return None

        drug_a_name = graph.nodes[drug_a_node].get("name", drug_a_node)
        drug_b_name = graph.nodes[drug_b_node].get("name", drug_b_node)

        steps: list[CascadeStep] = []
        enzyme_ids: list[str] = []
        severity = "minor"

        for i, (node, edge) in enumerate(zip(node_path[:-1], edge_path)):
            next_node = node_path[i + 1]
            relation = edge.get("relation", "unknown")
            strength = edge.get("strength", "moderate")

            current_name = graph.nodes[node].get("name", node)
            next_name = graph.nodes[next_node].get("name", next_node)
            next_type = graph.nodes[next_node].get("node_type", "drug")

            # Track enzymes in path
            if next_type == "enzyme":
                enzyme_id = graph.nodes[next_node].get("enzyme_id", next_node)
                enzyme_ids.append(enzyme_id)

            # Compute effect based on relation type
            effect = self._compute_effect(relation, strength, current_name, next_name, next_type)

            steps.append(
                CascadeStep(
                    source_drug=current_name,
                    target=next_name,
                    target_type=next_type,
                    relation=relation,
                    strength=strength,
                    effect=effect,
                )
            )

        # Infer cascade severity from the relation types present
        severity = self._infer_cascade_severity(steps)

        # Build description
        description = self._describe_cascade(drug_a_name, drug_b_name, steps, enzyme_ids)

        return CascadePath(
            steps=steps,
            net_severity=severity,
            description=description,
            drug_a_name=drug_a_name,
            drug_b_name=drug_b_name,
            enzyme_ids=enzyme_ids,
        )

    def _compute_effect(
        self,
        relation: str,
        strength: str,
        source_name: str,
        target_name: str,
        target_type: str,
    ) -> str:
        """Generate human-readable effect string for a single cascade step."""
        if target_type == "enzyme":
            if relation == "inhibits":
                return (
                    f"{strength} reduction in {target_name} activity → substrate drugs accumulate"
                )
            elif relation == "induces":
                return f"{strength} increase in {target_name} activity → substrate drugs depleted faster"
            elif relation == "metabolized_by":
                return f"{source_name} requires {target_name} for metabolism → competes with other substrates"
        else:
            # Drug -> drug transition through enzyme
            return f"altered {source_name} levels affect {target_name} pharmacokinetics"
        return "pharmacokinetic interaction"

    def _infer_cascade_severity(self, steps: list[CascadeStep]) -> str:
        """
        Infer cascade net severity from the combination of relation types and strengths.

        Strong inhibition -> major/critical
        Strong induction -> major
        Moderate inhibition -> moderate
        """
        has_strong = any(s.strength == "strong" for s in steps)
        has_inhibition = any(s.relation == "inhibits" for s in steps)
        has_induction = any(s.relation == "induces" for s in steps)

        if has_strong and has_inhibition:
            return "major"  # Could be critical if score pushes it there
        elif has_strong and has_induction:
            return "major"
        elif has_inhibition:
            return "moderate"
        elif has_induction:
            return "moderate"
        else:
            return "minor"

    def _describe_cascade(
        self,
        drug_a: str,
        drug_b: str,
        steps: list[CascadeStep],
        enzyme_ids: list[str],
    ) -> str:
        """Generate a concise cascade description string."""
        if not enzyme_ids:
            return f"{drug_a} may affect {drug_b} through indirect pharmacokinetic pathway."

        enzyme_str = ", ".join(enzyme_ids)

        # Find the dominant relation type
        relations = [s.relation for s in steps]
        if "inhibits" in relations:
            return (
                f"{drug_a} inhibits {enzyme_str}, which is required to metabolize {drug_b}. "
                f"Result: {drug_b} plasma levels increase, raising the risk of toxicity."
            )
        elif "induces" in relations:
            return (
                f"{drug_a} induces {enzyme_str}, accelerating {drug_b} metabolism. "
                f"Result: {drug_b} plasma levels decrease, potentially reducing efficacy."
            )
        else:
            return (
                f"{drug_a} and {drug_b} share the {enzyme_str} metabolic pathway. "
                f"Competition for the enzyme may lead to variable drug levels."
            )
