import contextlib

from fastapi import FastAPI

from .app import MCP_MAP
from .routers.helpers import router as helpers_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        for mcp in MCP_MAP.values():
            await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome!"}


@app.get("/health")
async def health():
    """Check the health of the server and list available tools."""
    return {
        "status": "healthy",
        "tools": list(MCP_MAP.keys()),
    }


app.include_router(helpers_router)

for name, mcp in MCP_MAP.items():
    app.mount(f"/{name}/compatible", mcp.sse_app())
    app.mount(f"/{name}", mcp.streamable_http_app())
