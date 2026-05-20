"""GAM contacts (advertiser/agency people) — Story 62.4."""

from __future__ import annotations

import json as _json
import os
from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render, render_detail

app = typer.Typer(help="Manage GAM contacts (Story 62.4)", no_args_is_help=True)

_COLUMNS = ["id", "name", "email", "companyId"]


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
def contacts_list(
    ctx: typer.Context,
    company_id: Optional[str] = typer.Option(
        None, "--company-id", help="Filter by GAM Company/Advertiser ID"
    ),
):
    """List GAM contacts (optionally filtered by company)."""
    params: dict[str, str] = {}
    if company_id:
        params["companyId"] = company_id
    try:
        data = get_client().get("/api/gam/contacts", params=params)
        if isinstance(data, dict):
            items = data.get("contacts", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create")
def contacts_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the contact body"),
):
    """Create a GAM contact. Body must include name, email, companyId."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/contacts", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("update")
def contacts_update(
    ctx: typer.Context,
    contact_id: str = typer.Argument(..., help="Contact ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a GAM contact (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/contacts/{contact_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
