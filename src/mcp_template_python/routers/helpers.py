from fastapi import APIRouter

from ..app import MCP_MAP
from ..models.helpers import ArgumentsRequest

router = APIRouter(prefix="/v1", tags=["helpers"])


@router.get("/details")
async def details():
    """Get details about all available tools, prompts, and resources."""
    tools = [
        {
            "name": name,
            "server_name": mcp.name,
            "dependencies": mcp.dependencies,
            "instructions": mcp.instructions,
            "prompts": await mcp.list_prompts(),
            "tools": await mcp.list_tools(),
            "resources": await mcp.list_resources(),
            "resource_templates": await mcp.list_resource_templates(),
        }
        for name, mcp in MCP_MAP.items()
    ]
    return {"tools": tools}


@router.post("/mcps/{mcp_name}/tools/{tool_name}/call")
async def call_tool(
    mcp_name: str,
    tool_name: str,
    request: ArgumentsRequest,
):
    """Call a specific tool with parameters."""
    if mcp_name not in MCP_MAP:
        return {"error": "MCP not found"}

    mcp = MCP_MAP[mcp_name]
    result = await mcp.call_tool(tool_name, request.arguments)
    return result


@router.post("/mcps/{mcp_name}/prompts/{prompt_name}/call")
async def call_prompt(
    mcp_name: str,
    prompt_name: str,
    request: ArgumentsRequest,
):
    """Call a specific prompt with parameters."""
    if mcp_name not in MCP_MAP:
        return {"error": "MCP not found"}

    mcp = MCP_MAP[mcp_name]
    result = await mcp.get_prompt(prompt_name, request.arguments)
    return result


@router.get("/mcps/{mcp_name}/resources/{uri}")
async def get_resource(mcp_name: str, uri: str):
    """Get a specific resource."""
    if mcp_name not in MCP_MAP:
        return {"error": "MCP not found"}

    mcp = MCP_MAP[mcp_name]
    result = await mcp.read_resource(uri)
    return result
