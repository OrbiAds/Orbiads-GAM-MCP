"""GAM Ad Review Center commands."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(help="Search, allow, and block Ad Review Center ads", no_args_is_help=True)

_COLUMNS = ["adReviewCenterAdId", "productType", "status", "manualReviewStatuses", "previewUrl"]


@app.command("search")
def search_ads(
    ctx: typer.Context,
    web_property: str = typer.Option(..., "--web-property", help="GAM web property ID"),
    search_text: list[str] = typer.Option(
        None, "--search-text", help="Free-text term (repeatable)"
    ),
    status: str | None = typer.Option(
        None, "--status", help="AdReviewCenterAdStatus enum, e.g. ELIGIBLE"
    ),
    manual_review_status: str | None = typer.Option(
        None, "--manual-review-status", help="ManualAdReviewCenterAdStatus enum"
    ),
    ad_id: list[str] = typer.Option(
        None, "--ad-id", help="Restrict to these Ad Review Center ad IDs (repeatable)"
    ),
    buyer_account_id: list[str] = typer.Option(
        None, "--buyer-account-id", help="RTB buyer account ID (repeatable)"
    ),
    start_time: str | None = typer.Option(None, "--start-time", help="RFC3339 range start"),
    end_time: str | None = typer.Option(None, "--end-time", help="RFC3339 range end"),
    page_size: int = typer.Option(50, "--page-size", min=1, max=1000),
    page_token: str | None = typer.Option(None, "--page-token"),
):
    """Search Ad Review Center ads."""
    payload = {
        "webPropertyId": web_property,
        "searchText": list(search_text) if search_text else None,
        "status": status,
        "manualReviewStatus": manual_review_status,
        "adReviewCenterAdIds": list(ad_id) if ad_id else None,
        "buyerAccountIds": list(buyer_account_id) if buyer_account_id else None,
        "startTime": start_time,
        "endTime": end_time,
        "pageSize": page_size,
        "pageToken": page_token,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    try:
        data = get_client().post("/api/gam/ad-review/search", json=payload)
        if ctx.obj and ctx.obj.format == "json":
            render_detail(data, ctx.obj)
        else:
            render(data.get("ads", []), _COLUMNS, ctx.obj)
            if data.get("nextPageToken"):
                typer.echo(f"nextPageToken: {data['nextPageToken']}", err=True)
    except CliApiError as e:
        handle_error(e)


@app.command("allow")
def allow_batch(
    ctx: typer.Context,
    ad_ids: list[str] = typer.Argument(..., help="Ad Review Center ad IDs"),
    web_property: str = typer.Option(..., "--web-property", help="GAM web property ID"),
):
    """Allow one or more Ad Review Center ads."""
    try:
        data = get_client().post(
            "/api/gam/ad-review/batch-allow",
            json={"webPropertyId": web_property, "adIds": ad_ids, "dryRun": False},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("block")
def block_batch(
    ctx: typer.Context,
    ad_ids: list[str] = typer.Argument(..., help="Ad Review Center ad IDs"),
    web_property: str = typer.Option(..., "--web-property", help="GAM web property ID"),
):
    """Block one or more Ad Review Center ads."""
    try:
        data = get_client().post(
            "/api/gam/ad-review/batch-block",
            json={"webPropertyId": web_property, "adIds": ad_ids, "dryRun": False},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
