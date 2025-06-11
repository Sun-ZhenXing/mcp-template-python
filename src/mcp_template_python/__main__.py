import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Run a MarkItDown MCP server")

    parser.add_argument(
        "--http",
        action="store_true",
        help="Run the server with Streamable HTTP and SSE transport rather than STDIO (default: False)",
    )
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port to listen on (default: 3001)"
    )
    args = parser.parse_args()

    if not args.http and (args.host or args.port):
        parser.error(
            "Host and port arguments are only valid when using streamable HTTP or SSE transport (see: --http)."
        )
        sys.exit(1)

    if args.http:
        import uvicorn

        from .server import app

        uvicorn.run(
            app,
            host=args.host or "127.0.0.1",
            port=args.port or 3001,
        )
    else:
        from .app.math import mcp

        mcp.run()


if __name__ == "__main__":
    main()
