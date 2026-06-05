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
def read(
    ctx: typer.Context,
    campaign_id: str = typer.Option(None, "--campaign-id", help="Campaign document ID"),
    order_id: int = typer.Option(None, "--order-id", help="GAM Order ID"),
):
    """Read a campaign recap from live GAM."""
    if campaign_id is None and order_id is None:
        typer.echo("Error: provide --campaign-id or --order-id", err=True)
        raise typer.Exit(code=2)
    try:
        params: dict[str, str | int] = {}
        if campaign_id is not None:
            params["campaignId"] = campaign_id
        if order_id is not None:
            params["orderId"] = order_id
        data = get_client().get("/api/campaigns/live-recap", params=params)
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("dry-run")
def dry_run(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    job_id: str = typer.Option(None, "--job-id", help="Legacy jobs/{jobId} alternative context"),
):
    """Build a deployment execution plan without mutating GAM."""
    try:
        payload: dict[str, str] = {}
        if job_id is not None:
            payload["jobId"] = job_id
        if payload:
            data = get_client().post(f"/api/campaigns/{campaign_id}/dry-run", json=payload)
        else:
            data = get_client().post(f"/api/campaigns/{campaign_id}/dry-run")
        out: OutputContext = ctx.obj
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def deploy(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build an ExecutionPlan without deploying"),
    confirmation_token: str = typer.Option(None, "--confirmation-token", help="Token from campaigns dry-run"),
):
    """Deploy a draft campaign to GAM."""
    try:
        out: OutputContext = ctx.obj
        if dry_run:
            data = get_client().post(f"/api/campaigns/{campaign_id}/dry-run")
            render_detail(data, out)
            return

        # Merge local --yes with global --yes
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Deploy campaign {campaign_id}?", effective_ctx):
            raise typer.Exit(code=0)

        info(f"Deploying campaign {campaign_id}...")
        client = get_client()
        if confirmation_token:
            client.post(
                f"/api/campaigns/{campaign_id}/deploy",
                json={"confirmationToken": confirmation_token},
            )
        else:
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
        client.post(
            "/api/campaigns/bulk-action",
            json={"campaignIds": [campaign_id], "action": "pause"},
        )
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


# === Story 61.4 — REST-ONLY sweep (campaigns) ===============================
# update_campaign / create_line_items_batch / create_licas / rollback_resources


def _load_json_payload(path: str) -> dict:
    """Helper — read a JSON file from disk for mutative bodies."""
    import json as _json
    import os
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command()
def update(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    file: str = typer.Option(..., "--file", "-f", help="Path to a JSON file with the patch body"),
):
    """Update a campaign (PATCH).

    Story 61.4 — maps MCP `update_campaign` → PATCH /api/campaigns/{id}.
    """
    out: OutputContext = ctx.obj
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/campaigns/{campaign_id}", json=payload)
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("add-line-items")
def add_line_items(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the line-items batch payload"),
):
    """Append line items to a campaign.

    Story 61.4 — maps MCP `create_line_items_batch` /
    `create_line_items` → POST /api/campaigns/{id}/line-items.
    """
    out: OutputContext = ctx.obj
    payload = _load_json_payload(file)
    try:
        data = get_client().post(f"/api/campaigns/{campaign_id}/line-items", json=payload)
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("attach-creatives")
def attach_creatives(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    line_item_id: str = typer.Argument(..., help="Line Item ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the LICA batch payload"),
):
    """Attach creatives to a line item via LICAs.

    Story 61.4 — maps MCP `create_licas` / `associate_creative` /
    `bulk_associate_creatives` → POST /api/campaigns/{id}/line-items/{li}/creatives.
    """
    out: OutputContext = ctx.obj
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            f"/api/campaigns/{campaign_id}/line-items/{line_item_id}/creatives",
            json=payload,
        )
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def recover(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Recover a failed/orphaned campaign (rollback orphan resources).

    Story 61.4 — maps MCP `rollback_resources` → POST /api/campaigns/{id}/recover.
    """
    try:
        out: OutputContext = ctx.obj
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Recover campaign {campaign_id}?", effective_ctx):
            raise typer.Exit(code=0)
        client = get_client()
        data = client.post(f"/api/campaigns/{campaign_id}/recover")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


def _mcp_campaign_payload(action: str, payload: dict) -> dict:
    """Build a Streamable HTTP MCP tools/call payload for the campaign parent."""
    return {
        "jsonrpc": "2.0",
        "id": f"campaign-{action}",
        "method": "tools/call",
        "params": {
            "name": "campaign",
            "arguments": {
                "action": action,
                "params": payload,
            },
        },
    }


@app.command("plan-deployment")
def plan_deployment(
    ctx: typer.Context,
    preset: str = typer.Option(..., "--preset", help="Deployment preset, e.g. video_vast"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with preset params"),
):
    """Create a media deployment execution plan through the campaign MCP parent."""
    out: OutputContext = ctx.obj
    preset_params = _load_json_payload(file)
    payload = {
        "preset": preset,
        "params": preset_params,
    }
    try:
        data = get_client().post_raw("/mcp", json=_mcp_campaign_payload("plan_deployment", payload))
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("deploy-media")
def deploy_media(
    ctx: typer.Context,
    confirmation_token: str = typer.Option(..., "--confirmation-token", help="Token from plan-deployment"),
    preset: str = typer.Option(..., "--preset", help="Deployment preset used for the plan"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the same preset params"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """Execute a planned media deployment through the campaign MCP parent."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Deploy media campaign with preset {preset}?", effective_ctx):
        raise typer.Exit(code=0)
    preset_params = _load_json_payload(file)
    payload = {
        "preset": preset,
        "params": preset_params,
        "confirmationToken": confirmation_token,
    }
    try:
        data = get_client().post_raw("/mcp", json=_mcp_campaign_payload("deploy_media", payload))
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)
