"""
Alembic migration runner for MEDGRAPH.

Provides programmatic access to run migrations without the alembic CLI.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)

_MIGRATIONS_DIR = Path(__file__).parent


def _make_config(db_path: Path | str | None = None) -> Config:
    """Build Alembic Config pointing at the migrations directory."""
    ini_path = _MIGRATIONS_DIR.parent.parent / "alembic.ini"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(_MIGRATIONS_DIR))

    resolved = str(db_path or os.environ.get("MEDGRAPH_DB_PATH", "data/medgraph.db"))
    cfg.set_main_option("sqlalchemy.url", f"sqlite:///{resolved}")
    return cfg


def upgrade(db_path: Path | str | None = None, revision: str = "head") -> None:
    """Run migrations up to *revision* (default: head)."""
    cfg = _make_config(db_path)
    command.upgrade(cfg, revision)
    logger.info("Database migrated to %s", revision)


def downgrade(db_path: Path | str | None = None, revision: str = "-1") -> None:
    """Downgrade by one revision (or to a specific revision)."""
    cfg = _make_config(db_path)
    command.downgrade(cfg, revision)
    logger.info("Database downgraded to %s", revision)


def current(db_path: Path | str | None = None) -> str | None:
    """Return the current migration revision, or None if not stamped."""
    from alembic.runtime.migration import MigrationContext
    from sqlalchemy import create_engine

    resolved = str(db_path or os.environ.get("MEDGRAPH_DB_PATH", "data/medgraph.db"))
    engine = create_engine(f"sqlite:///{resolved}")
    with engine.connect() as conn:
        ctx = MigrationContext.configure(conn)
        rev = ctx.get_current_revision()
    engine.dispose()
    return rev


def stamp(db_path: Path | str | None = None, revision: str = "head") -> None:
    """Stamp the database with a revision without running migrations."""
    cfg = _make_config(db_path)
    command.stamp(cfg, revision)
    logger.info("Database stamped at %s", revision)
