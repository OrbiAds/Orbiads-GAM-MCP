"""Run and export reports."""

import json
import sys

import typer

from orbiads_cli.client import CliApiError, get_client
from orbiads_cli.errors import handle_error
from orbiads_cli.output import render, render_detail, info

app = typer.Typer(help="Run and export reports", no_args_is_help=True)


@app.command()
def run(
    ctx: typer.Context,
    dimensions: str = typer.Option(..., "--dimensions", help="Comma-separated dimensions (e.g. DATE,AD_UNIT_NAME)"),
    metrics: str = typer.Option(..., "--metrics", help="Comma-separated metrics (e.g. IMPRESSIONS,CLICKS)"),
    start: str = typer.Option(..., "--start", help="Start date YYYY-MM-DD"),
    end: str = typer.Option(..., "--end", help="End date YYYY-MM-DD"),
):
    """Run a custom report."""
    try:
        client = get_client()
        dim_list = [d.strip() for d in dimensions.split(",") if d.strip()]
        met_list = [m.strip() for m in metrics.split(",") if m.strip()]

        data = client.post(
            "/api/gam/reports/custom",
            json={
                "dimensions": dim_list,
                "metrics": met_list,
                "startDate": start,
                "endDate": end,
            },
        )

        # The API returns a report result with headers and rows
        if isinstance(data, dict):
            rows = data.get("rows", [])
            headers = data.get("headers", dim_list + met_list)
            if rows:
                render(rows, headers, ctx.obj)
            else:
                render_detail(data, ctx.obj)
        elif isinstance(data, list):
            columns = dim_list + met_list
            render(data, columns, ctx.obj)
        else:
            info("No results returned.")
    except CliApiError as e:
        handle_error(e)


# === Story 61.5 — REST-ONLY sweep (reporting setup) =========================
# Helpers shared across the new templates / gam-reports / catalogue verbs.


def _load_json_payload(path: str) -> dict:
    import os
    if not os.path.isfile(path):
        typer.echo(f"Error: file not found: {path}", err=True)
        raise typer.Exit(code=2)
    try:
        return json.loads(open(path, "r", encoding="utf-8").read())
    except json.JSONDecodeError as e:
        typer.echo(f"Error: invalid JSON in {path}: {e}", err=True)
        raise typer.Exit(code=2)


# ── reporting templates sub-group (6 verbs) ────────────────────────────────
templates_app = typer.Typer(help="Manage report templates (Story 61.5)", no_args_is_help=True)
app.add_typer(templates_app, name="templates")

_TEMPLATE_LIST_COLUMNS = ["id", "name", "updatedAt"]


