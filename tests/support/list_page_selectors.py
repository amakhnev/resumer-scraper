"""
Selector contracts for list pages.

These match the HTML fixtures under tests/fixtures/html/. When live spiders
are implemented, update selectors here and adjust fixtures if the public DOM differs.
"""

from __future__ import annotations

from typing import Any

from parsel import Selector

# Outside IR35 — list / feed (fixture: outside_ir35_jobs_list.html)
OUTSIDE_IR35_JOB_LINK_CSS = "a.job-card:not(.job-card--sponsored)::attr(href)"
OUTSIDE_IR35_LOAD_MORE_CSS = "a.load-more::attr(href)"

# Quality Contracts — today feed (fixture: quality_contracts_list.html)
QUALITY_CONTRACTS_JOB_LINK_CSS = (
    "article.contract-card:not(.contract-card--ad) a.contract-card__link::attr(href)"
)
QUALITY_CONTRACTS_NEXT_CSS = "a.pagination__next::attr(href)"


def extract_outside_ir35_list(response_text: str) -> dict[str, Any]:
    sel = Selector(text=response_text)
    return {
        "non_sponsored_job_hrefs": sel.css(OUTSIDE_IR35_JOB_LINK_CSS).getall(),
        "load_more_href": sel.css(OUTSIDE_IR35_LOAD_MORE_CSS).get(),
    }


def extract_quality_contracts_list(response_text: str) -> dict[str, Any]:
    sel = Selector(text=response_text)
    return {
        "contract_detail_hrefs": sel.css(QUALITY_CONTRACTS_JOB_LINK_CSS).getall(),
        "next_page_href": sel.css(QUALITY_CONTRACTS_NEXT_CSS).get(),
    }
