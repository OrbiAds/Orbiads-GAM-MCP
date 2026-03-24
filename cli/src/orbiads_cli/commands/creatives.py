"""Manage GAM creatives."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, info, render, render_detail, success

app = typer.Typer(help="Manage GAM creatives", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "type", "size", "status"]


@app.command("list")
def list_creatives(
    ctx: typer.Context,
    type_filter: Optional[str] = typer.Option(
        None, "--type", help="Filter by creative type (e.g. image, html5)"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=200),
):
    """List creatives."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        params: dict[str, str | int] = {"limit": limit}
        if type_filter is not None:
            params["type"] = type_filter
        data = client.get("/api/gam/creatives", params=params)
        # Response may be a list or a dict with a "creatives" / "results" key
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
def upload(
    ctx: typer.Context,
    file: Path = typer.Option(
        ..., "--file", exists=True, readable=True, help="File to upload"
    ),
    name: str = typer.Option(..., "--name", help="Creative name"),
    advertiser_id: str = typer.Option(..., "--advertiser-id", help="Advertiser ID"),
    size: str = typer.Option(..., "--size", help="Size WxH e.g. 300x250"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Upload a creative asset.

    Uploads a local file as a new creative in GAM.  This is a write
    operation that consumes credits.
    """
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)

    if not confirm(
        f'Upload creative "{name}" ({size}) for advertiser {advertiser_id}? (costs credits)',
        effective_ctx,
    ):
        raise typer.Exit(code=0)

    try:
        info(f"Uploading {file.name}...")
        client = get_client()
        with open(file, "rb") as f:
            data = client.post(
                "/api/gam/creatives",
                files={"file": (file.name, f)},
                data={
                    "name": name,
                    "advertiserId": advertiser_id,
                    "size": size,
                },
            )
        if out.format == "json":
            render_detail(data, out)
        else:
            creative = data.get("creative", data) if isinstance(data, dict) else data
            creative_id = creative.get("id", "?") if isinstance(creative, dict) else "?"
            success(f"Creative created: {creative_id}")
    except CliApiError as e:
        handle_error(e)
