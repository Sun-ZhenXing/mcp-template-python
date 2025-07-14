ARG PYPI_MIRROR_URL=https://pypi.org/simple
ARG DEBIAN_MIRROR=ftp.cn.debian.org

FROM python:3.12-bookworm AS deps
ARG DEBIAN_FRONTEND=noninteractive
ARG PYPI_MIRROR_URL
WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

ENV UV_DEFAULT_INDEX=${PYPI_MIRROR_URL}

# Install dependencies
RUN pip -V && \
    pip config set global.index-url ${PYPI_MIRROR_URL} && \
    pip install uv
RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache,sharing=locked \
    uv sync --no-dev --no-install-project

FROM python:3.12-slim-bookworm AS runner
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBIAN_MIRROR
ARG PYPI_MIRROR_URL
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

COPY --from=deps /app/.venv/ ./.venv/
COPY . ./

RUN --mount=type=cache,target=/root/.cache/uv,id=uv-cache,sharing=locked \
    uv sync --no-dev

ARG PORT=3001
ENV PORT=${PORT}

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

EXPOSE ${PORT}
CMD ["sh", "-c", "uv run --no-sync prod --host 0.0.0.0 --port ${PORT}"]
