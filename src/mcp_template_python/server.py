import contextlib

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

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
    title=settings.title,
    description=settings.description,
    version=__version__,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allow_origins.split(","),
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allow_methods.split(","),
    allow_headers=settings.cors.allow_headers.split(","),
)


@app.get("/")
async def root():
    """Root endpoint."""
    return Response("<script>location.href='/docs'</script>")


@app.get("/health")
async def health():
    """Check the health of the server and list available tools."""
    return {
        "status": "healthy",
    }


if settings.mcp.enable_helpers_router:
    app.include_router(helpers_router)

for name, mcp in MCP_MAP.items():
    if settings.mcp.enable_sse:
        app.mount(f"/{name}/compatible", mcp.sse_app())
    if settings.mcp.enable_streamable_http:
        app.mount(f"/{name}", mcp.streamable_http_app())
