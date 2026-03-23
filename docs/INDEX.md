# MEDGRAPH Documentation Index

**Last Updated**: 2026-03-23 (Phase 3 Complete)
**Status**: Production-Ready with Observability

---

## Quick Start

1. **New to MEDGRAPH?** → Read [project-overview-pdr.md](#project-overview-pdr)
2. **Setting up locally?** → Read [deployment-guide.md](#deployment-guide)
3. **Building on the API?** → Read [api-hardening-phase2.md](#api-hardening-phase2)
4. **Monitoring & observability?** → Read [PHASE3-OBSERVABILITY.md](#phase3-observability)
5. **Contributing code?** → Read [code-standards.md](#code-standards)

---

## Core Documentation

### project-overview-pdr.md
**What**: Product vision, target users, MVP scope, success metrics
**Length**: ~50 lines
**Audience**: Stakeholders, new team members, product managers
**Key Sections**:
- Problem statement
- Target users and use cases
- MVP scope (89+ drugs, 28+ interactions, 8 enzymes, CPIC guidelines)
- Success metrics
- Non-goals

**When to Read**: First onboarding document; understand the "why"

---

### system-architecture.md
**What**: High-level architecture, data flow, database schema, API design
**Length**: ~95 lines
**Audience**: Architects, senior developers, system designers
**Key Sections**:
- Architecture diagram (client → API → graph engine → store)
- Data flow walkthrough
- Knowledge graph (NetworkX nodes/edges)
- Database schema (8 tables + WAL mode)
- API layer (versioning, error handling, request tracing, CORS)
- Frontend architecture (React Router, TanStack Query, Tailwind)

**When to Read**: Understand system design and integration points

---

### codebase-summary.md
**What**: Package structure, module responsibilities, endpoints, CI/CD
**Length**: ~140 lines
**Audience**: Developers, code reviewers, DevOps engineers
**Key Sections**:
- Backend package structure (`medgraph/api`, `engine`, `graph`, `data`)
- Frontend structure (`dashboard/src` with pages, components, lib)
- Key classes and responsibilities
- Database schema (with notes on genetic_guidelines)
- API endpoints summary table (with Phase 2 pagination/versioning)
- Testing coverage (17 Phase 2 hardening tests)
- CI/CD pipeline (GitHub Actions, Dependabot)

**When to Read**: Navigate codebase, find specific modules, understand CI

---

### api-hardening-phase2.md
**What**: Phase 2 API enhancements implementation guide
**Length**: ~280 lines
**Audience**: Backend developers, API integrators, frontend engineers
**Key Sections**:
- Dual-mount routing (/api/v1 + /api)
- RFC 7807 Problem Details errors
- X-Request-ID tracing middleware
- Paginated search responses
- OpenAPI metadata
- Migration guide for existing clients
- Error handling examples
- Pagination integration (TypeScript)
- Testing overview
- Files modified summary
- Configuration notes
- Backward compatibility guarantees
- Phase 3 roadmap

**When to Read**: Integrating with API, migrating clients, implementing features

---

### PHASE2-SUMMARY.md
**What**: Executive summary of Phase 2 completion
**Length**: ~380 lines
**Audience**: Team leads, project stakeholders, integration teams
**Key Sections**:
- What changed in Phase 2 (5 features)
- Before/after error format comparison
- Implementation files (new + modified)
- API endpoints summary table
- Test coverage breakdown (17 tests)
- Documentation updates
- Client integration checklist
- Deployment considerations
- Backward compatibility matrix
- Success criteria (all met)
- Phase 3 roadmap

**When to Read**: Phase completion review, stakeholder communication, planning

---

### PHASE3-OBSERVABILITY.md
**What**: Phase 3 observability & monitoring implementation guide
**Length**: ~420 lines
**Audience**: DevOps engineers, monitoring teams, platform engineers, backend developers
**Key Sections**:
- Prometheus metrics setup (/metrics endpoint)
- Custom app metrics (analysis duration, graph size)
- Health check endpoints (liveness, readiness, backward compat)
- Structured JSON logging with request_id tracing
- Optional Sentry error tracking (SENTRY_DSN gated)
- Architecture diagram with observability stack
- Environment variables (logging, traces, Sentry)
- Docker Compose deployment example
- Testing overview (14 new observability tests)
- Files changed (metrics, middleware, models, logging)
- Breaking changes (none — fully backward compatible)
- Next steps (alerting, dashboards, log aggregation)

**When to Read**: Setting up monitoring, configuring observability stack, deploying to production

---

## Reference Documentation

### code-standards.md
**What**: Development conventions, coding patterns, best practices
**Length**: ~100 lines
**Audience**: All developers
**Key Sections**:
- Code organization principles
- Naming conventions
- Type hints and Pydantic models
- Error handling patterns
- Testing requirements
- Documentation standards

**When to Read**: Before writing code; code review checklist

---

### design-guidelines.md
**What**: UI/UX principles, component patterns, design system
**Length**: ~130 lines
**Audience**: Frontend developers, designers
**Key Sections**:
- Design tokens (colors, typography, spacing)
- Component architecture
- Accessibility requirements
- Responsive design approach
- Theme system (light/dark)

**When to Read**: Building UI components, styling, theme updates

---

### deployment-guide.md
**What**: Setup, deployment, environment configuration, monitoring
**Length**: ~140 lines
**Audience**: DevOps engineers, deployment engineers, operations teams
**Key Sections**:
- Prerequisites and installation
- Database seeding
- Environment variables
- Running locally (API + frontend)
- Docker deployment
- Production checklist
- Monitoring and logging
- Troubleshooting

**When to Read**: Deploying to any environment

---

### project-roadmap.md
**What**: Feature roadmap, release planning, future directions
**Length**: ~90 lines
**Audience**: Product managers, team leads, strategic planners
**Key Sections**:
- Version history (MVP, Phase 2, Phase 3+)
- Phase 2 completion (API hardening)
- Phase 3 planned features (caching, async DB, WebSocket)
- Phase 4+ vision (mobile, enterprise features)
- Dependency considerations

**When to Read**: Planning, prioritization, stakeholder updates

---

### logic-diagrams.md
**What**: Cascade analysis logic, scoring algorithm, enzyme pathfinding
**Length**: ~650 lines
**Audience**: Algorithm designers, analysis engine developers
**Key Sections**:
- Cascade detection algorithm
- Risk scoring methodology
- CYP450 pathway modeling
- Evidence aggregation
- Severity classification
- Pharmacogenomics adjustments

**When to Read**: Understanding analysis logic, modifying scoring, debugging results

---

## Navigation by Role

### Product Manager
**Start here**: project-overview-pdr.md → project-roadmap.md → PHASE2-SUMMARY.md

### Backend Developer
**Start here**: codebase-summary.md → api-hardening-phase2.md → code-standards.md

### Frontend Developer
**Start here**: system-architecture.md → design-guidelines.md → api-hardening-phase2.md

### DevOps Engineer
**Start here**: deployment-guide.md → system-architecture.md → codebase-summary.md

### QA / Tester
**Start here**: PHASE2-SUMMARY.md (test section) → PHASE3-OBSERVABILITY.md (test section) → code-standards.md

### Architect
**Start here**: system-architecture.md → project-roadmap.md → logic-diagrams.md

### Site Reliability Engineer (SRE)
**Start here**: PHASE3-OBSERVABILITY.md → deployment-guide.md → system-architecture.md

### New Team Member
**Start here**:
1. project-overview-pdr.md (understand the product)
2. system-architecture.md (understand the system)
3. codebase-summary.md (find your way around)
4. code-standards.md (how we work)
5. PHASE3-OBSERVABILITY.md (operations and monitoring)

---

## Documentation by Topic

### API & Integration
- api-hardening-phase2.md — Comprehensive API guide
- codebase-summary.md — Endpoints table
- PHASE2-SUMMARY.md — Quick endpoint reference

### Architecture & Design
- system-architecture.md — System design (including Phase 3 observability)
- logic-diagrams.md — Analysis algorithms
- design-guidelines.md — UI/UX design

### Development
- code-standards.md — Code conventions
- codebase-summary.md — Package structure
- api-hardening-phase2.md — API development

### Operations & Deployment
- deployment-guide.md — Setup and deployment
- project-roadmap.md — Versions and support
- system-architecture.md — Infrastructure
- PHASE3-OBSERVABILITY.md — Monitoring and observability stack

### Observability & Monitoring
- PHASE3-OBSERVABILITY.md — Complete Phase 3 guide
- system-architecture.md#phase-3-observability-monitoring — Architecture overview
- codebase-summary.md — Metrics module documentation

### Business & Planning
- project-overview-pdr.md — Product definition
- project-roadmap.md — Roadmap and priorities
- PHASE2-SUMMARY.md — Phase 2 completion status
- PHASE3-OBSERVABILITY.md — Phase 3 completion status

---

## Key Concepts Explained

### Cascade Analysis
Multi-hop drug interaction detection through shared enzyme pathways. See:
- [project-overview-pdr.md](./project-overview-pdr.md#core-value-proposition)
- [system-architecture.md](./system-architecture.md#knowledge-graph)
- [logic-diagrams.md](./logic-diagrams.md#cascade-detection-algorithm)

### Phase 2 API Hardening
Versioning, error standardization, pagination, request tracing. See:
- [api-hardening-phase2.md](./api-hardening-phase2.md)
- [PHASE2-SUMMARY.md](./PHASE2-SUMMARY.md#what-changed-in-phase-2)

### Phase 3 Observability & Monitoring
Prometheus metrics, structured logging, health checks, Sentry integration. See:
- [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md)
- [system-architecture.md#phase-3-observability--monitoring](./system-architecture.md#phase-3-observability--monitoring)
- [codebase-summary.md#phase-3-features](./codebase-summary.md#phase-3-features)

### RFC 7807 Problem Details
Standard error response format. See:
- [api-hardening-phase2.md#2-rfc-7807-problem-details-errors](./api-hardening-phase2.md#2-rfc-7807-problem-details-errors)

### Pagination
Offset-based result pagination. See:
- [api-hardening-phase2.md#4-paginated-search-responses](./api-hardening-phase2.md#4-paginated-search-responses)

### Health Checks (K8s-Compatible)
Liveness and readiness probes. See:
- [PHASE3-OBSERVABILITY.md#2-health-check-endpoints-kubernetes-compatible](./PHASE3-OBSERVABILITY.md#2-health-check-endpoints-kubernetes-compatible)

### Prometheus Metrics
Application and request metrics. See:
- [PHASE3-OBSERVABILITY.md#1-prometheus-metrics](./PHASE3-OBSERVABILITY.md#1-prometheus-metrics)

### Structured Logging with Request Tracing
JSON logging with request_id correlation. See:
- [PHASE3-OBSERVABILITY.md#3-structured-logging-with-request-tracing](./PHASE3-OBSERVABILITY.md#3-structured-logging-with-request-tracing)

### CPIC Pharmacogenomics
Gene-specific drug dosing guidelines. See:
- [logic-diagrams.md](./logic-diagrams.md#pharmacogenomics-adjustments)

---

## Search & Find

### Finding Endpoints
→ [codebase-summary.md](./codebase-summary.md#api-endpoints) or [PHASE2-SUMMARY.md](./PHASE2-SUMMARY.md#api-endpoints-summary)

### Finding Database Tables
→ [system-architecture.md](./system-architecture.md#database-schema-sqlite) or [codebase-summary.md](./codebase-summary.md#database-schema)

### Finding Code Modules
→ [codebase-summary.md](./codebase-summary.md#backend-package-medgraph) (backend) or [codebase-summary.md](./codebase-summary.md#frontend-dashboardsrc) (frontend)

### Finding Environment Variables
→ [deployment-guide.md](./deployment-guide.md#environment-variables) or [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md#environment-variables-phase-3)

### Finding Error Codes
→ [api-hardening-phase2.md](./api-hardening-phase2.md#2-rfc-7807-problem-details-errors)

### Finding Monitoring Setup
→ [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md) (complete guide) or [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md#deployment-example) (Docker example)

### Finding Health Check Info
→ [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md#2-health-check-endpoints-kubernetes-compatible)

### Finding Metrics Info
→ [PHASE3-OBSERVABILITY.md](./PHASE3-OBSERVABILITY.md#1-prometheus-metrics)

### Finding Scoring Logic
→ [logic-diagrams.md](./logic-diagrams.md#risk-scoring-algorithm)

---

## Document Metadata

| Document | Size | Updated | Audience |
|----------|------|---------|----------|
| project-overview-pdr.md | ~50 L | 2026-03-23 | Stakeholders |
| system-architecture.md | ~130 L | 2026-03-23 | Architects |
| codebase-summary.md | ~160 L | 2026-03-23 | Developers |
| api-hardening-phase2.md | ~280 L | 2026-03-23 | Integrators |
| PHASE2-SUMMARY.md | ~380 L | 2026-03-23 | Leaders |
| **PHASE3-OBSERVABILITY.md** | **~420 L** | **2026-03-23** | **SREs / DevOps** |
| code-standards.md | ~100 L | 2025-Q4 | All devs |
| design-guidelines.md | ~130 L | 2025-Q4 | Designers |
| deployment-guide.md | ~140 L | 2025-Q4 | DevOps |
| project-roadmap.md | ~110 L | 2026-03-23 | PMs |
| logic-diagrams.md | ~650 L | 2025-Q3 | Engineers |
| **INDEX.md** | **~450 L** | **2026-03-23** | **Everyone** |
| **Total** | **~2,700 L** | — | — |

---

## Contributing to Documentation

When adding or updating docs:
1. Keep files concise (target: < 200 lines each)
2. Add to this INDEX when creating new files
3. Follow existing formatting (headers, tables, code blocks)
4. Include your role and the purpose of changes
5. Verify code examples against actual source
6. Link to related docs for context

---

## Links to Key Resources

- **GitHub**: https://github.com/HieuNTg/medgraph
- **API Docs** (live): http://localhost:8000/docs
- **Frontend** (dev): http://localhost:5173
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

## Document Version

**Current Phase**: 3 (Observability & Monitoring Complete)
**Total Docs**: 12 (including INDEX)
**Last Updated**: 2026-03-23 17:00 UTC
**Status**: Production Ready with Observability

---

*This index is your navigation hub. Bookmark it and refer back when you need to find information.*
