"""CreativeWrapper CRUD/actions CLI (Story 76.1)."""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render_detail

app = typer.Typer(help="Manage GAM CreativeWrappers", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return _json.load(fh)
    except _json.JSONDecodeError as exc:
        typer.echo(f"Error: invalid JSON in {path}: {exc}", err=True)
        raise typer.Exit(code=2) from exc


def _parse_custom_args(values: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            typer.echo(f"Error: --custom-arg must use key=value, got: {value}", err=True)
            raise typer.Exit(code=2)
        key, arg_value = value.split("=", 1)
        key = key.strip()
        if not key:
            typer.echo("Error: --custom-arg key must be non-empty", err=True)
            raise typer.Exit(code=2)
        parsed[key] = arg_value
    return parsed


@app.command("list")
def list_wrappers(
    ctx: typer.Context,
    label_id: int | None = typer.Option(
        None,
        "--label-id",
        min=1,
        help="Filter by CreativeWrapper label ID",
    ),
    status: str | None = typer.Option(None, "--status", help="ACTIVE or INACTIVE"),
    limit: int = typer.Option(100, "--limit", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """List CreativeWrappers."""
    params: dict[str, str | int] = {"limit": limit, "offset": offset}
    if label_id is not None:
        params["labelId"] = label_id
    if status:
        params["status"] = status
    try:
        data = get_client().get("/api/gam/creative-wrappers", params=params)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("get")
def get_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Get a CreativeWrapper by ID."""
    try:
        data = get_client().get(f"/api/gam/creative-wrappers/{wrapper_id}")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("create")
def create_wrapper(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON payload file"),
):
    """Create a CreativeWrapper from a JSON payload."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/creative-wrappers", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("provision")
def provision_wrapper(
    ctx: typer.Context,
    vendor: str = typer.Option(..., "--vendor", help="Preset key, e.g. IAS@v3"),
    label_name: str | None = typer.Option(
        None,
        "--label-name",
        help="CREATIVE_WRAPPER Label display name override",
    ),
    ad_unit_ids: list[int] = typer.Option(
        [],
        "--ad-unit-ids",
        help="Repeat for each AdUnit ID",
    ),
    placement_ids: list[int] = typer.Option(
        [],
        "--placement-ids",
        help="Repeat for each Placement ID",
    ),
    custom_args: list[str] = typer.Option(
        [],
        "--custom-arg",
        "--custom-args",
        help="Repeat as key=value for vendor template args",
    ),
    activate: bool = typer.Option(True, "--activate/--no-activate"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Return the provision plan only"),
):
    """Provision a vendor wrapper label, wrapper, inventory bindings, and activation."""
    payload: dict[str, object] = {
        "vendor": vendor,
        "adUnitIds": list(ad_unit_ids) or None,
        "placementIds": list(placement_ids) or None,
        "customArgs": _parse_custom_args(custom_args) or None,
        "labelName": label_name,
        "activate": activate,
        "dryRun": dry_run,
    }
    payload = {key: value for key, value in payload.items() if value is not None}
    try:
        data = get_client().post("/api/gam/creative-wrappers/provision", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("update")
def update_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON payload file"),
):
    """Update a CreativeWrapper from a JSON payload."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/creative-wrappers/{wrapper_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("set-data-declaration")
def set_data_declaration(
    ctx: typer.Context,
    wrapper_id: int = typer.Option(..., "--wrapper-id", min=1, help="CreativeWrapper ID"),
    declaration_type: str = typer.Option(
        ...,
        "--declaration-type",
        help="Declaration type: NONE or DECLARED",
    ),
    third_party_company_ids: list[int] = typer.Option(
        [],
        "--third-party-company-ids",
        help="Repeat for each RichMediaAdsCompany ID",
    ),
):
    """Set ThirdPartyDataDeclaration on a CreativeWrapper."""
    payload = {
        "declarationType": declaration_type,
        "thirdPartyCompanyIds": list(third_party_company_ids),
    }
    try:
        data = get_client().patch(
            f"/api/gam/creative-wrappers/{wrapper_id}/data-declaration",
            json=payload,
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("list-companies")
def list_companies(
    ctx: typer.Context,
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass the cache"),
):
    """List RichMediaAdsCompany vendor entries."""
    try:
        data = get_client().get(
            "/api/gam/rich-media-ads-companies",
            params={"forceRefresh": force_refresh},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("find-company")
def find_company(
    ctx: typer.Context,
    name: str = typer.Option(..., "--name", help="Company name to fuzzy-match"),
    min_score: float = typer.Option(0.6, "--min-score", min=0.0, max=1.0),
):
    """Find a RichMediaAdsCompany by fuzzy name match."""
    try:
        data = get_client().get(
            "/api/gam/rich-media-ads-companies/search",
            params={"name": name, "minScore": min_score},
        )
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("activate")
def activate_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Activate a CreativeWrapper."""
    try:
        data = get_client().post(f"/api/gam/creative-wrappers/{wrapper_id}/activate")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)


@app.command("deactivate")
def deactivate_wrapper(
    ctx: typer.Context,
    wrapper_id: int = typer.Argument(..., min=1, help="CreativeWrapper ID"),
):
    """Deactivate a CreativeWrapper."""
    try:
        data = get_client().post(f"/api/gam/creative-wrappers/{wrapper_id}/deactivate")
        render_detail(data, ctx.obj)
    except CliApiError as exc:
        handle_error(exc)
