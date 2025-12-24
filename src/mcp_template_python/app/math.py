from operator import add, mul, sub, truediv

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from mcp_template_python.config import settings

mcp = FastMCP(
    "math",
    instructions=settings.mcp.instructions,
    transport_security=TransportSecuritySettings(
        allowed_hosts=settings.cors.allow_hosts.split(","),
        allowed_origins=settings.cors.allow_origins.split(","),
        enable_dns_rebinding_protection=settings.mcp.enable_dns_rebinding_protection,
    ),
)


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
