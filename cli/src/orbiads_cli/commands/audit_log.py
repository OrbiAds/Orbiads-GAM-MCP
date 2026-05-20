"""Tenant audit log — Story 61.7.

Maps `query_audit_log` -> GET /api/settings/audit/.
"""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render

app = typer.Typer(help="Query the tenant audit log (Story 61.7)", no_args_is_help=True)

_COLUMNS = ["timestamp", "actor", "action", "target"]


@app.command("log")
def audit_log(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """Query the audit log."""
    try:
        data = get_client().get("/api/settings/audit/", params={"limit": limit})
        if isinstance(data, dict):
            items = data.get("entries", data.get("results", data.get("logs", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)
