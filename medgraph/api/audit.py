"""
Audit logging service for MEDGRAPH.

Records user actions to the audit_log table for compliance and debugging.
"""

import uuid
from datetime import datetime, timezone


class AuditLogger:
    """Write and query audit log entries."""

    def __init__(self, store) -> None:
        self.store = store

    def log(
        self,
        action: str,
        user_id: str | None = None,
        resource_type: str | None = None,
        resource_id: str | None = None,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> None:
        """Append an audit entry. Failures are silently swallowed to avoid breaking callers."""
        try:
            self.store.add_audit_log(
                log_id=str(uuid.uuid4()),
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                ip_address=ip_address,
                user_agent=user_agent,
                created_at=datetime.now(timezone.utc).isoformat(),
            )
        except Exception:  # nosec B110 — audit failures must not break primary operations
            pass

    def get_logs(
        self,
        user_id: str | None = None,
        action: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        """Return audit log entries as list of dicts."""
        return self.store.get_audit_logs(
            user_id=user_id,
            action=action,
            limit=limit,
            offset=offset,
        )
