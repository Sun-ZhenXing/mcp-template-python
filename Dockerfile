ARG PYPI_MIRROR_URL=https://pypi.org/simple

FROM python:3.12-bookworm AS deps
ARG PYPI_MIRROR_URL
WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./

ENV UV_DEFAULT_INDEX=${PYPI_MIRROR_URL}

# Install dependencies
RUN pip -V && \
    pip config set global.index-url ${PYPI_MIRROR_URL} && \
    pip install uv
RUN uv sync --no-dev --no-install-project

FROM python:3.12-slim-bookworm
ARG PYPI_MIRROR_URL
WORKDIR /app

RUN pip -V && \
    pip config set global.index-url ${PYPI_MIRROR_URL} && \
    pip install --no-cache-dir uv

COPY --from=deps /app/.venv/ ./.venv/
COPY . ./

EXPOSE 3001
CMD [ "uv", "run", "prod", "--host", "0.0.0.0" ]
