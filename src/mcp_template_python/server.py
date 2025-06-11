import contextlib

from fastapi import FastAPI

from .app.math import mcp as math

MCP_MAP = {
    "math": math,
}


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        for mcp in MCP_MAP.values():
            await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)

for name, mcp in MCP_MAP.items():
    app.mount(f"/{name}/compatible", mcp.sse_app())
    app.mount(f"/{name}", mcp.streamable_http_app())
