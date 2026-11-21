"""GAM programmatic commerce: PMP deals, private auctions, buyers, proposal and PLI lifecycle."""

from __future__ import annotations

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.guarded import run_guarded_post
from orbiads_cli.output import OutputContext, confirm, render, render_detail

app = typer.Typer(
    help="GAM programmatic surface — PMP deals, private auctions, buyers",
    no_args_is_help=True,
)

deals_app = typer.Typer(help="PMP deals", no_args_is_help=True)
auctions_app = typer.Typer(help="Private auctions", no_args_is_help=True)
buyers_app = typer.Typer(help="Programmatic buyers", no_args_is_help=True)
proposals_app = typer.Typer(
    help="Proposal lifecycle (pause, resume, unarchive, discard drafts, buyer review, push to order)",
    no_args_is_help=True,
)

app.add_typer(deals_app, name="deals")
app.add_typer(auctions_app, name="auctions")
app.add_typer(buyers_app, name="buyers")
pli_app = typer.Typer(
    help="Proposal line item lifecycle (pause, resume, reserve, release, unarchive, get)",
    no_args_is_help=True,
)

app.add_typer(proposals_app, name="proposals")
app.add_typer(pli_app, name="proposal-line-items")

_DEAL_LIST_COLUMNS = ["dealId", "displayName", "status", "floorPrice"]
_AUCTION_LIST_COLUMNS = ["privateAuctionId", "displayName", "description"]
_BUYER_LIST_COLUMNS = ["accountId", "displayName", "buyerStatus"]
_PROPOSAL_LIST_COLUMNS = [
    "id",
    "name",
    "status",
    "isProgrammatic",
    "negotiationStatus",
    "buyerAccountId",
    "lastModifiedDateTime",
]
_PLI_LIST_COLUMNS = ["id", "proposalId", "name", "reservationStatus", "isArchived"]


def _load_json_payload(path: str) -> dict:
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


def _list_params(
    page_size: int,
    page_token: Optional[str],
    filter_expr: Optional[str] = None,
) -> dict:
    params: dict[str, str | int] = {"pageSize": page_size}
    if page_token:
        params["pageToken"] = page_token
    if filter_expr:
        params["filter"] = filter_expr
    return params


def _items(data, *keys: str) -> list:
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return value
        fallback = data.get("results")
        return fallback if isinstance(fallback, list) else []
    return data if isinstance(data, list) else []


