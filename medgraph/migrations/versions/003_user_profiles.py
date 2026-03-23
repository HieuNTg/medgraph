"""User profiles, analysis history, sharing, and audit logging tables.

Revision ID: 003
Revises: 002
Create Date: 2026-03-23
"""

from __future__ import annotations

from alembic import op

revision: str = "003"
down_revision: str | None = "002"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id           TEXT PRIMARY KEY,
            email        TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT,
            created_at   TEXT NOT NULL,
            last_login   TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS medication_profiles (
            id         TEXT PRIMARY KEY,
            user_id    TEXT NOT NULL REFERENCES users(id),
            name       TEXT NOT NULL,
            drug_ids   TEXT NOT NULL,
            notes      TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id           TEXT PRIMARY KEY,
            user_id      TEXT REFERENCES users(id),
            drug_ids     TEXT NOT NULL,
            result_json  TEXT NOT NULL,
            overall_risk TEXT NOT NULL,
            created_at   TEXT NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS shared_results (
            id          TEXT PRIMARY KEY,
            analysis_id TEXT NOT NULL REFERENCES analysis_history(id),
            expires_at  TEXT,
            created_at  TEXT NOT NULL
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id            TEXT PRIMARY KEY,
            user_id       TEXT,
            action        TEXT NOT NULL,
            resource_type TEXT,
            resource_id   TEXT,
            ip_address    TEXT,
            user_agent    TEXT,
            created_at    TEXT NOT NULL
        )
    """)

    # Indexes
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_profiles_user ON medication_profiles(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_history_user ON analysis_history(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_history_created ON analysis_history(created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_shared_analysis ON shared_results(analysis_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at)")

    op.execute("""
        INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', '003')
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS audit_log")
    op.execute("DROP TABLE IF EXISTS shared_results")
    op.execute("DROP TABLE IF EXISTS analysis_history")
    op.execute("DROP TABLE IF EXISTS medication_profiles")
    op.execute("DROP TABLE IF EXISTS users")

    op.execute("""
        INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', '002')
    """)
