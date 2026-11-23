"""Manage GAM campaigns."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

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


def _mcp_only(command: str, mcp_call: str, alternative: str | None = None) -> None:
    """Fail honestly: this write has no REST route (Story 100.14 PO decision).

    Whole-campaign writes are MCP `campaign` parent + CampaignPipeline only. The CLI
    cannot reach `/mcp/` either: that endpoint only accepts its own OAuth tokens
    (FastMCP Google provider), not the CLI's Firebase ID token. Never print a success
    message here, always exit non-zero.
    """
    typer.echo(
        f"Error: `orbiads campaigns {command}` is not available from the CLI. "
        "Campaign writes are not exposed over REST; run it from an MCP client "
        f"(Claude, Cursor, ...) connected to https://orbiads.com/mcp: {mcp_call}.",
        err=True,
    )
    if alternative:
        typer.echo(f"REST alternative: {alternative}", err=True)
    raise typer.Exit(code=1)


@app.command()
def deploy(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID (used by --dry-run; a real deploy runs on --job-id)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build an ExecutionPlan without deploying"),
    job_id: str = typer.Option(
        None, "--job-id", help="Web job to deploy (mounted jobs router: plan, then deploy with the token)"
    ),
    confirmation_token: str = typer.Option(
        None, "--confirmation-token", help="Token returned by the plan step (omit it to get the plan)"
    ),
):
    """Preview (--dry-run) or deploy a web job in two steps (plan, then token).

    A campaign cannot be deployed over REST. For a web job: run with `--job-id J` to get
    the signed plan + confirmationToken (POST /api/jobs/J/deployment-plan), then again with
    `--confirmation-token T` to enqueue it (POST /api/jobs/J/deploy). Without `--job-id`
    the command fails: use the MCP `campaign(action="deploy")` tool.
    """
    out: OutputContext = ctx.obj
    try:
        if dry_run:
            data = get_client().post(f"/api/campaigns/{campaign_id}/dry-run")
            render_detail(data, out)
            return
        if not job_id:
            _mcp_only(
                "deploy",
                'campaign(action="deploy", ...)',
                "pass `--job-id <job_id>` to plan then deploy a web job through /api/jobs/{id}",
            )
        if not confirmation_token:
            data = get_client().post(f"/api/jobs/{job_id}/deployment-plan")
            render_detail(data, out)
            typer.echo(
                f"Plan only, nothing deployed. Re-run with --job-id {job_id} "
                "--confirmation-token <confirmationToken> to deploy.",
                err=True,
            )
            return
        effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
        if not confirm(f"Deploy job {job_id}?", effective_ctx):
            raise typer.Exit(code=0)
        data = get_client().post(
            f"/api/jobs/{job_id}/deploy", json={"confirmationToken": confirmation_token}
        )
        if not isinstance(data, dict) or data.get("status") != "queued":
            typer.echo(
                f"Error: deploy response does not confirm job {job_id} is queued: {data!r}",
                err=True,
            )
            raise typer.Exit(code=1)
        if out.format == "json":
            render_detail(data, out)
        success(f"Job {job_id} queued for deployment.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def pause(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="pause")."""
    _mcp_only(
        "pause",
        'campaign(action="pause", ...)',
        "`orbiads line-items lifecycle pause --ids <line item ids>` on explicit GAM line item IDs",
    )


@app.command()
def archive(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="archive")."""
    _mcp_only(
        "archive",
        'campaign(action="archive", ...)',
        "`orbiads line-items lifecycle archive --ids <line item ids>` on explicit GAM line item IDs",
    )


@app.command()
def update(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    file: str = typer.Option(None, "--file", "-f", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="update")."""
    _mcp_only("update", 'campaign(action="update", ...)')


@app.command("add-line-items")
def add_line_items(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    file: str = typer.Option(None, "--file", "-f", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="create_line_items_batch")."""
    _mcp_only("add-line-items", 'campaign(action="create_line_items_batch", ...)')


@app.command("attach-creatives")
def attach_creatives(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    line_item_id: str = typer.Argument(..., help="Line Item ID"),
    file: str = typer.Option(None, "--file", "-f", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="create_licas")."""
    _mcp_only("attach-creatives", 'campaign(action="create_licas", ...)')


@app.command()
def recover(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
    yes: bool = typer.Option(False, "--yes", "-y", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="rollback")."""
    _mcp_only("recover", 'campaign(action="rollback", ...)')


@app.command("plan-deployment")
def plan_deployment(
    ctx: typer.Context,
    preset: str = typer.Option(None, "--preset", hidden=True),
    file: str = typer.Option(None, "--file", "-f", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="plan_deployment")."""
    _mcp_only("plan-deployment", 'campaign(action="plan_deployment", preset=..., params=...)')


@app.command("deploy-media")
def deploy_media(
    ctx: typer.Context,
    confirmation_token: str = typer.Option(None, "--confirmation-token", hidden=True),
    preset: str = typer.Option(None, "--preset", hidden=True),
    file: str = typer.Option(None, "--file", "-f", hidden=True),
    yes: bool = typer.Option(False, "--yes", "-y", hidden=True),
):
    """Not available from the CLI (MCP-only): campaign(action="deploy_media")."""
    _mcp_only("deploy-media", 'campaign(action="deploy_media", ...)')
