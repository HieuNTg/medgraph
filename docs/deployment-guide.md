# MEDGRAPH — Deployment Guide

## Prerequisites
- Python 3.11+
- Node 20+
- Git

---

## Local Development

### 1. Install dependencies
```bash
pip install -e ".[dev]"
cd dashboard && npm install && cd ..
```

Or via Makefile:
```bash
make install
```

### 2. Seed the database

**Base seed (89 drugs, 28 interactions):**
```bash
python -m medgraph.cli seed
# creates data/medgraph.db with base dataset
```

**Expanded seed (507 drugs, 243 interactions, 182 enzyme relations):**
```bash
python -m medgraph.cli seed
python -m medgraph.cli expand
# adds 297 additional drugs from Flockhart CYP450 + DDInter
```

Or via Makefile:
```bash
make seed
```

### 3. Start the API server
```bash
python -m medgraph.cli serve
# Listening on http://localhost:8000
```

### 4. Start the frontend dev server (separate terminal)
```bash
cd dashboard && npm run dev
# Vite dev server at http://localhost:5173
```

Or `make dev` for the frontend shortcut.

---

## Production Deployment

### Architecture

```
Internet → Caddy (TLS, ports 80/443)
             ├─ /api/*     → medgraph:8000 (FastAPI)
             ├─ /health*   → medgraph:8000
             └─ /*         → static frontend (SPA)
           Prometheus → scrapes medgraph:8000/metrics (internal)
           Grafana    → queries Prometheus (localhost:3000)
```

### Minimum Requirements

- 1 CPU, 1 GB RAM, 10 GB disk
- Docker 24+ with Compose v2
- Ports 80/443 open (for Caddy TLS provisioning)
- A domain name pointed to the server (for auto HTTPS)

### Quick Start

```bash
# 1. Clone and configure
git clone <repo-url> && cd medgraph
cp .env.example .env

# 2. Edit .env — set at minimum:
#    MEDGRAPH_DOMAIN=yourdomain.com
#    MEDGRAPH_API_KEYS=your-secret-key
#    MEDGRAPH_ENV=production

# 3. Deploy (core services)
make deploy

# 4. Deploy with monitoring (adds Prometheus + Grafana)
make deploy-monitoring
```

### TLS / HTTPS Setup

Caddy auto-provisions TLS certificates via Let's Encrypt when:
1. `MEDGRAPH_DOMAIN` is set to a real domain (not `localhost`)
2. Ports 80 and 443 are accessible from the internet
3. DNS A record points to the server IP

**Fallback (manual certs):** Place cert/key files in `deploy/certs/` and update `deploy/Caddyfile`:
```
yourdomain.com {
    tls /etc/caddy/certs/cert.pem /etc/caddy/certs/key.pem
    # ... rest of config
}
```

### Makefile Targets

| Target | Description |
|--------|-------------|
| `make deploy` | Start production stack (Caddy + API) |
| `make deploy-monitoring` | Start with Prometheus + Grafana |
| `make down` | Stop all services |
| `make logs` | Tail production logs |
| `make status` | Show service status + health checks |
| `make backup` | Run online database backup |

### Docker Development (without TLS)

```bash
cp .env.example .env
docker compose up --build
# API at http://localhost:8000
```

Single container:
```bash
docker build -t medgraph .
docker run -p 8000:8000 -v $(pwd)/data:/app/data medgraph
```

---

## Phase 4: Migrations & Backups

### Running Database Migrations

MEDGRAPH uses Alembic for schema versioning. The baseline migration (`001_baseline_schema.py`) captures all tables from Phases 1–3 and adds schema_metadata for version tracking.

**Apply migrations on startup** (recommended for production):
```bash
python -m medgraph.cli db upgrade
# Applies all pending migrations up to 'head'
```

**Check current migration status**:
```bash
python -m medgraph.cli db status
# Output: Current migration revision: 001
```

**Downgrade to previous revision**:
```bash
python -m medgraph.cli db downgrade
# Reverts one migration step
```

### Database Backups

Create online backups without stopping the server:

```bash
# Auto-timestamped backup
python -m medgraph.cli db backup
# Output: Backup created: data/backups/medgraph-20260323-191700.db

# Custom output path
python -m medgraph.cli db backup --output /path/to/backup.db
```

Restore from backup:
```bash
python -m medgraph.cli db restore /path/to/backup.db
# Overwrites current DB with backup data
```

