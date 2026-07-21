# syntax=docker/dockerfile:1

ARG PYTHON_IMAGE=python:3.13.14-slim-bookworm@sha256:fcbd8dfc2605ba7c2eca646846c5e892b2931e41f6227985154a596f26ab8ed7

FROM ${PYTHON_IMAGE} AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.29 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

# Install the locked runtime dependencies in a cacheable layer.
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
      --locked \
      --no-dev \
      --no-install-project \
      --no-editable

# Install the application as a non-editable production package.
COPY src/ ./src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
      --locked \
      --no-dev \
      --no-editable


FROM ${PYTHON_IMAGE} AS runtime

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --system --gid 10001 app && \
    useradd \
      --system \
      --uid 10001 \
      --gid app \
      --home-dir /home/app \
      --create-home \
      app

WORKDIR /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER 10001:10001

EXPOSE 8000

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 CMD ["python", "-c", "import json, sys, urllib.request; response = json.load(urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)); sys.exit(0 if response == {'status': 'ok'} else 1)"]

CMD ["uvicorn", "secure_delivery_lab.main:app", "--host", "0.0.0.0", "--port", "8000"]
