from pydantic_settings import BaseSettings

from .app.math import mcp as math

MCP_MAP = {
    "math": math,
}


class Settings(BaseSettings):
    """
    Configuration settings for the MCP template application.
    """

    default_mcp: str = "math"
    default_host: str = "127.0.0.1"
    default_port: int = 3001

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
