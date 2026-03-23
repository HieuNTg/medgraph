"""
Prometheus metrics for MEDGRAPH API.

Provides auto-instrumentation via prometheus-fastapi-instrumentator
plus custom application-specific metrics.
"""

from __future__ import annotations

from prometheus_client import CollectorRegistry, Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator


def _get_or_create_histogram(
    name: str, documentation: str, buckets: tuple, registry: CollectorRegistry
) -> Histogram:
    """Get existing histogram or create new one (safe for test reloads)."""
    try:
        return Histogram(name, documentation, buckets=buckets, registry=registry)
    except ValueError:
        # Already registered — return existing collector
        return registry._names_to_collectors[name]  # type: ignore[attr-defined]


def _get_or_create_gauge(name: str, documentation: str, registry: CollectorRegistry) -> Gauge:
    """Get existing gauge or create new one (safe for test reloads)."""
    try:
        return Gauge(name, documentation, registry=registry)
    except ValueError:
        return registry._names_to_collectors[name]  # type: ignore[attr-defined]


def create_metrics(
    registry: CollectorRegistry | None = None,
) -> tuple[Histogram, Gauge, Gauge]:
    """Create application metrics, safe for repeated calls (test reloads).

    Args:
        registry: Custom CollectorRegistry for testing isolation.
                  Defaults to the global default registry.
    """
    from prometheus_client import REGISTRY

    reg = registry or REGISTRY

    analysis_duration = _get_or_create_histogram(
        "medgraph_analysis_duration_seconds",
        "Time spent running cascade analysis",
        buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
        registry=reg,
    )
    graph_nodes = _get_or_create_gauge(
        "medgraph_graph_nodes_total",
        "Total number of nodes in the knowledge graph",
        registry=reg,
    )
    graph_edges = _get_or_create_gauge(
        "medgraph_graph_edges_total",
        "Total number of edges in the knowledge graph",
        registry=reg,
    )
    return analysis_duration, graph_nodes, graph_edges


# Module-level metrics (safe for reload via _get_or_create helpers)
ANALYSIS_DURATION, GRAPH_NODES, GRAPH_EDGES = create_metrics()


def setup_metrics(app: object) -> Instrumentator:
    """Configure and attach Prometheus instrumentation to the FastAPI app.

    Returns the Instrumentator instance for testing access.
    """
    instrumentator = Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        excluded_handlers=["/metrics", "/health", "/health/live", "/health/ready"],
    )
    instrumentator.instrument(app)
    instrumentator.expose(app, include_in_schema=False)
    return instrumentator
