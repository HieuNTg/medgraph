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
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone

_logger = logging.getLogger(__name__)
_DEV_SECRET = "medgraph-dev-secret"

# Track failed login attempts per email: {email: (count, first_attempt_time)}
_login_attempts: dict[str, tuple[int, float]] = {}
_login_lock = threading.Lock()
_MAX_LOGIN_ATTEMPTS = 5
_LOGIN_LOCKOUT_SECONDS = 300  # 5 minutes

# In-memory token blacklist: {jti: expiry_timestamp}
_revoked_tokens: dict[str, float] = {}
_revoked_tokens_lock = threading.Lock()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(s: str) -> bytes:
    # Restore padding
    padding = 4 - len(s) % 4
    if padding != 4:
        s += "=" * padding
    return base64.urlsafe_b64decode(s)


def _revoke_token(jti: str, exp: float) -> None:
    """Add a JTI to the in-memory revocation blacklist."""
    with _revoked_tokens_lock:
        _revoked_tokens[jti] = exp


def _is_token_revoked(jti: str) -> bool:
    """Return True if the JTI is in the revocation blacklist."""
    with _revoked_tokens_lock:
        return jti in _revoked_tokens


def cleanup_revoked_tokens() -> int:
    """Remove expired entries from the in-memory blacklist. Returns count removed."""
    now = time.time()
    with _revoked_tokens_lock:
        expired = [jti for jti, exp in _revoked_tokens.items() if exp < now]
        for jti in expired:
            del _revoked_tokens[jti]
    return len(expired)


class UserAuth:
    """Handles user registration, login, and JWT token lifecycle."""

    _HASH_ITERATIONS = 260_000  # OWASP recommended for pbkdf2_hmac/sha256

    def __init__(self, store, secret_key: str | None = None) -> None:
        self.store = store
        resolved_secret = secret_key or os.environ.get("MEDGRAPH_JWT_SECRET")
        env = os.environ.get("MEDGRAPH_ENV", "development")

        if not resolved_secret:
            if env == "production":
                raise RuntimeError(
                    "MEDGRAPH_JWT_SECRET must be set in production. "
                    "Do not use the default development secret."
                )
            _logger.warning(
                "MEDGRAPH_JWT_SECRET not set. Using default dev secret. "
                "Set MEDGRAPH_JWT_SECRET for any shared environment."
            )
            resolved_secret = _DEV_SECRET
        elif resolved_secret == _DEV_SECRET and env == "production":
            raise RuntimeError(
                "MEDGRAPH_JWT_SECRET must not be the default dev secret in production."
            )
        self.secret_key = resolved_secret.encode()
        self.access_token_expiry = timedelta(minutes=15)
        self.refresh_token_expiry = timedelta(days=7)

    # ------------------------------------------------------------------
    # Brute-force protection
    # ------------------------------------------------------------------

    @staticmethod
    def _check_login_rate(email: str) -> None:
        """Raise ValueError if too many failed attempts for this email."""
        now = time.time()
        with _login_lock:
            if email in _login_attempts:
                count, first_time = _login_attempts[email]
                if now - first_time > _LOGIN_LOCKOUT_SECONDS:
                    del _login_attempts[email]
                    return
                if count >= _MAX_LOGIN_ATTEMPTS:
                    raise ValueError("Too many login attempts. Please try again later.")

    @staticmethod
    def _record_failed_login(email: str) -> None:
        """Record a failed login attempt."""
        now = time.time()
        with _login_lock:
            if email in _login_attempts:
                count, first_time = _login_attempts[email]
                if now - first_time > _LOGIN_LOCKOUT_SECONDS:
                    _login_attempts[email] = (1, now)
                else:
                    _login_attempts[email] = (count + 1, first_time)
            else:
                _login_attempts[email] = (1, now)

    @staticmethod
    def _clear_failed_logins(email: str) -> None:
        """Clear failed attempts on successful login."""
        with _login_lock:
            _login_attempts.pop(email, None)

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
        """Verify JWT and return payload dict, or None if invalid/expired/revoked."""
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
            now_ts = datetime.now(timezone.utc).timestamp()
            if payload.get("exp", 0) < now_ts:
                return None
            # Check in-memory blacklist
            jti = payload.get("jti")
            if jti and _is_token_revoked(jti):
                return None
            return payload
        except Exception:
            return None

    def logout(self, token: str) -> None:
        """Revoke an access token by adding its JTI to the in-memory blacklist."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return
            payload = json.loads(_b64url_decode(parts[1]))
            jti = payload.get("jti")
            exp = payload.get("exp", 0)
            if jti:
                _revoke_token(jti, float(exp))
        except Exception:
            pass

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
        if len(password) > 128:
            raise ValueError("Password must be at most 128 characters")

        existing = self.store.get_user_by_email(email)
        if existing:
            raise ValueError("Registration failed. Please try again or use a different email.")

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
        self._check_login_rate(email)
        row = self.store.get_user_by_email(email)
        if not row:
            self._record_failed_login(email)
            raise ValueError("Invalid email or password")
        if not self._verify_password(password, row["password_hash"]):
            self._record_failed_login(email)
            raise ValueError("Invalid email or password")

        self._clear_failed_logins(email)
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
        if not jti or not self.store.is_refresh_token_valid(jti, user_id):
            raise ValueError("Refresh token has been revoked or already used")

        user = self.store.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Invalidate old token before issuing new pair
        self.store.revoke_refresh_token(jti)
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
            "is_admin": bool(row.get("is_admin", 0)),
            "created_at": row["created_at"],
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_token_response(self, user: dict) -> dict:
        access_token = self._create_token(user["id"], "access", self.access_token_expiry)
        refresh_token = self._create_token(user["id"], "refresh", self.refresh_token_expiry)
        # Register the new refresh token's jti in persistent storage
        rt_payload = self.verify_token(refresh_token)
        if rt_payload and rt_payload.get("jti"):
            expires_iso = (datetime.now(timezone.utc) + self.refresh_token_expiry).isoformat()
            self.store.store_refresh_token(rt_payload["jti"], user["id"], expires_iso)
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
