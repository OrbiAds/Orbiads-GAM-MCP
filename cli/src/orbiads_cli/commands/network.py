"""Manage GAM network context."""

import json as _json
import os

import typer

from orbiads_cli import config
from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail, success

app = typer.Typer(help="Manage GAM network context", no_args_is_help=True)


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
        data = client.get("/api/gam/accessible-networks")
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
        client.post("/api/gam/switch-network", json={"networkCode": network_code})

        # Update local config
        cfg = config.load() or {}
        cfg["networkCode"] = network_code
        config.save(cfg)

        success(f"Switched to network {network_code}")
    except CliApiError as e:
        handle_error(e)


# === Story 62.5 — update ====================================================


@app.command("list-gam")
def list_gam(ctx: typer.Context):
    """List GAM networks and refresh the Firestore network cache."""
    try:
        client = get_client()
        data = client.get("/api/gam/networks")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("config")
def network_config(ctx: typer.Context):
    """Show cached GAM network configuration."""
    try:
        client = get_client()
        data = client.get("/api/gam/network-config")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("init")
def init_network(ctx: typer.Context):
    """Initialize GAM network configuration."""
    try:
        client = get_client()
        data = client.post("/api/gam/network-init")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("gam-info")
def gam_info(ctx: typer.Context):
    """Show GAM network details from the GAM route."""
    try:
        client = get_client()
        data = client.get("/api/gam/network-info")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("test-connection")
def test_connection(ctx: typer.Context):
    """Test the current GAM connection."""
    try:
        client = get_client()
        data = client.post("/api/gam/test-connection")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("parse-ad-tag")
def parse_ad_tag(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help='JSON file body, e.g. {"pastedText": "..."}. Extra keys return HTTP 422.',
    ),
):
    """Parse a GAM ad tag from a StrictPayload body."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/parse-ad-tag", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


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
