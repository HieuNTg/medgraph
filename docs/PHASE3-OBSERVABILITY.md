# MEDGRAPH — Phase 3: Observability & Monitoring

**Status**: Complete
**Completion Date**: 2026-03-23
**Test Coverage**: 14 new tests in `tests/test_observability.py`

## Overview

Phase 3 adds comprehensive observability and monitoring to MEDGRAPH. The system now exports Prometheus metrics, supports structured JSON logging with request tracing, implements health check probes (K8s-compatible), and provides optional error tracking via Sentry.

## Key Features

### 1. Prometheus Metrics

**Endpoint**: `GET /metrics` (no auth required)

**Format**: Prometheus text exposition format

**Custom Application Metrics**:
- `medgraph_analysis_duration_seconds` (Histogram)
  - Measures time spent running cascade analysis
  - Buckets: 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0 seconds
  - Automatically recorded on each `/api/v1/check` call

- `medgraph_graph_nodes_total` (Gauge)
  - Total number of nodes in the knowledge graph
  - Updated at server startup from GraphStore
  - Metric exported at `/metrics` endpoint

- `medgraph_graph_edges_total` (Gauge)
  - Total number of edges in the knowledge graph
  - Updated at server startup from GraphStore
  - Metric exported at `/metrics` endpoint

**Auto-Instrumented Metrics** (via `prometheus-fastapi-instrumentator`):
- `http_requests_total` — total request count by method, path, status
- `http_request_duration_seconds` — request latency histogram
- `http_request_size_bytes` — request payload size
- `http_response_size_bytes` — response payload size

**Excluded Paths** (not auto-instrumented):
- `/metrics` (avoid recursion)
- `/health` (health checks excluded)
- `/health/live`
- `/health/ready`

**Implementation Details**:
- Module: `medgraph/api/metrics.py`
- Safe for repeated calls / test reloads via `_get_or_create_histogram()` and `_get_or_create_gauge()`
- Metrics initialized at module load time; gauges updated during lifespan startup
- Prometheus client uses default global registry unless custom registry passed (for test isolation)

### 2. Health Check Endpoints (Kubernetes-Compatible)

**Liveness Probe** — `GET /health/live`
```json
{
  "status": "ok"
}
```
- No database checks
- Verifies process is responding
- Fast response (no I/O)
- Use case: Container restart if unresponsive

**Readiness Probe** — `GET /health/ready`
```json
{
  "status": "ok",
  "db_size": 123,
  "graph_nodes": 97,
  "graph_edges": 245
}
```
- Verifies database is accessible
- Verifies knowledge graph is loaded in memory
- Includes aggregate statistics
- Use case: Traffic routing / deployment verification

**Backward Compatibility** — `GET /health`
- Alias for `/health/ready`
- Maintained for existing clients
- Identical response format

**Docker & Kubernetes Integration**:
- `Dockerfile` healthcheck uses `/health/live`
- K8s liveness probe: `httpGet: {path: /health/live, port: 8000}`
- K8s readiness probe: `httpGet: {path: /health/ready, port: 8000}`

### 3. Structured Logging with Request Tracing

**Trigger**: Set environment variable `MEDGRAPH_LOG_FORMAT=json`

