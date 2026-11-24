"""MCM commands: earnings (Story 88.1) and child publishers (Stories 118-1, 118-2).

``invite`` (Story 118-2) creates a child publisher: GAM emails the invitation, so it is two-step
like the agreement actions (server preview of the email, then prompt / ``--yes``). ``update``
edits the editable fields (one call, or ``--dry-run`` / ``--confirmation-token``).

``mcm child-publishers list|get`` read the child publishers (GAM companies of type
CHILD_PUBLISHER with their delegation / invitation / account status). ``withdraw``,
``renegotiate`` and ``resend-invitation`` are two-step server-side: the server previews the
targets (and refuses a company that is not a child publisher in a compatible invitation status),
then the prompt or ``--yes`` confirms and the single-use token executes.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import quote

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.guarded import run_guarded_post
from orbiads_cli.output import OutputContext, confirm, render, render_detail

app = typer.Typer(help="Multi-Customer Management", no_args_is_help=True)


@app.command("earnings")
def mcm_earnings(
    ctx: typer.Context,
    month: int = typer.Option(..., "--month", help="Month (1-12)"),
    year: int = typer.Option(..., "--year", help="Year (4-digit)"),
    child_network_code: list[str] | None = typer.Option(
        None, "--child-network-code", help="Child network code (repeatable, OR-ed)"
    ),
    delegation_type: str | None = typer.Option(
        None, "--delegation-type", help="MANAGE_ACCOUNT or MANAGE_INVENTORY"
    ),
    order_by: str | None = typer.Option(
        None, "--order-by", help="'<field> [asc|desc]', e.g. 'totalEarnings desc'"
    ),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=1000, help="Page size (1-1000)"),
    page_token: str | None = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page (same options)"
    ),
    skip: int | None = typer.Option(None, "--skip", min=0, help="Rows to skip"),
) -> None:
    """Fetch MCM earnings for a given month (filters, sort and pagination: story 118-3)."""
    params: dict = {"month": month, "year": year}
    if child_network_code:
        params["child_network_code"] = child_network_code
    if delegation_type:
        params["delegation_type"] = delegation_type.upper()
    if order_by:
        params["order_by"] = order_by
    if limit != 50:
        params["page_size"] = limit
    if page_token:
        params["page_token"] = page_token
    if skip is not None:
        params["skip"] = skip
    try:
        data = get_client().get("/api/gam/mcm/earnings", params=params)
        render_detail(data, ctx.obj)
        if isinstance(data, dict) and data.get("nextPageToken"):
            typer.echo(f"More results: --page-token {data['nextPageToken']}", err=True)
    except CliApiError as exc:
        handle_error(exc)


child_app = typer.Typer(
    help="MCM child publishers: list, read, invite, update, withdraw, renegotiate, resend "
    "invitation (Stories 118-1, 118-2)",
    no_args_is_help=True,
)
app.add_typer(child_app, name="child-publishers")

_CHILD_COLUMNS = [
    "id",
    "name",
    "invitationStatus",
    "accountStatus",
    "childNetworkCode",
    "approvedDelegationType",
    "proposedRevenueSharePercent",
]


def _flat_child(item: dict) -> dict:
    """Lift the ``childPublisher`` fields to the top level for table / CSV output."""
    flat = {k: v for k, v in item.items() if k != "childPublisher"}
    child = item.get("childPublisher")
    if isinstance(child, dict):
        flat.update(child)
    return flat


@child_app.command("list")
def child_publishers_list(
    ctx: typer.Context,
    invitation_status: str | None = typer.Option(
        None,
        "--invitation-status",
        help="ACCEPTED, EXPIRED, PENDING, REJECTED, WITHDRAWN, DEACTIVATED_BY_AD_MANAGER",
    ),
    account_status: str | None = typer.Option(
        None,
        "--account-status",
        help="e.g. INVITED, APPROVED, PENDING_GOOGLE_APPROVAL, INACTIVE",
    ),
    limit: int = typer.Option(100, "--limit", "-l", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
) -> None:
    """List the child publishers of the active GAM network (0 credits)."""
    params: dict = {"limit": limit, "offset": offset}
    if invitation_status:
        params["invitation_status"] = invitation_status.upper()
    if account_status:
        params["account_status"] = account_status.upper()
    try:
        data = get_client().get("/api/gam/mcm/child-publishers", params=params)
        items = data.get("childPublishers", []) if isinstance(data, dict) else []
        render([_flat_child(i) for i in items], _CHILD_COLUMNS, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@child_app.command("get")
def child_publishers_get(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM company id of the child publisher"),
) -> None:
    """Read one child publisher (0 credits)."""
    try:
        data = get_client().get(
            f"/api/gam/mcm/child-publishers/{quote(company_id, safe='')}"
        )
        child = data.get("childPublisher", data) if isinstance(data, dict) else data
        render_detail(child, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


def _agreement(
    ctx: typer.Context,
    post: Callable[[Any, dict], Any],
    payload: dict,
    yes: bool,
    prompt: str,
) -> None:
    """``post(client, body)`` sends one request (literal path: the route parity guard reads it)."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    try:
        client = get_client()
        data = run_guarded_post(
            lambda body: post(client, body),
            payload,
            ctx=effective_ctx,
            prompt=prompt,
            confirm_fn=confirm,
            two_step=True,
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


def _load_json_object(path: str) -> dict:
    import json
    import os

    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError as exc:
        typer.echo(f"Error: invalid JSON in {path}: {exc}", err=True)
        raise typer.Exit(code=2) from exc
    if not isinstance(data, dict):
        typer.echo("Error: the JSON file must hold one object.", err=True)
        raise typer.Exit(code=2)
    return data


@child_app.command("invite")
def child_publishers_invite(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file: {name, email, delegationType (MANAGE_ACCOUNT | MANAGE_INVENTORY), "
        "childNetworkCode?, proposedRevenueShareMillipercent? (Manage Account), sellerId? "
        "(Manage Inventory), address?, phone?, faxNumber?, externalId?, comment?}",
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Invite a child publisher (createCompanies): GAM EMAILS the invitation. 0.5 credit."""
    payload = _load_json_object(file)
    email = payload.get("email", "?")
    _agreement(
        ctx,
        lambda c, body: c.post("/api/gam/mcm/child-publishers", json=body),
        payload,
        yes,
        f"GAM will email an MCM invitation to {email} (a third party, cannot be recalled). "
        "Send it?",
    )


@child_app.command("update")
def child_publishers_update(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM company id of the child publisher"),
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file: the fields to change (name, email, address, phone, faxNumber, "
        'externalId, comment, sellerId) or {"updates": {...}}',
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview the change (current vs new values) without writing"
    ),
    confirmation_token: str | None = typer.Option(
        None,
        "--confirmation-token",
        help="Execute exactly the previewed change (token of a --dry-run, same file)",
    ),
) -> None:
    """Update a child publisher's editable fields (delegation / revenue share: renegotiate)."""
    if dry_run and confirmation_token:
        typer.echo("Error: use either --dry-run or --confirmation-token, not both.", err=True)
        raise typer.Exit(code=2)
    payload = _load_json_object(file)
    body: dict = {"updates": payload.get("updates", payload)}
    if dry_run:
        body["dryRun"] = True
    if confirmation_token:
        body["confirmationToken"] = confirmation_token
    try:
        data = get_client().patch(
            f"/api/gam/mcm/child-publishers/{quote(company_id, safe='')}", json=body
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@child_app.command("withdraw")
def child_publishers_withdraw(
    ctx: typer.Context,
    company_ids: list[str] = typer.Argument(
        ..., help="Child publisher company id(s) (1-50)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """End the MCM relation (EndAgreementAction) — IRREVERSIBLE (invitation PENDING/ACCEPTED)."""
    _agreement(
        ctx,
        lambda c, body: c.post("/api/gam/mcm/child-publishers/withdraw", json=body),
        {"companyIds": company_ids},
        yes,
        f"Withdraw from being the MCM parent of {len(company_ids)} child publisher(s)? "
        "Only a new invitation the child accepts can restore it.",
    )


@child_app.command("renegotiate")
def child_publishers_renegotiate(
    ctx: typer.Context,
    company_ids: list[str] = typer.Argument(
        ..., help="Child publisher company id(s) (1-50)"
    ),
    delegation_type: str | None = typer.Option(
        None, "--delegation-type", help="MANAGE_ACCOUNT or MANAGE_INVENTORY"
    ),
    revenue_share_millipercent: int | None = typer.Option(
        None,
        "--revenue-share-millipercent",
        min=0,
        max=100000,
        help="Parent revenue share, 15000 = 15% (Manage Account only)",
    ),
    email: str | None = typer.Option(
        None, "--email", help="New child email (one company only)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Send a new invitation, optionally with new terms (ReInviteAction; REJECTED/WITHDRAWN)."""
    payload: dict = {"companyIds": company_ids}
    if delegation_type:
        payload["proposedDelegationType"] = delegation_type.upper()
    if revenue_share_millipercent is not None:
        payload["proposedRevenueShareMillipercent"] = revenue_share_millipercent
    if email:
        payload["proposedEmail"] = email
    _agreement(
        ctx,
        lambda c, body: c.post("/api/gam/mcm/child-publishers/renegotiate", json=body),
        payload,
        yes,
        f"Send a new MCM invitation email to {len(company_ids)} child publisher(s)?",
    )


@child_app.command("resend-invitation")
def child_publishers_resend_invitation(
    ctx: typer.Context,
    company_ids: list[str] = typer.Argument(
        ..., help="Child publisher company id(s) (1-50)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Resend the same invitation email (ResendInvitationAction; invitation EXPIRED)."""
    _agreement(
        ctx,
        lambda c, body: c.post(
            "/api/gam/mcm/child-publishers/resend-invitation", json=body
        ),
        {"companyIds": company_ids},
        yes,
        f"Resend the MCM invitation email to {len(company_ids)} child publisher(s)?",
    )
