"""Live stream ad break commands."""

from __future__ import annotations

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render_detail

app = typer.Typer(help="Live stream ad breaks", no_args_is_help=True)


@app.command("list")
def list_breaks(
    ctx: typer.Context,
    area: str = typer.Option(..., "--area", help="event_id, asset_key or custom_asset_key"),
    identifier: str = typer.Option(..., "--identifier", help="Event ID, asset key, or custom asset key"),
    page_size: int = typer.Option(50, "--page-size", min=1, max=200),
) -> None:
    """List ad breaks for a live stream event."""
    try:
        data = get_client().get(
            "/api/gam/live-stream/ad-breaks",
            params={"area": area, "event_identifier": identifier, "page_size": page_size},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("get")
def get_break(
    ctx: typer.Context,
    ad_break_id: str = typer.Argument(..., help="GAM ad break ID"),
    area: str = typer.Option(..., "--area", help="event_id, asset_key or custom_asset_key"),
    identifier: str = typer.Option(..., "--identifier", help="Event ID, asset key, or custom asset key"),
) -> None:
    """Get one live stream ad break."""
    try:
        data = get_client().get(
            f"/api/gam/live-stream/ad-breaks/{ad_break_id}",
            params={"area": area, "event_identifier": identifier},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("create")
def create_break(
    ctx: typer.Context,
    area: str = typer.Option(..., "--area", help="event_id, asset_key or custom_asset_key"),
    identifier: str = typer.Option(..., "--identifier", help="Event ID, asset key, or custom asset key"),
    start_time: str = typer.Option(..., "--start-time", help="RFC3339 start time"),
    duration: str = typer.Option(..., "--duration", help="Google duration, e.g. 60s"),
    break_type: str = typer.Option("MID_ROLL", "--break-type", help="MID_ROLL, PRE_ROLL or POST_ROLL"),
    slate_creative_id: str | None = typer.Option(None, "--slate-creative-id"),
) -> None:
    """Create a live stream ad break."""
    try:
        data = get_client().post(
            "/api/gam/live-stream/ad-breaks",
            json={
                "area": area,
                "eventIdentifier": identifier,
                "startTime": start_time,
                "duration": duration,
                "breakType": break_type,
                **({"slateCreativeId": slate_creative_id} if slate_creative_id else {}),
            },
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("patch")
def patch_break(
    ctx: typer.Context,
    ad_break_id: str = typer.Argument(..., help="GAM ad break ID"),
    asset_key: str = typer.Option(..., "--asset-key", help="GAM Studio asset key"),
    start_time: str | None = typer.Option(None, "--start-time", help="RFC3339 start time"),
    duration: str | None = typer.Option(None, "--duration", help="Google duration, e.g. 60s"),
    slate_creative_id: str | None = typer.Option(None, "--slate-creative-id"),
) -> None:
    """Patch an asset-key-scoped ad break."""
    payload = {
        "area": "asset_key",
        "assetKey": asset_key,
        **({"startTime": start_time} if start_time else {}),
        **({"duration": duration} if duration else {}),
        **({"slateCreativeId": slate_creative_id} if slate_creative_id else {}),
    }
    try:
        data = get_client().patch(f"/api/gam/live-stream/ad-breaks/{ad_break_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("delete")
def delete_break(
    ctx: typer.Context,
    ad_break_id: str = typer.Argument(..., help="GAM ad break ID"),
    asset_key: str = typer.Option(..., "--asset-key", help="GAM Studio asset key"),
) -> None:
    """Delete an asset-key-scoped ad break."""
    try:
        data = get_client().delete(
            f"/api/gam/live-stream/ad-breaks/{ad_break_id}",
            params={"area": "asset_key", "asset_key": asset_key},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)
