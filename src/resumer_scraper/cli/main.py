import subprocess
import sys

import typer

app = typer.Typer(help="resumer-scraper CLI")


def _run_checked(command: list[str], error_message: str) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        typer.echo(error_message, err=True)
        raise typer.Exit(code=1)


@app.command()
def run(source: str) -> None:
    """
    Run one source spider.
    """
    _run_checked([sys.executable, "-m", "scrapy", "crawl", source], f"Spider failed: {source}")


if __name__ == "__main__":
    app()
