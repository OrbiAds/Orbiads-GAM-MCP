"""Creative QA / compliance scans — Story 62.6 CLI wrapper.

Maps the 7 creative_qa MCP tools onto thin CLI commands under the
`creative-qa` noun. All are read-only validations/scans (no GAM mutations).
"""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render_detail

app = typer.Typer(help="Creative compliance scans (Story 62.6)", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command("scan-compliance")
def scan_compliance(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the creative payload"),
):
    """Scan a creative blob for compliance issues."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-qa/scan-compliance", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("validate-ssl")
def validate_ssl(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
    follow_redirects: bool = typer.Option(False, "--follow-redirects"),
):
    """Validate SSL/HTTPS on a creative's tag URLs."""
    try:
        data = get_client().get(
            f"/api/gam/creative-qa/creatives/{creative_id}/ssl",
            params={"followRedirects": "true" if follow_redirects else "false"},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("validate-ssl-batch")
def validate_ssl_batch(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with creative IDs"),
):
    """Validate SSL on a batch of creatives."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-qa/validate-ssl-batch", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("audit-tracking")
def audit_tracking(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
):
    """Audit a creative's tracking pixels & macros."""
    try:
        data = get_client().get(
            f"/api/gam/creative-qa/creatives/{creative_id}/tracking"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("audit-order-tracking")
def audit_order_tracking(
    ctx: typer.Context,
    order_id: str = typer.Argument(..., help="Order ID"),
):
    """Audit tracking across every line-item creative of an order."""
    try:
        data = get_client().get(f"/api/gam/creative-qa/orders/{order_id}/tracking")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("validate-tag")
def validate_tag(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the tag snippet"),
):
    """Validate a third-party tag snippet for safety/format issues."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-qa/validate-tag", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("pre-archive-check")
def pre_archive_check(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the check payload"),
):
    """Run pre-archive safety checks before retiring a creative."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-qa/pre-archive-check", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
