"""Integration tests against Postgres (optional in CI / local without DB)."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine, text


@pytest.mark.integration
def test_database_connects_with_database_url() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL not set; start Postgres and export DATABASE_URL to run integration tests.")

    engine = create_engine(url, pool_pre_ping=True)
    with engine.connect() as conn:
        assert conn.execute(text("SELECT 1")).scalar_one() == 1


@pytest.mark.integration
def test_scraper_schema_exists_when_migrated() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL not set.")

    engine = create_engine(url, pool_pre_ping=True)
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT 1 FROM information_schema.schemata WHERE schema_name = :name LIMIT 1"
            ),
            {"name": "scraper"},
        ).first()
    if row is None:
        pytest.skip("Schema 'scraper' not present; run `uv run python scripts/dev.py db migrate` first.")
    assert row is not None
