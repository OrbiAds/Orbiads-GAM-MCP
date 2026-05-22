"""GAM features probe commands."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import info, render_detail

app = typer.Typer(help="GAM features probe", no_args_is_help=True)


@app.command("list")
def features_list(ctx: typer.Context):
    """Show the cached GAM features probe for the active tenant."""
    try:
        data = get_client().get("/api/gam/features")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("probe")
def features_probe(ctx: typer.Context):
    """Force a fresh GAM features probe."""
    info("Probing GAM network features (this can take a few seconds)...")
    try:
        data = get_client().post("/api/gam/features:probe")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
