"""Manage GAM network context."""

import typer

from orbiads_cli import config
from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail, success

app = typer.Typer(help="Manage GAM network context", no_args_is_help=True)


@app.command()
def info(ctx: typer.Context):
    """Show current network info."""
    try:
        client = get_client()
        data = client.get("/api/auth/gam/connection-state")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("list")
def list_networks(ctx: typer.Context):
    """List accessible GAM networks."""
    try:
        client = get_client()
        data = client.get("/api/auth/gam/pending-networks")
        networks = data.get("networks", []) if isinstance(data, dict) else data
        render(networks, ["networkCode", "displayName"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def switch(
    ctx: typer.Context,
    network_code: str = typer.Option(..., "--network-code", help="GAM network code"),
):
    """Switch active GAM network."""
    try:
        client = get_client()
        client.post("/api/auth/gam/select-network", json={"networkCode": network_code})

        # Update local config
        cfg = config.load() or {}
        cfg["networkCode"] = network_code
        config.save(cfg)

        success(f"Switched to network {network_code}")
    except CliApiError as e:
        handle_error(e)


# === Story 62.5 — update ====================================================


@app.command()
def update(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body (e.g. {\"displayName\": \"...\"})"),
):
    """Update network settings (PATCH /api/gam/network)."""
    import json as _json, os
    if not os.path.isfile(file):
        typer.echo(f"Error: file not found: {file}", err=True)
        raise typer.Exit(code=2)
    try:
        payload = _json.loads(open(file, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {file}: {e}", err=True)
        raise typer.Exit(code=2)
    try:
        data = get_client().patch("/api/gam/network", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
