"""Evidence quality fields and evidence_sources table.

Revision ID: 002
Revises: 001
Create Date: 2026-03-23
"""

from __future__ import annotations

from alembic import op

revision: str = "002"
down_revision: str | None = "001"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # Add new columns to interactions
    op.execute("ALTER TABLE interactions ADD COLUMN evidence_level TEXT NOT NULL DEFAULT 'D'")
    op.execute("ALTER TABLE interactions ADD COLUMN source_citation TEXT")
    op.execute("ALTER TABLE interactions ADD COLUMN last_updated TEXT")
    op.execute("ALTER TABLE interactions ADD COLUMN clinical_significance TEXT")

    # Add new columns to drugs
    op.execute("ALTER TABLE drugs ADD COLUMN category TEXT NOT NULL DEFAULT 'prescription'")
    op.execute("ALTER TABLE drugs ADD COLUMN last_updated TEXT")
    op.execute("ALTER TABLE drugs ADD COLUMN atc_code TEXT")

    # Create evidence_sources table
    op.execute("""
        CREATE TABLE IF NOT EXISTS evidence_sources (
            id           TEXT PRIMARY KEY,
            interaction_id TEXT NOT NULL REFERENCES interactions(id),
            source_type  TEXT NOT NULL,
            citation     TEXT NOT NULL DEFAULT '',
            url          TEXT,
            year         INTEGER
        )
    """)

    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_evidence_sources_interaction"
        " ON evidence_sources(interaction_id)"
    )

    op.execute("""
        INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', '002')
    """)


def downgrade() -> None:
    # SQLite does not support DROP COLUMN in older versions; recreate tables
    op.execute("DROP TABLE IF EXISTS evidence_sources")

    # Recreate interactions without new columns
    op.execute("""
        CREATE TABLE interactions_backup AS
        SELECT id, drug_a_id, drug_b_id, severity, description, mechanism, source, evidence_count
        FROM interactions
    """)
    op.execute("DROP TABLE interactions")
    op.execute("ALTER TABLE interactions_backup RENAME TO interactions")

    # Recreate drugs without new columns
    op.execute("""
        CREATE TABLE drugs_backup AS
        SELECT id, name, brand_names, description, drug_class, rxnorm_cui
        FROM drugs
    """)
    op.execute("DROP TABLE drugs")
    op.execute("ALTER TABLE drugs_backup RENAME TO drugs")

    op.execute("""
        INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', '001')
    """)
