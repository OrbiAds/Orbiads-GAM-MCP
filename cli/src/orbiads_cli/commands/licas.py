"""Manage LICAs (line-item creative associations) — Story 62.1.

Wraps the 5 LICA Tier B routes added in
``backend/src/api/routes/gam/creatives_lica.py``.
"""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(
    help="Manage LICAs (line-item creative associations)", no_args_is_help=True
)

_LICA_COLUMNS = ["id", "lineItemId", "creativeId", "status"]


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command("list-by-line-item")
def list_by_line_item(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
):
    """List raw LICA associations for a line item."""
    try:
        data = get_client().get(f"/api/gam/line-items/{line_item_id}/licas")
        if isinstance(data, dict):
            items = data.get("licas", data.get("items", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LICA_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def batch(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with {lineItemIds: [...]} body"
    ),
):
    """Fetch LICAs for multiple line items in one batch call."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/licas/batch", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def update(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
    creative_id: str = typer.Argument(..., help="Creative ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a LICA (rotation weight, schedule, sizes, status)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/gam/licas/{line_item_id}/{creative_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def deactivate(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
    creative_id: str = typer.Argument(..., help="Creative ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Deactivate a single LICA (creative stops serving on this line item)."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(
        f"Deactivate LICA li={line_item_id} cr={creative_id}?", effective_ctx
    ):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/licas/{line_item_id}/{creative_id}/deactivate")
        success(f"LICA li={line_item_id} cr={creative_id} deactivated.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def delete(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the delete payload"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Detach multiple creatives from a line item in one call (REVERSIBLE).

    The association is set to INACTIVE; GAM exposes no hard-delete for a LICA.
    """
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm("Delete (deactivate) the LICAs in this payload?", effective_ctx):
        raise typer.Exit(code=0)
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/licas/delete", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
