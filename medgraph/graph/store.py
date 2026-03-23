"""
SQLite-backed storage for MEDGRAPH knowledge graph data.

Uses synchronous sqlite3 with context manager pattern. DB file at data/medgraph.db.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from medgraph.graph.models import (
    AdverseEvent,
    Drug,
    DrugEnzymeRelation,
    Enzyme,
    EvidenceSource,
    GeneticGuideline,
    Interaction,
)

# Default DB path — relative to project root
DEFAULT_DB_PATH = Path("data/medgraph.db")


class GraphStore:
    """
    Persistent storage for drug interaction graph data.

    Wraps SQLite with typed upsert/query methods for all entity types.
    DB is initialized (tables + indexes created) on first use.
    """

    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
        self._ensure_schema_metadata()

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager providing a SQLite connection with row_factory set."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

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

                CREATE TABLE IF NOT EXISTS genetic_guidelines (
                    drug_id              TEXT NOT NULL,
                    gene_id              TEXT NOT NULL,
                    phenotype            TEXT NOT NULL,
                    recommendation       TEXT NOT NULL DEFAULT '',
                    severity_multiplier  REAL NOT NULL DEFAULT 1.0,
                    PRIMARY KEY (drug_id, gene_id, phenotype)
                );

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
            """)

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
            total = conn.execute(f"SELECT COUNT(*) FROM drugs {where}", (pattern,)).fetchone()[0]
            rows = conn.execute(
                f"SELECT * FROM drugs {where} LIMIT ? OFFSET ?",
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
                """,
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
        # Pre-filter with LIKE to avoid full table scan, then verify in Python
        like_clauses = " OR ".join(["drug_ids LIKE ?"] * len(drug_ids))
        like_params = [f"%{did}%" for did in drug_ids]
        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT * FROM adverse_events WHERE {like_clauses}", like_params
            ).fetchall()
        drug_set = set(drug_ids)
        results = []
        for row in rows:
            ids = json.loads(row["drug_ids"])
            if drug_set.intersection(ids):
                results.append(
                    AdverseEvent(
                        id=row["id"],
                        drug_ids=ids,
                        reaction=row["reaction"],
                        count=row["count"],
                        seriousness=row["seriousness"],
                        source_url=row["source_url"],
                    )
                )
        return results

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
                f"SELECT * FROM audit_log {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
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
    # Stats
    # -------------------------------------------------------------------------

    def get_counts(self) -> dict[str, int]:
        with self._connect() as conn:
            return {
                "drugs": conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0],
                "enzymes": conn.execute("SELECT COUNT(*) FROM enzymes").fetchone()[0],
                "interactions": conn.execute("SELECT COUNT(*) FROM interactions").fetchone()[0],
                "drug_enzyme_relations": conn.execute(
                    "SELECT COUNT(*) FROM drug_enzyme_relations"
                ).fetchone()[0],
                "adverse_events": conn.execute("SELECT COUNT(*) FROM adverse_events").fetchone()[0],
            }

    # -------------------------------------------------------------------------
    # Private helpers
    # -------------------------------------------------------------------------

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
