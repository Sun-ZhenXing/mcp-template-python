import sys

import click

from .__about__ import __module_name__, __version__
from .app import MCP_MAP
from .config import settings


def run_server(
    module: str | None = None,
    host: str = settings.default_host,
    port: int = settings.default_port,
    reload: bool = False,
    **kwargs,
):
    """Run the MCP server in development mode."""
    import uvicorn

    if module is None:
        module = f"{__module_name__}.server:app"

    uvicorn.run(
        module,
        host=host,
        port=port,
        reload=reload,
        log_config=None,
        **kwargs,
    )


@click.command()
@click.option(
    "--stdio",
    is_flag=True,
    help="Run the server with STDIO (default: False)",
)
@click.option(
    "--mcp",
    type=click.Choice(list(MCP_MAP.keys()), case_sensitive=False),
    default=settings.mcp.default_mcp,
    help=f"Select the MCP to run in STDIO mode (default: {settings.mcp.default_mcp})",
)
@click.option(
    "--host",
    default=settings.default_host,
    help=f"Host to bind to (default: {settings.default_host})",
)
@click.option(
    "--port",
    type=int,
    default=settings.default_port,
    help=f"Port to listen on (default: {settings.default_port})",
)
@click.option(
    "--dev",
    is_flag=True,
    help="Run the server in development mode (default: False)",
)
@click.version_option(
    version=__version__,
    prog_name="mcp-template-python",
    help="Show the version of the MCP server",
)
def main(
    stdio: bool,
    mcp: str,
    host: str,
    port: int,
    dev: bool,
):
    """MCP Server"""
    if stdio:
        selected_mcp = MCP_MAP.get(mcp)
        if selected_mcp is None:
            click.echo(f"Error: MCP '{mcp}' not found.", err=True)
            sys.exit(1)
        selected_mcp.run()
    else:
        run_server(
            host=host,
            port=port,
            reload=dev,
        )


@click.command()
def dev():
    """Run the server in development mode."""
    run_server(reload=True)


if __name__ == "__main__":
    main()
