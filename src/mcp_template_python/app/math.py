from operator import add, mul, sub, truediv

from mcp_template_python.lib.better_mcp import BetterFastMCP

from ..config import settings

mcp = BetterFastMCP("math", settings=settings.instructions)


@mcp.tool()
async def add_num(a: float, b: float) -> float:
    """Adds two numbers."""
    return add(a, b)


@mcp.tool()
async def sub_num(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    return sub(a, b)


@mcp.tool()
async def mul_num(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return mul(a, b)


@mcp.tool()
async def div_num(a: float, b: float) -> float:
    """Divides the first number by the second."""
    return truediv(a, b)
