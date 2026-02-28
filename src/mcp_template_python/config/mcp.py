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

    stateless_http: bool = True
    """Whether the MCP server should operate in stateless mode."""

    instructions: str | None = None
    """Instructions to be used by the MCP server, defaults to None."""

    enable_helpers_router: bool = True
    """Enable the helpers router for the MCP server."""

    enable_streamable_http: bool = True
    """Enable streamable HTTP for the MCP server."""

    enable_dns_rebinding_protection: bool = False
    """Enable DNS rebinding protection for MCP server."""
