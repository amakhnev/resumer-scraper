"""Selector snapshot tests for Outside IR35 list-page contract."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests.conftest import load_html
from tests.support.list_page_selectors import extract_outside_ir35_list


@pytest.fixture
def snapshot_outside_ir35(fixtures_dir: Path) -> dict:
    path = fixtures_dir / "snapshots" / "outside_ir35_jobs_list_selectors.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_outside_ir35_list_selectors_match_snapshot(
    html_fixtures_dir: Path, snapshot_outside_ir35: dict
) -> None:
    html = load_html(html_fixtures_dir, "outside_ir35_jobs_list.html")
    extracted = extract_outside_ir35_list(html)

    assert extracted["non_sponsored_job_hrefs"] == snapshot_outside_ir35["non_sponsored_job_hrefs"]
    assert extracted["load_more_href"] == snapshot_outside_ir35["load_more_href"]
