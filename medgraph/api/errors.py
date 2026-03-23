"""
RFC 7807 Problem Details error handling for MEDGRAPH API.

Provides structured error responses in application/problem+json format.
See: https://www.rfc-editor.org/rfc/rfc7807
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


# Standard title mapping for HTTP status codes
_STATUS_TITLES = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Validation Error",
    429: "Too Many Requests",
    500: "Internal Server Error",
    503: "Service Unavailable",
}


def _build_problem(status: int, detail: str, instance: str | None = None) -> dict[str, Any]:
    """Build RFC 7807 problem detail dict."""
    body: dict[str, Any] = {
        "type": "about:blank",
        "title": _STATUS_TITLES.get(status, "Error"),
        "status": status,
        "detail": detail,
    }
    if instance is not None:
        body["instance"] = instance
    return body


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Convert FastAPI HTTPException to RFC 7807 Problem Details response."""
    # Handle dict detail (e.g., unresolved drugs with suggestions)
    if isinstance(exc.detail, dict):
        detail_str = exc.detail.get("message", str(exc.detail))
        body = _build_problem(exc.status_code, detail_str, str(request.url))
        body["extensions"] = exc.detail
    else:
        body = _build_problem(exc.status_code, str(exc.detail), str(request.url))

    return JSONResponse(
        status_code=exc.status_code,
        content=body,
        media_type="application/problem+json",
    )


async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Convert Pydantic validation errors to RFC 7807 format."""
    from fastapi.exceptions import RequestValidationError

    if isinstance(exc, RequestValidationError):
        errors = exc.errors()
        detail = "; ".join(
            f"{'.'.join(str(loc) for loc in e.get('loc', []))}: {e.get('msg', '')}" for e in errors
        )
    else:
        detail = str(exc)

    body = _build_problem(422, detail, str(request.url))
    return JSONResponse(
        status_code=422,
        content=body,
        media_type="application/problem+json",
    )


def register_error_handlers(app: FastAPI) -> None:
    """Register RFC 7807 error handlers on the FastAPI app."""
    from fastapi.exceptions import RequestValidationError

    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
