# ─────────────────────────────────────────
# Builder
# ─────────────────────────────────────────

FROM python:3.14.4-slim-trixie AS builder

# Copy UV binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.12.3 /uv /uvx /bin/

WORKDIR /app

# UV Docker optimizations
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

# Move venv outside the project so that mount `- ../..:/app` doesn't override it
ENV UV_PROJECT_ENVIRONMENT=/opt/venv

# Dependencies layer
COPY pyproject.toml uv.lock ./
# Runtime dependencies only
RUN uv sync --locked --no-install-project --no-dev

# Project layer
COPY . .
RUN uv sync --locked --no-dev --no-editable

# ─────────────────────────────────────────
# Dev
# ─────────────────────────────────────────

FROM builder AS dev

RUN uv sync --locked

RUN useradd --create-home --uid 1000 appuser
RUN chown -R appuser:appuser /app /opt/venv
USER appuser

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

CMD ["bash"]

# ─────────────────────────────────────────
# Runtime
# ─────────────────────────────────────────

FROM python:3.14.4-slim-trixie AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code
COPY . .

RUN useradd --create-home --uid 1000 appuser
RUN chown -R appuser:appuser /app /opt/venv
USER appuser

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]