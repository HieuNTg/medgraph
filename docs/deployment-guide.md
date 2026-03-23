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

## Production Build

### Build the frontend
```bash
cd dashboard && npm run build
# Output: dashboard/dist/
```

### Serve static files from FastAPI
Mount `dashboard/dist/` as a `StaticFiles` directory in `server.py`, or use nginx (see below).

### nginx (recommended for production)
```nginx
server {
    listen 80;
    root /app/dashboard/dist;
    index index.html;

    location /api/ { proxy_pass http://127.0.0.1:8000; }
    location /health { proxy_pass http://127.0.0.1:8000; }
    location / { try_files $uri $uri/ /index.html; }
}
```

---

## Docker Deployment

Build and run with Docker Compose (recommended):
```bash
cp .env.example .env   # set any overrides
docker compose up --build
```

Single container:
```bash
docker build -t medgraph .
docker run -p 8000:8000 -v $(pwd)/data:/app/data medgraph
```

See `Dockerfile` and `docker-compose.yml` at project root.

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
| `MEDGRAPH_ENV` | `development` | Set to `production` to enable HSTS security header |
| `MEDGRAPH_CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Comma-separated CORS allowed origins |
| `DRUGBANK_CSV` | _(unset)_ | Path to DrugBank full DB CSV for enrichment |
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
