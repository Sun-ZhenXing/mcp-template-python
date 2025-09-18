from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """
    Configuration settings for the MCP template application.
    """

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        extra="allow",
    )

    app_title: str = "MCP Template Application"
    """Title of the MCP application, defaults to 'MCP Template Application'."""

    app_description: str = "A template application for MCP using FastAPI."
    """Description of the MCP application, defaults to 'A template application for MCP using FastAPI.'"""

    default_mcp: str = "math"
    """Default MCP to be used by the application."""

    default_host: str = "127.0.0.1"
    """Default host for the MCP server, defaults to 127.0.0.1."""

    default_port: int = 3001
    """Default port for the MCP server, defaults to 3001."""

    instructions: str | None = None
    """Instructions to be used by the MCP server, defaults to None."""

    enable_helpers_router: bool = True
    """Enable the helpers router for the MCP server."""

    enable_sse: bool = True
    """Enable Server-Sent Events (SSE) for the MCP server."""

    enable_streamable_http: bool = True
    """Enable streamable HTTP for the MCP server."""

    websocket_path: str = "/ws"
    """Path for the WebSocket endpoint."""


settings = Settings()
