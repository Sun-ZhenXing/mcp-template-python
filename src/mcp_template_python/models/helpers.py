from typing import Any, Dict

from pydantic import BaseModel


class ArgumentsRequest(BaseModel):
    """Request model for tool and prompt calls."""

    arguments: Dict[str, Any]
