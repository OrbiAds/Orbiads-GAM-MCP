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
