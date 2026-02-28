# MCP FastAPI 应用模板

🌏 [中文](./README.zh.md) | [English](./README.md)

本项目提供了 FastAPI 集成的 MCP 应用模板。

- [x] 支持多 MCP 挂载
- [x] 支持命令行调用 Stdio 模式
- [x] 支持 StreamableHTTP
- [x] 支持打包分发

## 开始

安装依赖：

```bash
make
```

开发：

```bash
make dev
```

可通过 <http://127.0.0.1:3001/math/mcp> 访问示例 MCP 接口（Streamable HTTP）。

通过 `--stdio` 来调用命令行：

```bash
make prod -- --stdio
```

## 部署

生产：

```bash
make prod
```

构建 Python Wheel 包：

```bash
make build
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
