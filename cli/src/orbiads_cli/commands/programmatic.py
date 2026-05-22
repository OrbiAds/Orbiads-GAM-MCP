"""GAM programmatic commerce: PMP deals, private auctions, and buyers."""

from __future__ import annotations

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(
    help="GAM programmatic surface — PMP deals, private auctions, buyers",
    no_args_is_help=True,
)

deals_app = typer.Typer(help="PMP deals", no_args_is_help=True)
auctions_app = typer.Typer(help="Private auctions", no_args_is_help=True)
buyers_app = typer.Typer(help="Programmatic buyers", no_args_is_help=True)

app.add_typer(deals_app, name="deals")
app.add_typer(auctions_app, name="auctions")
app.add_typer(buyers_app, name="buyers")

_DEAL_LIST_COLUMNS = ["dealId", "displayName", "status", "floorPrice"]
_AUCTION_LIST_COLUMNS = ["privateAuctionId", "displayName", "description"]
_BUYER_LIST_COLUMNS = ["accountId", "displayName", "buyerStatus"]


def _load_json_payload(path: str) -> dict:
    import json as _json
    import os

    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


def _list_params(
    page_size: int,
    page_token: Optional[str],
    filter_expr: Optional[str] = None,
) -> dict:
    params: dict[str, str | int] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    if filter_expr:
        params["filter"] = filter_expr
    return params


def _items(data, *keys: str) -> list:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return value
        fallback = data.get("results")
        return fallback if isinstance(fallback, list) else []
    return data if isinstance(data, list) else []


@deals_app.command("list")
def deals_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
    filter_expr: Optional[str] = typer.Option(
        None, "--filter", help="GAM filter expression"
    ),
):
    """List PMP deals."""
    try:
        data = get_client().get(
            "/api/gam/pmp-deals",
            params=_list_params(page_size, page_token, filter_expr),
        )
        render(
            _items(data, "privateAuctionDeals", "deals"),
            _DEAL_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@deals_app.command("get")
def deals_get(
    ctx: typer.Context,
    deal_id: str = typer.Argument(..., help="Deal ID"),
):
    """Get a PMP deal."""
    try:
        data = get_client().get(f"/api/gam/pmp-deals/{deal_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@deals_app.command("create")
def deals_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON body for the new PMP deal"),
):
    """Create a PMP deal."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/pmp-deals", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@deals_app.command("update")
def deals_update(
    ctx: typer.Context,
    deal_id: str = typer.Argument(..., help="Deal ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON body with PATCH fields"),
):
    """Update a PMP deal."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/pmp-deals/{deal_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("list")
def auctions_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
):
    """List private auctions."""
    try:
        data = get_client().get(
            "/api/gam/private-auctions",
            params=_list_params(page_size, page_token),
        )
        render(
            _items(data, "privateAuctions", "auctions"),
            _AUCTION_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("get")
def auctions_get(
    ctx: typer.Context,
    auction_id: str = typer.Argument(..., help="Private auction ID"),
):
    """Get a private auction."""
    try:
        data = get_client().get(f"/api/gam/private-auctions/{auction_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("create")
def auctions_create(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON body for the new private auction"
    ),
):
    """Create a private auction."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/private-auctions", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("update")
def auctions_update(
    ctx: typer.Context,
    auction_id: str = typer.Argument(..., help="Private auction ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON body with PATCH fields"),
):
    """Update a private auction."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/private-auctions/{auction_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@buyers_app.command("list")
def buyers_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
):
    """List programmatic buyers."""
    try:
        data = get_client().get(
            "/api/gam/programmatic-buyers",
            params=_list_params(page_size, page_token),
        )
        render(
            _items(data, "programmaticBuyers", "buyers"),
            _BUYER_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@buyers_app.command("get")
def buyers_get(
    ctx: typer.Context,
    buyer_id: str = typer.Argument(..., help="Programmatic buyer ID"),
):
    """Get a programmatic buyer."""
    try:
        data = get_client().get(f"/api/gam/programmatic-buyers/{buyer_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
