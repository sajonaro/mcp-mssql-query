FROM python:3.13-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy project files and install
COPY pyproject.toml uv.lock ./
COPY . .
RUN uv sync --frozen

FROM python:3.13-slim

# Install FreeTDS ODBC driver and dependencies
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    freetds-bin \
    freetds-dev \
    tdsodbc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && odbcinst -i -d -f /usr/share/tdsodbc/odbcinst.ini

# Copy uv from the builder stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy the installed environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --from=builder /app .

# Make sure we use the venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["sleep", "infinity"]
