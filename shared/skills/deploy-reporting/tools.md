# Allowed Tools

## QA and Preview Before Push

- `check_creative_coverage` `[free]` — verify creative-to-line-item gaps before activation.
- `get_preview_urls` `[variable]` — generate targeted previews by line item and creative.
- `get_campaign_preview_urls` `[variable]` — generate a preview pack at order scope.

## Read and Monitor After Push

- `check_delivery_status` `[free]` — re-read the delivery state of a job.
- `fetch_delivery_report` `[variable]` — retrieve the standard delivery reporting for a job.
- `list_report_templates` `[free]` — list the available report templates.
- `get_report_result` `[free]` — re-read an already computed report result.
- `list_gam_reports` `[free]` — list existing GAM reports.
- `query_audit_log` `[free]` — re-read the tenant action trace.

## Report Execution

- `run_custom_report` `[variable]` — run an ad hoc GAM report.
- `fetch_inventory_report` `[variable]` — output a targeted inventory report.
- `export_report_csv` `[variable]` — export a custom report as CSV.
- `run_report_from_template` `[variable]` — execute a GAM or GA4 template.
- `run_gam_report` `[variable]` — execute an existing GAM report.
- `run_ga_report` `[variable]` — execute an existing GA4 report.
- `check_underdelivery_alerts` `[free]` — detect line items that are falling behind.
- `check_budget_alerts` `[free]` — detect campaigns approaching budget caps.
- `generate_billing_report` `[variable]` — produce a billing report.

## Reporting Configuration

- `save_report_template` `[free]` — save a reusable template.
- `create_gam_report` `[free]` — create a persistent GAM report.

## Campaign Actions with Mandatory Preview

- `deploy_campaign` `[free]` — deploy a job with `dry_run=True`, then confirmation.
- `update_campaign` `[free]` — prepare campaign changes before confirmation.
- `pause_campaign` `[free]` — prepare a controlled pause.
- `archive_campaign` `[free]` — prepare a full archive with human validation.
- `rollback_resources` `[free]` — exceptional manual cleanup, always with preview then confirmation.