FROM python:3.13-slim-trixie
ARG PYPI_MIRROR_URL=https://pypi.org/simple
ARG DEBIAN_MIRROR=deb.debian.org
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

COPY . ./

ENV UV_DEFAULT_INDEX=${PYPI_MIRROR_URL}
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
CMD ["sh", "-c", "uv run --no-sync mcp-template-python --host 0.0.0.0 --port ${PORT}"]
