"""Manage GAM advertisers."""

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM advertisers", no_args_is_help=True)


@app.command("list")
def list_advertisers(ctx: typer.Context):
    """List advertisers."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get("/api/gam/advertisers")
        # Response may be a model with "advertisers" key or a list
        if isinstance(data, dict):
            items = data.get("advertisers", data.get("companies", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "type"], out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def create(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Advertiser name"),
):
    """Create a new advertiser."""
    out: OutputContext = ctx.obj
    if not confirm(f'Create advertiser "{name}"?', out):
        raise typer.Exit(code=0)
    try:
        client = get_client()
        data = client.post("/api/gam/advertisers", json={"name": name})
        if out.format == "json":
            render_detail(data, out)
        else:
            adv_id = data.get("id", "?") if isinstance(data, dict) else "?"
            success(f"Advertiser created: {adv_id}")
    except CliApiError as e:
        handle_error(e)


# === Story 61.7 — find-or-create ==========================================


@app.command("find-or-create")
def find_or_create(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Advertiser name to find or create"),
    type_: str = typer.Option("ADVERTISER", "--type", help="Company type (ADVERTISER, AGENCY)"),
):
    """Find an advertiser by name, or create it if absent."""
    try:
        data = get_client().post(
            "/api/gam/advertisers/find-or-create",
            json={"name": name, "type": type_},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.4 — get / find / update + agencies sub-noun ==================


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


@app.command()
def get(
    ctx: typer.Context,
    advertiser_id: str = typer.Argument(..., help="Advertiser ID"),
):
    """Get advertiser details."""
    try:
        data = get_client().get(f"/api/gam/advertisers/{advertiser_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def find(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Advertiser name (exact match)"),
):
    """Find an advertiser by exact name (read-only; use `find-or-create` to upsert)."""
    try:
        data = get_client().get("/api/gam/advertisers/search", params={"name": name})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def update(
    ctx: typer.Context,
    advertiser_id: str = typer.Argument(..., help="Advertiser ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update an advertiser (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/advertisers/{advertiser_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def archive(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM Company ID to archive"),
    reason: str = typer.Option(None, "--reason", "-r", help="Optional reason (logged in audit_log)"),
):
    """Archive a GAM Advertiser (Story 87.1)."""
    out: OutputContext = ctx.obj
    if not confirm(f"Archive advertiser {company_id}?", out):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(
            f"/api/gam/companies/{company_id}/archive",
            json={"area": "advertisers", "reason": reason},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def activate(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM Company ID to activate"),
    reason: str = typer.Option(None, "--reason", "-r", help="Optional reason (logged in audit_log)"),
):
    """Activate (unarchive) a GAM Advertiser (Story 87.1)."""
    out: OutputContext = ctx.obj
    if not confirm(f"Activate advertiser {company_id}?", out):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(
            f"/api/gam/companies/{company_id}/activate",
            json={"area": "advertisers", "reason": reason},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("rich-media-list")
def rich_media_list(
    ctx: typer.Context,
    verified_only: bool = typer.Option(
        False,
        "--verified",
        hidden=True,
        help="Unsupported: GAM exposes no verification status for these partners",
    ),
    page_size: int = typer.Option(50, "--page-size", min=1, max=200, help="Maximum partners to fetch"),
):
    """List GAM RichMediaAdsCompany partners."""
    # Story 117-18: GAM's RichMediaAdsCompany has no verification status (discovery rev
    # 20261118: displayName, policyUrl, gdprStatus, companyGvlId), so --verified never filtered
    # anything. It now fails clearly instead of being silently ignored.
    if verified_only:
        typer.echo(
            "Error: --verified is not supported: GAM exposes no verification status for "
            "rich media ads companies.",
            err=True,
        )
        raise typer.Exit(code=2)
    try:
        data = get_client().get("/api/gam/companies/rich-media", params={"pageSize": page_size})
        items = data.get("richMediaCompanies", data) if isinstance(data, dict) else data
        render(
            items or [],
            ["id", "displayName", "gdprStatus", "companyGvlId", "policyUrl"],
            ctx.obj,
        )
    except CliApiError as e:
        handle_error(e)


@app.command("rich-media-get")
def rich_media_get(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM RichMediaAdsCompany ID"),
):
    """Get one GAM RichMediaAdsCompany partner."""
    try:
        data = get_client().get(f"/api/gam/companies/rich-media/{company_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── third-party companies (Story 111.3) ───────────────────────────────────
# Distinct resource from rich-media above: ad networks, ad servers and video
# technology partners. Read-only — every field but the identifier is output-only
# in GAM REST v1, so there is no create/update counterpart.


@app.command("third-party-list")
def third_party_list(
    ctx: typer.Context,
    filter_expr: str = typer.Option(
        None, "--filter", help='GAM filter, e.g. type="AD_SERVER" or status="ACTIVE"'
    ),
    page_size: int = typer.Option(
        50, "--page-size", min=1, max=1000, help="Maximum companies to fetch"
    ),
):
    """List GAM ThirdPartyCompany entries (ad networks, ad servers, VTPs)."""
    try:
        params: dict = {"pageSize": page_size}
        if filter_expr:
            params["filter"] = filter_expr
        data = get_client().get("/api/gam/companies/third-party", params=params)
        items = data.get("thirdPartyCompanies", data) if isinstance(data, dict) else data
        render(items or [], ["id", "displayName", "type", "status"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("third-party-get")
def third_party_get(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM ThirdPartyCompany ID"),
):
    """Get one GAM ThirdPartyCompany."""
    try:
        data = get_client().get(f"/api/gam/companies/third-party/{company_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── companies sub-noun (Story 117-4) ─────────────────────────────────────
# Read-only view of EVERY Company.Type (HOUSE_*, AD_NETWORK, PARTNER, CHILD_PUBLISHER,
# VIEWABILITY_PROVIDER included). Writes stay under `advertisers` / `agencies`.
companies_app = typer.Typer(
    help="List and read companies of any type (read-only, Story 117-4)", no_args_is_help=True
)
app.add_typer(companies_app, name="companies")

_COMPANY_COLUMNS = ["id", "name", "type", "creditStatus"]


@companies_app.command("list")
def companies_list(
    ctx: typer.Context,
    type_: Optional[str] = typer.Option(
        None,
        "--type",
        help="Company.Type: ADVERTISER, AGENCY, HOUSE_ADVERTISER, HOUSE_AGENCY, AD_NETWORK, "
        "PARTNER, CHILD_PUBLISHER, VIEWABILITY_PROVIDER",
    ),
    name_contains: Optional[str] = typer.Option(
        None, "--name-contains", help="Company name substring"
    ),
    credit_status: Optional[str] = typer.Option(
        None,
        "--credit-status",
        help="ACTIVE, ON_HOLD, CREDIT_STOP, INACTIVE or BLOCKED (applied client-side to each "
        "page; Company has no status filter)",
    ),
    since: Optional[str] = typer.Option(
        None,
        "--since",
        help="Modified on/after this ISO 8601 date or date-time (a date alone = 00:00 UTC)",
    ),
    order_by: Optional[str] = typer.Option(
        None, "--order-by", help="Sort: '<field> [asc|desc]' (id, name, lastModifiedDateTime)"
    ),
    page_token: Optional[str] = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List companies of any type (typed filters, sort, pagination)."""
    out: OutputContext = ctx.obj
    params: dict = {"limit": limit}
    for key, value in (
        ("type", type_),
        ("name_contains", name_contains),
        ("credit_status", credit_status),
        ("since", since),
        ("order_by", order_by),
        ("page_token", page_token),
    ):
        if value is not None:
            params[key] = value
    try:
        data = get_client().get("/api/gam/companies", params=params)
        items = data.get("items", []) if isinstance(data, dict) else data
        render(items, _COMPANY_COLUMNS, out)
        if isinstance(data, dict) and out.format != "json":
            if data.get("clientSideFilters"):
                typer.echo(
                    "Note: --credit-status is applied to each page after the read; a page may "
                    "hold fewer than --limit items.",
                    err=True,
                )
            if data.get("hasMore"):
                typer.echo(f"More results: --page-token {data.get('nextPageToken')}", err=True)
    except CliApiError as e:
        handle_error(e)


