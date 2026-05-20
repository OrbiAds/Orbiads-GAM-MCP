"""Manage GAM NativeStyles — Story 62.1.

Wraps the 5 NativeStyle Tier B routes added in
``backend/src/api/routes/gam/creatives_native_styles.py``.
"""

from __future__ import annotations

import json as _json
import os
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM NativeStyles", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "size", "creativeTemplateId"]


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command("list")
def list_styles(
    ctx: typer.Context,
    name_filter: Optional[str] = typer.Option(
        None, "--name-filter", help="Filter by name substring"
    ),
    limit: int = typer.Option(500, "--limit", "-l", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List active NativeStyles in the network."""
    try:
        params: dict = {"limit": limit, "offset": offset}
        if name_filter:
            params["nameFilter"] = name_filter
        data = get_client().get("/api/gam/native-styles", params=params)
        if isinstance(data, dict):
            items = data.get("items", data.get("nativeStyles", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    style_id: str = typer.Argument(..., help="NativeStyle ID"),
):
    """Fetch a single NativeStyle by ID."""
    try:
        data = get_client().get(f"/api/gam/native-styles/{style_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def update(
    ctx: typer.Context,
    style_id: str = typer.Argument(..., help="NativeStyle ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a NativeStyle (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/native-styles/{style_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def duplicate(
    ctx: typer.Context,
    style_id: str = typer.Argument(..., help="NativeStyle ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Duplicate a NativeStyle."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Duplicate NativeStyle {style_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(f"/api/gam/native-styles/{style_id}/duplicate")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def archive(
    ctx: typer.Context,
    style_id: str = typer.Argument(..., help="NativeStyle ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Archive a NativeStyle."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Archive NativeStyle {style_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/native-styles/{style_id}/archive")
        success(f"NativeStyle {style_id} archived.")
    except CliApiError as e:
        handle_error(e)
