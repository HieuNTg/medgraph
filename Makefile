.PHONY: install seed serve dev test lint format build clean all deploy deploy-monitoring down logs status backup

# ── Dependencies ──────────────────────────────────────────────────────────────

install:
	pip install -e ".[dev]"
	cd dashboard && npm install

# ── Data ─────────────────────────────────────────────────────────────────────

seed:
	python -m medgraph.cli seed

# ── Runtime ──────────────────────────────────────────────────────────────────

serve:
	python -m medgraph.cli serve

dev:
	cd dashboard && npm run dev

# ── Quality ──────────────────────────────────────────────────────────────────

test:
	python -m pytest tests/ -v

lint:
	ruff check medgraph/ tests/

format:
	ruff format medgraph/ tests/

# ── Build ─────────────────────────────────────────────────────────────────────

build:
	cd dashboard && npm run build

# ── Housekeeping ─────────────────────────────────────────────────────────────

clean:
	rm -rf data/medgraph.db dist/ dashboard/dist/

# ── Production Deployment ────────────────────────────────────────────────────

deploy:
	docker compose -f docker-compose.prod.yml up -d --build

deploy-monitoring:
	docker compose -f docker-compose.prod.yml --profile monitoring up -d --build

down:
	docker compose -f docker-compose.prod.yml down
	@docker compose -f docker-compose.prod.yml --profile monitoring down 2>/dev/null || true

logs:
	docker compose -f docker-compose.prod.yml logs -f --tail=100

status:
	@echo "=== Service Status ==="
	@docker compose -f docker-compose.prod.yml ps
	@echo ""
	@echo "=== Health Check ==="
	@docker compose -f docker-compose.prod.yml exec -T medgraph python -c "import urllib.request,json; r=urllib.request.urlopen('http://localhost:8000/health/ready'); print(json.dumps(json.load(r),indent=2))" 2>/dev/null || echo "API container not reachable"
	@curl -sf https://localhost/health/ready 2>/dev/null && echo "" || curl -sf http://localhost/health/ready 2>/dev/null && echo "" || echo "Caddy not reachable externally (check ports 80/443)"

backup:
	docker compose -f docker-compose.prod.yml exec medgraph python -m medgraph.cli db backup

# ── Composite ────────────────────────────────────────────────────────────────

all: install seed test build
