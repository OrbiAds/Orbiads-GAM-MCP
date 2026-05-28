"""Prebid.js / Header Bidding tooling CLI commands (Epic 70)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, render, render_detail

app = typer.Typer(
    help="Prebid.js / Header Bidding tooling (Epic 70)",
    no_args_is_help=True,
)

OutputFormat = str


def _parse_csv_floats(value: str | None) -> list[float] | None:
    if value is None or value == "":
        return None
    try:
        return [float(part.strip()) for part in value.split(",") if part.strip()]
    except ValueError:
        typer.echo("Error: expected comma-separated floats", err=True)
        raise typer.Exit(code=2)


def _parse_price_range(value: str) -> list[float]:
    parsed = _parse_csv_floats(value)
    if parsed is None or len(parsed) != 2:
        typer.echo("Error: --price-range must contain exactly two floats", err=True)
        raise typer.Exit(code=2)
    return parsed


def _parse_csv_strings(value: str | None) -> list[str] | None:
    if value is None or value == "":
        return None
    return [part.strip() for part in value.split(",") if part.strip()]


def _parse_creative_map(
    creative_map_str: str | None,
    creative_map_file: str | None,
) -> dict[str, list[int]]:
    if bool(creative_map_str) == bool(creative_map_file):
        typer.echo("Error: provide exactly one of --creative-map or --creative-map-file", err=True)
        raise typer.Exit(code=2)
    try:
        raw = (
            Path(creative_map_file).read_text(encoding="utf-8")
            if creative_map_file
            else creative_map_str
        )
        parsed = json.loads(raw or "{}")
    except (OSError, json.JSONDecodeError):
        typer.echo("Error: invalid creative-map JSON", err=True)
        raise typer.Exit(code=2)
    if not isinstance(parsed, dict):
        typer.echo("Error: creative-map JSON must be an object", err=True)
        raise typer.Exit(code=2)
    return {str(size): [int(item) for item in ids] for size, ids in parsed.items()}


def _with_confirmation_instruction(data: Any) -> Any:
    if not isinstance(data, dict):
        return data
    token = data.get("confirmationToken") or data.get("confirmation_token")
    if token:
        return {
            **data,
            "confirmationInstruction": (
                f"To confirm, re-run with --confirmation-token={token}"
            ),
        }
    return data


def _write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text, encoding="utf-8")
    else:
        typer.echo(text)


def _render_result(data: Any, fmt: OutputFormat, output: str | None) -> None:
    data = _with_confirmation_instruction(data)
    if fmt == "json":
        _write_output(json.dumps(data, indent=2, default=str), output)
        return

    if output:
        if isinstance(data, dict):
            text = "\n".join(f"{key}\t{value}" for key, value in data.items())
        elif isinstance(data, list):
            text = "\n".join(json.dumps(row, default=str) for row in data)
        else:
            text = str(data)
        _write_output(text, output)
        return

    ctx = OutputContext(format="table")
    if isinstance(data, list):
        columns = list(data[0].keys()) if data and isinstance(data[0], dict) else ["value"]
        rows = data if data and isinstance(data[0], dict) else [{"value": item} for item in data]
        render(rows, columns, ctx)
    elif isinstance(data, dict):
        render_detail(data, ctx)
    else:
        typer.echo(str(data))


def _validate_format(value: str) -> str:
    if value not in {"json", "table"}:
        typer.echo("Error: --format must be one of: json, table", err=True)
        raise typer.Exit(code=2)
    return value


def _line_item_payload(
    *,
    action: str,
    ad_unit_code: str,
    granularity: str,
    price_range: str,
    custom_buckets: str | None,
    sizes: str,
    creative_map: str | None,
    creative_map_file: str | None,
    priority: int,
    advertiser_id: int | None,
    order_id: int | None,
    currency: str,
    dry_run: bool,
    confirmation_token: str | None,
    on_conflict: str = "skip",
) -> dict[str, Any]:
    parsed_custom_buckets = _parse_csv_floats(custom_buckets)
    if granularity == "custom" and not parsed_custom_buckets:
        typer.echo("Error: --custom-buckets is required when --granularity=custom", err=True)
        raise typer.Exit(code=2)
    return {
        "action": action,
        "adUnitCode": ad_unit_code,
        "granularity": granularity,
        "priceRange": _parse_price_range(price_range),
        "customBuckets": parsed_custom_buckets,
        "sizes": _parse_csv_strings(sizes) or [],
        "creativeMap": _parse_creative_map(creative_map, creative_map_file),
        "priority": priority,
        "advertiserId": advertiser_id,
        "orderId": order_id,
        "currency": currency,
        "dryRun": dry_run,
        "confirmationToken": confirmation_token,
        "onConflict": on_conflict,
    }


@app.command("generate-line-items")
def generate_line_items(
    ad_unit_code: str = typer.Option(..., "--ad-unit-code"),
    granularity: str = typer.Option("med", "--granularity"),
    price_range: str = typer.Option("0.10,20.0", "--price-range"),
    custom_buckets: str | None = typer.Option(None, "--custom-buckets"),
    sizes: str = typer.Option(..., "--sizes"),
    creative_map: str | None = typer.Option(None, "--creative-map"),
    creative_map_file: str | None = typer.Option(None, "--creative-map-file"),
    priority: int = typer.Option(12, "--priority", min=1, max=16),
    advertiser_id: int | None = typer.Option(None, "--advertiser-id"),
    order_id: int | None = typer.Option(None, "--order-id"),
    currency: str = typer.Option("EUR", "--currency"),
    dry_run: bool = typer.Option(False, "--dry-run/--no-dry-run"),
    confirmation_token: str | None = typer.Option(None, "--confirmation-token"),
    fmt: str = typer.Option("json", "--format"),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    """Generate Prebid line items."""
    fmt = _validate_format(fmt)
    body = _line_item_payload(
        action="generate_line_items",
        ad_unit_code=ad_unit_code,
        granularity=granularity,
        price_range=price_range,
        custom_buckets=custom_buckets,
        sizes=sizes,
        creative_map=creative_map,
        creative_map_file=creative_map_file,
        priority=priority,
        advertiser_id=advertiser_id,
        order_id=order_id,
        currency=currency,
        dry_run=dry_run,
        confirmation_token=confirmation_token,
    )
    try:
        _render_result(get_client().post("/api/prebid/generate-line-items", json=body), fmt, output)
    except CliApiError as exc:
        handle_error(exc)


@app.command("generate-targeting-keys")
def generate_targeting_keys(
    schema: str = typer.Option("standard", "--schema"),
    prefix: str = typer.Option("hb_", "--prefix"),
    custom_keys: str | None = typer.Option(None, "--custom-keys"),
    dry_run: bool = typer.Option(False, "--dry-run/--no-dry-run"),
    fmt: str = typer.Option("json", "--format"),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    """Generate Prebid targeting keys."""
    fmt = _validate_format(fmt)
    parsed_custom_keys = _parse_csv_strings(custom_keys)
    if schema == "custom" and not parsed_custom_keys:
        typer.echo("Error: --custom-keys is required when --schema=custom", err=True)
        raise typer.Exit(code=2)
    body = {
        "action": "generate_targeting_keys",
        "schema": schema,
        "prefix": prefix,
        "customKeys": parsed_custom_keys,
        "dryRun": dry_run,
    }
    try:
        _render_result(get_client().post("/api/prebid/generate-targeting-keys", json=body), fmt, output)
    except CliApiError as exc:
        handle_error(exc)


@app.command("preview")
def preview(
    ad_unit_code: str = typer.Option(..., "--ad-unit-code"),
    granularity: str = typer.Option("med", "--granularity"),
    price_range: str = typer.Option("0.10,20.0", "--price-range"),
    custom_buckets: str | None = typer.Option(None, "--custom-buckets"),
    sizes: str = typer.Option(..., "--sizes"),
    creative_map: str | None = typer.Option(None, "--creative-map"),
    creative_map_file: str | None = typer.Option(None, "--creative-map-file"),
    priority: int = typer.Option(12, "--priority", min=1, max=16),
    advertiser_id: int | None = typer.Option(None, "--advertiser-id"),
    order_id: int | None = typer.Option(None, "--order-id"),
    currency: str = typer.Option("EUR", "--currency"),
    dry_run: bool = typer.Option(True, "--dry-run/--no-dry-run"),
    confirmation_token: str | None = typer.Option(None, "--confirmation-token"),
    on_conflict: str = typer.Option("skip", "--on-conflict"),
    fmt: str = typer.Option("json", "--format"),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    """Preview a Prebid line-item batch."""
    fmt = _validate_format(fmt)
    body = _line_item_payload(
        action="preview_batch",
        ad_unit_code=ad_unit_code,
        granularity=granularity,
        price_range=price_range,
        custom_buckets=custom_buckets,
        sizes=sizes,
        creative_map=creative_map,
        creative_map_file=creative_map_file,
        priority=priority,
        advertiser_id=advertiser_id,
        order_id=order_id,
        currency=currency,
        dry_run=dry_run,
        confirmation_token=confirmation_token,
        on_conflict=on_conflict,
    )
    try:
        _render_result(get_client().post("/api/prebid/preview", json=body), fmt, output)
    except CliApiError as exc:
        handle_error(exc)


@app.command("cleanup")
def cleanup(
    ad_unit_code: str = typer.Option(..., "--ad-unit-code"),
    order_id: int | None = typer.Option(None, "--order-id"),
    dry_run: bool = typer.Option(True, "--dry-run/--no-dry-run"),
    confirmation_token: str | None = typer.Option(None, "--confirmation-token"),
    fmt: str = typer.Option("json", "--format"),
    output: str | None = typer.Option(None, "--output"),
) -> None:
    """Preview or archive generated Prebid line items."""
    fmt = _validate_format(fmt)
    body = {
        "action": "cleanup",
        "adUnitCode": ad_unit_code,
        "orderId": order_id,
        "dryRun": dry_run,
        "confirmationToken": confirmation_token,
    }
    try:
        _render_result(get_client().post("/api/prebid/cleanup", json=body), fmt, output)
    except CliApiError as exc:
        handle_error(exc)
