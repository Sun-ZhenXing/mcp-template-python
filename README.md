# MCP FastAPI Application Template

🌏 [中文](./README.zh.md) | [English](./README.md)

This project provides an MCP application template integrated with FastAPI.

- [x] Support for multiple MCP mounting
- [x] Support for command-line invocation in Stdio mode
- [x] Support for SSE / StreamableHTTP
- [x] Support for packaging and distribution

## Getting Started

Install dependencies:

```bash
uv sync
```

Development:

```bash
uv run dev
```

You can access the example MCP interface (Streamable HTTP) via <http://127.0.0.1:3001/math/mcp>, or access the SSE interface via <http://127.0.0.1:3001/math/compatible/sse>.

Call via command line with `--stdio`:

```bash
uv run prod --stdio
```

## Deployment

Production:

```bash
uv run --no-sync prod
```

Build Python Wheel package:

```bash
uv build
```

## Docker Deployment

Run:

```bash
docker compose up -d
```

Build only:

```bash
docker compose build
```
