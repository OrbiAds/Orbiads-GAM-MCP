"""Preview links — Story 61.7.

Maps:
  - get_preview_urls          -> POST /api/preview/share
  - get_campaign_preview_urls -> POST /api/creatives/{job_id}/gam-preview-link
"""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render_detail

app = typer.Typer(help="Generate preview links (Story 61.7)", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


urls_app = typer.Typer(help="Manage saved preview URLs", no_args_is_help=True)
app.add_typer(urls_app, name="urls")


@urls_app.command("get")
def urls_get(
    ctx: typer.Context,
    network_code: str = typer.Option(
        None,
        "--network-code",
        "-n",
        help="GAM network code to scope the library (e.g. 45515589). Defaults to active network.",
    ),
):
    """Get saved preview URLs scoped to a GAM network."""
    kwargs: dict = {}
    if network_code:
        kwargs["params"] = {"networkCode": network_code}
    try:
        data = get_client().get("/api/gam/preview-urls", **kwargs)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@urls_app.command("set")
def urls_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with previewUrls array"),
    network_code: str = typer.Option(
        None,
        "--network-code",
        "-n",
        help="GAM network code to scope the library. Defaults to active network.",
    ),
):
    """Replace saved preview URLs for a GAM network."""
    payload = _load_json_payload(file)
    kwargs: dict = {"json": payload}
    if network_code:
        kwargs["params"] = {"networkCode": network_code}
    try:
        data = get_client().put("/api/gam/preview-urls", **kwargs)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def share(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the preview-share body"),
):
    """Generate a shareable preview token / URL."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/preview/share", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def campaign(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
    file: str = typer.Option(None, "--file", "-f", help="Optional JSON body"),
):
    """Generate GAM preview links for a campaign's creatives."""
    payload = _load_json_payload(file) if file else {}
    try:
        data = get_client().post(
            f"/api/creatives/{job_id}/gam-preview-link", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.5 — coverage =================================================


@app.command()
def coverage(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the coverage request"),
):
    """Check creative coverage across an inventory selection."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/coverage", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
