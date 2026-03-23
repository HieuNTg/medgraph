"""
Tests for Phase 4: Database & Data Scale.

Covers Alembic migrations, schema version tracking, backup/restore,
and data expansion.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from medgraph.graph.store import GraphStore
from medgraph.graph.models import Drug


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.unlink(path)  # Let GraphStore create it
    yield Path(path)
    # Cleanup
    try:
        os.unlink(path)
    except OSError:
        pass


@pytest.fixture
def store(temp_db):
    """Create a GraphStore with a temporary database."""
    return GraphStore(temp_db)


# ---------------------------------------------------------------------------
# Schema version tracking
# ---------------------------------------------------------------------------


class TestSchemaVersion:
    def test_default_version_is_unknown(self, store):
        """New DB without explicit version returns 'unknown'."""
        assert store.get_schema_version() == "unknown"

    def test_set_and_get_version(self, store):
        store.set_schema_version("001")
        assert store.get_schema_version() == "001"

    def test_update_version(self, store):
        store.set_schema_version("001")
        store.set_schema_version("002")
        assert store.get_schema_version() == "002"

    def test_schema_metadata_table_created(self, store):
        """schema_metadata table exists after store init."""
        import sqlite3

        conn = sqlite3.connect(store.db_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_metadata'"
        )
        assert cursor.fetchone() is not None
        conn.close()


# ---------------------------------------------------------------------------
# Backup / Restore
# ---------------------------------------------------------------------------


class TestBackupRestore:
    def test_backup_creates_file(self, store, tmp_path):
        """Backup creates a valid SQLite file."""
        backup_path = tmp_path / "backup.db"
        result = store.backup(backup_path)
        assert result == backup_path
        assert backup_path.exists()
        assert backup_path.stat().st_size > 0

    def test_backup_restore_roundtrip(self, store, tmp_path):
        """Data survives a backup → restore cycle."""
        # Insert test data
        store.upsert_drug(Drug(id="TEST001", name="TestDrug", brand_names=["TestBrand"]))
        assert store.get_drug_by_id("TEST001") is not None

        # Backup
        backup_path = tmp_path / "backup.db"
        store.backup(backup_path)

        # Corrupt the original by creating a fresh empty DB
        os.unlink(store.db_path)
        fresh_store = GraphStore(store.db_path)
        assert fresh_store.get_drug_by_id("TEST001") is None

        # Restore
        fresh_store.restore(backup_path)
        assert fresh_store.get_drug_by_id("TEST001") is not None
        drug = fresh_store.get_drug_by_id("TEST001")
        assert drug.name == "TestDrug"

    def test_restore_nonexistent_file_raises(self, store):
        """Restore from missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            store.restore("/nonexistent/path/backup.db")

    def test_backup_creates_parent_dirs(self, store, tmp_path):
        """Backup creates parent directories if they don't exist."""
        backup_path = tmp_path / "nested" / "dir" / "backup.db"
        result = store.backup(backup_path)
        assert result.exists()


# ---------------------------------------------------------------------------
# Alembic migrations
# ---------------------------------------------------------------------------


