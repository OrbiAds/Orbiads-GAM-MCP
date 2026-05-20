"""Manage GAM advertisers."""

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
    import json as _json, os
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
