"""MCM commands: earnings (Story 88.1) and child publishers (Story 118-1).

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
) -> None:
    """Fetch MCM earnings for a given month."""
    try:
        data = get_client().get(
            "/api/gam/mcm/earnings",
            params={"month": month, "year": year},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


child_app = typer.Typer(
    help="MCM child publishers: list, read, withdraw, renegotiate, resend invitation "
    "(Story 118-1)",
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