**Output Format** (one JSON object per log line):
```json
{
  "timestamp": "2026-03-23T14:30:45.123456+00:00",
  "level": "INFO",
  "logger": "medgraph.api.server",
  "message": "MEDGRAPH loaded: 89 drugs, 28 interactions, 97 graph nodes, 245 graph edges",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Configuration**:
- `MEDGRAPH_LOG_FORMAT` (default: "text")
  - "text" → human-readable format
  - "json" → structured JSON output
- `MEDGRAPH_LOG_LEVEL` (default: "INFO")
  - Controls logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

**Request ID Injection**:
- Middleware generates/retrieves `X-Request-ID` header (UUID4 if missing)
- Automatically injected into all log records via `LogRecord.request_id` attribute
- Persists across entire request lifecycle
- Enables full request tracing in log aggregation systems

**Implementation**:
- Module: `medgraph/logging_config.py`
  - `JSONFormatter.format()` — converts LogRecord to single-line JSON
  - `configure_logging()` — sets up handlers based on env vars
- Middleware: `medgraph/api/middleware.py`
  - Logs `request_start` and `request_end` events with request_id
  - Records path, method, and status_code

**Log Aggregation Integration**:
- Fluentd, Splunk, DataDog, CloudWatch can parse JSON logs
- Request tracing: correlate all logs with same `request_id`
- Structured fields enable metric extraction and alerting

### 4. Error Tracking (Sentry Integration - Optional)

**Trigger**: Set `SENTRY_DSN` environment variable

**Configuration**:
- `SENTRY_DSN` (required)
  - Sentry DSN URL; if not set, Sentry is disabled (no warning)
  - Format: `https://{key}@{org}.ingest.sentry.io/{project}`

- `SENTRY_TRACES_RATE` (optional, default: 0.1)
  - Trace sample rate for performance monitoring
  - Range: 0.0–1.0
  - 0.1 = 10% of requests sampled

- `MEDGRAPH_ENV` (optional, default: "development")
  - Environment tag in Sentry (e.g., "production", "staging")

**Dependencies**:
- Requires `sentry-sdk[fastapi]` (optional dependency)
- Install: `pip install -e ".[sentry]"`
- If SENTRY_DSN is set but sentry-sdk not installed → warning logged, continues without tracking

**What Gets Tracked**:
- Unhandled exceptions in endpoints
- HTTP error responses (4xx, 5xx)
- Performance metrics (response time, payload size)
- Request context (method, path, status code)

**Implementation**:
- Module: `medgraph/api/server.py`, function `_init_sentry()`
- Called at app startup; catches ImportError if sentry-sdk unavailable
- Configures FastAPI integration for automatic instrumentation

**Example**: Production deployment
```bash
export SENTRY_DSN="https://abc123@myorg.ingest.sentry.io/7890"
export SENTRY_TRACES_RATE=0.05
export MEDGRAPH_ENV="production"
python -m medgraph.cli serve
```

## Architecture Diagram (Updated)

```
┌────────────────────────────────────────────────────┐
│              Observability Stack                    │
├────────────────────────────────────────────────────┤
│ Prometheus (scrapes /metrics)                       │
│ │                                                   │
│ └─→ medgraph_analysis_duration_seconds (histogram) │
│     medgraph_graph_nodes_total (gauge)             │
│     medgraph_graph_edges_total (gauge)             │
│     http_* (auto-instrumented)                     │
├────────────────────────────────────────────────────┤
│ Structured Logs (JSON format)                       │
│ │                                                   │
│ └─→ {"timestamp", "level", "logger", "message",   │
│      "request_id", "exception?"}                   │
│     → Fluentd / Splunk / CloudWatch / Datadog      │
├────────────────────────────────────────────────────┤
│ Sentry (optional, SENTRY_DSN gated)                │
│ │                                                   │
│ └─→ Errors, traces, performance metrics            │
└────────────────────────────────────────────────────┘
        ↓
┌────────────────────────────────────────────────────┐
│            FastAPI Application                      │
│                                                     │
│  GET /metrics             → Prometheus format      │
│  GET /health/live         → liveness probe         │
│  GET /health/ready        → readiness probe        │
│  GET /health              → backward compat        │
│  All endpoints            → request_id in logs     │
│  (SENTRY_DSN set?)        → error tracking         │
└────────────────────────────────────────────────────┘
```

## Environment Variables (Phase 3)

| Variable | Default | Purpose |
|----------|---------|---------|
| `MEDGRAPH_LOG_FORMAT` | "text" | "text" or "json" for logging format |
| `MEDGRAPH_LOG_LEVEL` | "INFO" | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| `SENTRY_DSN` | (none) | Sentry DSN; if unset, error tracking disabled |
| `SENTRY_TRACES_RATE` | 0.1 | Trace sample rate (0.0–1.0) for Sentry |
| `MEDGRAPH_ENV` | "development" | Environment tag for Sentry |

