"""Manage GAM creatives."""

from __future__ import annotations

import json as _json
import mimetypes
import os
import re
from typing import Any

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, render, render_detail, success

app = typer.Typer(help="Manage GAM creatives", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "type", "size", "status"]

_EXT_TO_TYPE: dict[str, str] = {
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".gif": "image",
    ".svg": "image",
    ".zip": "html5",
    ".mp4": "video",
    ".webm": "video",
    ".mov": "video",
    ".qt": "video",
    ".mp3": "audio",
    ".ogg": "audio",
    ".aac": "audio",
}

_SIZE_RE = re.compile(r"^(\d+)x(\d+)$", re.IGNORECASE)


def _auto_detect_type(path: str) -> str | None:
    ext = os.path.splitext(path)[1].lower()
    return _EXT_TO_TYPE.get(ext)


def _parse_size(value: str | None) -> str | None:
    """Convert WxH input to the JSON string expected by the multipart route."""
    if not value:
        return None
    match = _SIZE_RE.match(value.strip())
    if not match:
        typer.echo(f"Error: --size must be WxH (e.g. 300x250), got: {value}", err=True)
        raise typer.Exit(code=2)
    return _json.dumps(
        {"width": int(match.group(1)), "height": int(match.group(2))},
        separators=(",", ":"),
    )


def _format_dry_run_fields(fields: dict[str, str]) -> str:
    parts: list[str] = []
    for key, value in fields.items():
        display = _json.dumps(value) if key == "name" else value
        parts.append(f"{key}={display}")
    return " ".join(parts)


def _compute_transcode_status(creative: dict[str, Any]) -> dict[str, Any]:
    creative_type = creative.get("creativeType") or creative.get("type") or ""
    status = creative.get("status")
    vast_preview_url = creative.get("vastPreviewUrl") or creative.get("vast_preview_url")
    error = creative.get("lastError") or creative.get("error")
    if creative_type not in {"VideoCreative", "AudioCreative", "VIDEO", "AUDIO"}:
        return {
            "status": "INVALID_CREATIVE_TYPE",
            "message": f"Creative type {creative_type or '<unknown>'} is not VIDEO/AUDIO.",
            "vastPreviewUrl": None,
        }
    if error:
        return {"status": "FAILED", "message": str(error), "vastPreviewUrl": vast_preview_url}
    if vast_preview_url:
        return {
            "status": "READY",
            "message": "Transcode complete.",
            "vastPreviewUrl": vast_preview_url,
        }
    if creative_type in {"AudioCreative", "AUDIO"} and status == "ACTIVE":
        return {
            "status": "READY",
            "message": "Audio creative is active.",
            "vastPreviewUrl": None,
        }
    return {
        "status": "PROCESSING",
        "message": f"Transcode in progress (status={status or 'unknown'}).",
        "vastPreviewUrl": None,
    }


def _check_file(p: str) -> None:
    if not os.path.isfile(p):
        typer.echo(f"Error: file not found: {p}", err=True)
        raise typer.Exit(code=2)


def _post_many_files(client, path: str, file_paths: list[str], field_name: str = "files"):
    """POST multipart with N files under the same field name."""
    items, handles = [], []
    try:
        for fp in file_paths:
            ctype, _ = mimetypes.guess_type(fp)
            ctype = ctype or "application/octet-stream"
            fh = open(fp, "rb")
            handles.append(fh)
            items.append((field_name, (os.path.basename(fp), fh, ctype)))
        return client._request("POST", path, files=items)
    finally:
        for fh in handles:
            fh.close()


