"""
Shared pytest configuration and fixtures for the MEDGRAPH test suite.

Fixture hierarchy
-----------------
seeded_store  (module scope) — a GraphStore pre-populated with built-in seed
                               data (OpenFDA fetch skipped for speed).
                               Individual test modules may override this with
                               their own module-scoped version when they need
                               an isolated database path.

tmp_store     (function scope) — a blank GraphStore backed by a unique temp
                                 file; used for CRUD unit tests.

Note: test_api.py and test_engine.py each declare their own module-scoped
``seeded_store`` fixture for naming isolation (different tmp dir prefixes).
Those local definitions take precedence over this one within those modules.
New test modules should use the fixture defined here unless isolation is
required.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from medgraph.graph.store import GraphStore


# ---------------------------------------------------------------------------
# Module-scoped seeded store (shared baseline)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def seeded_store(tmp_path_factory) -> GraphStore:
    """
    Module-scoped GraphStore seeded with built-in pharmacological data.

    OpenFDA network fetch is skipped so the suite runs offline and fast.
    The database is created once per test module and reused across all tests
    in that module.
    """
    from medgraph.data.seed import DataSeeder

    tmp_path = tmp_path_factory.mktemp("shared_test")
    store = GraphStore(tmp_path / "shared_test.db")
    seeder = DataSeeder(store=store, skip_openfda=True)
    seeder.run()
    return store


# ---------------------------------------------------------------------------
# Function-scoped blank store (for CRUD / unit tests)
# ---------------------------------------------------------------------------


@pytest.fixture
def tmp_store(tmp_path: Path) -> GraphStore:
    """
    Function-scoped blank GraphStore backed by a temporary file.

    A fresh database is created for every test function that requests this
    fixture, guaranteeing full isolation.
    """
    return GraphStore(tmp_path / "unit_test.db")
