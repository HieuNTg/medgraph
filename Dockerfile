# ── Stage 1: Build frontend ───────────────────────────────────────────────────
FROM node:20-alpine AS frontend-build

WORKDIR /build

# Install deps first (layer cache)
COPY dashboard/package.json dashboard/package-lock.json ./
RUN npm ci

# Copy source and build
COPY dashboard/ ./
RUN npm run build
# Output: /build/dist/

# ── Stage 2: Production image ─────────────────────────────────────────────────
FROM python:3.11-slim AS production

WORKDIR /app

# Install Python deps
COPY pyproject.toml ./
# Install the package without editable mode (no source needed for pip deps)
RUN pip install --no-cache-dir \
    "pydantic>=2.0" \
    "click>=8.0" \
    "rich>=13.0" \
    "httpx>=0.27" \
    "networkx>=3.0" \
    "fastapi>=0.115" \
    "uvicorn[standard]>=0.30"

# Copy Python package
COPY medgraph/ ./medgraph/

# Copy built frontend into static serving location
COPY --from=frontend-build /build/dist/ ./dashboard/dist/

# Create data directory for SQLite volume mount
RUN mkdir -p /app/data

EXPOSE 8000

# Seed DB then start server
CMD ["sh", "-c", "python -m medgraph.cli seed && python -m medgraph.cli serve"]
