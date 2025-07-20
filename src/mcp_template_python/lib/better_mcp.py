import logging
from typing import Literal

from mcp.server.auth.middleware.auth_context import AuthContextMiddleware
from mcp.server.auth.middleware.bearer_auth import (
    BearerAuthBackend,
    RequireAuthMiddleware,
)
from mcp.server.fastmcp import FastMCP
from mcp.server.websocket import websocket_server
from mcp.types import ToolAnnotations
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Mount, Route
from starlette.websockets import WebSocket

from ..config import settings

logger = logging.getLogger(__name__)


class BetterFastMCP(FastMCP):
    def run(
        self,
        transport: Literal["stdio", "sse", "streamable-http", "ws"] = "stdio",
        mount_path: str | None = None,
    ) -> None:
        import anyio

        if transport == "ws":
            anyio.run(self.run_ws_async)
        else:
            super().run(transport=transport, mount_path=mount_path)

    async def run_ws_async(self) -> None:
        """Run the server using WebSocket transport."""
        import uvicorn

        starlette_app = self.ws_app()

        config = uvicorn.Config(
            app=starlette_app,
            host=self.settings.host,
            port=self.settings.port,
            log_level=self.settings.log_level.lower(),
        )
        server = uvicorn.Server(config)
        await server.serve()

    def ws_app(self) -> Starlette:
        """Return an instance of the Websocket server app."""

        async def handle_ws(websocket: WebSocket):
            async with websocket_server(
                websocket.scope, websocket.receive, websocket.send
            ) as (ws_read_stream, ws_write_stream):
                await self._mcp_server.run(
                    ws_read_stream,
                    ws_write_stream,
                    self._mcp_server.create_initialization_options(),
                    raise_exceptions=self.settings.debug,
                )

        # Create routes
        routes: list[Route | Mount] = []
        middleware: list[Middleware] = []
        required_scopes = []

        # Set up auth if configured
        if self.settings.auth:
            required_scopes = self.settings.auth.required_scopes or []

            # Add auth middleware if token verifier is available
            if self._token_verifier:
                middleware = [
                    Middleware(
                        AuthenticationMiddleware,
                        backend=BearerAuthBackend(self._token_verifier),
                    ),
                    Middleware(AuthContextMiddleware),
                ]

            # Add auth endpoints if auth server provider is configured
            if self._auth_server_provider:
                from mcp.server.auth.routes import create_auth_routes

                routes.extend(
                    create_auth_routes(
                        provider=self._auth_server_provider,
                        issuer_url=self.settings.auth.issuer_url,
                        service_documentation_url=self.settings.auth.service_documentation_url,
                        client_registration_options=self.settings.auth.client_registration_options,
                        revocation_options=self.settings.auth.revocation_options,
                    )
                )

        # Set up routes with or without auth
        if self._token_verifier:
            # Determine resource metadata URL
            resource_metadata_url = None
            if self.settings.auth and self.settings.auth.resource_server_url:
                from pydantic import AnyHttpUrl

                resource_metadata_url = AnyHttpUrl(
                    str(self.settings.auth.resource_server_url).rstrip("/")
                    + "/.well-known/oauth-protected-resource"
                )

            routes.append(
                Route(
                    settings.websocket_path,
                    endpoint=RequireAuthMiddleware(
                        handle_ws, required_scopes, resource_metadata_url
                    ),
                )
            )
        else:
            # Auth is disabled, no wrapper needed
            routes.append(
                Route(
                    settings.websocket_path,
                    endpoint=handle_ws,
                )
            )

        # Add protected resource metadata endpoint if configured as RS
        if self.settings.auth and self.settings.auth.resource_server_url:
            from mcp.server.auth.handlers.metadata import (
                ProtectedResourceMetadataHandler,
            )
            from mcp.server.auth.routes import cors_middleware
            from mcp.shared.auth import ProtectedResourceMetadata

            protected_resource_metadata = ProtectedResourceMetadata(
                resource=self.settings.auth.resource_server_url,
                authorization_servers=[self.settings.auth.issuer_url],
                scopes_supported=self.settings.auth.required_scopes,
            )
            routes.append(
                Route(
                    "/.well-known/oauth-protected-resource",
                    endpoint=cors_middleware(
                        ProtectedResourceMetadataHandler(
                            protected_resource_metadata
                        ).handle,
                        ["GET", "OPTIONS"],
                    ),
                    methods=["GET", "OPTIONS"],
                )
            )

        routes.extend(self._custom_starlette_routes)

        return Starlette(
            debug=self.settings.debug,
            routes=routes,
            middleware=middleware,
            lifespan=lambda app: self.session_manager.run(),
        )

    def better_tool(
        self,
        name: str | None = None,
        title: str | None = None,
        description: str | None = None,
        annotations: ToolAnnotations | None = None,
        structured_output: bool | None = None,
    ):
        """Decorator to register a tool.
        TODO: Implement a better tool function decorator.
        """
        # tool_mcp = self._tool_manager._tools
        # existing = tool_mcp.get(name)
        # if existing:
        #     if self._tool_manager.warn_on_duplicate_tools:
        #         logger.warning(f"Tool already exists: {tool.name}")
        #     return existing
        # self._tools[tool.name] = tool
        # return tool
