"""Manage GAM creatives."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render, render_detail

app = typer.Typer(help="Manage GAM creatives", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "type", "size", "status"]


@app.command("list")
def list_creatives(
    ctx: typer.Context,
    advertiser_id: str = typer.Option(
        ..., "--advertiser-id", "-a", help="GAM advertiser (company) ID to list creatives for"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=200),
):
    """List creatives for an advertiser.

    Audit F0-3: the previous implementation called the non-existent
    ``/api/gam/creatives`` collection endpoint and always 404'd. The backend
    only exposes creatives scoped to an advertiser, so ``--advertiser-id`` is
    now required.
    """
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get(
            f"/api/gam/advertisers/{advertiser_id}/creatives",
            params={"limit": limit},
        )
        if isinstance(data, dict):
            items = data.get("creatives", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
):
    """Get creative details."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get(f"/api/gam/creatives/{creative_id}")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def upload(ctx: typer.Context):
    """Creative upload is not available via the REST CLI.

    Audit F0-3: the previous implementation POSTed to a non-existent
    ``/api/gam/creatives`` endpoint and always 404'd. GAM v202602 uploads
    creative bytes inline via createCreatives, which the thin REST CLI does
    not surface. Fail fast with guidance instead of a confusing 404.
    """
    typer.echo(
        "Error: creative upload is not supported by the orbiads CLI.\n"
        "Use the MCP tools instead (create_image_creative, "
        "upload_html5_zip_creative, create_video_creative, ...) or deploy "
        "creatives through the campaign pipeline (orbiads campaigns deploy).",
        err=True,
    )
    raise typer.Exit(code=1)
