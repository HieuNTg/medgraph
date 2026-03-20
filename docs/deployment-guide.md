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
```bash
python -m medgraph.cli seed
# creates data/medgraph.db with 89 drugs, 28 interactions, 8 enzymes
```

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

## Environment Variables

Copy `.env.example` to `.env` and edit as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `MEDGRAPH_DB_PATH` | `data/medgraph.db` | SQLite database file path |
| `MEDGRAPH_HOST` | `0.0.0.0` | Bind host for uvicorn |
| `MEDGRAPH_PORT` | `8000` | Bind port |
| `DRUGBANK_CSV` | _(unset)_ | Path to DrugBank full DB CSV for enrichment |
| `OPENFDA_API_KEY` | _(unset)_ | OpenFDA API key (rate-limit relief) |

---

## Database Management

| Task | Command |
|------|---------|
| Initial seed | `python -m medgraph.cli seed` |
| Backup | `cp data/medgraph.db data/medgraph.db.bak` |
| Reset | `rm data/medgraph.db && python -m medgraph.cli seed` |
| DrugBank import | `python -m medgraph.data.drugbank <path/to/drugbank.csv>` |

---

## Monitoring

Health endpoint returns HTTP 200 with JSON when the server is up and the DB is accessible:

```bash
curl http://localhost:8000/health
# {"status":"ok","db_size":145,"graph_nodes":97}
```

Use this URL for load-balancer health checks or uptime monitors.