@templates_app.command("list")
def templates_list(ctx: typer.Context):
    """List report templates."""
    try:
        data = get_client().get("/api/gam/reports/templates")
        if isinstance(data, dict):
            items = data.get("templates", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _TEMPLATE_LIST_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@templates_app.command("save")
def templates_save(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the template body"),
):
    """Save a new report template."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/templates", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@templates_app.command("update")
def templates_update(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the update body"),
):
    """Update a report template (PUT)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().put(f"/api/gam/reports/templates/{template_id}", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@templates_app.command("delete")
def templates_delete(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
):
    """Delete a report template."""
    try:
        get_client().delete(f"/api/gam/reports/templates/{template_id}")
        info(f"Template {template_id} deleted.")
    except CliApiError as e:
        handle_error(e)


@templates_app.command("duplicate")
def templates_duplicate(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID to clone"),
):
    """Duplicate a report template."""
    try:
        data = get_client().post(f"/api/gam/reports/templates/{template_id}/clone")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@templates_app.command("run")
def templates_run(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="Template ID"),
):
    """Run a report from an existing template."""
    try:
        data = get_client().post(f"/api/gam/reports/templates/{template_id}/run")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── reporting gam-reports sub-group (4 verbs) ─────────────────────────────
gam_reports_app = typer.Typer(help="Manage GAM reports linked to OrbiAds templates", no_args_is_help=True)
app.add_typer(gam_reports_app, name="gam-reports")

_GAM_REPORT_LIST_COLUMNS = ["id", "name", "templateId", "status"]


@gam_reports_app.command("list")
def gam_reports_list(ctx: typer.Context):
    """List GAM reports."""
    try:
        data = get_client().get("/api/gam/reports/gam-reports")
        if isinstance(data, dict):
            items = data.get("gamReports", data.get("results", []))
        else:
            items = data if isinstance(data, list) else []
        render(items, _GAM_REPORT_LIST_COLUMNS, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@gam_reports_app.command("get")
def gam_reports_get(
    ctx: typer.Context,
    gam_report_id: str = typer.Argument(..., help="GAM report ID"),
):
    """Get a GAM report's metadata."""
    try:
        data = get_client().get(f"/api/gam/reports/gam-reports/{gam_report_id}")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@gam_reports_app.command("create-from-template")
def gam_reports_create_from_template(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="OrbiAds template ID to publish to GAM"),
):
    """Publish an OrbiAds template as a saved GAM report."""
    try:
        data = get_client().post(
            f"/api/gam/reports/templates/{template_id}/publish-to-gam"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@gam_reports_app.command("update-from-template")
def gam_reports_update_from_template(
    ctx: typer.Context,
    template_id: str = typer.Argument(..., help="OrbiAds template ID"),
):
    """Push template changes to the linked GAM report."""
    try:
        data = get_client().post(
            f"/api/gam/reports/templates/{template_id}/update-in-gam"
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── catalogue + executions + delivery / forecast / alerts (10 verbs) ──────


@app.command()
def dimensions(ctx: typer.Context):
    """List available report dimensions (REST catalogue)."""
    try:
        data = get_client().get("/api/gam/reports/available-dimensions")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def metrics(ctx: typer.Context):
    """List available report metrics (REST catalogue)."""
    try:
        data = get_client().get("/api/gam/reports/available-metrics")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("date-ranges")
def date_ranges(ctx: typer.Context):
    """List available report date ranges (REST catalogue)."""
    try:
        data = get_client().get("/api/gam/reports/available-date-ranges")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def executions(ctx: typer.Context):
    """List recent report executions."""
    try:
        data = get_client().get("/api/gam/reports/executions")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def inventory(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the inventory-report request"),
):
    """Run an inventory report (POST body in --file)."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/inventory", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("delivery-status")
def delivery_status(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Get delivery status for a job."""
    try:
        data = get_client().get(f"/api/gam/jobs/{job_id}/delivery-status")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("delivery-report")
def delivery_report(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Fetch the delivery report for a job."""
    try:
        data = get_client().get(f"/api/jobs/{job_id}/report")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("forecast-line-item")
def forecast_line_item(
    ctx: typer.Context,
    job_id: str = typer.Argument(..., help="Job ID"),
):
    """Get the delivery forecast for the line items of a job."""
    try:
        data = get_client().get(f"/api/jobs/{job_id}/forecast")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("alerts-underdelivery")
def alerts_underdelivery(ctx: typer.Context):
    """List under-delivery alerts across campaigns."""
    try:
        data = get_client().get("/api/campaigns/alerts")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command("alerts-budget")
def alerts_budget(
    ctx: typer.Context,
    campaign_id: str = typer.Argument(..., help="Campaign ID"),
):
    """List budget alerts for a campaign."""
    try:
        data = get_client().get(f"/api/campaigns/{campaign_id}/health-alerts")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@app.command()
def export(
    ctx: typer.Context,
    report_id: str = typer.Option(..., "--report-id", help="GAM report ID"),
    fmt: str = typer.Option("csv", "--format", help="Export format: csv, json"),
):
    """Export a report result to stdout (pipeable)."""
    try:
        client = get_client()

        # Run the GAM report and retrieve results
        data = client.post(f"/api/gam/reports/gam-reports/{report_id}/run")

        if fmt == "json":
            print(json.dumps(data, indent=2, default=str))
        else:
            # CSV output: headers + rows
            import csv

            if isinstance(data, dict):
                rows = data.get("rows", [])
                headers = data.get("headers", [])
                if not headers and rows:
                    headers = list(rows[0].keys())
            elif isinstance(data, list):
                rows = data
                headers = list(rows[0].keys()) if rows else []
            else:
                rows = []
                headers = []

            writer = csv.DictWriter(sys.stdout, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({h: row.get(h, "") for h in headers})
    except CliApiError as e:
        handle_error(e)


# === Story 62.2 — GA4 + forecast sub-nouns + export-csv + delete gam-report ===

# ── ga4 sub-noun (3 verbs) ────────────────────────────────────────────────
ga4_app = typer.Typer(help="GA4 reporting (Story 62.2)", no_args_is_help=True)
app.add_typer(ga4_app, name="ga4")


@ga4_app.command("run")
def ga4_run(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the GA4 report request"),
):
    """Run a GA4 report."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/ga4/run", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@ga4_app.command("dimensions")
def ga4_dimensions(ctx: typer.Context):
    """List GA4 available dimensions."""
    try:
        data = get_client().get("/api/gam/reports/ga4/dimensions")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@ga4_app.command("metrics")
def ga4_metrics(ctx: typer.Context):
    """List GA4 available metrics."""
    try:
        data = get_client().get("/api/gam/reports/ga4/metrics")
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── forecast sub-noun (3 verbs) ───────────────────────────────────────────
forecast_app = typer.Typer(help="GAM forecasting (Story 62.2)", no_args_is_help=True)
app.add_typer(forecast_app, name="forecast")


@forecast_app.command("standalone")
def forecast_standalone(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the forecast request"),
):
    """Run a standalone inventory forecast."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/forecast/standalone", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@forecast_app.command("prospective")
def forecast_prospective(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the forecast request"),
):
    """Prospective delivery forecast."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/forecast/prospective", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@forecast_app.command("traffic")
def forecast_traffic(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the forecast request"),
):
    """Get inventory traffic data."""
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/forecast/traffic", json=payload)
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# ── top-level: export-csv + gam-reports delete ───────────────────────────


@app.command("export-csv")
def export_csv(
    ctx: typer.Context,
    execution_id: str = typer.Argument(..., help="Execution / correlation ID"),
    file: str = typer.Option(..., "--file", "-f", help="JSON file with the report spec (dimensions/metrics/dates)"),
):
    """Stream a custom-report result as CSV (text/csv body to stdout).

    Backend route is POST /api/gam/reports/{execution_id}/export.csv; the
    execution_id is a correlation token echoed back via X-Execution-Id. Story
    62.2: backend doesn't fetch pre-existing GAM executions — every call
    re-runs the spec (same as MCP behaviour).
    """
    payload = _load_json_payload(file)
    try:
        # The CSV body is streamed; render_detail handles dict but for the CSV
        # body we just dump it to stdout via client.post returning bytes/str.
        data = get_client().post(
            f"/api/gam/reports/{execution_id}/export.csv", json=payload
        )
        if isinstance(data, (str, bytes)):
            sys.stdout.write(data if isinstance(data, str) else data.decode("utf-8"))
        else:
            render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


@gam_reports_app.command("delete")
def gam_reports_delete(
    ctx: typer.Context,
    gam_report_id: str = typer.Argument(..., help="GAM report ID"),
):
    """Delete a saved GAM report."""
    try:
        get_client().delete(f"/api/gam/reports/gam-reports/{gam_report_id}")
        info(f"GAM report {gam_report_id} deleted.")
    except CliApiError as e:
        handle_error(e)


# === Story 62.2a — billing-report (extracted from MCP 501 stub) ============


@app.command("billing-report")
def billing_report(
    ctx: typer.Context,
    file: str = typer.Option(..., "--file", "-f", help="JSON with startDate/endDate/exportFormat/lineItemTypes/orderIds"),
):
    """Generate a per-order billing report (JSON envelope or streamed CSV).

    Story 62.2a — replaces the previous 501 stub (services/billing_report_service.py
    extracted from src/mcp/tools/reporting.py inline body). When `exportFormat:csv`,
    the backend streams text/csv; otherwise the JSON envelope is returned.
    """
    payload = _load_json_payload(file)
    try:
        data = get_client().post("/api/gam/reports/billing", json=payload)
        # CSV streaming returns a str/bytes body; JSON returns a dict.
        if isinstance(data, (str, bytes)):
            sys.stdout.write(data if isinstance(data, str) else data.decode("utf-8"))
        else:
            render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)


# === Story 66.1 (Epic 66) — reporting_skill parent>child tool =================


@app.command("skill")
def skill(
    ctx: typer.Context,
    action: str = typer.Option(
        ...,
        "--action",
        help=(
            "One of: schedule_from_template | create_alert | cancel_run | "
            "historical_aggregates | fetch_mcm_earnings"
        ),
    ),
    params_file: str = typer.Option(
        None,
        "--params-file",
        "-f",
        help="JSON file path containing the action params (use this OR --params-json).",
    ),
    params_json: str = typer.Option(
        None,
        "--params-json",
        help="Inline JSON string of the action params (use this OR --params-file).",
    ),
):
    """Dispatch a reporting skill action via the parent>child orchestration tool.

    Posts to `POST /api/gam/reporting/skill` with `{action, params}`. The
    server validates `params` via a Pydantic discriminated union (one schema
    per action) and routes to the right service method.

    Examples :

      orbiads reporting skill --action cancel_run \\
        --params-json '{"operationName":"networks/123/operations/reports/runs/456"}'

      orbiads reporting skill --action create_alert --params-file alert.json
    """
    if (params_file is None) == (params_json is None):
        info("Provide exactly one of --params-file or --params-json.")
        raise typer.Exit(code=2)
    if params_file:
        payload = _load_json_payload(params_file)
    else:
        try:
            payload = json.loads(params_json)
        except json.JSONDecodeError as exc:
            info(f"Invalid JSON in --params-json: {exc}")
            raise typer.Exit(code=2)
    try:
        data = get_client().post(
            "/api/gam/reporting/skill",
            json={"action": action, "params": payload},
        )
        render_detail(data, ctx.obj)
    except CliApiError as e:
        handle_error(e)
