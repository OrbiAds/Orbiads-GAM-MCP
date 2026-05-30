"""Manage tenant settings — Story 61.7 (REST-ONLY sweep).

Maps the 9 REST-ONLY settings MCP tools to thin CLI commands under the
`settings` noun (the existing `config_cmd.py` handles LOCAL CLI config only —
this module handles server-side tenant settings).
"""

from __future__ import annotations

import json as _json
import os

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, info, render, render_detail

app = typer.Typer(help="Manage tenant settings (Story 61.7)", no_args_is_help=True)


def _load_json_payload(path: str) -> dict:
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return _json.loads(open(path, "r", encoding="utf-8").read())
    except _json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


# ── presets ────────────────────────────────────────────────────────────────
presets_app = typer.Typer(help="Manage delivery presets", no_args_is_help=True)
app.add_typer(presets_app, name="presets")


@presets_app.command("list")
def presets_list(ctx: typer.Context):
    """List presets."""
    try:
        data = get_client().get("/api/settings/presets")
        if isinstance(data, dict):
            items = data.get("presets", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, ["id", "name", "type"], ctx.obj)
    except CliApiError as e:
        handle_error(e)


@presets_app.command("create")
def presets_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the preset body"),
):
    """Create a preset."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/settings/presets", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@presets_app.command("update")
def presets_update(
    ctx: typer.Context,
    preset_id: str = typer.Argument(..., help="Preset ID"),
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file with the partial update body (name and/or config)",
    ),
):
    """Update an existing preset (partial: name and/or config).

    Story 83-4-9 — closes the MCP/CLI gap (REST endpoint was already shipped).
    """
    payload = _load_json_payload(file)
    try:
        data = get_client().put(f"/api/settings/presets/{preset_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@presets_app.command("delete")
def presets_delete(
    ctx: typer.Context,
    preset_id: str = typer.Argument(..., help="Preset ID"),
):
    """Delete a preset."""
    try:
        get_client().delete(f"/api/settings/presets/{preset_id}")
        info(f"Preset {preset_id} deleted.")
    except CliApiError as e:
        handle_error(e)


# ── general / naming / delivery-defaults — explicit get+set sub-Typers ────
# These are inlined (rather than built by a factory) so the parity-matrix
# generator's AST parser can statically detect every sub-command.

# general
general_app = typer.Typer(help="Manage tenant general settings", no_args_is_help=True)
app.add_typer(general_app, name="general")


@general_app.command("get")
def general_get(ctx: typer.Context):
    """Get tenant general settings."""
    try:
        data = get_client().get("/api/settings/general")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@general_app.command("set")
def general_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the full body"),
):
    """Replace tenant general settings (PUT)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/settings/general", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# naming
naming_app = typer.Typer(help="Manage naming conventions", no_args_is_help=True)
app.add_typer(naming_app, name="naming")


@naming_app.command("get")
def naming_get(ctx: typer.Context):
    """Get naming conventions."""
    try:
        data = get_client().get("/api/settings/naming")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@naming_app.command("set")
def naming_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the full body"),
):
    """Replace naming conventions (PUT)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/settings/naming", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# delivery-defaults
delivery_defaults_app = typer.Typer(help="Manage delivery defaults", no_args_is_help=True)
app.add_typer(delivery_defaults_app, name="delivery-defaults")


@delivery_defaults_app.command("get")
def delivery_defaults_get(ctx: typer.Context):
    """Get delivery defaults."""
    try:
        data = get_client().get("/api/settings/delivery-defaults")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@delivery_defaults_app.command("set")
def delivery_defaults_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the full body"),
):
    """Replace delivery defaults (PUT)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/settings/delivery-defaults", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# GAM preferences
gam_preferences_app = typer.Typer(help="Manage saved GAM targeting preferences", no_args_is_help=True)
app.add_typer(gam_preferences_app, name="gam-preferences")


@gam_preferences_app.command("get")
def gam_preferences_get(ctx: typer.Context):
    """Get saved GAM targeting preferences."""
    try:
        data = get_client().get("/api/gam/preferences")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@gam_preferences_app.command("set")
def gam_preferences_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the GAM preferences body"),
):
    """Replace saved GAM targeting preferences."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/gam/preferences", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# segmentation
segmentation_app = typer.Typer(help="Manage segmentation preferences", no_args_is_help=True)
app.add_typer(segmentation_app, name="segmentation")


@segmentation_app.command("get")
def segmentation_get(ctx: typer.Context):
    """Get segmentation preferences."""
    try:
        data = get_client().get("/api/gam/segmentation-preferences")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@segmentation_app.command("set")
def segmentation_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the segmentation preferences body"),
):
    """Replace segmentation preferences."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/gam/segmentation-preferences", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# format-keys
format_keys_app = typer.Typer(help="Manage GAM format-key config", no_args_is_help=True)
app.add_typer(format_keys_app, name="format-keys")


@format_keys_app.command("get")
def format_keys_get(ctx: typer.Context):
    """Get GAM format-key config."""
    try:
        data = get_client().get("/api/gam/format-keys-config")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@format_keys_app.command("set")
def format_keys_set(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the format-key config body"),
):
    """Replace GAM format-key config."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put("/api/gam/format-keys-config", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