@app.command("list")
def list_creatives(
    ctx: typer.Context,
    advertiser_id: str = typer.Option(
        ..., "--advertiser-id", "-a", help="GAM advertiser (company) ID to list creatives for"
    ),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=200),
):
    """List creatives for an advertiser.

    Audit F0-3: the previous implementation called the non-existent
    ``/api/gam/creatives`` collection endpoint and always 404'd. The backend
    only exposes creatives scoped to an advertiser, so ``--advertiser-id`` is
    now required.
    """
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get(
            f"/api/gam/advertisers/{advertiser_id}/creatives",
            params={"limit": limit},
        )
        if isinstance(data, dict):
            items = data.get("creatives", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def get(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
):
    """Get creative details."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        data = client.get(f"/api/gam/creatives/{creative_id}")
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def upload(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the creative asset (PNG/JPG/GIF/ZIP/MP4/MP3)"),
    name: str = typer.Option(..., "--name", "-n", help="Creative display name"),
    advertiser_id: int = typer.Option(
        ..., "--advertiser-id", "-a", help="GAM advertiser (company) ID"
    ),
    creative_type: str | None = typer.Option(
        None,
        "--type",
        help=(
            "image | html5 | native | video | audio (auto-detected from extension if omitted; "
            "native requires --metadata)"
        ),
    ),
    size: str | None = typer.Option(
        None,
        "--size",
        help="Creative size as WxH (e.g. 300x250). Required for IMAGE.",
    ),
    destination_url: str | None = typer.Option(
        None, "--destination-url", help="Click-through URL (IMAGE/NATIVE)"
    ),
    metadata: str | None = typer.Option(
        None,
        "--metadata",
        help='NATIVE only - JSON: {"template_id": int, "headline": str, "body": str, ...}',
    ),
    duration_ms: int | None = typer.Option(
        None,
        "--duration-ms",
        help="Required for VIDEO/AUDIO, e.g. 30000 for a 30s clip",
        min=1,
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Print the planned request without hitting the network"
    ),
):
    """Stream a creative asset directly to GAM.

    This replaces the Story 61.3 legacy job-pipeline upload stub.
    """
    out: OutputContext = ctx.obj
    _check_file(file)

    resolved_type = (creative_type or "").lower() or _auto_detect_type(file)
    if not resolved_type:
        typer.echo(
            f"Error: cannot auto-detect creative type for '{file}'. "
            "Pass --type explicitly (image | html5 | native | video | audio).",
            err=True,
        )
        raise typer.Exit(code=2)

    size_json = _parse_size(size)
    if resolved_type == "image" and not size_json:
        typer.echo(
            "Error: --size is required for IMAGE creatives (e.g. --size 300x250)",
            err=True,
        )
        raise typer.Exit(code=2)
    if resolved_type == "video" and not size_json:
        typer.echo(
            "Error: --size is required for VIDEO creatives (e.g. --size 1280x720)",
            err=True,
        )
        raise typer.Exit(code=2)
    if resolved_type in {"video", "audio"} and duration_ms is None:
        typer.echo(
            "Error: --duration-ms is required for VIDEO/AUDIO creatives",
            err=True,
        )
        raise typer.Exit(code=2)
    if resolved_type == "native" and not metadata:
        typer.echo(
            "Error: --metadata is required for NATIVE creatives "
            '(e.g. --metadata \'{"template_id":789,"headline":"Buy Now"}\')',
            err=True,
        )
        raise typer.Exit(code=2)
    if metadata:
        try:
            _json.loads(metadata)
        except _json.JSONDecodeError as exc:
            typer.echo(f"Error: invalid --metadata JSON: {exc}", err=True)
            raise typer.Exit(code=2) from exc

    fields: dict[str, str] = {
        "advertiser_id": str(advertiser_id),
        "name": name,
        "type": resolved_type.upper(),
    }
    if size_json:
        fields["size"] = size_json
    if destination_url:
        fields["destination_url"] = destination_url
    if metadata:
        fields["metadata"] = metadata
    if duration_ms is not None:
        fields["duration_ms"] = str(duration_ms)

    content_type, _ = mimetypes.guess_type(file)
    content_type = content_type or "application/octet-stream"
    filename = os.path.basename(file)
    size_bytes = os.path.getsize(file)

    if dry_run:
        typer.echo("[dry-run] POST /api/gam/creatives/upload", err=True)
        typer.echo(f"[dry-run] file: {filename} ({size_bytes} bytes, {content_type})", err=True)
        typer.echo(f"[dry-run] fields: {_format_dry_run_fields(fields)}", err=True)
        raise typer.Exit(code=0)

    try:
        client = get_client()
        with open(file, "rb") as fh:
            # Keep client.post() and the literal /api/gam path visible to the
            # AST route-parity guard; post_multipart() is intentionally avoided.
            data = client.post(
                "/api/gam/creatives/upload",
                files={"file": (filename, fh, content_type)},
                data=fields,
            )
        render_detail(data, out)
        if data.get("status") == "PENDING_TRANSCODE" and data.get("creativeId"):
            typer.echo(
                "Transcode in progress - poll with "
                f"`orbiads creatives transcode-status {data['creativeId']}` "
                "(5-15 min typical).",
                err=True,
            )
    except CliApiError as e:
        handle_error(e)


@app.command("transcode-status")
def transcode_status(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="GAM video/audio creative ID"),
):
    """Poll hosted video/audio transcode status."""
    out: OutputContext = ctx.obj
    try:
        data = get_client().get(f"/api/gam/creatives/{creative_id}")
        creative = data.get("data", data) if isinstance(data, dict) else {}
        render_detail(_compute_transcode_status(creative), out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def register(
    ctx: typer.Context,
    creative_type: str = typer.Option(..., "--type", help="VIDEO or AUDIO"),
    advertiser_id: int = typer.Option(..., "--advertiser-id", "-a", help="GAM advertiser ID"),
    name: str = typer.Option(..., "--name", "-n", help="Creative display name"),
    vast_url: str = typer.Option(..., "--vast-url", help="VAST 3/4 XML URL"),
    size: str | None = typer.Option(
        None, "--size", help="Size WxH (default 640x360 for VIDEO)"
    ),
    duration_ms: int = typer.Option(
        30000, "--duration-ms", help="Duration in milliseconds", min=1
    ),
    dry_run: bool = typer.Option(False, "--dry-run"),
):
    """Register a VIDEO or AUDIO creative via VAST redirect URL."""
    out: OutputContext = ctx.obj
    resolved_type = creative_type.upper()
    if resolved_type not in {"VIDEO", "AUDIO"}:
        typer.echo(f"Error: --type must be VIDEO or AUDIO, got: {creative_type}", err=True)
        raise typer.Exit(code=2)

    body: dict[str, Any] = {
        "type": resolved_type,
        "advertiserId": advertiser_id,
        "name": name,
        "vastRedirectUrl": vast_url,
        "durationMs": duration_ms,
    }
    if size:
        match = _SIZE_RE.match(size.strip())
        if not match:
            typer.echo(f"Error: --size must be WxH (e.g. 640x360), got: {size}", err=True)
            raise typer.Exit(code=2)
        body["size"] = {"width": int(match.group(1)), "height": int(match.group(2))}

    if dry_run:
        typer.echo("[dry-run] POST /api/gam/creatives/upload/register", err=True)
        typer.echo(f"[dry-run] body: {_json.dumps(body, sort_keys=True)}", err=True)
        raise typer.Exit(code=0)

    try:
        data = get_client().post("/api/gam/creatives/upload/register", json=body)
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-url")
def upload_url(
    ctx: typer.Context,
    asset_url: str = typer.Argument(..., help="Public http(s) URL of the creative asset"),
    name: str = typer.Option(..., "--name", "-n", help="Creative display name"),
    advertiser_id: int = typer.Option(..., "--advertiser-id", "-a", help="GAM advertiser ID"),
    creative_type: str | None = typer.Option(
        None,
        "--type",
        help="image | html5 | native (auto-detected from Content-Type if omitted)",
    ),
    size: str | None = typer.Option(None, "--size", help="Size WxH (required for IMAGE)"),
    destination_url: str | None = typer.Option(None, "--destination-url"),
    metadata: str | None = typer.Option(
        None,
        "--metadata",
        help='NATIVE only - JSON: {"template_id": int, "headline": str, ...}',
    ),
    dry_run: bool = typer.Option(False, "--dry-run"),
):
    """Fetch a remote asset URL server-side and create a GAM creative."""
    out: OutputContext = ctx.obj
    if not (asset_url.startswith("http://") or asset_url.startswith("https://")):
        typer.echo(f"Error: --asset-url must be http(s):// URL (got: {asset_url})", err=True)
        raise typer.Exit(code=2)

    body: dict[str, Any] = {
        "assetUrl": asset_url,
        "advertiserId": advertiser_id,
        "name": name,
    }
    if creative_type:
        resolved_type = creative_type.upper()
        if resolved_type not in {"IMAGE", "HTML5", "NATIVE"}:
            typer.echo(
                f"Error: --type must be image|html5|native (got: {creative_type}). "
                "For VIDEO/AUDIO use `creatives register --type VIDEO|AUDIO --vast-url ...`.",
                err=True,
            )
            raise typer.Exit(code=2)
        body["type"] = resolved_type
    if size:
        match = _SIZE_RE.match(size.strip())
        if not match:
            typer.echo(f"Error: --size must be WxH (e.g. 300x250), got: {size}", err=True)
            raise typer.Exit(code=2)
        body["size"] = {"width": int(match.group(1)), "height": int(match.group(2))}
    if destination_url:
        body["destinationUrl"] = destination_url
    if metadata:
        try:
            body["metadata"] = _json.loads(metadata)
        except _json.JSONDecodeError as exc:
            typer.echo(f"Error: invalid --metadata JSON: {exc}", err=True)
            raise typer.Exit(code=2) from exc

    if dry_run:
        typer.echo("[dry-run] POST /api/gam/creatives/upload/from-url", err=True)
        typer.echo(f"[dry-run] body: {_json.dumps(body, sort_keys=True)}", err=True)
        raise typer.Exit(code=0)

    try:
        data = get_client().post("/api/gam/creatives/upload/from-url", json=body)
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-third-party")
def upload_third_party(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the third-party tag asset"),
):
    """Upload a third-party creative tag."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-third-party", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-html5")
def upload_html5(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the HTML5 .zip bundle"),
):
    """Upload an HTML5 bundle (covers 3 MCP variants via capability parity)."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-html5", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-video")
def upload_video(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the video asset"),
):
    """Upload a video creative."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-video", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-audio")
def upload_audio(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the audio asset"),
):
    """Upload an audio creative."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-audio", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-images")
def upload_images(
    ctx: typer.Context,
    files: list[str] = typer.Argument(..., help="One or more image files"),
):
    """Upload one or more image creatives (bulk)."""
    for fp in files:
        _check_file(fp)
    try:
        data = _post_many_files(get_client(), "/api/creatives/upload-images", files)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-native-classic")
def upload_native_classic(
    ctx: typer.Context,
    main_image: str = typer.Option(..., "--main-image", help="Main image file"),
    logo: str = typer.Option(None, "--logo", help="Optional logo file"),
):
    """Upload a classic native creative (main image + optional logo)."""
    _check_file(main_image)
    handles = []
    try:
        ct, _ = mimetypes.guess_type(main_image)
        fh = open(main_image, "rb")
        handles.append(fh)
        files = [("main_image", (os.path.basename(main_image), fh, ct or "application/octet-stream"))]
        if logo:
            _check_file(logo)
            ctl, _ = mimetypes.guess_type(logo)
            fhl = open(logo, "rb")
            handles.append(fhl)
            files.append(("logo", (os.path.basename(logo), fhl, ctl or "application/octet-stream")))
        data = get_client()._request("POST", "/api/creatives/upload-native-classic", files=files)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
    finally:
        for fh in handles:
            fh.close()


@app.command("list-by-line-item")
def list_by_line_item(
    ctx: typer.Context,
    line_item_id: str = typer.Argument(..., help="Line item ID"),
):
    """List creatives attached to a line item."""
    try:
        data = get_client().get(f"/api/gam/line-items/{line_item_id}/creatives")
        if isinstance(data, dict):
            items = data.get("creatives", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "type", "size"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


@app.command()
def update(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a creative (PATCH /api/gam/creatives/{id})."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/creatives/{creative_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def archive(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Archive (deactivate) a creative; reversible via the GAM UI."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Archive creative {creative_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().post(f"/api/gam/creatives/{creative_id}/archive")
        success(f"Creative {creative_id} archived.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def duplicate(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Duplicate a creative (POST /api/gam/creatives/{id}/duplicate)."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Duplicate creative {creative_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        data = get_client().post(f"/api/gam/creatives/{creative_id}/duplicate")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("preview-url")
def preview_url(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
):
    """Get the preview URL for a creative."""
    try:
        data = get_client().get(f"/api/gam/creatives/{creative_id}/preview-url")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("native-style-previews")
def native_style_previews(
    ctx: typer.Context,
    creative_id: str = typer.Argument(..., help="Creative ID"),
):
    """Get native-style preview URLs for a creative."""
    try:
        data = get_client().get(
            f"/api/gam/creatives/{creative_id}/native-style-previews"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("list-by-network")
def list_by_network(
    ctx: typer.Context,
    query: str = typer.Option(None, "--query", "-q", help="Optional name search"),
    limit: int = typer.Option(100, "--limit", "-l", help="Max results", min=1, max=500),
    offset: int = typer.Option(0, "--offset", help="Pagination offset", min=0),
):
    """Search all creatives in the GAM network by name (paginated)."""
    try:
        params: dict = {"limit": limit, "offset": offset}
        if query:
            params["q"] = query
        data = get_client().get("/api/gam/creatives", params=params)
        if isinstance(data, dict):
            items = data.get("items", data.get("creatives", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _LIST_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-vast-redirect")
def upload_vast_redirect(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the VAST redirect XML/JSON payload"),
):
    """Upload a VAST redirect creative (multipart)."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-vast-redirect", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("upload-companion")
def upload_companion(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the companion banner asset"),
):
    """Upload a companion creative (multipart)."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/upload-companion", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("compress-image")
def compress_image(
    ctx: typer.Context,
    file: str = typer.Argument(..., help="Path to the image to compress"),
):
    """Compress an image creative (multipart)."""
    _check_file(file)
    try:
        data = get_client().post_multipart("/api/creatives/compress-image", file)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
