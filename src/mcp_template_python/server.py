import contextlib

from fastapi import FastAPI

from .config import MCP_MAP


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        for mcp in MCP_MAP.values():
            await stack.enter_async_context(mcp.session_manager.run())
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to the MCP Template Python Server!"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


for name, mcp in MCP_MAP.items():
    app.mount(f"/{name}/compatible", mcp.sse_app())
    app.mount(f"/{name}", mcp.streamable_http_app())
