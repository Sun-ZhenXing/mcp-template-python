from pydantic_settings import BaseSettings, SettingsConfigDict


class MCPSettings(BaseSettings):
    """
    Configuration settings for the MCP template application.
    """

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        extra="ignore",
    )

    default_mcp: str = "math"
    """Default MCP to be used by the application."""

    instructions: str | None = None
    """Instructions to be used by the MCP server, defaults to None."""

    enable_helpers_router: bool = True
    """Enable the helpers router for the MCP server."""

    enable_sse: bool = True
    """Enable Server-Sent Events (SSE) for the MCP server."""

    enable_streamable_http: bool = True
    """Enable streamable HTTP for the MCP server."""
