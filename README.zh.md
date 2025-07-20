# MCP FastAPI 应用模板

🌏 [中文](./README.zh.md) | [English](./README.md)

本项目提供了 FastAPI 集成的 MCP 应用模板。

- [x] 支持多 MCP 挂载
- [x] 支持命令行调用 Stdio 模式
- [x] 支持 SSE / StreamableHTTP / WebSocket 兼容
- [x] 支持打包分发

从 v0.1.2 开始，我们使用 `BetterFastMCP` 替换 `FastMCP`，提供比官方 `FastMCP` 更完善的功能：

- [x] 支持入参为 Pydantic 模型，以便支持更复杂的输入参数类型并方便添加描述
- [x] 支持 WebSocket 作为传输层，通过 `/{mcp_name}/websocket/ws` 访问

## 开始

安装依赖：

```bash
uv sync
```

开发：

```bash
uv run dev
```

可通过 <http://127.0.0.1:3001/math/mcp> 访问示例 MCP 接口（Streamable HTTP），或 <http://127.0.0.1:3001/math/compatible/sse> 访问 SSE 接口。

通过 `--stdio` 来调用命令行：

```bash
uv run prod --stdio
```

## 部署

生产：

```bash
uv run --no-sync prod
```

构建 Python Wheel 包：

```bash
uv build
```

## Docker 部署

运行：

```bash
docker compose up -d
```

仅构建：

```bash
docker compose build
```
