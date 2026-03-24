"""Explore GAM inventory."""

from __future__ import annotations

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render

app = typer.Typer(help="Explore GAM inventory", no_args_is_help=True)

_AD_UNIT_COLUMNS = ["id", "name", "sizes", "parentPath"]
_PLACEMENT_COLUMNS = ["id", "name", "adUnitCount"]
_KEY_COLUMNS = ["id", "name", "type", "valuesCount"]
_VALUE_COLUMNS = ["id", "name"]


@app.command("ad-units")
def ad_units(
    ctx: typer.Context,
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search by name"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List ad units."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        params: dict[str, str | int] = {"limit": limit}
        if search is not None:
            params["search"] = search
        data = client.get("/api/gam/ad-units", params=params)
        # Response may be a list or a dict with an "adUnits" / "results" key
        if isinstance(data, dict):
            items = data.get("adUnits", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        # Sizes may be a list of objects — join them as strings for display
        for item in items:
            sizes = item.get("sizes")
            if isinstance(sizes, list):
                item["sizes"] = ", ".join(
                    f"{s.get('width', '?')}x{s.get('height', '?')}"
                    if isinstance(s, dict) else str(s)
                    for s in sizes
                )
        render(items, _AD_UNIT_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def placements(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List placements."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        params: dict[str, str | int] = {"limit": limit}
        data = client.get("/api/gam/placements", params=params)
        if isinstance(data, dict):
            items = data.get("placements", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _PLACEMENT_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def keys(
    ctx: typer.Context,
    key_id: Optional[str] = typer.Option(None, "--key-id", help="Targeting key ID"),
    values: bool = typer.Option(False, "--values", help="Show values for key"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List custom targeting keys.

    Without --key-id: lists all targeting keys.
    With --key-id and --values: lists all values for that key.
    """
    out: OutputContext = ctx.obj
    try:
        client = get_client()

        if key_id and values:
            # Fetch values for a specific key
            data = client.get(
                f"/api/gam/targeting-keys/{key_id}/values",
                params={"limit": limit},
            )
            if isinstance(data, dict):
                items = data.get("values", data.get("results", []))
            else:
                items = data if isinstance(data, list) else []
            render(items, _VALUE_COLUMNS, out)
        else:
            # List all targeting keys
            params: dict[str, str | int] = {"limit": limit}
            data = client.get("/api/gam/targeting-keys", params=params)
            if isinstance(data, dict):
                items = data.get("keys", data.get("results", []))
            else:
                items = data if isinstance(data, list) else []
            render(items, _KEY_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)
