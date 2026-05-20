"""GAM roles — Story 62.4 (read-only)."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render

app = typer.Typer(help="List GAM roles (Story 62.4)", no_args_is_help=True)

_COLUMNS = ["id", "name", "description"]


@app.command("list")
def roles_list(ctx: typer.Context):
    """List GAM roles."""
    try:
        data = get_client().get("/api/gam/roles")
        if isinstance(data, dict):
            items = data.get("roles", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)
