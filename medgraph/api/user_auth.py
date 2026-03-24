"""
JWT-based user authentication for MEDGRAPH.

Uses stdlib only:
- hashlib.pbkdf2_hmac for password hashing
- HMAC-SHA256 for JWT signing (no python-jose/passlib needed)
"""

import base64
import hashlib
import hmac
import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone

_logger = logging.getLogger(__name__)
_DEV_SECRET = "medgraph-dev-secret"


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    # Restore padding
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


class UserAuth:
    """Handles user registration, login, and JWT token lifecycle."""

    _HASH_ITERATIONS = 260_000  # OWASP recommended for pbkdf2_hmac/sha256

    # Maps user_id -> set of valid refresh token jti values
    _refresh_tokens: dict[str, set[str]] = {}

    def __init__(self, store, secret_key: str | None = None) -> None:
        self.store = store
        resolved_secret = secret_key or os.environ.get("MEDGRAPH_JWT_SECRET", _DEV_SECRET)
        if os.environ.get("MEDGRAPH_ENV") == "production" and resolved_secret == _DEV_SECRET:
            raise RuntimeError(
                "MEDGRAPH_JWT_SECRET must be set to a strong secret in production. "
                "Do not use the default development secret."
            )
        if resolved_secret == _DEV_SECRET:
            _logger.warning(
                "Using default dev JWT secret. Set MEDGRAPH_JWT_SECRET for any shared environment."
            )
        self.secret_key = resolved_secret.encode()
        self.access_token_expiry = timedelta(minutes=15)
        self.refresh_token_expiry = timedelta(days=7)

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def _hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, self._HASH_ITERATIONS)
        return f"pbkdf2:sha256:{self._HASH_ITERATIONS}:{_b64url_encode(salt)}:{_b64url_encode(dk)}"

    def _verify_password(self, password: str, stored_hash: str) -> bool:
        try:
            parts = stored_hash.split(":")
            # format: pbkdf2:sha256:<iterations>:<salt_b64>:<dk_b64>
            iterations = int(parts[2])
            salt = _b64url_decode(parts[3])
            expected_dk = _b64url_decode(parts[4])
            dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
            return hmac.compare_digest(dk, expected_dk)
        except Exception:
            return False

    # ------------------------------------------------------------------
    # JWT helpers
    # ------------------------------------------------------------------

    def _create_token(self, user_id: str, token_type: str, expiry: timedelta) -> str:
        now = datetime.now(timezone.utc)
        exp = int((now + expiry).timestamp())
        jti = str(uuid.uuid4())
        header = _b64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode())
        payload = _b64url_encode(
            json.dumps({"sub": user_id, "exp": exp, "type": token_type, "jti": jti}).encode()
        )
        signing_input = f"{header}.{payload}"
        sig = hmac.new(
            self.secret_key,
            signing_input.encode(),
            hashlib.sha256,
        ).digest()
        return f"{signing_input}.{_b64url_encode(sig)}"

    def verify_token(self, token: str) -> dict | None:
        """Verify JWT and return payload dict, or None if invalid/expired."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None
            signing_input = f"{parts[0]}.{parts[1]}"
            expected_sig = hmac.new(
                self.secret_key,
                signing_input.encode(),
                hashlib.sha256,
            ).digest()
            actual_sig = _b64url_decode(parts[2])
            if not hmac.compare_digest(expected_sig, actual_sig):
                return None
            payload = json.loads(_b64url_decode(parts[1]))
            if payload.get("exp", 0) < datetime.now(timezone.utc).timestamp():
                return None
            return payload
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, email: str, password: str, display_name: str | None = None) -> dict:
        """Register a new user. Raises ValueError if email already taken."""
        email = email.strip().lower()
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        existing = self.store.get_user_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        password_hash = self._hash_password(password)

        self.store.create_user(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            display_name=display_name,
            created_at=now,
        )

        user = {"id": user_id, "email": email, "display_name": display_name, "created_at": now}
        return self._build_token_response(user)

    def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens. Raises ValueError on failure."""
        email = email.strip().lower()
        row = self.store.get_user_by_email(email)
        if not row:
            raise ValueError("Invalid email or password")
        if not self._verify_password(password, row["password_hash"]):
            raise ValueError("Invalid email or password")

        now = datetime.now(timezone.utc).isoformat()
        self.store.update_user_login(row["id"], now)
        row = dict(row)
        row["last_login"] = now
        return self._build_token_response(row)

    def refresh(self, refresh_token: str) -> dict:
        """Exchange a valid refresh token for a new token pair. Raises ValueError on failure."""
        payload = self.verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise ValueError("Invalid or expired refresh token")

        user_id = payload["sub"]
        jti = payload.get("jti")
        valid_jtis = UserAuth._refresh_tokens.get(user_id, set())
        if jti not in valid_jtis:
            raise ValueError("Refresh token has been revoked or already used")

        user = self.store.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Invalidate old token before issuing new pair
        valid_jtis.discard(jti)
        return self._build_token_response(user)

    def get_user(self, user_id: str) -> dict | None:
        """Return user dict by ID, or None."""
        row = self.store.get_user_by_id(user_id)
        if not row:
            return None
        return {
            "id": row["id"],
            "email": row["email"],
            "display_name": row["display_name"],
            "created_at": row["created_at"],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_token_response(self, user: dict) -> dict:
        access_token = self._create_token(user["id"], "access", self.access_token_expiry)
        refresh_token = self._create_token(user["id"], "refresh", self.refresh_token_expiry)
        # Register the new refresh token's jti so it can be validated on use
        rt_payload = self.verify_token(refresh_token)
        if rt_payload and rt_payload.get("jti"):
            UserAuth._refresh_tokens.setdefault(user["id"], set()).add(rt_payload["jti"])
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "display_name": user.get("display_name"),
                "created_at": user.get("created_at"),
            },
        }
