"""Manage GAM advertisers."""

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM advertisers", no_args_is_help=True)


@app.command("list")
def list_advertisers(ctx: typer.Context):
    """List advertisers."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get("/api/gam/advertisers")
        # Response may be a model with "advertisers" key or a list
        if isinstance(data, dict):
            items = data.get("advertisers", data.get("companies", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "type"], out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def create(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Advertiser name"),
):
    """Create a new advertiser."""
    out: OutputContext = ctx.obj
    if not confirm(f'Create advertiser "{name}"?', out):
        raise typer.Exit(code=0)
    try:
        client = get_client()
        data = client.post("/api/gam/advertisers", json={"name": name})
        if out.format == "json":
            render_detail(data, out)
        else:
            adv_id = data.get("id", "?") if isinstance(data, dict) else "?"
            success(f"Advertiser created: {adv_id}")
    except CliApiError as e:
        handle_error(e)
