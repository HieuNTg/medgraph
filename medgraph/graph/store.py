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
        """Create all tables and indexes if they don't exist."""
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS drugs (
                    id          TEXT PRIMARY KEY,
                    name        TEXT NOT NULL,
                    brand_names TEXT NOT NULL DEFAULT '[]',
                    description TEXT NOT NULL DEFAULT '',
                    drug_class  TEXT,
                    rxnorm_cui  TEXT
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
                    id             TEXT PRIMARY KEY,
                    drug_a_id      TEXT NOT NULL,
                    drug_b_id      TEXT NOT NULL,
                    severity       TEXT NOT NULL,
                    description    TEXT NOT NULL DEFAULT '',
                    mechanism      TEXT,
                    source         TEXT NOT NULL DEFAULT 'seed',
                    evidence_count INTEGER NOT NULL DEFAULT 0
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
            """)

    # -------------------------------------------------------------------------
    # Upsert methods
    # -------------------------------------------------------------------------

    def upsert_drug(self, drug: Drug) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO drugs (id, name, brand_names, description, drug_class, rxnorm_cui)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name        = excluded.name,
                    brand_names = excluded.brand_names,
                    description = excluded.description,
                    drug_class  = excluded.drug_class,
                    rxnorm_cui  = excluded.rxnorm_cui
                """,
                (
                    drug.id,
                    drug.name,
                    json.dumps(drug.brand_names),
                    drug.description,
                    drug.drug_class,
                    drug.rxnorm_cui,
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
                    (id, drug_a_id, drug_b_id, severity, description, mechanism, source, evidence_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    severity       = excluded.severity,
                    description    = excluded.description,
                    mechanism      = excluded.mechanism,
                    source         = excluded.source,
                    evidence_count = excluded.evidence_count
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
        return Interaction(
            id=row["id"],
            drug_a_id=row["drug_a_id"],
            drug_b_id=row["drug_b_id"],
            severity=row["severity"],
            description=row["description"],
            mechanism=row["mechanism"],
            source=row["source"],
            evidence_count=row["evidence_count"],
        )

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
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM adverse_events").fetchall()
        results = []
        for row in rows:
            ids = json.loads(row["drug_ids"])
            if any(d in drug_ids for d in ids):
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
        return Drug(
            id=row["id"],
            name=row["name"],
            brand_names=json.loads(row["brand_names"]),
            description=row["description"] or "",
            drug_class=row["drug_class"],
            rxnorm_cui=row["rxnorm_cui"],
        )

    @staticmethod
    def _row_to_interaction(row: sqlite3.Row) -> Interaction:
        return Interaction(
            id=row["id"],
            drug_a_id=row["drug_a_id"],
            drug_b_id=row["drug_b_id"],
            severity=row["severity"],
            description=row["description"] or "",
            mechanism=row["mechanism"],
            source=row["source"],
            evidence_count=row["evidence_count"],
        )
