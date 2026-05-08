"""create initial scraper schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-05-08 10:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

SCHEMA = "scraper"


# revision identifiers, used by Alembic.
revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA}"'))

    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("external_url_normalized", sa.String(length=2048), nullable=False),
        sa.Column("external_url_raw", sa.String(length=2048), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=True),
        sa.Column("employer_name", sa.String(length=255), nullable=True),
        sa.Column("recruiter_name", sa.String(length=255), nullable=True),
        sa.Column("country_code", sa.String(length=8), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("location_text", sa.String(length=512), nullable=True),
        sa.Column("work_mode", sa.String(length=64), nullable=True),
        sa.Column("ir35_status", sa.String(length=64), nullable=True),
        sa.Column("rate_min", sa.Numeric(12, 2), nullable=True),
        sa.Column("rate_max", sa.Numeric(12, 2), nullable=True),
        sa.Column("rate_unit", sa.String(length=32), nullable=True),
        sa.Column("currency", sa.String(length=8), nullable=True),
        sa.Column("posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("description_raw", sa.Text(), nullable=True),
        sa.Column("description_clean", sa.Text(), nullable=True),
        sa.Column("source_quality", sa.Float(), nullable=True),
        sa.Column("parser_confidence", sa.Float(), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("content_hash", sa.String(length=128), nullable=True),
        sa.UniqueConstraint("external_url_normalized", name="uq_jobs_external_url_normalized"),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_jobs_external_url_normalized",
        "jobs",
        ["external_url_normalized"],
        unique=True,
        schema=SCHEMA,
    )

    op.create_table(
        "job_occurrences",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(length=128), nullable=False),
        sa.Column("source_listing_url", sa.String(length=2048), nullable=False),
        sa.Column("source_provider", sa.String(length=255), nullable=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey(f"{SCHEMA}.jobs.id"), nullable=True),
        sa.Column("source_job_id", sa.String(length=255), nullable=True),
        sa.Column("source_posted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("crawl_run_id", sa.String(length=255), nullable=True),
        sa.Column("resolution_state", sa.String(length=64), nullable=False),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.UniqueConstraint("source_name", "source_listing_url", name="uq_source_occurrence"),
        schema=SCHEMA,
    )

    op.create_table(
        "raw_payloads",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("job_occurrence_id", sa.Integer(), sa.ForeignKey(f"{SCHEMA}.job_occurrences.id"), nullable=False),
        sa.Column("payload_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("payload_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        schema=SCHEMA,
    )
    op.create_index(
        "ix_raw_payloads_job_occurrence_id",
        "raw_payloads",
        ["job_occurrence_id"],
        unique=False,
        schema=SCHEMA,
    )

    op.create_table(
        "crawl_state",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(length=128), nullable=False),
        sa.Column("last_successful_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("stop_markers", sa.JSON(), nullable=True),
        sa.Column("seen_markers", sa.JSON(), nullable=True),
        sa.Column("next_page_cursor", sa.String(length=255), nullable=True),
        sa.Column("hard_stop_counter", sa.Integer(), nullable=True),
        sa.Column("resume_token", sa.String(length=255), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_name", name="uq_crawl_state_source_name"),
        schema=SCHEMA,
    )

    op.create_table(
        "quota_state",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(length=128), nullable=False),
        sa.Column("requests_used", sa.Integer(), nullable=False),
        sa.Column("jobs_used", sa.Integer(), nullable=False),
        sa.Column("cycle_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cycle_end_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("accrued_daily_tokens", sa.Float(), nullable=False),
        sa.Column("last_reset_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_name", name="uq_quota_state_source_name"),
        schema=SCHEMA,
    )

    op.create_table(
        "job_enrichments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey(f"{SCHEMA}.jobs.id"), nullable=False),
        sa.Column("normalized_skills", sa.JSON(), nullable=True),
        sa.Column("category_labels", sa.JSON(), nullable=True),
        sa.Column("contract_length", sa.String(length=128), nullable=True),
        sa.Column("tool_stack", sa.JSON(), nullable=True),
        sa.Column("sectors", sa.JSON(), nullable=True),
        sa.Column("extraction_payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        schema=SCHEMA,
    )
    op.create_index("ix_job_enrichments_job_id", "job_enrichments", ["job_id"], unique=False, schema=SCHEMA)


def downgrade() -> None:
    op.drop_index("ix_job_enrichments_job_id", table_name="job_enrichments", schema=SCHEMA)
    op.drop_table("job_enrichments", schema=SCHEMA)
    op.drop_table("quota_state", schema=SCHEMA)
    op.drop_table("crawl_state", schema=SCHEMA)
    op.drop_index("ix_raw_payloads_job_occurrence_id", table_name="raw_payloads", schema=SCHEMA)
    op.drop_table("raw_payloads", schema=SCHEMA)
    op.drop_table("job_occurrences", schema=SCHEMA)
    op.drop_index("ix_jobs_external_url_normalized", table_name="jobs", schema=SCHEMA)
    op.drop_table("jobs", schema=SCHEMA)
