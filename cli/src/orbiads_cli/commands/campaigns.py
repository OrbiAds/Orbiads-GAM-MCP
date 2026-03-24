"""Manage GAM campaigns."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, info, render, render_detail, success

app = typer.Typer(help="Manage GAM campaigns", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "status", "createdAt"]


@app.command("list")
def list_campaigns(
    ctx: typer.Context,
    status: str = typer.Option(None, "--status", help="Filter by status (comma-separated, e.g. draft,deployed)"),
    limit: int = typer.Option(None, "--limit", help="Max number of campaigns to return"),
):
    """List campaigns."""
    try:
        client = get_client()
        params: dict[str, str | int] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        data = client.get("/api/campaigns", params=params)
        out: OutputContext = ctx.obj
        render(data, _LIST_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
):
    """Get campaign details."""
    try:
        client = get_client()
        data = client.get(f"/api/campaigns/{campaign_id}")
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def deploy(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Deploy a draft campaign to GAM."""
    try:
        out: OutputContext = ctx.obj
        # Merge local --yes with global --yes
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Deploy campaign {campaign_id}?", effective_ctx):
            raise typer.Exit(code=0)

        info(f"Deploying campaign {campaign_id}...")
        client = get_client()
        client.post(f"/api/campaigns/{campaign_id}/deploy")
        success(f"Campaign {campaign_id} deployed successfully.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def pause(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Pause a deployed campaign."""
    try:
        out: OutputContext = ctx.obj
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Pause campaign {campaign_id}?", effective_ctx):
            raise typer.Exit(code=0)

        client = get_client()
        client.post(f"/api/campaigns/{campaign_id}/pause")
        success(f"Campaign {campaign_id} paused successfully.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def archive(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Archive a campaign."""
    try:
        out: OutputContext = ctx.obj
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Archive campaign {campaign_id}?", effective_ctx):
            raise typer.Exit(code=0)

        client = get_client()
        client.post(f"/api/campaigns/{campaign_id}/archive")
        success(f"Campaign {campaign_id} archived successfully.")
    except CliApiError as e:
        handle_error(e)
