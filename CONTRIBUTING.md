# Contributing to MEDGRAPH

Thank you for considering a contribution. This document covers everything you need to get started.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating you agree to uphold it. Report unacceptable behaviour to the project maintainers.

---

## How to Contribute

Good starting points:

- Fix a bug listed in [Issues](../../issues)
- Improve test coverage for the engine or data layers
- Add drug/interaction data to the seed files
- Improve frontend accessibility or mobile layout
- Improve API documentation or error messages

For larger features, **open an issue first** to discuss scope before writing code.

---

## Development Setup

### Prerequisites

- Python 3.11+
- Node 20+
- Git

### Backend

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Seed the database
python -m medgraph.cli seed

# Run the API
python -m medgraph.cli serve
```

### Frontend

```bash
cd dashboard
npm install
npm run dev
```

### Run all tests

```bash
pytest tests/ -v
```

### Lint and format

```bash
ruff check medgraph/ tests/    # lint
ruff format medgraph/ tests/   # format
```

---

## Code Standards

### Python

- **Formatter / linter**: `ruff` (configured in `pyproject.toml`, line length 100)
- **Type hints**: required on all public functions and class methods
- **Docstrings**: module-level and public API docstrings expected
- All new code must have associated `pytest` tests
- Do not add optional dependencies unless strictly necessary

### TypeScript / React

- **Strict mode** TypeScript — no `any` without justification
- Tailwind CSS v4 utility classes; no custom CSS unless unavoidable
- Components in `dashboard/src/components/`, hooks in `dashboard/src/hooks/`
- Prefer functional components and React hooks

### Commit messages

Follow conventional commits:

```
feat: add enzyme inhibition strength display
fix: handle missing RxNorm CUI gracefully
docs: update API endpoint table in README
test: add pathfinder max-depth edge case
refactor: extract risk scorer into standalone module
```

---

## Pull Request Process

1. Fork the repository and create a feature branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. Make your changes, write tests, and verify everything passes:
   ```bash
   pytest tests/ -v
   ruff check medgraph/ tests/
   cd dashboard && npm run build
   ```

3. Open a pull request against `main` with:
   - A clear title following the commit convention
   - Description of what changed and why
   - Reference to any related issues (`Closes #42`)

4. A maintainer will review within a few days. Address review comments in new commits (do not force-push during review).

5. Once approved and CI passes, a maintainer will merge.

---

## Reporting Issues

When filing a bug, include:

- MEDGRAPH version / git SHA
- Python version and OS
- Exact steps to reproduce
- Expected behaviour vs actual behaviour
- Relevant log output or error messages

For security-sensitive issues, do **not** file a public issue — contact the maintainers directly.
