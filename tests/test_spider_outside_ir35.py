"""Smoke tests for Outside IR35 spider (no network)."""

from __future__ import annotations

from scrapy import Request
from scrapy.http import HtmlResponse

from resumer_scraper.spiders.outside_ir35 import OutsideIr35Spider


def test_spider_identity() -> None:
    spider = OutsideIr35Spider()
    assert spider.name == "outside_ir35"
    assert "outsideir35.org.uk" in spider.allowed_domains


def test_parse_returns_iterable(html_fixtures_dir) -> None:
    spider = OutsideIr35Spider()
    body = (html_fixtures_dir / "outside_ir35_jobs_list.html").read_bytes()
    response = HtmlResponse(
        url="https://outsideir35.org.uk/tech-jobs",
        body=body,
        encoding="utf-8",
        request=Request("https://outsideir35.org.uk/tech-jobs"),
    )
    out = list(spider.parse(response))
    assert out == []
