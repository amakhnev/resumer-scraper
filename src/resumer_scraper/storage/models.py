from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from resumer_scraper.config import settings
from resumer_scraper.storage.base import Base

SCHEMA = settings.db_schema


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_url_normalized: Mapped[str] = mapped_column(String(2048), unique=True, nullable=False, index=True)
    external_url_raw: Mapped[str | None] = mapped_column(String(2048))
    title: Mapped[str | None] = mapped_column(String(512))
    employer_name: Mapped[str | None] = mapped_column(String(255))
    recruiter_name: Mapped[str | None] = mapped_column(String(255))
    country_code: Mapped[str | None] = mapped_column(String(8))
    city: Mapped[str | None] = mapped_column(String(128))
    location_text: Mapped[str | None] = mapped_column(String(512))
    work_mode: Mapped[str | None] = mapped_column(String(64))
    ir35_status: Mapped[str | None] = mapped_column(String(64))
    rate_min: Mapped[float | None] = mapped_column(Numeric(12, 2))
    rate_max: Mapped[float | None] = mapped_column(Numeric(12, 2))
    rate_unit: Mapped[str | None] = mapped_column(String(32))
    currency: Mapped[str | None] = mapped_column(String(8))
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    description_raw: Mapped[str | None] = mapped_column(Text)
    description_clean: Mapped[str | None] = mapped_column(Text)
    source_quality: Mapped[float | None] = mapped_column(Float)
    parser_confidence: Mapped[float | None] = mapped_column(Float)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(64), default="active", nullable=False)
    content_hash: Mapped[str | None] = mapped_column(String(128))


class JobOccurrence(Base):
    __tablename__ = "job_occurrences"
    __table_args__ = (UniqueConstraint("source_name", "source_listing_url", name="uq_source_occurrence"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(128), nullable=False)
    source_listing_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    source_provider: Mapped[str | None] = mapped_column(String(255))
    job_id: Mapped[int | None] = mapped_column(ForeignKey(f"{SCHEMA}.jobs.id"))
    source_job_id: Mapped[str | None] = mapped_column(String(255))
    source_posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    crawl_run_id: Mapped[str | None] = mapped_column(String(255))
    resolution_state: Mapped[str] = mapped_column(String(64), default="resolved", nullable=False)
    metadata_json: Mapped[dict | None] = mapped_column(JSON)


class RawPayload(Base):
    __tablename__ = "raw_payloads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_occurrence_id: Mapped[int] = mapped_column(
        ForeignKey(f"{SCHEMA}.job_occurrences.id"), nullable=False, index=True
    )
    payload_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict | None] = mapped_column(JSON)
    payload_text: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class CrawlState(Base):
    __tablename__ = "crawl_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    last_successful_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    stop_markers: Mapped[dict | None] = mapped_column(JSON)
    seen_markers: Mapped[dict | None] = mapped_column(JSON)
    next_page_cursor: Mapped[str | None] = mapped_column(String(255))
    hard_stop_counter: Mapped[int | None] = mapped_column(Integer)
    resume_token: Mapped[str | None] = mapped_column(String(255))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class QuotaState(Base):
    __tablename__ = "quota_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    requests_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    jobs_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    cycle_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cycle_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    accrued_daily_tokens: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    last_reset_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


class JobEnrichment(Base):
    __tablename__ = "job_enrichments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(ForeignKey(f"{SCHEMA}.jobs.id"), nullable=False, index=True)
    normalized_skills: Mapped[list | None] = mapped_column(JSON)
    category_labels: Mapped[list | None] = mapped_column(JSON)
    contract_length: Mapped[str | None] = mapped_column(String(128))
    tool_stack: Mapped[list | None] = mapped_column(JSON)
    sectors: Mapped[list | None] = mapped_column(JSON)
    extraction_payload: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
