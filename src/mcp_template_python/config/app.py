from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

from mcp_template_python.config.cors import CORSSettings

from .mcp import MCPSettings

load_dotenv()


class AppSettings(BaseSettings):
    """
    Configuration settings for the MCP template application.
    """

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        extra="allow",
    )

    mcp: MCPSettings = MCPSettings()
    """MCP settings, defaults to MCPSettings()."""

    cors: CORSSettings = CORSSettings()
    """CORS settings, defaults to CORSSettings()."""

    title: str = "MCP Template Application"
    """Title of the MCP application, defaults to 'MCP Template Application'."""

    description: str = "A template application for MCP using FastAPI."
    """Description of the MCP application, defaults to 'A template application for MCP using FastAPI.'"""

    default_host: str = "127.0.0.1"
    """Default host for the MCP server, defaults to 127.0.0.1."""

    default_port: int = 3001
    """Default port for the MCP server, defaults to 3001."""

    log_level: str = "INFO"
    """Logging level for the MCP server, defaults to 'info'."""

    rich_console: bool = False
    """Enable rich console output, defaults to False."""


settings = AppSettings()
