"""Manage GAM creatives."""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, info, render, render_detail, success

app = typer.Typer(help="Manage GAM creatives", no_args_is_help=True)

_LIST_COLUMNS = ["id", "name", "type", "size", "status"]


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
    file: str = typer.Argument(..., help="Path to the creative file to upload"),
):
    """Upload a single creative file — Story 61.3.

    Replaces the previous "use MCP" stub (audit F0-3) with a real multipart
    POST to ``/api/creatives/upload-single`` (backend creatives.py:302).
    The backend enforces extension allow-list and a 5MB size limit.

    Sibling upload routes exist for HTML5 / video / audio / image / native /
    third-party — those verbs will land with Stories 61.4-61.7.
    """
    import os

    out: OutputContext = ctx.obj
    if not os.path.isfile(file):
        typer.echo(f"Error: file not found: {file}", err=True)
        raise typer.Exit(code=2)
    try:
        client = get_client()
        data = client.post_multipart("/api/creatives/upload-single", file)
        render_detail(data, out)
    except CliApiError as e:
        handle_error(e)


# === Story 61.7 — upload variants + list-by-line-item ======================


def _check_file(p: str) -> None:
    if not os.path.isfile(p):
        typer.echo(f"Error: file not found: {p}", err=True)
        raise typer.Exit(code=2)


def _post_many_files(client, path: str, file_paths: list[str], field_name: str = "files"):
    """POST multipart with N files under the same field name."""
    import mimetypes
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
    import mimetypes
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
        from orbiads_cli.output import render
        render(items, ["id", "name", "type", "size"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.1 — creatives Tier B (update/archive/duplicate/preview/list) ==


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
    """Archive (deactivate) a creative — reversible via the GAM UI."""
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
