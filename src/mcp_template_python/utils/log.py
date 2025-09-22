from typing import Any

from rich.console import Console
from rich.logging import RichHandler


class UvicornRichHandler(RichHandler):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            console=Console(stderr=True), rich_tracebacks=True, *args, **kwargs
        )


UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(message)s",
            "use_colors": False,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            "use_colors": False,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "mcp_template_python.utils.log.UvicornRichHandler",
        },
        "access": {
            "formatter": "access",
            "class": "mcp_template_python.utils.log.UvicornRichHandler",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}
