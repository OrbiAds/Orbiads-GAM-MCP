"""Manage OrbiAds product catalog entries."""

from __future__ import annotations

import json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail

app = typer.Typer(help="Manage product catalog entries", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "status", "deliveryType"]


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except json.JSONDecodeError as exc:
        typer.echo(f"Error: invalid JSON in {path}: {exc}", err=True)
        raise typer.Exit(code=2)
    if not isinstance(payload, dict):
        typer.echo("Error: JSON payload must be an object", err=True)
        raise typer.Exit(code=2)
    return payload


def _confirmation_headers(token: str | None) -> dict[str, str] | None:
    if not token:
        return None
    return {"X-Confirmation-Token": token}


@app.command("list")
def list_products(
    ctx: typer.Context,
    status: str = typer.Option(None, "--status", help="Filter by product status"),
    delivery_type: str = typer.Option(None, "--delivery-type", help="Filter by delivery type"),
):
    """List products."""
    params: dict[str, str] = {}
    if status is not None:
        params["status"] = status
    if delivery_type is not None:
        params["deliveryType"] = delivery_type
    try:
        data = get_client().get("/api/products", params=params)
        out: OutputContext = ctx.obj
        products = data.get("products", data) if isinstance(data, dict) else data
        render(products, _LIST_COLUMNS, out)
    except CliApiError as exc:
        handle_error(exc)


@app.command("get")
def get_product(
    ctx: typer.Context,
    product_id: str = typer.Argument(..., help="Product ID"),
):
    """Get product details."""
    try:
        data = get_client().get(f"/api/products/{product_id}")
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as exc:
        handle_error(exc)


@app.command("create")
def create_product(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the product payload"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Return a CatalogExposurePreview"),
    confirmation_token: str = typer.Option(None, "--confirmation-token", help="Token from a prior dry-run"),
):
    """Create a product."""
    payload = _load_json_payload(file)
    params = {"dryRun": "true"} if dry_run else None
    headers = _confirmation_headers(confirmation_token)
    try:
        data = get_client().post("/api/products", json=payload, params=params, headers=headers)
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as exc:
        handle_error(exc)


@app.command("update")
def update_product(
    ctx: typer.Context,
    product_id: str = typer.Argument(..., help="Product ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Return a CatalogExposurePreview"),
    confirmation_token: str = typer.Option(None, "--confirmation-token", help="Token from a prior dry-run"),
):
    """Update a product."""
    payload = _load_json_payload(file)
    params = {"dryRun": "true"} if dry_run else None
    headers = _confirmation_headers(confirmation_token)
    try:
        data = get_client().patch(
            f"/api/products/{product_id}",
            json=payload,
            params=params,
            headers=headers,
        )
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as exc:
        handle_error(exc)


@app.command("archive")
def archive_product(
    ctx: typer.Context,
    product_id: str = typer.Argument(..., help="Product ID"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Return a CatalogExposurePreview"),
    confirmation_token: str = typer.Option(None, "--confirmation-token", help="Token from a prior dry-run"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Archive a product."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not dry_run and not confirm(f"Archive product {product_id}?", effective_ctx):
        raise typer.Exit(code=0)

    params = {"dryRun": "true"} if dry_run else None
    headers = _confirmation_headers(confirmation_token)
    try:
        data = get_client().post(
            f"/api/products/{product_id}:archive",
            params=params,
            headers=headers,
        )
        render_detail(data, out)
    except CliApiError as exc:
        handle_error(exc)

