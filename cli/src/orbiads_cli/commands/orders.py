"""Manage GAM orders."""

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM orders", no_args_is_help=True)


@app.command("list")
def list_orders(
    ctx: typer.Context,
    advertiser_id: Optional[str] = typer.Option(
        None, "--advertiser-id", help="Filter by advertiser ID"
    ),
    query: Optional[str] = typer.Option(None, "--query", "-q", help="Search query"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=200),
    offset: int = typer.Option(0, "--offset", help="Pagination offset", min=0),
):
    """List orders."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        if advertiser_id:
            # Use the advertiser-scoped endpoint
            data = client.get(
                "/api/gam/orders", params={"advertiser_id": advertiser_id}
            )
            # Response is a model with "orders" key
            items = data.get("orders", []) if isinstance(data, dict) else data
        else:
            # Use the paginated endpoint
            params: dict = {"limit": limit, "offset": offset}
            if query:
                params["q"] = query
            data = client.get("/api/gam/orders", params=params)
            # Paginated response may have "orders" or "results" key
            if isinstance(data, dict):
                items = data.get("orders", data.get("results", []))
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
