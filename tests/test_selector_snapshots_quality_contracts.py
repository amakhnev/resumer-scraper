"""Selector snapshot tests for Quality Contracts list-page contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.conftest import load_html
from tests.support.list_page_selectors import extract_quality_contracts_list


@pytest.fixture
def snapshot_quality_contracts(fixtures_dir: Path) -> dict:
    path = fixtures_dir / "snapshots" / "quality_contracts_list_selectors.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_quality_contracts_list_selectors_match_snapshot(
    html_fixtures_dir: Path, snapshot_quality_contracts: dict
) -> None:
    html = load_html(html_fixtures_dir, "quality_contracts_list.html")
    extracted = extract_quality_contracts_list(html)

    assert (
        extracted["contract_detail_hrefs"]
        == snapshot_quality_contracts["contract_detail_hrefs"]
    )
    assert extracted["next_page_href"] == snapshot_quality_contracts["next_page_href"]
