from pydantic_settings import BaseSettings, SettingsConfigDict


class CORSSettings(BaseSettings):
    """
    Configuration settings for CORS (Cross-Origin Resource Sharing).
    """

    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        extra="ignore",
    )

    allow_hosts: str = "*"
    """CORS allow hosts, defaults to '*'."""

    allow_origins: str = "*"
    """CORS allow origins, defaults to '*'."""

    allow_credentials: bool = True
    """CORS allow credentials, defaults to True."""

    allow_methods: str = "*"
    """CORS allow methods, defaults to '*'."""

    allow_headers: str = "*"
    """CORS allow headers, defaults to '*'."""
