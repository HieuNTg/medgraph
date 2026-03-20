# MEDGRAPH — Code Standards

## Python Backend

### Tooling
- **Linter / formatter**: `ruff` — `line-length = 100`, `target-version = "py311"`
- Run: `ruff check medgraph/ tests/` and `ruff format medgraph/ tests/`

### Style Rules
- All public functions and methods must have type hints
- All data models use **Pydantic V2** (`model_config`, `model_validator`, no V1 `__fields__`)
- `from __future__ import annotations` at top of every module
- Prefer `Path` over `str` for file paths
- No bare `except:`; always catch specific exception types
- Use `logging` not `print` in library code

### Module Organization
```
medgraph/
  api/       — FastAPI routes + Pydantic request/response models
  engine/    — Pure analysis logic (no I/O)
  graph/     — NetworkX graph construction + SQLite store
  data/      — Seed data + optional external data pipelines
  cli.py     — Click CLI entry points
```

## TypeScript Frontend

### Compiler
- `strict: true` in `tsconfig.json`
- `noImplicitAny: true` — **never use `any`**; use `unknown` + type guards

### Style Rules
- Functional components only; no class components
- Custom hooks prefixed `use` and placed in `lib/` or co-located
- Props interfaces named `[ComponentName]Props`
- No inline styles; use Tailwind utility classes
- All API response shapes typed in `lib/types.ts`

### File Naming
- Components: `kebab-case.tsx`
- Pages: `kebab-case.tsx` in `pages/`
- Utilities: `kebab-case.ts` in `lib/`

## CSS / Tailwind
- Tailwind v4 with `@theme` CSS variables for theming
- Severity colors defined as CSS variables: `--color-critical`, `--color-major`, `--color-moderate`, `--color-minor`
- No hardcoded hex colors in component files — reference variables

## Testing
- **Backend**: `pytest` with `pytest-asyncio` (`asyncio_mode = "auto"`)
  - Test files in `tests/`, mirror `medgraph/` structure
  - Coverage target: 80 %+ for `engine/` module
- **Frontend**: No test suite yet (v0.2.0 target)

## Git Conventions
- **Commit format**: Conventional Commits — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
- **Branch naming**: `feat/<short-desc>`, `fix/<issue-or-desc>`
- PRs require passing CI before merge

## Code Review Checklist
- [ ] Type hints present on all new functions
- [ ] No `any` in TypeScript, no bare `except` in Python
- [ ] Pydantic models used for all API boundaries
- [ ] No secrets or API keys committed
- [ ] `ruff check` passes with zero errors
- [ ] `tsc --noEmit` passes
- [ ] New backend logic covered by at least one pytest
- [ ] Medical disclaimer still visible in UI (no layout changes that hide it)
