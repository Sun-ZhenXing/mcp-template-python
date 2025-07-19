from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the MCP template application.
    """

    default_mcp: str = "math"
    default_host: str = "127.0.0.1"
    default_port: int = 3001

    instructions: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="MCP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