@companies_app.command("get")
def companies_get(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM Company ID (any type)"),
):
    """Get one company of any type (childPublisher / viewabilityProvider included)."""
    try:
        data = get_client().get(f"/api/gam/companies/{company_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── partners sub-noun (Story 118-4) ──────────────────────────────────────
# GAM companies of type PARTNER (publishing partners; = REST v1 `Partner`).
partners_app = typer.Typer(
    help="List, read and update partners (companies of type PARTNER, Story 118-4)",
    no_args_is_help=True,
)
app.add_typer(partners_app, name="partners")


@partners_app.command("list")
def partners_list(
    ctx: typer.Context,
    name_contains: Optional[str] = typer.Option(
        None, "--name-contains", help="Partner name substring"
    ),
    credit_status: Optional[str] = typer.Option(
        None,
        "--credit-status",
        help="ACTIVE, ON_HOLD, CREDIT_STOP, INACTIVE or BLOCKED (applied client-side to each "
        "page)",
    ),
    since: Optional[str] = typer.Option(
        None, "--since", help="Modified on/after this ISO 8601 date or date-time"
    ),
    order_by: Optional[str] = typer.Option(
        None, "--order-by", help="Sort: '<field> [asc|desc]' (id, name, lastModifiedDateTime)"
    ),
    page_token: Optional[str] = typer.Option(
        None, "--page-token", help="nextPageToken of the previous page"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List partners (companies of type PARTNER)."""
    out: OutputContext = ctx.obj
    params: dict = {"limit": limit}
    for key, value in (
        ("name_contains", name_contains),
        ("credit_status", credit_status),
        ("since", since),
        ("order_by", order_by),
        ("page_token", page_token),
    ):
        if value is not None:
            params[key] = value
    try:
        data = get_client().get("/api/gam/partners", params=params)
        items = data.get("items", []) if isinstance(data, dict) else data
        render(items, _COMPANY_COLUMNS, out)
        if isinstance(data, dict) and out.format != "json" and data.get("hasMore"):
            typer.echo(f"More results: --page-token {data.get('nextPageToken')}", err=True)
    except CliApiError as e:
        handle_error(e)


@partners_app.command("get")
def partners_get(
    ctx: typer.Context,
    partner_id: str = typer.Argument(..., help="GAM company ID of the partner"),
):
    """Get one partner (a company of another type is refused)."""
    try:
        data = get_client().get(f"/api/gam/partners/{partner_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@partners_app.command("update")
def partners_update(
    ctx: typer.Context,
    partner_id: str = typer.Argument(..., help="GAM company ID of the partner"),
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file: the fields to change (name, address, email, phone, faxNumber, "
        "externalId, comment, primaryContactId, appliedTeamIds, creditStatus), or "
        '{"updates": {...}}',
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview the change (current vs new values) without writing"
    ),
    confirmation_token: Optional[str] = typer.Option(
        None,
        "--confirmation-token",
        help="Execute exactly the previewed change (token of a --dry-run, same file)",
    ),
):
    """Update a partner (read-modify-write; a company of another type is refused)."""
    if dry_run and confirmation_token:
        typer.echo("Error: use either --dry-run or --confirmation-token, not both.", err=True)
        raise typer.Exit(code=2)
    payload = _load_json_payload(file)
    updates = payload.get("updates", payload) if isinstance(payload, dict) else payload
    body: dict = {"updates": updates}
    if dry_run:
        body["dryRun"] = True
    if confirmation_token:
        body["confirmationToken"] = confirmation_token
    try:
        data = get_client().patch(f"/api/gam/partners/{partner_id}", json=body)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── agencies sub-noun ─────────────────────────────────────────────────────
agencies_app = typer.Typer(help="Manage GAM agencies (Story 62.4)", no_args_is_help=True)
app.add_typer(agencies_app, name="agencies")


@agencies_app.command("list")
def agencies_list(ctx: typer.Context):
    """List GAM agencies."""
    try:
        data = get_client().get("/api/gam/agencies")
        if isinstance(data, dict):
            items = data.get("agencies", data.get("companies", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "type"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


@agencies_app.command("create")
def agencies_create(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Agency name"),
):
    """Create a GAM agency."""
    try:
        data = get_client().post("/api/gam/agencies", json={"name": name})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@agencies_app.command("update")
def agencies_update(
    ctx: typer.Context,
    agency_id: str = typer.Argument(..., help="Agency ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update an agency (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/agencies/{agency_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@agencies_app.command("archive")
def agencies_archive(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM Agency company ID to archive"),
    reason: str = typer.Option(None, "--reason", "-r", help="Optional reason (logged in audit_log)"),
):
    """Archive a GAM Agency (Story 87.1)."""
    out: OutputContext = ctx.obj
    if not confirm(f"Archive agency {company_id}?", out):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(
            f"/api/gam/companies/{company_id}/archive",
            json={"area": "agencies", "reason": reason},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@agencies_app.command("activate")
def agencies_activate(
    ctx: typer.Context,
    company_id: str = typer.Argument(..., help="GAM Agency company ID to activate"),
    reason: str = typer.Option(None, "--reason", "-r", help="Optional reason (logged in audit_log)"),
):
    """Activate (unarchive) a GAM Agency (Story 87.1)."""
    out: OutputContext = ctx.obj
    if not confirm(f"Activate agency {company_id}?", out):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(
            f"/api/gam/companies/{company_id}/activate",
            json={"area": "agencies", "reason": reason},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
