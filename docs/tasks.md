# resumer-scraper implementation tasks

High-level task list to deliver the PRD. Each item is a self-contained slice with clear scope.

## Overall status

| Metric | Value |
|--------|--------|
| **Last reviewed** | 2026-05-08 |
| **Outstanding tasks** | **6** of 9 not complete (**1** partial) |
| **Blockers** | None identified |

**Summary:** Scaffolding, local dev tooling, Docker Compose, runtime image, core DB tables, Alembic migrations, and a **`tests/`** tree (fixtures, selector snapshots, integration hooks) are in place. Ingest pipeline, real spiders/adapters, enrichment worker, version-history table, and GHCR CI workflows remain.

---

1. **Project scaffolding and developer workflow** — **Done**
   - Set up Python project (`uv`, `pyproject.toml`, `src/` layout) with `spiders/`, `items/`, `loaders/`, `pipelines/`, `services/`, `storage/`, `cli/`, `tests/`.
   - Provide `scripts/dev.py` for local dev (`db up|down|migrate`, `run`).
   - Add `Dockerfile` (runtime-only) and `docker-compose.yml` (local Postgres with healthcheck and named volume).
   - **Tests:** `tests/` with HTML fixtures, JSON selector snapshots (Outside IR35 + Quality Contracts), spider smoke tests, and `@pytest.mark.integration` DB checks (`uv sync --extra dev`, `uv run pytest`).

2. **Persistence layer and migrations** — **Partial**
   - Define SQLAlchemy models for `jobs`, `job_occurrences`, `raw_payloads`, `crawl_state`, `quota_state`, `job_enrichments` (and version history table).
   - Enforce unique indexes on `jobs.external_url_normalized` and `(source_name, source_listing_url)`.
   - Implement Alembic migrations targeting `resumer_app` DB and `scraper` schema.
   - **Outstanding:** `job_description_versions` (or equivalent append-only snapshot table keyed by `job_id` + `content_hash`) in models and migrations.

3. **Shared ingest pipeline** — **Not started**
   - Implement common Item contract and Item Loaders for normalized fields.
   - Build Scrapy item pipeline for: validation, URL canonicalisation, dedupe by `external_url_normalized`, upsert via `ON CONFLICT`, occurrence linkage, raw payload storage.
   - Enforce rule that listings without a resolved external URL stay in `job_occurrences` with `resolution_state = 'pending_external_url'`.

4. **Outside IR35 spider** — **Not started** (scaffold only)
   - Crawl main jobs page, ignore sponsored cards, paginate via `?p=N` Load-more link.
   - Stop on first previously seen non-sponsored URL, end-of-feed, or 1,000-job hard stop.
   - Parse detail pages to extract title, description, skills, location, work type, rate, recruiter, source provider, external Apply URL.

5. **Quality Contracts spider** — **Not started**
   - Consume today-only contract feed, paginate by page number, ignore promo/sign-up blocks.
   - Implement three-marker rolling stop window plus end-of-feed and hard limit.
   - Parse structured detail fields (rate, IR35, working arrangement, city, country, summary, employer description) and treat the source URL as occurrence URL only.

6. **Fantastic.jobs adapter (RapidAPI)** — **Not started**
   - API client with config-driven filters (`country`, `city`, `keyword`, `remote_only`, `results_limit`, `offset`, `request_timeout`).
   - Postgres-persisted quota state with daily token accrual based on remaining requests/jobs and days-to-cycle-end.
   - Budget-aware scheduler that respects monthly budget and per-second burst rate; no naive hourly polling in dev.

7. **Adzuna adapter (metadata-safe by default)** — **Not started**
   - UK search endpoint, sorted by date, one-day age filtering.
   - Persist snippet, `redirect_url`, source metadata, posted time into staging.
   - Redirect-follow / external page fetch path implemented but disabled behind a licensing flag, off by default.

8. **Post-ingest cleaning and enrichment worker** — **Not started**
   - Source-aware cleaning (strip site chrome, sponsored boilerplate, sign-up prompts; preserve responsibilities/requirements/skills/etc).
   - Structured field extraction (work mode, IR35, contract type/duration, rate min/max/unit/currency, parser confidence, description quality).
   - Skills enrichment to a controlled vocabulary; persist enrichments and version history (`content_hash`-keyed snapshots).

9. **Release and CI/CD to GHCR** — **Not started**
   - GitHub Actions workflow on `release.published` building and pushing `latest` + release tag to `ghcr.io/resumer-io/scraper`.
   - Separate `workflow_dispatch` workflow to build and push `dev` on demand.
   - Use `docker/metadata-action`, `GITHUB_TOKEN` auth, and `org.opencontainers.image.source` label on the image.
