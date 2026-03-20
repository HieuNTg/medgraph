.PHONY: install seed serve dev test lint format build clean all

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

# ── Composite ────────────────────────────────────────────────────────────────

all: install seed test build
