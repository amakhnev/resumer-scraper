from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from resumer_scraper.config import settings


class Base(DeclarativeBase):
    """Base declarative class for ORM models."""

    metadata = MetaData(schema=settings.db_schema)
