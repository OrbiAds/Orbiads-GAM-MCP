"""GAM Ad Review Center commands."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail

app = typer.Typer(help="Search, allow, and block Ad Review Center ads", no_args_is_help=True)

_COLUMNS = ["adId", "displayUrl", "advertiserName", "category", "state", "impressions7d"]


@app.command("search")
def search_ads(
    ctx: typer.Context,
    web_property: str = typer.Option(..., "--web-property", help="GAM web property ID"),
    filter: str | None = typer.Option(None, "--filter", help="GAM filter expression"),
    page_size: int = typer.Option(50, "--page-size", min=1, max=200),
    page_token: str | None = typer.Option(None, "--page-token"),
    order_by: str | None = typer.Option(None, "--order-by"),
):
    """Search Ad Review Center ads."""
    payload = {
        "webPropertyId": web_property,
        "filter": filter,
        "pageSize": page_size,
        "pageToken": page_token,
        "orderBy": order_by,
    }
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
    reason: str = typer.Option(..., "--reason", help="Audit reason for the block"),
):
    """Block one or more Ad Review Center ads."""
    try:
        data = get_client().post(
            "/api/gam/ad-review/batch-block",
            json={
                "webPropertyId": web_property,
                "adIds": ad_ids,
                "reason": reason,
                "dryRun": False,
            },
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
