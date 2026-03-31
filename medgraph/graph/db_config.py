"""
Database configuration for MEDGRAPH.

Reads DATABASE_URL from environment to support both SQLite (default) and PostgreSQL.
Designed for future PostgreSQL migration — currently only SQLite is fully supported.

Usage:
    from medgraph.graph.db_config import get_db_config, DatabaseConfig

    config = get_db_config()
    # config.backend  -> "sqlite" or "postgresql"
    # config.db_path  -> Path for SQLite, or None for PostgreSQL
    # config.dsn      -> Full connection string for PostgreSQL
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection configuration."""

    backend: str  # "sqlite" or "postgresql"
    db_path: Optional[Path] = None  # SQLite file path
    dsn: Optional[str] = None  # PostgreSQL connection string
    pool_min: int = 2
    pool_max: int = 10

    @property
    def is_sqlite(self) -> bool:
        return self.backend == "sqlite"

    @property
    def is_postgresql(self) -> bool:
        return self.backend == "postgresql"


def get_db_config() -> DatabaseConfig:
    """
    Build DatabaseConfig from DATABASE_URL environment variable.

    Supported formats:
        - Not set / empty       -> SQLite at data/medgraph.db
        - sqlite:///path/to.db  -> SQLite at specified path
        - postgresql://...      -> PostgreSQL (future)
        - postgres://...        -> PostgreSQL (Supabase format, future)

    Returns:
        DatabaseConfig with backend type and connection details.
    """
    url = os.environ.get("DATABASE_URL", "").strip()

    if not url or url.startswith("sqlite"):
        # Extract path from sqlite:///path or default
        if url.startswith("sqlite:///"):
            path = Path(url.replace("sqlite:///", ""))
        else:
            path = Path("data/medgraph.db")
        return DatabaseConfig(backend="sqlite", db_path=path)

    if url.startswith(("postgresql://", "postgres://")):
        pool_min = int(os.environ.get("DB_POOL_MIN", "2"))
        pool_max = int(os.environ.get("DB_POOL_MAX", "10"))
        return DatabaseConfig(
            backend="postgresql",
            dsn=url,
            pool_min=pool_min,
            pool_max=pool_max,
        )

    raise ValueError(
        f"Unsupported DATABASE_URL scheme: {url[:20]}... Expected sqlite:/// or postgresql://"
    )
