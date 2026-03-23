"""
API key authentication and rate limiting for MEDGRAPH.

Rate limiting uses an in-memory sliding window counter per IP/key.
Auth is optional — disabled when MEDGRAPH_API_KEYS env var is unset.
"""

from __future__ import annotations

import hashlib
import os
import time
from collections import defaultdict
from typing import Optional

from fastapi import HTTPException, Request

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Comma-separated API keys. If empty/unset, auth is disabled (open access).
_API_KEYS: Optional[set[str]] = None

# Rate limit: requests per window per client
RATE_LIMIT = int(os.environ.get("MEDGRAPH_RATE_LIMIT", "60"))
RATE_WINDOW = int(os.environ.get("MEDGRAPH_RATE_WINDOW", "60"))  # seconds


def _load_api_keys() -> Optional[set[str]]:
    """Load API keys from environment. Returns None if auth disabled."""
    raw = os.environ.get("MEDGRAPH_API_KEYS", "").strip()
    if not raw:
        return None
    keys = {k.strip() for k in raw.split(",") if k.strip()}
    return keys if keys else None


def _get_api_keys() -> Optional[set[str]]:
    """Lazy-load and cache API keys."""
    global _API_KEYS  # noqa: PLW0603
    if _API_KEYS is None:
        _API_KEYS = _load_api_keys()
    return _API_KEYS


def reload_api_keys() -> None:
    """Force reload of API keys (for testing)."""
    global _API_KEYS  # noqa: PLW0603
    _API_KEYS = _load_api_keys()


# ---------------------------------------------------------------------------
# Rate limiter (sliding window counter)
# ---------------------------------------------------------------------------

_request_log: dict[str, list[float]] = defaultdict(list)


def _get_client_id(request: Request) -> str:
    """Derive a rate-limit key from request. Uses API key if present, else IP."""
    api_key = request.headers.get("x-api-key", "")
    if api_key:
        return f"key:{hashlib.sha256(api_key.encode()).hexdigest()[:16]}"
    client_ip = request.client.host if request.client else "unknown"
    return f"ip:{client_ip}"


def _check_rate_limit(client_id: str) -> bool:
    """Return True if request is allowed, False if rate-limited."""
    now = time.monotonic()
    window_start = now - RATE_WINDOW

    # Prune old entries
    timestamps = _request_log[client_id]
    _request_log[client_id] = [t for t in timestamps if t > window_start]

    if len(_request_log[client_id]) >= RATE_LIMIT:
        return False

    _request_log[client_id].append(now)
    return True


def reset_rate_limits() -> None:
    """Clear all rate limit state (for testing)."""
    _request_log.clear()


# ---------------------------------------------------------------------------
# Public middleware functions
# ---------------------------------------------------------------------------


def verify_api_key(request: Request) -> None:
    """
    Verify API key from X-Api-Key header.

    Raises HTTPException 401 if auth is enabled and key is invalid.
    No-op if auth is disabled (MEDGRAPH_API_KEYS unset).
    """
    keys = _get_api_keys()
    if keys is None:
        return  # Auth disabled

    api_key = request.headers.get("x-api-key", "").strip()
    if not api_key or api_key not in keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Set X-Api-Key header.",
        )


def check_rate_limit(request: Request) -> None:
    """
    Enforce per-client rate limiting.

    Raises HTTPException 429 if client exceeds rate limit.
    """
    client_id = _get_client_id(request)
    if not _check_rate_limit(client_id):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded ({RATE_LIMIT} requests per {RATE_WINDOW}s). Try again later.",
        )