@deals_app.command("list")
def deals_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
    filter_expr: Optional[str] = typer.Option(
        None, "--filter", help="GAM filter expression"
    ),
):
    """List PMP deals."""
    try:
        data = get_client().get(
            "/api/gam/pmp-deals",
            params=_list_params(page_size, page_token, filter_expr),
        )
        render(
            _items(data, "privateAuctionDeals", "deals"),
            _DEAL_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@deals_app.command("get")
def deals_get(
    ctx: typer.Context,
    deal_id: str = typer.Argument(..., help="Deal ID"),
):
    """Get a PMP deal."""
    try:
        data = get_client().get(f"/api/gam/pmp-deals/{deal_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@deals_app.command("create")
def deals_create(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON body for the new PMP deal"
    ),
):
    """Create a PMP deal."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/pmp-deals", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@deals_app.command("update")
def deals_update(
    ctx: typer.Context,
    deal_id: str = typer.Argument(..., help="Deal ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON body with PATCH fields"),
):
    """Update a PMP deal."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/pmp-deals/{deal_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("list")
def auctions_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
):
    """List private auctions."""
    try:
        data = get_client().get(
            "/api/gam/private-auctions",
            params=_list_params(page_size, page_token),
        )
        render(
            _items(data, "privateAuctions", "auctions"),
            _AUCTION_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("get")
def auctions_get(
    ctx: typer.Context,
    auction_id: str = typer.Argument(..., help="Private auction ID"),
):
    """Get a private auction."""
    try:
        data = get_client().get(f"/api/gam/private-auctions/{auction_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("create")
def auctions_create(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON body for the new private auction"
    ),
):
    """Create a private auction."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/private-auctions", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@auctions_app.command("update")
def auctions_update(
    ctx: typer.Context,
    auction_id: str = typer.Argument(..., help="Private auction ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON body with PATCH fields"),
):
    """Update a private auction."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/gam/private-auctions/{auction_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@buyers_app.command("list")
def buyers_list(
    ctx: typer.Context,
    page_size: int = typer.Option(200, "--page-size", min=1, max=200),
    page_token: Optional[str] = typer.Option(None, "--page-token"),
):
    """List programmatic buyers."""
    try:
        data = get_client().get(
            "/api/gam/programmatic-buyers",
            params=_list_params(page_size, page_token),
        )
        render(
            _items(data, "programmaticBuyers", "buyers"),
            _BUYER_LIST_COLUMNS,
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@buyers_app.command("get")
def buyers_get(
    ctx: typer.Context,
    buyer_id: str = typer.Argument(..., help="Programmatic buyer ID"),
):
    """Get a programmatic buyer."""
    try:
        data = get_client().get(f"/api/gam/programmatic-buyers/{buyer_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── Proposal lifecycle (Story 116-4) ─────────────────────────────────────────
# Wraps POST /api/gam/proposals/{pause,resume,unarchive,discard-drafts,
# request-buyer-review,push-to-order}. All six drive ProposalService
# performProposalAction on one or more proposal IDs (1-50) and are feature-gated
# (Marketplace/programmatic): a network without it answers GAM_FEATURE_NOT_AVAILABLE.


def _proposal_body(
    ctx: typer.Context,
    ids: list[str],
    yes: bool,
    prompt: str,
    extra: dict | None = None,
) -> dict:
    """Confirm with the user, then build the {proposalIds, ...} body."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(prompt, effective_ctx):
        raise typer.Exit(code=0)
    body: dict = {"proposalIds": ids}
    if extra:
        body.update(extra)
    return body


def _pli_body(
    ctx: typer.Context,
    ids: list[str],
    yes: bool,
    prompt: str,
    extra: dict | None = None,
) -> dict:
    """Confirm with the user, then build the {pliIds, ...} body."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(prompt, effective_ctx):
        raise typer.Exit(code=0)
    body: dict = {"pliIds": ids}
    if extra:
        body.update(extra)
    return body


@proposals_app.command("pause")
def proposals_pause(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    reason: str = typer.Option(
        ..., "--reason", help="Why the proposals are paused (min 3 chars)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Pause programmatic proposals."""
    body = _proposal_body(
        ctx, ids, yes, f"Pause {len(ids)} proposal(s)?", {"reason": reason}
    )
    try:
        data = get_client().post("/api/gam/proposals/pause", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@proposals_app.command("resume")
def proposals_resume(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Resume paused proposals."""
    body = _proposal_body(ctx, ids, yes, f"Resume {len(ids)} proposal(s)?")
    try:
        data = get_client().post("/api/gam/proposals/resume", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@proposals_app.command("unarchive")
def proposals_unarchive(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Unarchive proposals."""
    body = _proposal_body(ctx, ids, yes, f"Unarchive {len(ids)} proposal(s)?")
    try:
        data = get_client().post("/api/gam/proposals/unarchive", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@proposals_app.command("discard-drafts")
def proposals_discard_drafts(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Discard local edits: revert to the latest Marketplace terms (IRREVERSIBLE).

    Always two-step (story 116-10b): the server previews the proposals, then ``--yes`` or
    the prompt confirms and the single-use token executes.
    """
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    try:
        client = get_client()
        data = run_guarded_post(
            lambda body: client.post("/api/gam/proposals/discard-drafts", json=body),
            {"proposalIds": ids},
            ctx=effective_ctx,
            prompt=f"Discard the local edits of {len(ids)} proposal(s)? They cannot be recovered.",
            confirm_fn=confirm,
            two_step=True,
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@proposals_app.command("request-buyer-review")
def proposals_request_buyer_review(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Request buyer review of proposals."""
    body = _proposal_body(
        ctx, ids, yes, f"Request buyer review for {len(ids)} proposal(s)?"
    )
    try:
        data = get_client().post("/api/gam/proposals/request-buyer-review", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@proposals_app.command("push-to-order")
def proposals_push_to_order(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Update the Order of finalized Marketplace proposals with the seller's data."""
    body = _proposal_body(ctx, ids, yes, f"Push {len(ids)} proposal(s) to their Order?")
    try:
        data = get_client().post("/api/gam/proposals/push-to-order", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── Proposal line item lifecycle (Story 116-5) ───────────────────────────────
# Wraps POST /api/gam/proposal-line-items/{pause,resume,reserve,release,unarchive}
# and GET /api/gam/proposal-line-items/{id}. The five writes drive
# ProposalLineItemService performProposalLineItemAction on 1-50 line item IDs and
# are feature-gated (Marketplace/programmatic): a network without it answers
# GAM_FEATURE_NOT_AVAILABLE.


@pli_app.command("pause")
def pli_pause(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal line item ID(s) (1-50)"),
    reason: str = typer.Option(
        ..., "--reason", help="Why the line items are paused (min 3 chars)"
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Pause proposal line items."""
    body = _pli_body(
        ctx, ids, yes, f"Pause {len(ids)} proposal line item(s)?", {"reason": reason}
    )
    try:
        data = get_client().post("/api/gam/proposal-line-items/pause", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("resume")
def pli_resume(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal line item ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Resume paused proposal line items."""
    body = _pli_body(ctx, ids, yes, f"Resume {len(ids)} proposal line item(s)?")
    try:
        data = get_client().post("/api/gam/proposal-line-items/resume", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("reserve")
def pli_reserve(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal line item ID(s) (1-50)"),
    allow_overbook: bool = typer.Option(
        False,
        "--allow-overbook",
        help="Reserve even beyond the forecast availability (may reduce other deliveries)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Reserve inventory for proposal line items."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    try:
        client = get_client()
        if allow_overbook:
            # Story 116-10b: overbook is always two-step (preview -> token); --yes only
            # skips the human prompt.
            data = run_guarded_post(
                lambda body: client.post("/api/gam/proposal-line-items/reserve", json=body),
                {"pliIds": ids, "allowOverbook": True},
                ctx=effective_ctx,
                prompt=(
                    f"Reserve inventory for {len(ids)} proposal line item(s) EVEN BEYOND "
                    "availability (overbook)?"
                ),
                confirm_fn=confirm,
                two_step=True,
            )
        else:
            body = _pli_body(
                ctx, ids, yes, f"Reserve inventory for {len(ids)} proposal line item(s)?"
            )
            data = run_guarded_post(
                lambda b: client.post("/api/gam/proposal-line-items/reserve", json=b),
                body,
                ctx=effective_ctx,
                prompt="",
                confirm_fn=confirm,
                two_step=False,
            )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("release")
def pli_release(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal line item ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Release the reserved inventory of proposal line items."""
    body = _pli_body(
        ctx, ids, yes, f"Release the inventory of {len(ids)} proposal line item(s)?"
    )
    try:
        data = get_client().post("/api/gam/proposal-line-items/release", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("unarchive")
def pli_unarchive(
    ctx: typer.Context,
    ids: list[str] = typer.Argument(..., help="Proposal line item ID(s) (1-50)"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Unarchive proposal line items."""
    body = _pli_body(ctx, ids, yes, f"Unarchive {len(ids)} proposal line item(s)?")
    try:
        data = get_client().post("/api/gam/proposal-line-items/unarchive", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("get")
def pli_get(
    ctx: typer.Context,
    pli_id: str = typer.Argument(..., help="Proposal line item ID"),
):
    """Get one proposal line item (status, reservationStatus, pause state)."""
    try:
        data = get_client().get(f"/api/gam/proposal-line-items/{pli_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ---------------------------------------------------------------------------
# Story 116-6 — filtered listing. Wraps GET /api/gam/proposals and
# GET /api/gam/proposal-line-items (typed query parameters, validated server side).
# ---------------------------------------------------------------------------


def _paging_hint(data: object) -> None:
    if isinstance(data, dict) and data.get("hasMore"):
        next_offset = int(data.get("offset", 0)) + int(data.get("limit", 0))
        typer.echo(f"More results available: rerun with --offset {next_offset}", err=True)
    if isinstance(data, dict) and data.get("clientSideFilters"):
        typer.echo(
            "Note: "
            + ", ".join(data["clientSideFilters"])
            + " filtered on the returned page only (GAM has no such filter).",
            err=True,
        )


@proposals_app.command("list")
def proposals_list(
    ctx: typer.Context,
    status: Optional[str] = typer.Option(
        None, "--status", help="DRAFT, PENDING_APPROVAL, APPROVED or REJECTED"
    ),
    negotiation_status: Optional[str] = typer.Option(
        None, "--negotiation-status", help="e.g. AWAITING_SELLER_REVIEW, FINALIZED"
    ),
    buyer: Optional[str] = typer.Option(
        None, "--buyer", help="Buyer account ID (filters the returned page only)"
    ),
    programmatic: Optional[bool] = typer.Option(
        None,
        "--programmatic/--non-programmatic",
        help="Only programmatic / only non-programmatic proposals (default: both)",
    ),
    archived: Optional[bool] = typer.Option(
        None, "--archived/--not-archived", help="Filter on the archived flag"
    ),
    since: Optional[str] = typer.Option(
        None, "--since", help="Only proposals modified after this ISO 8601 date-time"
    ),
    limit: int = typer.Option(200, "--limit", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List proposals (programmatic or not) with typed filters."""
    params: dict = {"limit": limit, "offset": offset}
    for key, value in (
        ("status", status),
        ("negotiationStatus", negotiation_status),
        ("buyerId", buyer),
        ("isProgrammatic", programmatic),
        ("isArchived", archived),
        ("lastModifiedAfter", since),
    ):
        if value is not None:
            params[key] = str(value).lower() if isinstance(value, bool) else value
    try:
        data = get_client().get("/api/gam/proposals", params=params)
        render(_items(data, "proposals"), _PROPOSAL_LIST_COLUMNS, ctx.obj)
        _paging_hint(data)
    except CliApiError as e:
        handle_error(e)


@pli_app.command("list")
def pli_list(
    ctx: typer.Context,
    proposal_id: Optional[str] = typer.Option(
        None, "--proposal-id", help="Restrict to one proposal (default: whole network)"
    ),
    reservation_status: Optional[str] = typer.Option(
        None,
        "--status",
        help="RESERVED, NOT_RESERVED, RELEASED or CHECK_LINE_ITEM_RESERVATION_STATUS "
        "(filters the returned page only)",
    ),
    programmatic: Optional[bool] = typer.Option(
        None, "--programmatic/--non-programmatic", help="Default: both"
    ),
    include_archived: bool = typer.Option(False, "--include-archived"),
    since: Optional[str] = typer.Option(
        None, "--since", help="Only items modified after this ISO 8601 date-time"
    ),
    limit: int = typer.Option(200, "--limit", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List proposal line items, optionally for a single proposal."""
    params: dict = {"limit": limit, "offset": offset}
    if include_archived:
        params["includeArchived"] = "true"
    for key, value in (
        ("proposalId", proposal_id),
        ("reservationStatus", reservation_status),
        ("isProgrammatic", programmatic),
        ("lastModifiedAfter", since),
    ):
        if value is not None:
            params[key] = str(value).lower() if isinstance(value, bool) else value
    try:
        data = get_client().get("/api/gam/proposal-line-items", params=params)
        render(_items(data, "lineItems"), _PLI_LIST_COLUMNS, ctx.obj)
        _paging_hint(data)
    except CliApiError as e:
        handle_error(e)
