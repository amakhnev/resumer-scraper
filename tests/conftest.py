"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    return Path(__file__).resolve().parent / "fixtures"


@pytest.fixture(scope="session")
def html_fixtures_dir(fixtures_dir: Path) -> Path:
    return fixtures_dir / "html"


def load_html(html_fixtures_dir: Path, name: str) -> str:
    return (html_fixtures_dir / name).read_text(encoding="utf-8")
