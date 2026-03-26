"""Tests for database configuration module."""

from __future__ import annotations

import os
import pytest
from pathlib import Path

from medgraph.graph.db_config import get_db_config, DatabaseConfig


class TestDatabaseConfig:
    def test_default_sqlite(self, monkeypatch):
        """No DATABASE_URL → SQLite at default path."""
        monkeypatch.delenv("DATABASE_URL", raising=False)
        config = get_db_config()
        assert config.backend == "sqlite"
        assert config.db_path == Path("data/medgraph.db")
        assert config.is_sqlite is True
        assert config.is_postgresql is False

    def test_empty_url_defaults_sqlite(self, monkeypatch):
        """Empty DATABASE_URL → SQLite default."""
        monkeypatch.setenv("DATABASE_URL", "")
        config = get_db_config()
        assert config.backend == "sqlite"

    def test_sqlite_explicit_path(self, monkeypatch):
        """sqlite:///custom/path.db → SQLite at custom path."""
        monkeypatch.setenv("DATABASE_URL", "sqlite:///tmp/test.db")
        config = get_db_config()
        assert config.backend == "sqlite"
        assert config.db_path == Path("tmp/test.db")

    def test_postgresql_url(self, monkeypatch):
        """postgresql:// URL → PostgreSQL config."""
        monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/db")
        monkeypatch.delenv("DB_POOL_MIN", raising=False)
        monkeypatch.delenv("DB_POOL_MAX", raising=False)
        config = get_db_config()
        assert config.backend == "postgresql"
        assert config.dsn == "postgresql://user:pass@host:5432/db"
        assert config.is_postgresql is True
        assert config.is_sqlite is False
        assert config.pool_min == 2
        assert config.pool_max == 10

    def test_postgres_url_supabase_format(self, monkeypatch):
        """postgres:// (Supabase) → PostgreSQL config."""
        monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@db.supabase.co:5432/postgres")
        config = get_db_config()
        assert config.backend == "postgresql"

    def test_custom_pool_settings(self, monkeypatch):
        """DB_POOL_MIN/MAX env vars override defaults."""
        monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/db")
        monkeypatch.setenv("DB_POOL_MIN", "5")
        monkeypatch.setenv("DB_POOL_MAX", "20")
        config = get_db_config()
        assert config.pool_min == 5
        assert config.pool_max == 20

    def test_unsupported_scheme_raises(self, monkeypatch):
        """Unsupported URL scheme → ValueError."""
        monkeypatch.setenv("DATABASE_URL", "mysql://localhost/db")
        with pytest.raises(ValueError, match="Unsupported DATABASE_URL"):
            get_db_config()

    def test_config_is_frozen(self):
        """DatabaseConfig should be immutable."""
        config = DatabaseConfig(backend="sqlite", db_path=Path("test.db"))
        with pytest.raises(AttributeError):
            config.backend = "postgresql"
