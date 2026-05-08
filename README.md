# resumer-scraper

Scrapy-based ingestion platform scaffold with PostgreSQL persistence and Alembic migrations.

## Quick start

1. Copy `.env.example` to `.env` and adjust values if needed.
2. Create/update the project environment with `uv`:
   - `uv sync`
3. Start local development DB:
   - `uv run python scripts/dev.py db up`

4. Run database migrations:
   - `uv run python scripts/dev.py db migrate`
   - or simply `uv run python scripts/dev.py db` (defaults to migrate)

5. Run one source with local Docker bootstrap:
   - `uv run python scripts/dev.py run outside_ir35`

6. Stop local development DB:
   - `uv run python scripts/dev.py db down`

7. Or run the application command directly (no Docker orchestration):
   - `uv run python -m resumer_scraper.cli.main outside_ir35`

`uv` automatically manages an isolated `.venv` for this repository.

The application `run` command performs only:
- Spider run (`python -m scrapy crawl <source>`)

Development-only Docker helper:
- `scripts/dev.py db up|down` manages local Postgres via Compose.
- `scripts/dev.py db migrate` runs Alembic using `DATABASE_URL`.
- `scripts/dev.py run <source>` does `db up`, `db migrate`, then calls the application CLI.
- No Docker checks exist in production application code.

Database URL resolution for dev helpers:
- Uses `DATABASE_URL` from the environment when set.
- If unset, tries to load `DATABASE_URL` from `.env`.

Default database settings:
- Database name: `resumer_app`
- Schema: `scraper`

## Database and migrations

- Migration config: `alembic.ini`
- Migration env: `alembic/env.py`
- Initial schema: `alembic/versions/0001_initial_schema.py`

## Docker

- Compose service: `docker-compose.yml`
- Image build file: `Dockerfile`