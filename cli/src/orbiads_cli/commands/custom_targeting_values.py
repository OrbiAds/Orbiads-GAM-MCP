"""Custom-targeting-values CRUD + action — Story 62.5."""

from __future__ import annotations

import json as _json
import os
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, info, render, render_detail

app = typer.Typer(
    help="Manage GAM custom-targeting values (Story 62.5)", no_args_is_help=True
)

_COLUMNS = ["id", "name", "displayName", "matchType"]


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
def values_list(
    ctx: typer.Context,
    key_id: Optional[str] = typer.Option(None, "--key-id", help="Filter by key ID"),
    search: Optional[str] = typer.Option(None, "--search", "-s"),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """List custom-targeting values."""
    params: dict[str, str | int] = {"limit": limit}
    if key_id:
        params["keyId"] = key_id
    if search:
        params["search"] = search
    try:
        data = get_client().get("/api/gam/custom-targeting-values", params=params)
        if isinstance(data, dict):
            items = data.get("values", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create")
def values_create(
    ctx: typer.Context,
    key_id: str = typer.Argument(..., help="Custom-targeting key ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the values array"),
):
    """Create one or more values for a key."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            f"/api/gam/custom-targeting-keys/{key_id}/values", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("update")
def values_update(
    ctx: typer.Context,
    value_id: str = typer.Argument(..., help="Value ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a single custom-targeting value (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/gam/custom-targeting-values/{value_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("action")
def values_action(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with valueIds + action"),
):
    """Perform a bulk action (activate / deactivate / delete) on a set of values."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/custom-targeting-values/action", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
