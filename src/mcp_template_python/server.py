import contextlib

from fastapi import FastAPI

from .__about__ import __version__
from .app import MCP_MAP
from .config import settings
from .routers.helpers import router as helpers_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        for mcp in MCP_MAP.values():
            await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=__version__,
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome!",
        "tools": list(MCP_MAP.keys()),
    }


@app.get("/health")
async def health():
    """Check the health of the server and list available tools."""
    return {
        "status": "healthy",
    }


if settings.enable_helpers_router:
    app.include_router(helpers_router)

for name, mcp in MCP_MAP.items():
    if settings.enable_sse:
        app.mount(f"/{name}/compatible", mcp.sse_app())
    if settings.enable_streamable_http:
        app.mount(f"/{name}", mcp.streamable_http_app())
