"""Manage GAM orders."""

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.guarded import run_guarded_post
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM orders", no_args_is_help=True)


@app.command("list")
def list_orders(
    ctx: typer.Context,
    advertiser_id: Optional[str] = typer.Option(
        None, "--advertiser-id", help="Filter by advertiser ID"
    ),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    status: Optional[str] = typer.Option(
        None,
        "--status",
        help="OrderStatus filter: DRAFT, PENDING_APPROVAL, APPROVED, DISAPPROVED, PAUSED, CANCELED, DELETED",
    ),
    start_after: Optional[str] = typer.Option(
        None, "--start-after", help="Orders starting on/after this ISO 8601 date or date-time"
    ),
    end_before: Optional[str] = typer.Option(
        None, "--end-before", help="Orders ending on/before this ISO 8601 date or date-time"
    ),
    order_by: Optional[str] = typer.Option(
        None,
        "--order-by",
        help="Sort: '<field> [asc|desc]' (id, name, startDateTime, endDateTime, lastModifiedDateTime)",
    ),
    page_token: Optional[str] = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results (500 with filters)", min=1, max=500),
    offset: int = typer.Option(0, "--offset", help="Pagination offset", min=0),
):
    """List orders (typed filters: status, dates, advertiser; sort and paginate)."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        typed = any(v is not None for v in (status, start_after, end_before, order_by, page_token))
        if typed:
            # Story 117-2 — typed filters, validated server side (INVALID_PARAMETERS lists the
            # valid fields/values). Same route as the legacy list, extra query parameters.
            params: dict = {"limit": limit, "offset": offset}
            for key, value in (
                ("advertiser_id", advertiser_id),
                ("status", status),
                ("start_after", start_after),
                ("end_before", end_before),
                ("order_by", order_by),
                ("page_token", page_token),
            ):
                if value is not None:
                    params[key] = value
            data = client.get("/api/gam/orders", params=params)
            items = data.get("orders", data.get("items", [])) if isinstance(data, dict) else data
            render(items, ["id", "name", "advertiserId", "status"], out)
            if isinstance(data, dict) and data.get("hasMore") and out.format != "json":
                typer.echo(f"More results: --page-token {data.get('nextPageToken')}", err=True)
            return
        if advertiser_id:
            # Use the advertiser-scoped endpoint
            data = client.get(
                "/api/gam/orders", params={"advertiser_id": advertiser_id}
            )
            # Response is a model with "orders" key
            items = data.get("orders", []) if isinstance(data, dict) else data
        else:
            # Use the paginated endpoint
            params = {"limit": limit, "offset": offset}
            if query:
                params["q"] = query
            data = client.get("/api/gam/orders", params=params)
            # Paginated response may have "orders" or "results" key
            if isinstance(data, dict):
                items = data.get("items", data.get("orders", data.get("results", [])))
            else:
                items = data if isinstance(data, list) else []
        render(items, ["id", "name", "advertiserName", "status"], out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
):
    """Get order details."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get(f"/api/gam/orders/{order_id}")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def create(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Order name"),
    advertiser_id: str = typer.Option(..., "--advertiser-id", help="Advertiser ID"),
):
    """Create a new order."""
    out: OutputContext = ctx.obj
    if not confirm(f'Create order "{name}" for advertiser {advertiser_id}?', out):
        raise typer.Exit(code=0)
    try:
        client = get_client()
        data = client.post(
            "/api/gam/orders",
            json={"name": name, "advertiserId": advertiser_id},
        )
        if out.format == "json":
            render_detail(data, out)
        else:
            order = data.get("order", data) if isinstance(data, dict) else data
            order_id = order.get("id", "?") if isinstance(order, dict) else "?"
            success(f"Order created: {order_id}")
    except CliApiError as e:
        handle_error(e)


# === Story 61.7 — approve + delivering filter ==============================


@app.command()
def approve(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Approve an order (Draft -> Approved in GAM)."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Approve order {order_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/orders/{order_id}/approve")
        success(f"Order {order_id} approved.")
    except CliApiError as e:
        handle_error(e)


@app.command("list-delivering")
def list_delivering(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=200),
):
    """List orders currently delivering (filter shorthand)."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().get(
            "/api/gam/orders", params={"limit": limit, "status": "delivering"}
        )
        if isinstance(data, dict):
            items = data.get("orders", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "advertiserId", "status"], out)
    except CliApiError as e:
        handle_error(e)


# === Story 62.4 — archive / update =========================================


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


@app.command()
def archive(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Archive an order."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Archive order {order_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/orders/{order_id}/archive")
        success(f"Order {order_id} archived.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def lifecycle(
    ctx: typer.Context,
    action: str = typer.Argument(
        ...,
        help=(
            "Lifecycle action: approve, approve_without_reservation_changes, archive, "
            "unarchive, pause, resume, retire, disapprove, submit_for_approval, "
            "approve_and_overbook, resume_and_overbook, submit_for_approval_and_overbook, "
            "disapprove_without_reservation_changes, retire_without_reservation_changes, "
            "submit_for_approval_without_reservation_changes, delete."
        ),
    ),
    order_ids: list[str] = typer.Argument(
        ..., help="One or more GAM Order IDs (max 50; direct IDs — no job_id needed)"
    ),
    acknowledge_overbook: bool = typer.Option(
        False,
        "--acknowledge-overbook",
        help="Required for the *_and_overbook actions: inventory is reserved beyond forecast availability.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Run a lifecycle action on one or several Orders by direct GAM ID (Epic 68 §9).

    REST parity for MCP `order_lifecycle`. Covers all 16 OrderAction WSDL
    subtypes: the 9 base transitions, the 3 *_and_overbook variants, the 3
    *_without_reservation_changes variants and `delete` (irreversible: removes
    the order and its line items; GAM refuses if a line item ever served).
    GAM reports one aggregated numChanges, not a per-order outcome.
    """
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    ids_label = ", ".join(order_ids)
    # Story 116-10: delete and *_and_overbook are two-step (preview -> token); the server
    # refuses them otherwise. Reversible actions stay one call, confirmed up front.
    two_step = action == "delete" or action.endswith("_and_overbook")
    prompt = f"Run lifecycle action '{action}' on order(s) {ids_label}?"
    if not two_step and not confirm(prompt, effective_ctx):
        raise typer.Exit(code=0)
    payload: dict = {"order_ids": order_ids, "action": action}
    if acknowledge_overbook:
        payload["acknowledge_overbook"] = True
    try:
        client = get_client()
        data = run_guarded_post(
            lambda body: client.post("/api/gam/orders/lifecycle", json=body),
            payload,
            ctx=effective_ctx,
            prompt=prompt,
            confirm_fn=confirm,
            two_step=two_step,
        )
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def update(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update an order (PATCH). Read-only fields (start/end dates, totals,
    currency) are rejected by the server with 422 VALIDATION_ERROR.
    """
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/orders/{order_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
