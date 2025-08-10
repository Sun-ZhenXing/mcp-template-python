ARG PYPI_MIRROR_URL=https://pypi.org/simple
ARG DEBIAN_MIRROR=ftp.cn.debian.org

# Base stage
FROM python:3.12-bookworm AS deps
ARG DEBIAN_FRONTEND=noninteractive
ARG PYPI_MIRROR_URL
WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

ENV UV_DEFAULT_INDEX=${PYPI_MIRROR_URL}

# Install dependencies
RUN pip -V && \
    pip config set global.index-url ${PYPI_MIRROR_URL} && \
    pip install --no-cache-dir uv

# Sync dependencies
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache,sharing=locked \
    uv sync --no-dev --no-install-project

# Runner stage
FROM python:3.12-slim-bookworm AS runner
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBIAN_MIRROR
ARG PYPI_MIRROR_URL

# rootless user args
ARG APP_USER=app
ARG APP_UID=1000
ARG APP_GID=1000
WORKDIR /app

RUN sed -i "s/deb.debian.org/${DEBIAN_MIRROR}/g" /etc/apt/sources.list.d/debian.sources && \
    apt update && \
    apt install -y --no-install-recommends \
    curl
RUN apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip -V && \
    pip config set global.index-url ${PYPI_MIRROR_URL} && \
    pip install --no-cache-dir uv

# Create non-root user/group for rootless execution
RUN groupadd -g ${APP_GID} ${APP_USER} && \
    useradd -m -u ${APP_UID} -g ${APP_GID} -s /bin/bash ${APP_USER}

# Copy venv and sources with proper ownership
COPY --from=deps --chown=${APP_UID}:${APP_GID} /app/.venv/ ./.venv/
COPY --chown=${APP_UID}:${APP_GID} . ./

# Ensure dependencies sync
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache,sharing=locked \
    uv sync --no-dev && \
    chown -R ${APP_UID}:${APP_GID} /app

# Environment for venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

ARG PORT=3001
ENV PORT=${PORT}

# Switch to non-root user
USER ${APP_UID}:${APP_GID}

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}
CMD ["sh", "-c", "uv run --no-sync prod --host 0.0.0.0 --port ${PORT}"]
