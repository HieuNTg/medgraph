"""Baseline schema — captures existing MEDGRAPH tables.

Revision ID: 001
Revises: None
Create Date: 2026-03-23
"""

from __future__ import annotations

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS drugs (
            id          TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            brand_names TEXT NOT NULL DEFAULT '[]',
            description TEXT NOT NULL DEFAULT '',
            drug_class  TEXT,
            rxnorm_cui  TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id      TEXT PRIMARY KEY,
            name    TEXT NOT NULL,
            drug_id TEXT NOT NULL REFERENCES drugs(id)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS enzymes (
            id   TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gene TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id             TEXT PRIMARY KEY,
            drug_a_id      TEXT NOT NULL,
            drug_b_id      TEXT NOT NULL,
            severity       TEXT NOT NULL,
            description    TEXT NOT NULL DEFAULT '',
            mechanism      TEXT,
            source         TEXT NOT NULL DEFAULT 'seed',
            evidence_count INTEGER NOT NULL DEFAULT 0
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS drug_enzyme_relations (
            drug_id       TEXT NOT NULL,
            enzyme_id     TEXT NOT NULL,
            relation_type TEXT NOT NULL,
            strength      TEXT NOT NULL DEFAULT 'moderate',
            PRIMARY KEY (drug_id, enzyme_id, relation_type)
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS adverse_events (
            id          TEXT PRIMARY KEY,
            drug_ids    TEXT NOT NULL DEFAULT '[]',
            reaction    TEXT NOT NULL,
            count       INTEGER NOT NULL DEFAULT 0,
            seriousness TEXT NOT NULL DEFAULT 'unknown',
            source_url  TEXT
        )
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS genetic_guidelines (
            drug_id              TEXT NOT NULL,
            gene_id              TEXT NOT NULL,
            phenotype            TEXT NOT NULL,
            recommendation       TEXT NOT NULL DEFAULT '',
            severity_multiplier  REAL NOT NULL DEFAULT 1.0,
            PRIMARY KEY (drug_id, gene_id, phenotype)
        )
    """)

    # Indexes
    op.execute("CREATE INDEX IF NOT EXISTS idx_drugs_name ON drugs(name)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_drugs_name_lower ON drugs(LOWER(name))")
    op.execute("CREATE INDEX IF NOT EXISTS idx_drugs_rxnorm ON drugs(rxnorm_cui)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_interactions_ab ON interactions(drug_a_id, drug_b_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_interactions_ba ON interactions(drug_b_id, drug_a_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS idx_drug_enzyme_drug ON drug_enzyme_relations(drug_id)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_drug_enzyme_enzyme ON drug_enzyme_relations(enzyme_id)"
    )

    # Schema metadata table for version tracking
    op.execute("""
        CREATE TABLE IF NOT EXISTS schema_metadata (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    op.execute("""
        INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', '001')
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS schema_metadata")
    op.execute("DROP TABLE IF EXISTS genetic_guidelines")
    op.execute("DROP TABLE IF EXISTS adverse_events")
    op.execute("DROP TABLE IF EXISTS drug_enzyme_relations")
    op.execute("DROP TABLE IF EXISTS interactions")
    op.execute("DROP TABLE IF EXISTS enzymes")
    op.execute("DROP TABLE IF EXISTS ingredients")
    op.execute("DROP TABLE IF EXISTS drugs")
