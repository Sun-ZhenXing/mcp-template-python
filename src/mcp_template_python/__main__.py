import argparse
import sys

from .__about__ import __module_name__, __version__
from .config import settings


def main():
    from .app import MCP_MAP

    parser = argparse.ArgumentParser(description="MCP Server")

    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run the server with STDIO (default: False)",
    )
    parser.add_argument(
        "--mcp",
        type=str,
        default=settings.default_mcp,
        choices=list(MCP_MAP.keys()),
        help=f"Select the MCP to run in STDIO mode (default: {settings.default_mcp})",
    )
    parser.add_argument(
        "--host",
        default=settings.default_host,
        help=f"Host to bind to (default: {settings.default_host})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.default_port,
        help=f"Port to listen on (default: {settings.default_port})",
    )
    parser.add_argument(
        "--dev",
        default=False,
        action="store_true",
        help="Run the server in development mode (default: False)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show the version of the MCP server",
    )
    args = parser.parse_args()

    if args.dev:
        dev(args.host, args.port)
        sys.exit(0)

    if args.stdio:
        mcp = MCP_MAP.get(args.mcp)
        if mcp is None:
            print(f"Error: MCP '{args.mcp}' not found.")
            sys.exit(1)
        mcp.run()
    else:
        import uvicorn

        from .server import app

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
        )


def dev(
    host: str = settings.default_host,
    port: int = settings.default_port,
):
    """Run the MCP server in development mode."""
    import uvicorn

    uvicorn.run(
        f"{__module_name__}.server:app",
        host=host,
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
