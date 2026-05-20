"""GAM users — Story 62.4 (read-only)."""

from __future__ import annotations

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render

app = typer.Typer(help="List GAM users (Story 62.4)", no_args_is_help=True)

_COLUMNS = ["id", "name", "email", "roleId"]


@app.command("list")
def users_list(
    ctx: typer.Context,
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Name filter"),
    limit: int = typer.Option(200, "--limit", "-l", min=1, max=200),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List GAM users."""
    params: dict[str, str | int] = {"limit": limit, "offset": offset}
    if search:
        params["search"] = search
    try:
        data = get_client().get("/api/gam/users", params=params)
        if isinstance(data, dict):
            items = data.get("users", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)
