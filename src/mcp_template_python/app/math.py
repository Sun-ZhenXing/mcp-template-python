from operator import add, mul, sub, truediv

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("math")


@mcp.tool()
async def add_nums(a: float, b: float) -> float:
    """
    Adds two numbers.
    """
    return add(a, b)


@mcp.tool()
async def sub_nums(a: float, b: float) -> float:
    """
    Subtracts the second number from the first.
    """
    return sub(a, b)


@mcp.tool()
async def mul_nums(a: float, b: float) -> float:
    """
    Multiplies two numbers.
    """
    return mul(a, b)


@mcp.tool()
async def div_nums(a: float, b: float) -> float:
    """
    Divides the first number by the second.
    """
    return truediv(a, b)


if __name__ == "__main__":
    mcp.run()
