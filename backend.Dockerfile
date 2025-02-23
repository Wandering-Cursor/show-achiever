FROM python:3.13-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apk add --no-cache bash

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

COPY .python-version /app/.python-version
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

RUN --mount=type=ssh uv sync --frozen --no-cache --compile-bytecode --no-dev

COPY --chown=appuser:appuser ./show_achiever /app/show_achiever
# COPY --chown=appuser:appuser ./scripts /app/scripts

RUN mkdir -p -m 0750 media static
RUN uv run --no-dev python /app/show_achiever/manage.py collectstatic --noinput

ENTRYPOINT ["uv", "run", "--no-dev", "fastapi", "run", "show_achiever/main.py"]
