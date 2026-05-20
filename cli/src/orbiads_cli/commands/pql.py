"""GAM PQL query passthrough — Story 62.5."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render_detail

app = typer.Typer(help="Run GAM PQL queries (Story 62.5)", no_args_is_help=True)


@app.command()
def query(
    ctx: typer.Context,
    statement: str = typer.Argument(..., help="PQL SELECT statement"),
):
    """Run a PQL query against GAM and return the rows."""
    try:
        data = get_client().post("/api/gam/pql", json={"query": statement})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
