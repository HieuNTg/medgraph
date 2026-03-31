"""
SQLite-backed storage for MEDGRAPH knowledge graph data.

Uses synchronous sqlite3 with context manager pattern. DB file at data/medgraph.db.
Supports DATABASE_URL env var for future PostgreSQL migration.
"""

from __future__ import annotations

import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Optional

from medgraph.graph.db_config import get_db_config
from medgraph.graph.models import (
    AdverseEvent,
    Drug,
    DrugEnzymeRelation,
    Enzyme,
    EvidenceSource,
    GeneticGuideline,
    Interaction,
)

logger = logging.getLogger(__name__)

# Default DB path — relative to project root
DEFAULT_DB_PATH = Path("data/medgraph.db")


class GraphStore:
    """
    Persistent storage for drug interaction graph data.

    Wraps SQLite with typed upsert/query methods for all entity types.
    DB is initialized (tables + indexes created) on first use.

    Reads DATABASE_URL env var via db_config module. Currently only SQLite
    is fully implemented; PostgreSQL support is planned for April 2026.
    """

    def __init__(self, db_path: Path | str | None = None) -> None:
        config = get_db_config()
        if db_path is not None:
            # Explicit path overrides env config (backward compat)
            self.db_path = Path(db_path)
        elif config.db_path is not None:
            self.db_path = config.db_path
        else:
            self.db_path = DEFAULT_DB_PATH

        if config.is_postgresql:
            logger.warning(
                "DATABASE_URL points to PostgreSQL but only SQLite is currently "
                "supported. Falling back to SQLite at %s. PostgreSQL migration "
                "planned for April 2026.",
                self.db_path,
            )

        self.db_config = config
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self._migrate_add_is_admin()
        self._ensure_schema_metadata()
        self._backfill_adverse_event_drugs()

    @contextmanager
    def connect(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager providing a SQLite connection with row_factory set."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA synchronous=NORMAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # Backward-compatible alias
    _connect = connect

    def init_db(self) -> None:
        """Create all tables and indexes if they don't exist.

        NOTE: For production, use Alembic migrations (medgraph/migrations/)
        as the canonical DDL source. This method serves as a safe fallback
        ensuring the app works without running migrations first.
        """
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id            TEXT PRIMARY KEY,
                    email         TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name  TEXT,
                    is_admin      INTEGER NOT NULL DEFAULT 0,
                    created_at    TEXT NOT NULL,
                    last_login    TEXT
                );

                CREATE TABLE IF NOT EXISTS medication_profiles (
                    id         TEXT PRIMARY KEY,
                    user_id    TEXT NOT NULL REFERENCES users(id),
                    name       TEXT NOT NULL,
                    drug_ids   TEXT NOT NULL,
                    notes      TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS analysis_history (
                    id           TEXT PRIMARY KEY,
                    user_id      TEXT REFERENCES users(id),
                    drug_ids     TEXT NOT NULL,
                    result_json  TEXT NOT NULL,
                    overall_risk TEXT NOT NULL,
                    created_at   TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS shared_results (
                    id          TEXT PRIMARY KEY,
                    analysis_id TEXT NOT NULL REFERENCES analysis_history(id),
                    expires_at  TEXT,
                    created_at  TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS audit_log (
                    id            TEXT PRIMARY KEY,
                    user_id       TEXT,
                    action        TEXT NOT NULL,
                    resource_type TEXT,
                    resource_id   TEXT,
                    ip_address    TEXT,
                    user_agent    TEXT,
                    created_at    TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_users_email
                    ON users(email);
                CREATE INDEX IF NOT EXISTS idx_profiles_user
                    ON medication_profiles(user_id);
                CREATE INDEX IF NOT EXISTS idx_history_user
                    ON analysis_history(user_id);
                CREATE INDEX IF NOT EXISTS idx_history_created
                    ON analysis_history(created_at);
                CREATE INDEX IF NOT EXISTS idx_shared_analysis
                    ON shared_results(analysis_id);
                CREATE INDEX IF NOT EXISTS idx_audit_user
                    ON audit_log(user_id);
                CREATE INDEX IF NOT EXISTS idx_audit_created
                    ON audit_log(created_at);
                CREATE INDEX IF NOT EXISTS idx_analysis_user_created
                    ON analysis_history(user_id, created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_shared_expires
                    ON shared_results(expires_at);
                CREATE INDEX IF NOT EXISTS idx_audit_user_created
                    ON audit_log(user_id, created_at DESC);

                CREATE TABLE IF NOT EXISTS drugs (
                    id          TEXT PRIMARY KEY,
                    name        TEXT NOT NULL,
                    brand_names TEXT NOT NULL DEFAULT '[]',
                    description TEXT NOT NULL DEFAULT '',
                    drug_class  TEXT,
                    rxnorm_cui  TEXT,
                    category    TEXT NOT NULL DEFAULT 'prescription',
                    last_updated TEXT,
                    atc_code    TEXT
                );

                CREATE TABLE IF NOT EXISTS ingredients (
                    id      TEXT PRIMARY KEY,
                    name    TEXT NOT NULL,
                    drug_id TEXT NOT NULL REFERENCES drugs(id)
                );

                CREATE TABLE IF NOT EXISTS enzymes (
                    id   TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    gene TEXT
                );

                CREATE TABLE IF NOT EXISTS interactions (
                    id                   TEXT PRIMARY KEY,
                    drug_a_id            TEXT NOT NULL,
                    drug_b_id            TEXT NOT NULL,
                    severity             TEXT NOT NULL,
                    description          TEXT NOT NULL DEFAULT '',
                    mechanism            TEXT,
                    source               TEXT NOT NULL DEFAULT 'seed',
                    evidence_count       INTEGER NOT NULL DEFAULT 0,
                    evidence_level       TEXT NOT NULL DEFAULT 'D',
                    source_citation      TEXT,
                    last_updated         TEXT,
                    clinical_significance TEXT
                );

                CREATE TABLE IF NOT EXISTS evidence_sources (
                    id             TEXT PRIMARY KEY,
                    interaction_id TEXT NOT NULL REFERENCES interactions(id),
                    source_type    TEXT NOT NULL,
                    citation       TEXT NOT NULL DEFAULT '',
                    url            TEXT,
                    year           INTEGER
                );

                CREATE TABLE IF NOT EXISTS drug_enzyme_relations (
                    drug_id       TEXT NOT NULL,
                    enzyme_id     TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    strength      TEXT NOT NULL DEFAULT 'moderate',
                    PRIMARY KEY (drug_id, enzyme_id, relation_type)
                );

                CREATE TABLE IF NOT EXISTS adverse_events (
                    id          TEXT PRIMARY KEY,
                    drug_ids    TEXT NOT NULL DEFAULT '[]',
                    reaction    TEXT NOT NULL,
                    count       INTEGER NOT NULL DEFAULT 0,
                    seriousness TEXT NOT NULL DEFAULT 'unknown',
                    source_url  TEXT
                );

                CREATE TABLE IF NOT EXISTS adverse_event_drugs (
                    event_id TEXT NOT NULL,
                    drug_id  TEXT NOT NULL,
                    PRIMARY KEY (event_id, drug_id),
                    FOREIGN KEY (event_id) REFERENCES adverse_events(id),
                    FOREIGN KEY (drug_id) REFERENCES drugs(id)
                );

                CREATE INDEX IF NOT EXISTS idx_aed_drug_id ON adverse_event_drugs(drug_id);

                CREATE TABLE IF NOT EXISTS genetic_guidelines (
                    drug_id              TEXT NOT NULL,
                    gene_id              TEXT NOT NULL,
                    phenotype            TEXT NOT NULL,
                    recommendation       TEXT NOT NULL DEFAULT '',
                    severity_multiplier  REAL NOT NULL DEFAULT 1.0,
                    PRIMARY KEY (drug_id, gene_id, phenotype)
                );

                CREATE TABLE IF NOT EXISTS food_interactions (
                    id TEXT PRIMARY KEY,
                    food_name TEXT NOT NULL,
                    food_category TEXT NOT NULL,
                    drug_id TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    mechanism TEXT,
                    evidence_level TEXT DEFAULT 'C',
                    FOREIGN KEY (drug_id) REFERENCES drugs(id)
                );

                CREATE INDEX IF NOT EXISTS idx_food_drug ON food_interactions(drug_id);

                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    jti       TEXT PRIMARY KEY,
                    user_id   TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON refresh_tokens(user_id);

                -- Indexes for performance
                CREATE INDEX IF NOT EXISTS idx_drugs_name
                    ON drugs(name);
                CREATE INDEX IF NOT EXISTS idx_drugs_name_lower
                    ON drugs(LOWER(name));
                CREATE INDEX IF NOT EXISTS idx_drugs_rxnorm
                    ON drugs(rxnorm_cui);
                CREATE INDEX IF NOT EXISTS idx_interactions_ab
                    ON interactions(drug_a_id, drug_b_id);
                CREATE INDEX IF NOT EXISTS idx_interactions_ba
                    ON interactions(drug_b_id, drug_a_id);
                CREATE INDEX IF NOT EXISTS idx_drug_enzyme_drug
                    ON drug_enzyme_relations(drug_id);
                CREATE INDEX IF NOT EXISTS idx_drug_enzyme_enzyme
                    ON drug_enzyme_relations(enzyme_id);
                CREATE INDEX IF NOT EXISTS idx_evidence_sources_interaction
                    ON evidence_sources(interaction_id);

                CREATE INDEX IF NOT EXISTS idx_adverse_event_drugs ON adverse_event_drugs(event_id, drug_id);
                CREATE INDEX IF NOT EXISTS idx_genetic_guidelines_drug_gene ON genetic_guidelines(drug_id, gene_id);
                CREATE INDEX IF NOT EXISTS idx_food_interactions_drug_id ON food_interactions(drug_id);
                CREATE INDEX IF NOT EXISTS idx_refresh_tokens_jti ON refresh_tokens(jti);
                CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id);

                CREATE TABLE IF NOT EXISTS refresh_metadata (
                    id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    source         TEXT NOT NULL,
                    last_refresh   TEXT NOT NULL,
                    records_updated INTEGER NOT NULL DEFAULT 0,
                    status         TEXT NOT NULL DEFAULT 'completed',
                    created_at     TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_refresh_metadata_source ON refresh_metadata(source);
                CREATE INDEX IF NOT EXISTS idx_refresh_metadata_created ON refresh_metadata(created_at DESC);
            """)

    def _migrate_add_is_admin(self) -> None:
        """Add is_admin column to existing users table if missing."""
        with self._connect() as conn:
            columns = [row[1] for row in conn.execute("PRAGMA table_info(users)").fetchall()]
            if "is_admin" not in columns:
                conn.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0")

    # -------------------------------------------------------------------------
    # Upsert methods
    # -------------------------------------------------------------------------

    def upsert_drug(self, drug: Drug) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO drugs (id, name, brand_names, description, drug_class, rxnorm_cui,
                                   category, last_updated, atc_code)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name         = excluded.name,
                    brand_names  = excluded.brand_names,
                    description  = excluded.description,
                    drug_class   = excluded.drug_class,
                    rxnorm_cui   = excluded.rxnorm_cui,
                    category     = excluded.category,
                    last_updated = excluded.last_updated,
                    atc_code     = excluded.atc_code
                """,
                (
                    drug.id,
                    drug.name,
                    json.dumps(drug.brand_names),
                    drug.description,
                    drug.drug_class,
                    drug.rxnorm_cui,
                    drug.category,
                    drug.last_updated,
                    drug.atc_code,
                ),
            )

    def upsert_enzyme(self, enzyme: Enzyme) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO enzymes (id, name, gene)
                VALUES (?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    gene = excluded.gene
                """,
                (enzyme.id, enzyme.name, enzyme.gene),
            )

    def upsert_interaction(self, interaction: Interaction) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO interactions
                    (id, drug_a_id, drug_b_id, severity, description, mechanism, source,
                     evidence_count, evidence_level, source_citation, last_updated,
                     clinical_significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    severity              = excluded.severity,
                    description           = excluded.description,
                    mechanism             = excluded.mechanism,
                    source                = excluded.source,
                    evidence_count        = excluded.evidence_count,
                    evidence_level        = excluded.evidence_level,
                    source_citation       = excluded.source_citation,
                    last_updated          = excluded.last_updated,
                    clinical_significance = excluded.clinical_significance
                """,
                (
                    interaction.id,
                    interaction.drug_a_id,
                    interaction.drug_b_id,
                    interaction.severity,
                    interaction.description,
                    interaction.mechanism,
                    interaction.source,
                    interaction.evidence_count,
                    interaction.evidence_level,
                    interaction.source_citation,
                    interaction.last_updated,
                    interaction.clinical_significance,
                ),
            )

    def upsert_drug_enzyme_relation(self, relation: DrugEnzymeRelation) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO drug_enzyme_relations (drug_id, enzyme_id, relation_type, strength)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(drug_id, enzyme_id, relation_type) DO UPDATE SET
                    strength = excluded.strength
                """,
                (relation.drug_id, relation.enzyme_id, relation.relation_type, relation.strength),
            )

    def upsert_adverse_event(self, event: AdverseEvent) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO adverse_events (id, drug_ids, reaction, count, seriousness, source_url)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    drug_ids    = excluded.drug_ids,
                    reaction    = excluded.reaction,
                    count       = excluded.count,
                    seriousness = excluded.seriousness,
                    source_url  = excluded.source_url
                """,
                (
                    event.id,
                    json.dumps(event.drug_ids),
                    event.reaction,
                    event.count,
                    event.seriousness,
                    event.source_url,
                ),
            )
            # Keep junction table in sync
            conn.execute("DELETE FROM adverse_event_drugs WHERE event_id = ?", (event.id,))
            conn.executemany(
                "INSERT OR IGNORE INTO adverse_event_drugs (event_id, drug_id) VALUES (?, ?)",
                [(event.id, did) for did in event.drug_ids],
            )

    def upsert_evidence_source(self, source: EvidenceSource) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO evidence_sources (id, interaction_id, source_type, citation, url, year)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    interaction_id = excluded.interaction_id,
                    source_type    = excluded.source_type,
                    citation       = excluded.citation,
                    url            = excluded.url,
                    year           = excluded.year
                """,
                (
                    source.id,
                    source.interaction_id,
                    source.source_type,
                    source.citation,
                    source.url,
                    source.year,
                ),
            )

    # -------------------------------------------------------------------------
    # Query methods
    # -------------------------------------------------------------------------

    def get_drug_by_id(self, drug_id: str) -> Optional[Drug]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM drugs WHERE id = ?", (drug_id,)).fetchone()
        return self._row_to_drug(row) if row else None

    def get_drugs_by_ids(self, drug_ids: list[str]) -> dict[str, "Drug"]:
        """Batch fetch drugs by IDs. Returns {drug_id: Drug} dict."""
        if not drug_ids:
            return {}
        placeholders = ",".join("?" * len(drug_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM drugs WHERE id IN ({placeholders})",  # nosec B608
                drug_ids,
            ).fetchall()
        return {r["id"]: self._row_to_drug(r) for r in rows}

    def get_drug_by_name(self, name: str) -> Optional[Drug]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM drugs WHERE LOWER(name) = LOWER(?)", (name,)
            ).fetchone()
        return self._row_to_drug(row) if row else None

    @staticmethod
    def _escape_like(query: str) -> str:
        """Escape LIKE wildcard characters (%, _) in user input."""
        return query.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    def search_drugs(self, query: str, limit: int = 10, offset: int = 0) -> list[Drug]:
        escaped = self._escape_like(query)
        pattern = f"%{escaped}%"
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM drugs WHERE LOWER(name) LIKE LOWER(?) ESCAPE '\\' LIMIT ? OFFSET ?",
                (pattern, limit, offset),
            ).fetchall()
        return [self._row_to_drug(r) for r in rows]

    def search_drugs_with_count(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> tuple[list["Drug"], int]:
        """Search drugs and return (results, total_count) in a single connection."""
        escaped = self._escape_like(query)
        pattern = f"%{escaped}%"
        where = "WHERE LOWER(name) LIKE LOWER(?) ESCAPE '\\'"
        with self._connect() as conn:
            total = conn.execute(f"SELECT COUNT(*) FROM drugs {where}", (pattern,)).fetchone()[0]  # nosec B608  # noqa: E501
            rows = conn.execute(
                f"SELECT * FROM drugs {where} LIMIT ? OFFSET ?",  # nosec B608
                (pattern, limit, offset),
            ).fetchall()
        return [self._row_to_drug(r) for r in rows], total

    def count_search_drugs(self, query: str) -> int:
        """Count total matching drugs for a search query."""
        escaped = self._escape_like(query)
        pattern = f"%{escaped}%"
        with self._connect() as conn:
            row = conn.execute(
                "SELECT COUNT(*) FROM drugs WHERE LOWER(name) LIKE LOWER(?) ESCAPE '\\'",
                (pattern,),
            ).fetchone()
        return row[0]

    def get_all_drugs(self) -> list[Drug]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM drugs").fetchall()
        return [self._row_to_drug(r) for r in rows]

    def get_all_enzymes(self) -> list[Enzyme]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM enzymes").fetchall()
        return [Enzyme(id=r["id"], name=r["name"], gene=r["gene"]) for r in rows]

    def get_all_interactions(self) -> list[Interaction]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM interactions").fetchall()
        return [self._row_to_interaction(r) for r in rows]

    def get_interaction_by_id(self, interaction_id: str) -> Optional[Interaction]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM interactions WHERE id = ?", (interaction_id,)
            ).fetchone()
        if not row:
            return None
        return self._row_to_interaction(row)

    def get_all_drug_enzyme_relations(self) -> list[DrugEnzymeRelation]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM drug_enzyme_relations").fetchall()
        return [
            DrugEnzymeRelation(
                drug_id=r["drug_id"],
                enzyme_id=r["enzyme_id"],
                relation_type=r["relation_type"],
                strength=r["strength"],
            )
            for r in rows
        ]

    def get_interactions_for_drugs(self, drug_ids: list[str]) -> list[Interaction]:
        if not drug_ids:
            return []
        placeholders = ",".join("?" * len(drug_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT * FROM interactions
                WHERE drug_a_id IN ({placeholders}) OR drug_b_id IN ({placeholders})
                """,  # nosec B608
                drug_ids + drug_ids,
            ).fetchall()
        return [self._row_to_interaction(r) for r in rows]

    def get_direct_interaction(self, drug_a_id: str, drug_b_id: str) -> Optional[Interaction]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT * FROM interactions
                WHERE (drug_a_id = ? AND drug_b_id = ?)
                   OR (drug_a_id = ? AND drug_b_id = ?)
                LIMIT 1
                """,
                (drug_a_id, drug_b_id, drug_b_id, drug_a_id),
            ).fetchone()
        return self._row_to_interaction(row) if row else None

    def get_enzyme_relations(self, drug_id: str) -> list[DrugEnzymeRelation]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM drug_enzyme_relations WHERE drug_id = ?", (drug_id,)
            ).fetchall()
        return [
            DrugEnzymeRelation(
                drug_id=r["drug_id"],
                enzyme_id=r["enzyme_id"],
                relation_type=r["relation_type"],
                strength=r["strength"],
            )
            for r in rows
        ]

    def get_adverse_events(self, drug_ids: list[str]) -> list[AdverseEvent]:
        if not drug_ids:
            return []
        placeholders = ",".join("?" * len(drug_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"""
                SELECT DISTINCT ae.*
                FROM adverse_events ae
                JOIN adverse_event_drugs aed ON ae.id = aed.event_id
                WHERE aed.drug_id IN ({placeholders})
                """,  # nosec B608
                drug_ids,
            ).fetchall()
        return [
            AdverseEvent(
                id=row["id"],
                drug_ids=json.loads(row["drug_ids"]),
                reaction=row["reaction"],
                count=row["count"],
                seriousness=row["seriousness"],
                source_url=row["source_url"],
            )
            for row in rows
        ]

    def upsert_genetic_guideline(self, g: GeneticGuideline) -> None:
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO genetic_guidelines (drug_id, gene_id, phenotype, recommendation, severity_multiplier)
                   VALUES (?, ?, ?, ?, ?)
                   ON CONFLICT(drug_id, gene_id, phenotype) DO UPDATE SET
                       recommendation=excluded.recommendation,
                       severity_multiplier=excluded.severity_multiplier""",
                (g.drug_id, g.gene_id, g.phenotype, g.recommendation, g.severity_multiplier),
            )

    def get_genetic_guidelines(self, drug_id: str, gene_id: str) -> list[GeneticGuideline]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM genetic_guidelines WHERE drug_id = ? AND gene_id = ?",
                (drug_id, gene_id),
            ).fetchall()
        return [GeneticGuideline(**dict(r)) for r in rows]

    def get_guidelines_for_drug(self, drug_id: str) -> list[GeneticGuideline]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM genetic_guidelines WHERE drug_id = ?",
                (drug_id,),
            ).fetchall()
        return [GeneticGuideline(**dict(r)) for r in rows]

    def get_guidelines_for_drugs(self, drug_ids: list[str]) -> list[GeneticGuideline]:
        """Batch lookup: return all genetic guidelines for a list of drug IDs."""
        if not drug_ids:
            return []
        placeholders = ",".join("?" * len(drug_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM genetic_guidelines WHERE drug_id IN ({placeholders})",  # nosec B608
                drug_ids,
            ).fetchall()
        return [GeneticGuideline(**dict(r)) for r in rows]

    def get_all_guidelines(self) -> list[GeneticGuideline]:
        """Return every genetic guideline row (used for in-memory caching)."""
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM genetic_guidelines").fetchall()
        return [GeneticGuideline(**dict(r)) for r in rows]

    def get_evidence_sources(self, interaction_id: str) -> list[EvidenceSource]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM evidence_sources WHERE interaction_id = ?",
                (interaction_id,),
            ).fetchall()
        return [
            EvidenceSource(
                id=r["id"],
                interaction_id=r["interaction_id"],
                source_type=r["source_type"],
                citation=r["citation"] or "",
                url=r["url"],
                year=r["year"],
            )
            for r in rows
        ]

    # -------------------------------------------------------------------------
    # Users
    # -------------------------------------------------------------------------

    def create_user(
        self,
        user_id: str,
        email: str,
        password_hash: str,
        display_name: Optional[str],
        created_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO users (id, email, password_hash, display_name, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user_id, email, password_hash, display_name, created_at),
            )

    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def get_user_by_email(self, email: str) -> Optional[dict]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

    def update_user_login(self, user_id: str, last_login: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (last_login, user_id))

    # -------------------------------------------------------------------------
    # Medication Profiles
    # -------------------------------------------------------------------------

    def create_profile(
        self,
        profile_id: str,
        user_id: str,
        name: str,
        drug_ids: list[str],
        notes: Optional[str],
        created_at: str,
        updated_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO medication_profiles
                    (id, user_id, name, drug_ids, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (profile_id, user_id, name, json.dumps(drug_ids), notes, created_at, updated_at),
            )

    def get_profiles_by_user(self, user_id: str) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM medication_profiles WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        return [self._row_to_profile(r) for r in rows]

    def get_profile_by_id(self, profile_id: str) -> Optional[dict]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM medication_profiles WHERE id = ?", (profile_id,)
            ).fetchone()
        return self._row_to_profile(row) if row else None

    def update_profile(
        self,
        profile_id: str,
        name: str,
        drug_ids: list[str],
        notes: Optional[str],
        updated_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE medication_profiles
                SET name = ?, drug_ids = ?, notes = ?, updated_at = ?
                WHERE id = ?
                """,
                (name, json.dumps(drug_ids), notes, updated_at, profile_id),
            )

    def delete_profile(self, profile_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM medication_profiles WHERE id = ?", (profile_id,))

    @staticmethod
    def _row_to_profile(row: sqlite3.Row) -> dict:
        d = dict(row)
        d["drug_ids"] = json.loads(d["drug_ids"])
        return d

    # -------------------------------------------------------------------------
    # Analysis History
    # -------------------------------------------------------------------------

    def save_analysis(
        self,
        analysis_id: str,
        user_id: Optional[str],
        drug_ids: list[str],
        result_json: str,
        overall_risk: str,
        created_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO analysis_history
                    (id, user_id, drug_ids, result_json, overall_risk, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (analysis_id, user_id, json.dumps(drug_ids), result_json, overall_risk, created_at),
            )

    def get_history_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM analysis_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
                """,
                (user_id, limit, offset),
            ).fetchall()
        return [self._row_to_history(r) for r in rows]

    def get_analysis_by_id(self, analysis_id: str) -> Optional[dict]:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM analysis_history WHERE id = ?", (analysis_id,)
            ).fetchone()
        return self._row_to_history(row) if row else None

    @staticmethod
    def _row_to_history(row: sqlite3.Row) -> dict:
        d = dict(row)
        d["drug_ids"] = json.loads(d["drug_ids"])
        return d

    # -------------------------------------------------------------------------
    # Shared Results
    # -------------------------------------------------------------------------

    def create_shared_result(
        self,
        share_id: str,
        analysis_id: str,
        expires_at: Optional[str],
        created_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO shared_results (id, analysis_id, expires_at, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (share_id, analysis_id, expires_at, created_at),
            )

    def get_shared_result(self, share_id: str) -> Optional[dict]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM shared_results WHERE id = ?", (share_id,)).fetchone()
        return dict(row) if row else None

    # -------------------------------------------------------------------------
    # Audit Log
    # -------------------------------------------------------------------------

    def add_audit_log(
        self,
        log_id: str,
        user_id: Optional[str],
        action: str,
        resource_type: Optional[str],
        resource_id: Optional[str],
        ip_address: Optional[str],
        user_agent: Optional[str],
        created_at: str,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO audit_log
                    (id, user_id, action, resource_type, resource_id,
                     ip_address, user_agent, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    log_id,
                    user_id,
                    action,
                    resource_type,
                    resource_id,
                    ip_address,
                    user_agent,
                    created_at,
                ),
            )

    def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        conditions: list[str] = []
        params: list = []
        if user_id is not None:
            conditions.append("user_id = ?")
            params.append(user_id)
        if action is not None:
            conditions.append("action = ?")
            params.append(action)
        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        params.extend([limit, offset])
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM audit_log {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",  # nosec B608
                params,
            ).fetchall()
        return [dict(r) for r in rows]

    # -------------------------------------------------------------------------
    # Schema metadata
    # -------------------------------------------------------------------------

    def _ensure_schema_metadata(self) -> None:
        """Create schema_metadata table if missing (for pre-migration DBs)."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_metadata (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            """)

    # -------------------------------------------------------------------------
    # Refresh metadata (FAERS pipeline)
    # -------------------------------------------------------------------------

    def save_refresh_metadata(self, source: str, records_updated: int, status: str) -> None:
        """Insert a refresh run record into refresh_metadata."""
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO refresh_metadata (source, last_refresh, records_updated, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (source, now, records_updated, status, now),
            )

    def get_last_refresh(self, source: str) -> Optional[dict]:
        """Return the most recent refresh record for a source, or None."""
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT id, source, last_refresh, records_updated, status, created_at
                FROM refresh_metadata
                WHERE source = ?
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (source,),
            ).fetchone()
        return dict(row) if row else None

    def get_refresh_history(self, limit: int = 20) -> list[dict]:
        """Return recent refresh records across all sources, newest first."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, source, last_refresh, records_updated, status, created_at
                FROM refresh_metadata
                ORDER BY created_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_schema_version(self) -> str:
        """Return the current schema version string."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
            ).fetchone()
        return row["value"] if row else "unknown"

    def set_schema_version(self, version: str) -> None:
        """Update the schema version in metadata."""
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO schema_metadata (key, value) VALUES ('schema_version', ?)",
                (version,),
            )

    # -------------------------------------------------------------------------
    # Backup / Restore
    # -------------------------------------------------------------------------

    def backup(self, dest_path: Path | str) -> Path:
        """Create a backup of the database using SQLite online backup API.

        Returns the path to the backup file.
        """
        import sqlite3 as _sqlite3

        dest = Path(dest_path)
        dest.parent.mkdir(parents=True, exist_ok=True)

        src_conn = _sqlite3.connect(self.db_path)
        dst_conn = _sqlite3.connect(dest)
        try:
            src_conn.backup(dst_conn)
        finally:
            dst_conn.close()
            src_conn.close()
        return dest

    def restore(self, src_path: Path | str) -> None:
        """Restore the database from a backup file using SQLite online backup API."""
        import sqlite3 as _sqlite3

        src = Path(src_path)
        if not src.exists():
            raise FileNotFoundError(f"Backup file not found: {src}")

        src_conn = _sqlite3.connect(src)
        dst_conn = _sqlite3.connect(self.db_path)
        try:
            src_conn.backup(dst_conn)
        finally:
            dst_conn.close()
            src_conn.close()

    # -------------------------------------------------------------------------
    # Food Interactions
    # -------------------------------------------------------------------------

    def seed_food_interactions(self, food_data: list[dict]) -> None:
        """Bulk insert/replace food interaction records."""
        with self._connect() as conn:
            for row in food_data:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO food_interactions
                        (id, food_name, food_category, drug_id, severity, description, mechanism, evidence_level)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        row["id"],
                        row["food_name"],
                        row["food_category"],
                        row["drug_id"],
                        row["severity"],
                        row["description"],
                        row.get("mechanism"),
                        row.get("evidence_level", "C"),
                    ),
                )

    def get_food_interactions(self, drug_ids: list[str]) -> list[dict]:
        """Return food interactions for the given drug IDs."""
        if not drug_ids:
            return []
        placeholders = ",".join("?" * len(drug_ids))
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM food_interactions WHERE drug_id IN ({placeholders})",  # nosec B608
                drug_ids,
            ).fetchall()
        return [dict(r) for r in rows]

    # -------------------------------------------------------------------------
    # Stats
    # -------------------------------------------------------------------------

    def get_counts(self) -> dict[str, int]:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                    (SELECT COUNT(*) FROM drugs) AS drugs,
                    (SELECT COUNT(*) FROM enzymes) AS enzymes,
                    (SELECT COUNT(*) FROM interactions) AS interactions,
                    (SELECT COUNT(*) FROM drug_enzyme_relations) AS drug_enzyme_relations,
                    (SELECT COUNT(*) FROM adverse_events) AS adverse_events
                """
            ).fetchone()
        return {
            "drugs": row["drugs"],
            "enzymes": row["enzymes"],
            "interactions": row["interactions"],
            "drug_enzyme_relations": row["drug_enzyme_relations"],
            "adverse_events": row["adverse_events"],
        }

    # -------------------------------------------------------------------------
    # Note: upsert_evidence_source and get_evidence_sources are defined above
    # (lines ~393 and ~616) using proper EvidenceSource model objects.
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # Refresh Tokens
    # -------------------------------------------------------------------------

    def store_refresh_token(self, jti: str, user_id: str, expires_at: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO refresh_tokens (jti, user_id, expires_at) VALUES (?, ?, ?)",
                (jti, user_id, expires_at),
            )

    def is_refresh_token_valid(self, jti: str, user_id: str) -> bool:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT expires_at FROM refresh_tokens WHERE jti = ? AND user_id = ?",
                (jti, user_id),
            ).fetchone()
        if not row:
            return False
        return row["expires_at"] > datetime.now(timezone.utc).isoformat()

    def revoke_refresh_token(self, jti: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM refresh_tokens WHERE jti = ?", (jti,))

    def cleanup_expired_tokens(self) -> int:
        with self._connect() as conn:
            now = datetime.now(timezone.utc).isoformat()
            cursor = conn.execute("DELETE FROM refresh_tokens WHERE expires_at < ?", (now,))
            return cursor.rowcount

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

    def _backfill_adverse_event_drugs(self) -> None:
        """Populate adverse_event_drugs from existing adverse_events rows.

        Only runs when the junction table is empty, making it safe to call
        on every startup without duplicating data.

        FK enforcement is disabled during backfill because legacy rows may
        reference drug IDs no longer present in the drugs table.
        """
        with self._connect() as conn:
            count = conn.execute("SELECT COUNT(*) FROM adverse_event_drugs").fetchone()[0]
            if count > 0:
                return
            rows = conn.execute("SELECT id, drug_ids FROM adverse_events").fetchall()
            pairs = []
            for row in rows:
                try:
                    ids = json.loads(row["drug_ids"])
                except (ValueError, TypeError):
                    ids = []
                for did in ids:
                    pairs.append((row["id"], did))
            if pairs:
                conn.execute("PRAGMA foreign_keys=OFF")
                conn.executemany(
                    "INSERT OR IGNORE INTO adverse_event_drugs (event_id, drug_id) VALUES (?, ?)",
                    pairs,
                )
                conn.execute("PRAGMA foreign_keys=ON")

    @staticmethod
    def _row_to_drug(row: sqlite3.Row) -> Drug:
        keys = row.keys()
        return Drug(
            id=row["id"],
            name=row["name"],
            brand_names=json.loads(row["brand_names"]),
            description=row["description"] or "",
            drug_class=row["drug_class"],
            rxnorm_cui=row["rxnorm_cui"],
            category=row["category"] if "category" in keys else "prescription",
            last_updated=row["last_updated"] if "last_updated" in keys else None,
            atc_code=row["atc_code"] if "atc_code" in keys else None,
        )

    @staticmethod
    def _row_to_interaction(row: sqlite3.Row) -> Interaction:
        keys = row.keys()
        return Interaction(
            id=row["id"],
            drug_a_id=row["drug_a_id"],
            drug_b_id=row["drug_b_id"],
            severity=row["severity"],
            description=row["description"] or "",
            mechanism=row["mechanism"],
            source=row["source"],
            evidence_count=row["evidence_count"],
            evidence_level=row["evidence_level"] if "evidence_level" in keys else "D",
            source_citation=row["source_citation"] if "source_citation" in keys else None,
            last_updated=row["last_updated"] if "last_updated" in keys else None,
            clinical_significance=row["clinical_significance"]
            if "clinical_significance" in keys
            else None,
        )