### Environment Variables (Phase 4)

No new env vars for Phase 4; existing `MEDGRAPH_DB_PATH` controls migration location.

---

## Environment Variables

Copy `.env.example` to `.env` and edit as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `MEDGRAPH_DB_PATH` | `data/medgraph.db` | SQLite database file path |
| `MEDGRAPH_HOST` | `0.0.0.0` | Bind host for uvicorn |
| `MEDGRAPH_PORT` | `8000` | Bind port |
| `MEDGRAPH_ENV` | `development` | Set to `production` for HSTS + strict headers |
| `MEDGRAPH_API_KEYS` | _(unset)_ | Comma-separated API keys (auth disabled if unset) |
| `MEDGRAPH_CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Comma-separated CORS origins |
| `MEDGRAPH_RATE_LIMIT` | `60` | Max requests per rate window |
| `MEDGRAPH_RATE_WINDOW` | `60` | Rate limit window in seconds |
| `MEDGRAPH_DOMAIN` | `localhost` | Domain for Caddy TLS auto-provisioning |
| `SENTRY_DSN` | _(unset)_ | Sentry error tracking DSN |
| `MEDGRAPH_LOG_FORMAT` | `text` | Log format: `json` for production, `text` for dev |
| `GRAFANA_ADMIN_PASSWORD` | `changeme` | Grafana admin password (monitoring profile) |
| `DRUGBANK_CSV` | _(unset)_ | Path to DrugBank full DB CSV |
| `OPENFDA_API_KEY` | _(unset)_ | OpenFDA API key (rate-limit relief) |

---

## Database Management

| Task | Command |
|------|---------|
| Initial seed | `python -m medgraph.cli seed` |
| Expand data | `python -m medgraph.cli expand` (adds 297 drugs, 182 enzyme relations) |
| Apply migrations | `python -m medgraph.cli db upgrade` |
| Check migration status | `python -m medgraph.cli db status` |
| Backup (online) | `python -m medgraph.cli db backup [--output path]` |
| Restore from backup | `python -m medgraph.cli db restore <backup_file>` |
| Reset | `rm data/medgraph.db && python -m medgraph.cli seed` |
| DrugBank import | `python -m medgraph.data.drugbank <path/to/drugbank.csv>` |

---

## Monitoring

**Liveness Check** (process responding, no DB check):
```bash
curl http://localhost:8000/health/live
# {"status":"ok"}
```

**Readiness Check** (DB accessible, graph loaded, schema verified):
```bash
curl http://localhost:8000/health/ready
# {"status":"ok","db_size":145,"graph_nodes":97,"schema_version":"001"}
```

**Backward Compatibility** (alias for readiness):
```bash
curl http://localhost:8000/health
# {"status":"ok","db_size":145,"graph_nodes":97,"schema_version":"001"}
```

Use `/health/live` for liveness probes and `/health/ready` for readiness probes in Kubernetes; use `/health` for simple uptime monitors.

**Prometheus Metrics**:
```bash
curl http://localhost:8000/metrics
# Exposes Prometheus-format metrics (analysis duration, graph size, request counts)
```

### Prometheus + Grafana Stack

Deploy with monitoring profile:
```bash
make deploy-monitoring
# Prometheus: internal (scrapes medgraph:8000/metrics)
# Grafana:    http://localhost:3000 (localhost only)
```

- **Grafana login**: admin / `$GRAFANA_ADMIN_PASSWORD` (default: `changeme`)
- **Dashboard**: Pre-provisioned "MEDGRAPH Overview" with request rate, latency p50/p99, error rate, graph size
- **Config files**: `deploy/prometheus.yml`, `deploy/grafana/`

### Backup Schedule

Recommended production backup schedule (add to server crontab — replace paths with your actual install location):
```bash
# Daily backup at 2 AM (replace /opt/medgraph with your project path)
0 2 * * * cd /opt/medgraph && make backup >> /var/log/medgraph-backup.log 2>&1

# Weekly cleanup: keep backups for 30 days
0 3 * * 0 docker compose -f /opt/medgraph/docker-compose.prod.yml exec -T medgraph find /app/data/backups -name "*.db" -mtime +30 -delete
```

Manual backup:
```bash
make backup
# or directly:
docker compose -f docker-compose.prod.yml exec medgraph python -m medgraph.cli db backup
```
