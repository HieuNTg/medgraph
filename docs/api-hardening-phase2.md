# Phase 2: API Hardening — Implementation Guide

## Overview

Phase 2 introduces production-ready API enhancements: RFC 7807 error standardization, request tracing, pagination, and versioning with backward compatibility.

## Key Changes

### 1. Dual-Mount Routing (/api/v1 + /api)

All endpoints are mounted at both prefixes:
- **`/api/v1/*`** — Canonical, version-locked path
- **`/api/*`** — Backward compatibility alias

Example:
```bash
# Both return identical results
curl http://localhost:8000/api/v1/drugs/search?q=aspirin
curl http://localhost:8000/api/drugs/search?q=aspirin
```

**Implementation**: `server.py` creates single `APIRouter`, mounted twice with `app.include_router()`.

### 2. RFC 7807 Problem Details Errors

All error responses now conform to [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807) standard format.

**Content-Type**: `application/problem+json`

**Example error response (400 — Bad Request)**:
```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Some drugs were not found",
  "instance": "http://localhost:8000/api/v1/check",
  "extensions": {
    "unresolved": ["UnknownDrug1"],
    "suggestions": {
      "UnknownDrug1": ["DrugA", "DrugB"]
    }
  }
}
```

**Fields**:
- `type` (string) — URI reference (default: "about:blank")
- `title` (string) — HTTP status title (e.g., "Bad Request")
- `status` (int) — HTTP status code
- `detail` (string) — Human-readable explanation
- `instance` (string, optional) — Request URI that caused the error
- `extensions` (object, optional) — Additional context (drug suggestions, validation errors, etc.)

**Implementation**: `errors.py` provides `register_error_handlers()` for HTTPException and RequestValidationError.

### 3. Request ID Tracing (X-Request-ID)

Every response includes a unique request ID for logging and debugging.

**Header**: `X-Request-ID`

**Behavior**:
- If client sends `X-Request-ID`, it is respected and echoed
- If absent, middleware generates UUID4
- Available in endpoint handlers via `request.state.request_id`

**Example**:
```bash
curl -i http://localhost:8000/api/v1/stats -H "X-Request-ID: my-request-123"
# Response includes: X-Request-ID: my-request-123

curl -i http://localhost:8000/api/v1/stats
# Response includes: X-Request-ID: a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6
```

**Implementation**: `middleware.py` defines `RequestIDMiddleware` (BaseHTTPMiddleware).
CORS is configured to expose this header: `expose_headers=["X-Request-ID"]`.

### 4. Paginated Search Responses

The `/api/v1/drugs/search` endpoint now returns paginated results.

**Request parameters**:
- `q` (string, required) — Drug name search query
- `limit` (int, optional, default=10, max=50) — Results per page
- `offset` (int, optional, default=0) — Number of results to skip

**Response model**: `PaginatedResponse[SearchResult]`

```json
{
  "items": [
    {
      "id": "DB00001",
      "name": "Aspirin",
      "brand_names": ["Bayer", "Ecotrin"],
      "drug_class": "Anti-Inflammatory Agents"
    }
  ],
  "total": 42,
  "offset": 0,
  "limit": 10,
  "has_more": true
}
```

**Fields**:
- `items` (array) — Page of SearchResult objects
- `total` (int) — Total matching drugs across all pages
- `offset` (int) — Results skipped from start
- `limit` (int) — Results per page (echoed)
- `has_more` (bool) — True if more results exist after this page

**Implementation**:
- `models.py` defines `PaginatedResponse[T]` as a generic Pydantic model
- `store.py` implements `search_drugs_with_count()` for atomic total + results query
- Wildcard escaping: `LIKE ? ESCAPE '\\'` prevents SQL injection

### 5. OpenAPI Metadata

The OpenAPI spec includes project and contact information.

**Spec location**: `http://localhost:8000/docs`

