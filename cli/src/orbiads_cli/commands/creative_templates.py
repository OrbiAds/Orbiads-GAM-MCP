"""Manage GAM CreativeTemplates — Story 62.1.

Wraps the 3 CreativeTemplate Tier B routes added in
``backend/src/api/routes/gam/creative_templates.py``.
"""

from __future__ import annotations

import json as _json
import os
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(help="Manage GAM CreativeTemplates", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "type", "status"]


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
def list_templates(
    ctx: typer.Context,
    name_filter: Optional[str] = typer.Option(
        None, "--name-filter", help="Filter by name substring"
    ),
    limit: int = typer.Option(500, "--limit", "-l", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List USER_DEFINED CreativeTemplates with full variable metadata."""
    try:
        params: dict = {"limit": limit, "offset": offset}
        if name_filter:
            params["nameFilter"] = name_filter
        data = get_client().get("/api/gam/creative-templates", params=params)
        if isinstance(data, dict):
            items = data.get(
                "items", data.get("creativeTemplates", data.get("results", []))
            )
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="CreativeTemplate ID"),
):
    """Fetch a single CreativeTemplate by ID."""
    try:
        data = get_client().get(f"/api/gam/creative-templates/{template_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("ensure-classic-native")
def ensure_classic_native(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the ensure-template payload"
    ),
):
    """Look up — or register — the Classic Native CreativeTemplate ID."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            "/api/gam/creative-templates/classic-native/ensure", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
