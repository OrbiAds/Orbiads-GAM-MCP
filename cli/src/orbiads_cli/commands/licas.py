"""Manage LICAs (line-item creative associations) — Story 62.1.

Wraps the 5 LICA Tier B routes added in
the server-side LICA API, plus the irreversible `delete-permanent` (Story 116-1).
"""

from __future__ import annotations

import json as _json
import os
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.guarded import run_guarded_post
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(
    help="Manage LICAs (line-item creative associations)", no_args_is_help=True
)

_LICA_COLUMNS = ["id", "lineItemId", "creativeId", "status"]
# A LICA has no scalar id (composite key lineItemId + creativeId): no `id` column.
_LICA_KEY_COLUMNS = ["lineItemId", "creativeId", "status"]


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


def _render_lica_page(data, ctx: typer.Context) -> None:
    items = data.get("licas", data.get("items", [])) if isinstance(data, dict) else data
    render(items if isinstance(items, list) else [], _LICA_KEY_COLUMNS, ctx.obj)
    if isinstance(data, dict) and data.get("hasMore") and ctx.obj.format != "json":
        typer.echo(f"More results: --page-token {data.get('nextPageToken')}", err=True)


@app.command("list-by-creative")
def list_by_creative(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
    status: Optional[str] = typer.Option(None, "--status", help="LICA status: ACTIVE, INACTIVE"),
    page_token: Optional[str] = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page"
    ),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """List the LICAs of a creative: which line items does it run on?"""
    params: dict = {"limit": limit}
    if status is not None:
        params["status"] = status
    if page_token is not None:
        params["page_token"] = page_token
    try:
        data = get_client().get(f"/api/gam/creatives/{creative_id}/licas", params=params)
        _render_lica_page(data, ctx)
    except CliApiError as e:
        handle_error(e)


@app.command("list")
def list_licas(
    ctx: typer.Context,
    line_item_id: Optional[str] = typer.Option(None, "--line-item-id", help="Line item ID"),
    creative_id: Optional[str] = typer.Option(None, "--creative-id", help="Creative ID"),
    status: Optional[str] = typer.Option(None, "--status", help="LICA status: ACTIVE, INACTIVE"),
    since: Optional[str] = typer.Option(
        None,
        "--since",
        help="Modified on/after this ISO 8601 date or date-time (a date alone = 00:00 UTC)",
    ),
    page_token: Optional[str] = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page"
    ),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """List LICAs with typed filters. One of --line-item-id / --creative-id / --since is required
    (an unbounded scan is refused by the server)."""
    params: dict = {"limit": limit}
    for key, value in (
        ("line_item_id", line_item_id),
        ("creative_id", creative_id),
        ("status", status),
        ("since", since),
        ("page_token", page_token),
    ):
        if value is not None:
            params[key] = value
    try:
        data = get_client().get("/api/gam/licas", params=params)
        _render_lica_page(data, ctx)
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

    Each association is set to INACTIVE (it is NOT deleted) and can be
    reactivated. For an irreversible removal use `licas delete-permanent`.
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


@app.command("delete-permanent")
def delete_permanent(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file with {lineItemId, creativeIds: [...]} (max 100 creatives)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Permanently delete LICAs from a line item (IRREVERSIBLE).

    Unlike `licas delete` (which deactivates), the associations are removed
    from GAM and cannot be restored. Only existing associations are deleted;
    the command fails if none of the creatives is associated.
    """
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    payload = _load_json_payload(file)
    # Story 116-10: always two-step (preview -> token); --yes only skips the human prompt.
    try:
        client = get_client()
        data = run_guarded_post(
            lambda body: client.post("/api/gam/licas/delete-permanent", json=body),
            payload,
            ctx=effective_ctx,
            prompt="PERMANENTLY delete these LICAs? This cannot be undone.",
            confirm_fn=confirm,
            two_step=True,
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
