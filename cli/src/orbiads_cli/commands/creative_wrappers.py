"""CreativeWrapper CRUD/actions CLI (Story 76.1)."""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render_detail

app = typer.Typer(help="Manage GAM CreativeWrappers", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return _json.load(fh)
    except _json.JSONDecodeError as exc:
        typer.echo(f"Error: invalid JSON in {path}: {exc}", err=True)
        raise typer.Exit(code=2) from exc


@app.command("list")
def list_wrappers(
    ctx: typer.Context,
    label_id: int | None = typer.Option(
        None,
        "--label-id",
        min=1,
        help="Filter by CreativeWrapper label ID",
    ),
    status: str | None = typer.Option(None, "--status", help="ACTIVE or INACTIVE"),
    limit: int = typer.Option(100, "--limit", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List CreativeWrappers."""
    params: dict[str, str | int] = {"limit": limit, "offset": offset}
    if label_id is not None:
        params["labelId"] = label_id
    if status:
        params["status"] = status
    try:
        data = get_client().get("/api/gam/creative-wrappers", params=params)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("get")
def get_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Get a CreativeWrapper by ID."""
    try:
        data = get_client().get(f"/api/gam/creative-wrappers/{wrapper_id}")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("create")
def create_wrapper(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON payload file"),
):
    """Create a CreativeWrapper from a JSON payload."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-wrappers", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("update")
def update_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON payload file"),
):
    """Update a CreativeWrapper from a JSON payload."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/creative-wrappers/{wrapper_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("activate")
def activate_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Activate a CreativeWrapper."""
    try:
        data = get_client().post(f"/api/gam/creative-wrappers/{wrapper_id}/activate")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("deactivate")
def deactivate_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Deactivate a CreativeWrapper."""
    try:
        data = get_client().post(f"/api/gam/creative-wrappers/{wrapper_id}/deactivate")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)
