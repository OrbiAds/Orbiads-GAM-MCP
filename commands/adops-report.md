---
name: adops-report
description: Query GAM reporting — custom reports, delivery status, CSV export, saved templates, billing reports. Read-only and free unless noted.
argument-hint: "<run|delivery|export|templates|billing|forecast> [params]"
allowed-tools: mcp__orbiads__reporting
model: sonnet
---

# GAM Reporting

Always confirm the tenant first: `get_my_tenant_id`. Most operations are read-only. Credit costs are shown per action.

**Note:** The REST Interactive Reports API does not work on test network 45515589. Use the production network.

## delivery `[campaign-id]`

`reporting(action="check_delivery_status", params={job_id})` — free. Shows pacing %, impressions vs. goal, fill rate.

Then call `reporting(action="check_underdelivery_alerts")` — costs 0.25 cr — to surface active delivery anomalies. If pacing < 80%, suggest running `/adops audit delivery`.

## run

Build a custom report interactively:

1. Fetch available dimensions: `reporting(action="get_report_dimensions")` — free.
2. Fetch available metrics: `reporting(action="get_report_metrics")` — free.
3. Fetch valid date range options: `reporting(action="get_report_date_ranges")` — free.
4. Submit the report: `reporting(action="run_custom_report", params={dimensions, metrics, date_range, filters})` — costs 0.5 cr.
5. Poll until complete: `reporting(action="get_report_result", params={execution_id})` — free.
6. Render the first 20 rows inline. Offer to export the rest.

For a saved GAM report: `reporting(action="run_gam_report", params={report_id})` — free. Fetch existing reports first via `reporting(action="list_gam_reports")`.

For Google Analytics data: `reporting(action="run_ga_report", params={metrics, dimensions, date_range})` — costs 0.5 cr. Fetch GA dimensions/metrics via `reporting(action="get_ga_dimensions")` and `reporting(action="get_ga_metrics")`.

## export `<execution-id>`

`reporting(action="export_report_csv", params={execution_id})` — costs 0.5 cr. Confirm the row count after export.

## templates `[list|save|run <id>]`

**list** — `reporting(action="list_report_templates")` — free.

**save** — Build template params from the user's input, then `reporting(action="save_report_template", params={name, dimensions, metrics, date_range, filters})` — free.

**run `<id>`** — `reporting(action="run_report_from_template", params={template_id})` — costs 0.5 cr. Follow the same poll/render flow as `run` above.

Template edits: `reporting(action="update_report_template", params={template_id, ...})`. Removal: `reporting(action="delete_report_template", params={template_id})`.

## billing `[YYYY-MM]`

`reporting(action="generate_billing_report", params={month})` — costs 0.5 cr. Show impressions billed, eCPM, and revenue breakdown by line item type. Offer export if results exceed 50 rows.

Check budget alerts separately: `reporting(action="check_budget_alerts")` — costs 0.25 cr.

## forecast

Two paths depending on whether a line item already exists:

**Prospective (draft line item being planned):** `reporting(action="get_standalone_forecast", params={targeting, line_item_type, start_date_time, end_date_time, units_bought, cost_type, cost_per_unit})` — free. Surface `available_units` vs. `units_bought`. This is the mandatory pre-deploy check in `/adops campaign deploy`.

**Existing line item:** `reporting(action="get_delivery_forecast_by_line_item", params={line_item_id})` — free.

**Post-setup recheck:** `reporting(action="get_prospective_delivery_forecast", params={line_item_id})` — free. Run this after creatives are associated to catch targeting conflicts that only appear with the full setup in place.

Traffic analysis: `reporting(action="get_traffic_data", params={targeting, date_range})` — free. Useful for sizing before creating line items.

Delivery summary without a job ID: `reporting(action="fetch_delivery_report", params={advertiser_id, date_range})` — free.
Inventory-level report: `reporting(action="fetch_inventory_report", params={ad_unit_id, date_range})` — costs 0.5 cr.

## Quick routing

| User says | Sub-verb |
| --- | --- |
| "Show me delivery last 7 days" | `run` with `LAST_7_DAYS` date range |
| "Is my campaign pacing?" | `delivery <campaign-id>` |
| "Export results" | `export <last execution-id>` |
| "What metrics can I use?" | `run` — fetch and display metric catalogue |
| "Forecast for this targeting" | `forecast` → `get_standalone_forecast` |
