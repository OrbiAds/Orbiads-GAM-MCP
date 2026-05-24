"""Explore GAM inventory."""

from __future__ import annotations

from typing import Optional

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import OutputContext, confirm, info, render, render_detail

app = typer.Typer(help="Explore GAM inventory", no_args_is_help=True)

_AD_UNIT_COLUMNS = ["id", "name", "sizes", "parentPath"]
_PLACEMENT_COLUMNS = ["id", "name", "adUnitCount"]
_KEY_COLUMNS = ["id", "name", "type", "valuesCount"]
_VALUE_COLUMNS = ["id", "name"]
_BP_TEMPLATE_COLUMNS = ["id", "name", "description", "icon"]
_BP_BUNDLE_COLUMNS = ["id", "name", "createdAt"]
_BP_POSITION_COLUMNS = ["id", "name", "label", "usageCount"]


@app.command("ad-units")
def ad_units(
    ctx: typer.Context,
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search by name"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List ad units."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        params: dict[str, str | int] = {"limit": limit}
        if search is not None:
            params["search"] = search
        data = client.get("/api/gam/ad-units", params=params)
        # Response may be a list or a dict with an "adUnits" / "results" key
        if isinstance(data, dict):
            items = data.get("adUnits", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        # Sizes may be a list of objects — join them as strings for display
        for item in items:
            sizes = item.get("sizes")
            if isinstance(sizes, list):
                item["sizes"] = ", ".join(
                    f"{s.get('width', '?')}x{s.get('height', '?')}"
                    if isinstance(s, dict) else str(s)
                    for s in sizes
                )
        render(items, _AD_UNIT_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def placements(
    ctx: typer.Context,
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List placements."""
    out: OutputContext = ctx.obj
    try:
        client = get_client()
        params: dict[str, str | int] = {"limit": limit}
        data = client.get("/api/gam/placements", params=params)
        if isinstance(data, dict):
            items = data.get("placements", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _PLACEMENT_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


@app.command()
def keys(
    ctx: typer.Context,
    key_id: Optional[str] = typer.Option(None, "--key-id", help="Targeting key ID"),
    values: bool = typer.Option(False, "--values", help="Show values for key"),
    limit: int = typer.Option(50, "--limit", "-l", help="Max results", min=1, max=500),
):
    """List custom targeting keys.

    Without --key-id: lists all targeting keys.
    With --key-id and --values: lists all values for that key.
    """
    out: OutputContext = ctx.obj
    try:
        client = get_client()

        if key_id and values:
            # Story 61.2 — `get_custom_targeting_values` is MCP-ONLY (no REST
            # route yet); the previous `/api/gam/targeting-keys/{id}/values`
            # path 404'd. Surfacing this honestly until Epic 62 adds the route.
            typer.echo(
                "orbiads inventory keys --values is not yet supported via REST "
                "(pending Epic 62 — get_custom_targeting_values route).",
                err=True,
            )
            raise typer.Exit(code=1)
        else:
            # List all targeting keys.
            # Story 61.2 — backend serves `/api/gam/custom-targeting-keys`
            # (network.py:268). The legacy `/api/gam/targeting-keys` path 404'd.
            params: dict[str, str | int] = {"limit": limit}
            data = client.get("/api/gam/custom-targeting-keys", params=params)
            if isinstance(data, dict):
                # CustomTargetingKeysResult.model_dump(by_alias=True) -> {"keys": [...]}
                # see backend/src/domain/gam_targeting.py:291-296.
                items = data.get("keys", data.get("results", []))
            else:
                items = data if isinstance(data, list) else []
            render(items, _KEY_COLUMNS, out)
    except CliApiError as e:
        handle_error(e)


# === Story 61.6 — REST-ONLY sweep (inventory + targeting + placements) ======


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


# ── ad-unit mutations ────────────────────────────────────────────────────


@app.command("save-adunits")
def save_adunits(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file: selectedAdUnitIds array"),
):
    """Save selected ad units (batch create/import)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units/save-adunits", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create-ad-units")
def create_ad_units(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help="JSON file containing a single ad-unit object OR a list of ad-unit objects.",
    ),
):
    """Create one or more ad units."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("import-ad-units")
def import_ad_units(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with {units: [...], dryRun: bool}"
    ),
    dry_run: Optional[bool] = typer.Option(
        None,
        "--dry-run/--no-dry-run",
        help="Override body's dryRun. If unset, the file's dryRun is used as-is.",
    ),
):
    """Bulk import ad units with dependency resolution."""
    payload = _load_json_payload(file)
    if dry_run is not None and isinstance(payload, dict):
        payload["dryRun"] = dry_run
    try:
        data = get_client().post("/api/gam/ad-units/import", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("update-ad-unit")
def update_ad_unit(
    ctx: typer.Context,
    ad_unit_id: str = typer.Argument(..., help="Ad unit ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with patch body"),
):
    """Update an ad unit (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/ad-units/{ad_unit_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("archive-ad-unit")
def archive_ad_unit(
    ctx: typer.Context,
    ad_unit_id: str = typer.Argument(..., help="Ad unit ID"),
):
    """Archive (soft-delete) an ad unit."""
    try:
        get_client().delete(f"/api/gam/ad-units/{ad_unit_id}")
        info(f"Ad unit {ad_unit_id} archived.")
    except CliApiError as e:
        handle_error(e)


@app.command()
def audit(
    ctx: typer.Context,
    file: str = typer.Option(None, "--file", "-f", help="Optional JSON body for the audit request"),
):
    """Run an inventory audit."""
    payload = _load_json_payload(file) if file else {}
    try:
        data = get_client().post("/api/gam/inventory/audit", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("ads-json")
def ads_json(ctx: typer.Context):
    """Fetch the ads.json manifest for the network."""
    try:
        data = get_client().get("/api/gam/inventory/manifest/ads.json")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# Inventory understanding and size mappings (Story 73.7) ----------------------
understanding_app = typer.Typer(
    help="Inventory understanding analyses", no_args_is_help=True
)
app.add_typer(understanding_app, name="understanding")

size_mappings_app = typer.Typer(
    help="Manage GAM responsive size mappings", no_args_is_help=True
)
app.add_typer(size_mappings_app, name="size-mappings")


@understanding_app.command("analyze")
def understanding_analyze(
    ctx: typer.Context,
    reuse_latest: bool = typer.Option(
        False,
        "--reuse-latest/--no-reuse-latest",
        help=(
            "Return the latest cached analysis if one exists. Default: run a "
            "fresh synchronous analysis, which can take several minutes on "
            "large GAM networks."
        ),
    ),
):
    """Run or reuse an inventory understanding analysis.

    Note: this call runs synchronously and can take several minutes on large
    GAM networks. Until Epic 71 ships an async pattern, use --reuse-latest for
    fast cached reads when possible.
    """
    try:
        data = get_client().post(
            "/api/gam/inventory/understanding/analyze",
            json={"reuseLatest": reuse_latest},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@understanding_app.command("latest")
def understanding_latest(ctx: typer.Context):
    """Return the most recent non-expired inventory analysis (Story 71.2).

    Reads the L1 in-process cache first, then falls back to the Firestore
    L2 cache that survives Cloud Run cold starts. Returns 404
    NO_LATEST_ANALYSIS if neither layer has a valid candidate.
    """
    try:
        data = get_client().get(
            "/api/gam/inventory/understanding/analyses/latest"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@understanding_app.command("get")
def understanding_get(
    ctx: typer.Context,
    analysis_id: str = typer.Argument(..., help="Analysis ID"),
):
    """Fetch a previously run inventory understanding analysis by ID."""
    try:
        data = get_client().get(
            f"/api/gam/inventory/understanding/analyses/{analysis_id}"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@size_mappings_app.command("create")
def size_mappings_create(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help='JSON file with {"adUnitId": "...", "mappings": [...]}',
    ),
):
    """Create a size mapping for an ad unit."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/size-mappings", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@size_mappings_app.command("get")
def size_mappings_get(
    ctx: typer.Context,
    ad_unit_id: str = typer.Argument(..., help="Ad unit ID"),
):
    """Get the size mapping for an ad unit."""
    try:
        data = get_client().get(f"/api/gam/inventory/size-mappings/{ad_unit_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@size_mappings_app.command("update")
def size_mappings_update(
    ctx: typer.Context,
    ad_unit_id: str = typer.Argument(..., help="Ad unit ID"),
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the mappings body"
    ),
):
    """Replace the size mapping for an ad unit."""
    payload = _load_json_payload(file)
    payload["adUnitId"] = ad_unit_id
    try:
        data = get_client().put(
            f"/api/gam/inventory/size-mappings/{ad_unit_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@size_mappings_app.command("delete")
def size_mappings_delete(
    ctx: typer.Context,
    ad_unit_id: str = typer.Argument(..., help="Ad unit ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Delete the size mapping for an ad unit."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Delete size mapping for {ad_unit_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().delete(f"/api/gam/inventory/size-mappings/{ad_unit_id}")
        info(f"Size mapping for {ad_unit_id} deleted.")
    except CliApiError as e:
        handle_error(e)


@app.command("health")
def inventory_health(
    ctx: typer.Context,
    period: str = typer.Option(
        "30d", "--period", help="Lookback window: 7d, 30d, or 90d"
    ),
):
    """Inventory health snapshot."""
    try:
        data = get_client().get("/api/gam/inventory/health", params={"period": period})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# Inventory blueprint sub-Typer (Story 73.6) ----------------------------------
blueprint_app = typer.Typer(help="Manage inventory blueprints", no_args_is_help=True)
app.add_typer(blueprint_app, name="blueprint")

bp_templates_app = typer.Typer(help="Browse blueprint templates", no_args_is_help=True)
blueprint_app.add_typer(bp_templates_app, name="templates")

bp_bundles_app = typer.Typer(help="Manage size bundles", no_args_is_help=True)
blueprint_app.add_typer(bp_bundles_app, name="size-bundles")

bp_positions_app = typer.Typer(help="Manage custom positions", no_args_is_help=True)
blueprint_app.add_typer(bp_positions_app, name="custom-positions")


@blueprint_app.command("validate")
def blueprint_validate(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the blueprint to validate"
    ),
):
    """Validate a blueprint against best-practice rules."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/blueprint/validate", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@blueprint_app.command("export")
def blueprint_export(
    ctx: typer.Context,
    file: str = typer.Option(
        ...,
        "--file",
        "-f",
        help='JSON file with {"blueprint": {...}, "format": "json"|"csv"|"gam_batch"}',
    ),
):
    """Export a blueprint to JSON, CSV, or GAM Batch."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/blueprint/export", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_templates_app.command("list")
def bp_templates_list(ctx: typer.Context):
    """List predefined blueprint templates."""
    try:
        data = get_client().get("/api/gam/inventory/blueprint/templates")
        if isinstance(data, dict):
            items = data.get("templates", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _BP_TEMPLATE_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_templates_app.command("get")
def bp_templates_get(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
):
    """Fetch a blueprint template by ID."""
    try:
        data = get_client().get(f"/api/gam/inventory/blueprint/templates/{template_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_bundles_app.command("list")
def bp_bundles_list(ctx: typer.Context):
    """List size bundles."""
    try:
        data = get_client().get("/api/gam/inventory/blueprint/size-bundles")
        if isinstance(data, dict):
            items = data.get("sizeBundles", data.get("bundles", data.get("results", [])))
        else:
            items = data if isinstance(data, list) else []
        render(items, _BP_BUNDLE_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_bundles_app.command("create")
def bp_bundles_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the bundle body"),
):
    """Create a size bundle."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            "/api/gam/inventory/blueprint/size-bundles", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_bundles_app.command("delete")
def bp_bundles_delete(
    ctx: typer.Context,
    bundle_id: str = typer.Argument(..., help="Bundle ID"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    """Delete a size bundle."""
    out: OutputContext = ctx.obj
    effective_ctx = OutputContext(format=out.format, yes=out.yes or yes)
    if not confirm(f"Delete size bundle {bundle_id}?", effective_ctx):
        raise typer.Exit(code=0)
    try:
        get_client().delete(f"/api/gam/inventory/blueprint/size-bundles/{bundle_id}")
        info(f"Size bundle {bundle_id} deleted.")
    except CliApiError as e:
        handle_error(e)


@blueprint_app.command("recalculate-sizes")
def blueprint_recalculate_sizes(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the blueprint / selector body"
    ),
):
    """Recalculate sizes for a blueprint."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            "/api/gam/inventory/blueprint/recalculate-sizes", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_positions_app.command("list")
def bp_positions_list(ctx: typer.Context):
    """List custom positions."""
    try:
        data = get_client().get("/api/gam/inventory/blueprint/custom-positions")
        if isinstance(data, dict):
            items = data.get(
                "customPositions", data.get("positions", data.get("results", []))
            )
        else:
            items = data if isinstance(data, list) else []
        render(items, _BP_POSITION_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@bp_positions_app.command("create")
def bp_positions_create(
    ctx: typer.Context,
    file: str = typer.Option(
        ..., "--file", "-f", help="JSON file with the custom position body"
    ),
):
    """Create a custom position."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post(
            "/api/gam/inventory/blueprint/custom-positions", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("blueprint-generate")
def blueprint_generate(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the blueprint request"),
):
    """Generate an inventory blueprint (dry run)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/blueprint/generate", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("blueprint-push")
def blueprint_push(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the blueprint to push"),
):
    """Push an inventory blueprint to GAM."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/blueprint/push", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── targeting / forecast / reference data ────────────────────────────────


@app.command("validate-fluid")
def validate_fluid(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with adUnitIds[] + jobId"),
):
    """Validate that the selected ad units support Fluid sizing."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units/validate-fluid", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("validate-fluid-batch")
def validate_fluid_batch(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with {adUnitIds: [...]}"),
):
    """Batch-validate Fluid ad-unit compatibility."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units/validate-fluid-batch", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def forecast(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the forecast request"),
):
    """Run an inventory forecast (line-item probabilistic delivery)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/inventory/forecast", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def countries(ctx: typer.Context):
    """List available geo-targets (countries)."""
    try:
        data = get_client().get("/api/gam/geo-targets")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("device-categories")
def device_categories(ctx: typer.Context):
    """List available device categories."""
    try:
        data = get_client().get("/api/gam/device-categories")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── custom targeting key mutations ───────────────────────────────────────


@app.command("technology-targets")
def technology_targets(
    ctx: typer.Context,
    target_type: str = typer.Option(..., "--type", help="Target type: device, os, browser"),
):
    """List available technology targets."""
    try:
        data = get_client().get("/api/gam/technology-targets", params={"type": target_type})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("create-key")
def create_key(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the key body"),
):
    """Create a custom targeting key."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/custom-targeting-keys", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("update-key")
def update_key(
    ctx: typer.Context,
    key_id: str = typer.Argument(..., help="Custom targeting key ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a custom targeting key (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(
            f"/api/gam/custom-targeting-keys/{key_id}", json=payload
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("delete-key")
def delete_key(
    ctx: typer.Context,
    key_id: str = typer.Argument(..., help="Custom targeting key ID"),
):
    """Delete a custom targeting key."""
    try:
        get_client().delete(f"/api/gam/custom-targeting-keys/{key_id}")
        info(f"Custom targeting key {key_id} deleted.")
    except CliApiError as e:
        handle_error(e)


# ── placement mutations ──────────────────────────────────────────────────


@app.command("placement-update")
def placement_update(
    ctx: typer.Context,
    placement_id: str = typer.Argument(..., help="Placement ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the patch body"),
):
    """Update a placement (PATCH)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().patch(f"/api/gam/placements/{placement_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("placement-archive")
def placement_archive(
    ctx: typer.Context,
    placement_id: str = typer.Argument(..., help="Placement ID"),
):
    """Archive a placement."""
    try:
        get_client().delete(f"/api/gam/placements/{placement_id}")
        info(f"Placement {placement_id} archived.")
    except CliApiError as e:
        handle_error(e)


# === Story 62.5 — inventory residual + new placement create + targeting search ===


@app.command("placement-create")
def placement_create(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the placement body"),
):
    """Create a placement."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/placements", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("search-ad-units")
def search_ad_units(
    ctx: typer.Context,
    q: str = typer.Option(..., "--query", "-q", help="Search query"),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
    offset: int = typer.Option(0, "--offset", min=0),
):
    """Search ad units by name/code."""
    try:
        data = get_client().get(
            "/api/gam/ad-units/search",
            params={"q": q, "limit": limit, "offset": offset},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("ad-units-by-ids")
def ad_units_by_ids(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file: {adUnitIds: [...]}"),
):
    """Bulk-fetch ad units by ID."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units/by-ids", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def sizes(ctx: typer.Context):
    """List all distinct ad-unit sizes in the network."""
    try:
        data = get_client().get("/api/gam/ad-units/sizes")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("search-custom-targeting")
def search_custom_targeting(
    ctx: typer.Context,
    q: str = typer.Option(..., "--query", "-q", help="Search query (keys + values)"),
):
    """Search custom-targeting keys + values by name."""
    try:
        data = get_client().get("/api/gam/custom-targeting/search", params={"q": q})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def languages(
    ctx: typer.Context,
    q: str = typer.Option(None, "--query", "-q"),
    limit: int = typer.Option(50, "--limit", "-l", min=1, max=500),
):
    """List available targeting languages."""
    params: dict[str, str | int] = {"limit": limit}
    if q:
        params["q"] = q
    try:
        data = get_client().get("/api/gam/languages", params=params)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 62.5a — find/archive inactive ad-units (InventoryService unblocked) ===


@app.command("list-inactive")
def list_inactive(
    ctx: typer.Context,
    days: int = typer.Option(90, "--days", "-d", min=1, max=365, help="Look-back window in days"),
):
    """List ad units with zero impressions in the last N days (Story 62.5a)."""
    try:
        data = get_client().get("/api/gam/ad-units/inactive", params={"days": days})
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("archive-inactive")
def archive_inactive(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with {adUnitIds: [...]}"),
):
    """Archive a batch of inactive ad units (Story 62.5a)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/ad-units/archive-inactive", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
