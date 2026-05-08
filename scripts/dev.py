import os
import shutil
import subprocess
import sys
from pathlib import Path

import typer

CONTAINER_NAME = "resumer-scraper-db"
SERVICE_NAME = "db"

app = typer.Typer(help="Development helper commands.")
db_app = typer.Typer(help="Local database helpers.")
app.add_typer(db_app, name="db")


def _run_checked(command: list[str], error_message: str) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        typer.echo(error_message, err=True)
        raise typer.Exit(code=1)


def _ensure_docker_available() -> None:
    if not shutil.which("docker"):
        typer.echo("Docker CLI is not installed or not available in PATH.", err=True)
        raise typer.Exit(code=1)

    _run_checked(["docker", "version"], "Docker is unavailable.")


def _load_database_url_from_env_file() -> None:
    if os.environ.get("DATABASE_URL"):
        return

    env_file = Path(".env")
    if not env_file.exists():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "DATABASE_URL" and value.strip():
            os.environ["DATABASE_URL"] = value.strip().strip("\"'")
            return


def _ensure_database_url() -> None:
    _load_database_url_from_env_file()
    if not os.environ.get("DATABASE_URL"):
        typer.echo(
            "DATABASE_URL is required. Set it explicitly or provide it in .env for local development.",
            err=True,
        )
        raise typer.Exit(code=1)


@db_app.callback(invoke_without_command=True)
def db_default(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        db_migrate()


@db_app.command("up")
def db_up() -> None:
    """Start local Postgres service for development."""
    _ensure_docker_available()
    _run_checked(["docker", "compose", "up", "-d", SERVICE_NAME, "--wait"], "Could not start postgres service.")
    typer.echo(f"Database service '{SERVICE_NAME}' is up.")


@db_app.command("down")
def db_down() -> None:
    """Stop local Postgres service for development."""
    _ensure_docker_available()
    _run_checked(["docker", "compose", "stop", SERVICE_NAME], "Could not stop postgres service.")
    typer.echo(f"Database service '{SERVICE_NAME}' is down.")


@db_app.command("migrate")
def db_migrate() -> None:
    """Run Alembic migrations using DATABASE_URL."""
    _ensure_database_url()
    _run_checked([sys.executable, "-m", "alembic", "upgrade", "head"], "Database migration failed.")
    typer.echo("Database migrations applied.")


@app.command()
def run(source: str) -> None:
    """Start local DB, apply migrations, then run one source."""
    db_up()
    db_migrate()
    _run_checked([sys.executable, "-m", "resumer_scraper.cli.main", source], "Application run failed.")


if __name__ == "__main__":
    app()
