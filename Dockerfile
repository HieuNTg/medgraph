# MEDGRAPH — Multi-stage Docker build
# Stage 1: Build React frontend
# Stage 2: Production Python image with frontend assets

# ── Stage 1: Build frontend ───────────────────────────────────────────────────
FROM node:20-alpine AS frontend-build

WORKDIR /build

# Install deps first (layer cache)
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm ci --ignore-scripts

# Copy source and build
COPY dashboard/ ./
RUN npm run build
# Output: /build/dist/

# ── Stage 2: Production image ─────────────────────────────────────────────────
FROM python:3.12-slim AS production

WORKDIR /app

# System deps for reportlab (PDF generation)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps from pyproject.toml
COPY pyproject.toml ./
COPY medgraph/__init__.py ./medgraph/__init__.py
RUN pip install --no-cache-dir .

# Copy full application code
COPY medgraph/ ./medgraph/

# Copy built frontend into static serving location
COPY --from=frontend-build /build/dist/ ./dashboard/dist/

# Create data directory for SQLite volume mount
RUN mkdir -p /app/data

# Non-root user for security
RUN useradd -m -r medgraph && chown -R medgraph:medgraph /app
USER medgraph

# Environment defaults
ENV MEDGRAPH_DB_PATH=/app/data/medgraph.db \
    PYTHONUNBUFFERED=1 \
    MEDGRAPH_LOG_FORMAT=json

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Seed DB (if not already seeded via volume) then start server
CMD ["sh", "-c", "python -m medgraph.cli seed 2>/dev/null; uvicorn medgraph.api.server:app --host 0.0.0.0 --port 8000 --workers 2"]
