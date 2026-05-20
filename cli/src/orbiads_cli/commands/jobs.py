"""Manage OrbiAds jobs — Story 61.4 (REST-ONLY sweep).

Maps the 3 REST-ONLY job MCP tools onto thin CLI commands:
  - list_jobs      -> GET  /api/jobs/
  - get_job        -> GET  /api/jobs/{job_id}
  - duplicate_job  -> POST /api/jobs/{job_id}/duplicate
"""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render, render_detail

app = typer.Typer(help="Manage OrbiAds jobs (Epic 61.4)", no_args_is_help=True)

_LIST_COLUMNS = ["id", "status", "campaignId", "createdAt"]


@app.command("list")
def list_jobs(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500, help="Max results"),
    status: str = typer.Option(None, "--status", help="Filter by job status"),
):
    """List jobs."""
    out: OutputContext = ctx.obj
    params: dict[str, str | int] = {"limit": limit}
    if status:
        params["status"] = status
    try:
        data = get_client().get("/api/jobs/", params=params)
        if isinstance(data, dict):
            items = data.get("jobs", data.get("results", data.get("items", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Get a job's full state."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().get(f"/api/jobs/{job_id}")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def duplicate(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID to duplicate"),
):
    """Duplicate a job (creates a new draft from an existing job)."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().post(f"/api/jobs/{job_id}/duplicate")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)
