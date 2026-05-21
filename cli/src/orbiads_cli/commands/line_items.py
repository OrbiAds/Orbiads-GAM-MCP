"""Manage GAM line items — Story 61.4 (REST-ONLY sweep).

Maps the 8 REST-ONLY line-item MCP tools onto thin CLI commands:
  - activate_line_items       -> POST /api/gam/jobs/{job_id}/line-items/activate
  - pause_line_items          -> POST /api/gam/jobs/{job_id}/line-items/pause
  - archive_line_item         -> POST /api/gam/jobs/{job_id}/line-items/archive
  - update_line_item          -> POST /api/gam/jobs/{job_id}/line-items/{li}/update
  - duplicate_line_item       -> POST /api/gam/line-items/{li}/duplicate
  - verify_line_item_setup    -> GET  /api/gam/jobs/{job_id}/verify
  - update_line_item_targeting -> PATCH /api/campaigns/{id}/line-items/{li}/targeting

The MCP tools `get_line_item`, `list_line_items_by_order`, `approve_line_item`,
`create_adexchange_line_item`, `create_open_bidding_line_item`,
`create_preferred_deal_line_item`, `list_private_deals` are MCP-ONLY (no REST
route yet) and will land via Epic 62 → 63.
"""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render_detail, success

app = typer.Typer(help="Manage GAM line items (Epic 61.4)", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command()
def activate(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID owning the line items"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Activate all line items for a job."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Activate line items of job {job_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/jobs/{job_id}/line-items/activate")
        success(f"Line items of job {job_id} activated.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def pause(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID owning the line items"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Pause all line items for a job."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Pause line items of job {job_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/jobs/{job_id}/line-items/pause")
        success(f"Line items of job {job_id} paused.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def archive(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID owning the line items"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Archive all line items for a job."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Archive line items of job {job_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/jobs/{job_id}/line-items/archive")
        success(f"Line items of job {job_id} archived.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def lifecycle(
    ctx: typer.Context,
    action: str = typer.Argument(
        ...,
        help="Lifecycle action: activate, pause, resume, approve, archive, unarchive, reserve, release, retire.",
    ),
    ids: str = typer.Option(
        ...,
        "--ids",
        help="Comma-separated GAM Line Item IDs (e.g. '12345,67890'). Direct GAM IDs — no Firestore job_id required.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Run a lifecycle action on Line Items by direct GAM ID (Epic 68 §9).

    Works on Line Items created directly in GAM, bypassing the
    Firestore job model. REST parity for MCP `line_item_lifecycle`.
    """
    out: OutputContext = ctx.obj
    line_item_ids = [s.strip() for s in ids.split(",") if s.strip()]
    if not line_item_ids:
        typer.echo("Error: --ids must contain at least one numeric ID", err=True)
        raise typer.Exit(code=2)

    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(
        f"Run lifecycle action '{action}' on {len(line_item_ids)} line item(s)?",
        effective_ctx,
    ):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(
            "/api/gam/line-items/lifecycle",
            json={"line_item_ids": line_item_ids, "action": action},
        )
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def update(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
    line_item_id: str = typer.Argument(..., help="Line Item ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the update body"),
):
    """Update a single line item under a job context."""
    out: OutputContext = ctx.obj
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            f"/api/gam/jobs/{job_id}/line-items/{line_item_id}/update", json=payload
        )
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def duplicate(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line Item ID to duplicate"),
):
    """Duplicate a line item."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().post(f"/api/gam/line-items/{line_item_id}/duplicate")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def verify(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Verify line-item setup for a job (read-only health check)."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().get(f"/api/gam/jobs/{job_id}/verify")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("update-targeting")
def update_targeting(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    line_item_id: str = typer.Argument(..., help="Line Item ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the targeting patch"),
):
    """Patch the targeting of a line item under a campaign."""
    out: OutputContext = ctx.obj
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/campaigns/{campaign_id}/line-items/{line_item_id}/targeting",
            json=payload,
        )
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


# === Story 62.3 — get / approve / list-by-order / private-deals ============


@app.command()
def get(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
):
    """Get a line item's details."""
    try:
        data = get_client().get(f"/api/gam/line-items/{line_item_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def approve(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Approve a line item (transition draft -> approved in GAM)."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Approve line item {line_item_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/line-items/{line_item_id}/approve")
        success(f"Line item {line_item_id} approved.")
    except CliApiError as e:
        handle_error(e)


@app.command("list-by-order")
def list_by_order(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=200),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List line items for an order."""
    from orbiads_cli.output import render
    try:
        data = get_client().get(
            f"/api/gam/orders/{order_id}/line-items",
            params={"limit": limit, "offset": offset},
        )
        if isinstance(data, dict):
            items = data.get("lineItems", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "status", "type"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("private-deals")
def private_deals(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=200),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List GAM private (programmatic) deals."""
    from orbiads_cli.output import render
    try:
        data = get_client().get(
            "/api/gam/private-deals", params={"limit": limit, "offset": offset}
        )
        if isinstance(data, dict):
            items = data.get("deals", data.get("proposals", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "status", "advertiserId"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.3a — advanced line-item creation (LineItemCreationService unblocked) ===


@app.command("create-adexchange")
def create_adexchange(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON body with orderId/adUnitIds/name + optional overrides"),
):
    """Create an Ad Exchange line item (Story 62.3a)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/line-items/adexchange", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create-open-bidding")
def create_open_bidding(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON body for Open Bidding line item"),
):
    """Create an Open Bidding line item (Story 62.3a)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/line-items/open-bidding", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create-preferred-deal")
def create_preferred_deal(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON body for Preferred Deal line item (must include dealId)"),
):
    """Create a Preferred Deal line item (Story 62.3a)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/line-items/preferred-deal", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
