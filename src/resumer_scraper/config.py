from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/resumer_app"
    db_schema: str = "scraper"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        extra="ignore",
    )


settings = AppSettings()