class TestAlembicMigrations:
    def test_upgrade_to_head(self, temp_db, monkeypatch):
        """Alembic upgrade to head creates all tables."""
        from medgraph.migrations.runner import upgrade, current

        monkeypatch.setenv("MEDGRAPH_DB_PATH", str(temp_db))
        upgrade(db_path=temp_db)

        rev = current(db_path=temp_db)
        assert rev == "001"

    def test_downgrade_removes_tables(self, temp_db, monkeypatch):
        """Alembic downgrade to base removes all tables."""
        from medgraph.migrations.runner import upgrade, downgrade, current

        monkeypatch.setenv("MEDGRAPH_DB_PATH", str(temp_db))
        upgrade(db_path=temp_db)
        downgrade(db_path=temp_db, revision="base")

        rev = current(db_path=temp_db)
        assert rev is None

    def test_upgrade_downgrade_upgrade_cycle(self, temp_db, monkeypatch):
        """Full upgrade → downgrade → upgrade cycle works."""
        from medgraph.migrations.runner import upgrade, downgrade, current

        monkeypatch.setenv("MEDGRAPH_DB_PATH", str(temp_db))

        upgrade(db_path=temp_db)
        assert current(db_path=temp_db) == "001"

        downgrade(db_path=temp_db, revision="base")
        assert current(db_path=temp_db) is None

        upgrade(db_path=temp_db)
        assert current(db_path=temp_db) == "001"

    def test_stamp_without_running(self, temp_db, monkeypatch):
        """Stamp marks revision without running migration SQL."""
        from medgraph.migrations.runner import stamp, current

        monkeypatch.setenv("MEDGRAPH_DB_PATH", str(temp_db))
        stamp(db_path=temp_db, revision="001")
        assert current(db_path=temp_db) == "001"

    def test_migration_creates_schema_metadata(self, temp_db, monkeypatch):
        """Migration creates schema_metadata table with version."""
        import sqlite3

        from medgraph.migrations.runner import upgrade

        monkeypatch.setenv("MEDGRAPH_DB_PATH", str(temp_db))
        upgrade(db_path=temp_db)

        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT value FROM schema_metadata WHERE key = 'schema_version'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row["value"] == "001"


# ---------------------------------------------------------------------------
# Data expansion
# ---------------------------------------------------------------------------


class TestDataExpansion:
    def test_extended_drugs_importable(self):
        """Extended drug data can be imported without errors."""
        from medgraph.data.seed_drugs_extended import DRUGS_EXTENDED

        assert len(DRUGS_EXTENDED) >= 290

    def test_extended_interactions_importable(self):
        """Extended interactions data can be imported without errors."""
        from medgraph.data.seed_interactions_extended import (
            INTERACTIONS_EXTENDED,
            DRUG_ENZYME_RELATIONS_EXTENDED,
        )

        assert len(INTERACTIONS_EXTENDED) >= 50
        assert len(DRUG_ENZYME_RELATIONS_EXTENDED) >= 100

    def test_no_duplicate_ids_across_datasets(self):
        """No duplicate drug IDs across all seed datasets."""
        from medgraph.data.seed_data import DRUGS
        from medgraph.data.seed_drugs_expanded import DRUGS_EXPANDED
        from medgraph.data.seed_drugs_extended import DRUGS_EXTENDED

        base_ids = {d["id"] for d in DRUGS}
        expanded_ids = {d["id"] for d in DRUGS_EXPANDED}
        extended_ids = {d["id"] for d in DRUGS_EXTENDED}

        # Extended should not overlap with base or expanded
        assert not (extended_ids & base_ids), "Extended overlaps with base"
        assert not (extended_ids & expanded_ids), "Extended overlaps with expanded"

    def test_seed_produces_500_plus_drugs(self, store):
        """Full seed pipeline produces 500+ drugs."""
        from medgraph.data.seed import DataSeeder

        seeder = DataSeeder(store=store)
        counts = seeder.run()
        assert counts["drugs"] >= 500

    def test_all_enzyme_ids_valid(self):
        """All enzyme relations reference valid enzyme IDs."""
        from medgraph.data.seed_data import ENZYMES
        from medgraph.data.seed_interactions_extended import DRUG_ENZYME_RELATIONS_EXTENDED

        valid_ids = {e["id"] for e in ENZYMES}
        for rel in DRUG_ENZYME_RELATIONS_EXTENDED:
            assert rel["enzyme_id"] in valid_ids, (
                f"Invalid enzyme_id: {rel['enzyme_id']} for drug {rel['drug_id']}"
            )


# ---------------------------------------------------------------------------
# Health endpoint with schema version
# ---------------------------------------------------------------------------


class TestHealthSchemaVersion:
    def test_health_response_includes_schema_version(self):
        """HealthResponse model includes schema_version field."""
        from medgraph.api.models import HealthResponse

        resp = HealthResponse(status="ok", db_size=100, graph_nodes=50, schema_version="001")
        assert resp.schema_version == "001"

    def test_health_response_default_schema_version(self):
        """HealthResponse defaults to 'unknown' for schema_version."""
        from medgraph.api.models import HealthResponse

        resp = HealthResponse(status="ok", db_size=100, graph_nodes=50)
        assert resp.schema_version == "unknown"
