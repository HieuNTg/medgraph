"""
Request ID middleware for MEDGRAPH API.

Generates a UUID4 request ID if X-Request-ID header is absent,
attaches it to the response headers, and injects it into the logging context.
"""

from __future__ import annotations

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware that ensures every request has a unique X-Request-ID."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Use existing header or generate new UUID4
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())

        # Store on request state for access in endpoint handlers
        request.state.request_id = request_id

        # Log the request with its ID
        logger.debug(
            "request_start",
            extra={"request_id": request_id, "path": request.url.path, "method": request.method},
        )

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        logger.debug(
            "request_end",
            extra={
                "request_id": request_id,
                "path": request.url.path,
                "status_code": response.status_code,
            },
        )

        return response
