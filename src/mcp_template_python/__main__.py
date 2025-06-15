import argparse
import sys

from .__about__ import __module_name__, __version__


def main():
    parser = argparse.ArgumentParser(description="MCP Server")

    parser.add_argument(
        "--stdio",
        action="store_true",
        help="Run the server with STDIO (default: False)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3001,
        help="Port to listen on (default: 3001)",
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
        from .app.math import mcp

        mcp.run()
    else:
        import uvicorn

        from .server import app

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
        )


def dev(host: str = "127.0.0.1", port: int = 3001):
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