## Deployment Example

### Docker Compose (Observability Stack)

```yaml
version: '3.8'

services:
  medgraph-api:
    image: medgraph:latest
    ports:
      - "8000:8000"
    environment:
      MEDGRAPH_LOG_FORMAT: json
      MEDGRAPH_LOG_LEVEL: INFO
      SENTRY_DSN: https://key@org.ingest.sentry.io/123
      SENTRY_TRACES_RATE: "0.1"
      MEDGRAPH_ENV: production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 5s

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  # Fluentd for log aggregation
  fluentd:
    image: fluent/fluent-bit:latest
    ports:
      - "24224:24224"
    volumes:
      - ./fluent-bit.conf:/fluent-bit/etc/fluent-bit.conf
```

### Prometheus Config Scrape Job

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'medgraph'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

## Testing

**Test File**: `tests/test_observability.py` (14 tests)

**Test Coverage**:
1. Prometheus metrics endpoint returns 200
2. Prometheus metrics output contains expected format (#HELP, #TYPE lines)
3. Custom metrics are present in output
4. Analysis duration metric recorded on /api/v1/check
5. Graph nodes/edges gauges set at startup
6. Health check split:
   - `/health/live` returns 200 with LivenessResponse
   - `/health/ready` returns 200 with HealthResponse + db_size + graph_nodes
   - `/health` aliases to `/health/ready`
7. Structured logging:
   - JSONFormatter produces valid JSON
   - request_id field present when set
   - timestamp, level, logger, message fields present
8. Sentry initialization:
   - Initializes when SENTRY_DSN set
   - Logs warning when SENTRY_DSN set but sentry-sdk not installed

**Run Tests**:
```bash
pytest tests/test_observability.py -v
```

## Files Changed

**Backend**:
- `medgraph/api/metrics.py` — NEW: Prometheus metrics setup
- `medgraph/api/server.py` — Updated: health endpoint split, setup_metrics(), _init_sentry()
- `medgraph/api/middleware.py` — Updated: request_end log with status_code, request_id injection
- `medgraph/api/models.py` — NEW: LivenessResponse model
- `medgraph/logging_config.py` — NEW: JSONFormatter, structured logging config

**Configuration**:
- `pyproject.toml` — Added: prometheus-fastapi-instrumentator, sentry optional dep

**Deployment**:
- `Dockerfile` — Updated: healthcheck uses /health/live
- `docker-compose.yml` — Updated: healthcheck uses /health/live

**Tests**:
- `tests/test_observability.py` — NEW: 14 tests for Phase 3

## Breaking Changes

None. Phase 3 is fully backward-compatible:
- New endpoints do not conflict with existing API
- Structured logging is opt-in (MEDGRAPH_LOG_FORMAT=json)
- Sentry is opt-in (SENTRY_DSN env var)
- Old `/health` endpoint remains as alias for `/health/ready`

## Next Steps

1. **Metrics Alerting** — Configure Prometheus alerting rules
   - High analysis duration: `medgraph_analysis_duration_seconds > 5`
   - API errors: `increase(http_requests_total{status=~"5.."}[5m])`

2. **Dashboards** — Create Grafana dashboards
   - Analysis performance (latency, throughput)
   - Graph size (nodes, edges) over time
   - Error rates by endpoint

3. **Log Aggregation** — Deploy ELK / Splunk / Datadog
   - Ingest JSON logs from containers
   - Enable request tracing across services

4. **Distributed Tracing** — Consider OpenTelemetry
   - Trace cascade analysis calls to Graph operations
   - Export to Jaeger or CloudTrace

## Summary

Phase 3 brings MEDGRAPH to production readiness:
- **Observability** — Prometheus metrics + structured JSON logs
- **Reliability** — Health checks (K8s-compatible liveness/readiness)
- **Debugging** — Request tracing via X-Request-ID
- **Errors** — Optional error tracking via Sentry
- **Compatibility** — Zero breaking changes; all opt-in features