**Metadata**:
```python
FastAPI(
    title="MEDGRAPH API",
    description="Drug Interaction Cascade Analyzer",
    version=__version__,
    openapi_tags=[
        {"name": "system", "description": "Health checks and statistics"},
        {"name": "drugs", "description": "Drug lookup and search"},
        {"name": "analysis", "description": "Drug interaction analysis"},
        {"name": "reports", "description": "Report generation"},
        {"name": "pharmacogenomics", "description": "CPIC guidelines"},
    ],
    contact={"name": "MEDGRAPH Team", "url": "https://github.com/HieuNTg/medgraph"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)
```

Each endpoint is tagged to enable Swagger UI grouping by category.

## Migration Guide

### Existing Clients (Using `/api/*`)

No action required. All endpoints remain available at `/api/*` indefinitely.

```bash
# Still works
curl http://localhost:8000/api/drugs/search?q=aspirin
```

### New Clients (Recommended: Use `/api/v1/*`)

Adopt the versioned path for stability:

```bash
# Preferred
curl http://localhost:8000/api/v1/drugs/search?q=aspirin
```

### Error Handling

Update error handlers to expect RFC 7807 format:

**Before (Phase 1)**:
```json
{
  "detail": "Some drugs were not found"
}
```

**After (Phase 2)**:
```json
{
  "type": "about:blank",
  "title": "Bad Request",
  "status": 400,
  "detail": "Some drugs were not found",
  "instance": "...",
  "extensions": { ... }
}
```

Parse `response.json()["detail"]` or `response.json()["extensions"]` for error context.

### Pagination Integration

For search endpoints, always handle pagination:

```typescript
// React/TypeScript example
const response = await fetch(
  `/api/v1/drugs/search?q=${query}&limit=10&offset=${currentOffset}`
);
const data = await response.json(); // PaginatedResponse[SearchResult]

const hasNextPage = data.has_more;
const nextOffset = data.offset + data.limit;
```

## Testing

Run Phase 2 test suite to validate all features:

```bash
pytest tests/test_api_hardening.py -v
```

Test categories:
- **API v1 routing**: Endpoints accessible at both /api/v1/* and /api/*
- **RFC 7807 compliance**: Error responses match spec
- **Pagination**: offset/limit/total/has_more behavior
- **Request ID**: Header presence and propagation
- **OpenAPI metadata**: Tags, contact, license in spec

## Files Modified

| File | Changes |
|------|---------|
| `medgraph/api/errors.py` | New: RFC 7807 error handlers |
| `medgraph/api/middleware.py` | New: RequestIDMiddleware |
| `medgraph/api/models.py` | New: PaginatedResponse[T] generic |
| `medgraph/api/search.py` | Updated: count() method for pagination |
| `medgraph/api/server.py` | Dual-mount routing, error handlers, OpenAPI metadata |
| `medgraph/graph/store.py` | New: search_drugs_with_count(); LIKE escape |
| `tests/test_api.py` | Updated: pagination/RFC7807 assertions |
| `tests/test_api_hardening.py` | New: 17 hardening tests |

## Configuration

### CORS Headers

Expose X-Request-ID to clients:

```python
app.add_middleware(
    CORSMiddleware,
    ...,
    expose_headers=["X-Request-ID"],
)
```

### Error Handler Registration

Install at app creation time:

```python
app = FastAPI(...)
register_error_handlers(app)
```

## Backward Compatibility

- `/api/*` routes remain fully functional (mapped to same router as /api/v1/*)
- Existing CheckRequest/CheckResponse models unchanged
- Error detail fields still populate from exceptions
- No breaking changes to database schema or core logic

## What's Next (Phase 3)

- **Caching layer** — Redis/Memcached for stats + search results
- **Async database** — async SQLite or PostgreSQL driver for better concurrency
- **Rate limiting enhancements** — Per-user limits + sliding window algorithm
- **WebSocket support** — Real-time cascade analysis stream
