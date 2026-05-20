"""GAM audience segments — Story 61.7.

Only `list_audience_segments` has a REST endpoint right now (the 4 mutative
audience-segment tools are MCP-ONLY → covered by Epic 62 → 63).
"""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render

app = typer.Typer(help="Manage GAM audience segments (Story 61.7)", no_args_is_help=True)

_AUDIENCE_COLUMNS = ["id", "name", "type", "size"]


@app.command("list")
def audiences_list(ctx: typer.Context):
    """List audience segments."""
    try:
        data = get_client().get("/api/gam/audience-segments")
        if isinstance(data, dict):
            items = data.get("audienceSegments", data.get("segments", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _AUDIENCE_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.5 — get / create / update / action ============================


def _load_json_payload(path: str) -> dict:
    import json as _json, os
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


from orbiads_cli.output import render_detail  # noqa: E402  (lazy import for the new verbs)


@app.command("get")
def audiences_get(
    ctx: typer.Context,
    segment_id: str = typer.Argument(..., help="Audience segment ID"),
):
    """Get an audience segment's details."""
    try:
        data = get_client().get(f"/api/gam/audience-segments/{segment_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create")
def audiences_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the segment body"),
):
    """Create an audience segment."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/audience-segments", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("update")
def audiences_update(
    ctx: typer.Context,
    segment_id: str = typer.Argument(..., help="Audience segment ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update an audience segment (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/gam/audience-segments/{segment_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("action")
def audiences_action(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with segmentIds + action"),
):
    """Perform a bulk action (activate/deactivate/delete) on audience segments."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/audience-segments/action", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
