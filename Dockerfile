FROM python:3.12-slim

LABEL org.opencontainers.image.source="https://github.com/resumer-io/scraper"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY scrapy.cfg /app/scrapy.cfg

RUN pip install --no-cache-dir .

CMD ["python", "-m", "resumer_scraper.cli.main", "outside_ir35"]
