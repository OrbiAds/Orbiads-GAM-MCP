# Available CLI Commands

## Campaigns

- `orbiads campaigns list [--status <s>] [--limit N]` `[free]` — list campaigns.
- `orbiads campaigns get <campaign_id>` `[free]` — full campaign config and status.
- `orbiads campaigns deploy <campaign_id> [--yes] [--json]` `[5 credits]` — deploy a draft to GAM. Returns a job ID for polling.
- `orbiads campaigns update <campaign_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads campaigns pause <campaign_id> [--yes]` `[free]` — pause delivery.
- `orbiads campaigns archive <campaign_id> [--yes]` `[free]` — archive.
- `orbiads campaigns add-line-items <campaign_id> --file <lis.json>` `[free]` — append line items (covers MCP create_line_items + create_line_items_batch).
- `orbiads campaigns attach-creatives <campaign_id> <line_item_id> --file <licas.json>` `[free]` — attach creatives via LICAs (covers MCP create_licas + associate_creative + bulk_associate_creatives).
- `orbiads campaigns recover <campaign_id> [--yes]` `[free]` — rollback orphan resources after a failed deploy (maps MCP rollback_resources).

## Line items (under a job context)

- `orbiads line-items get <line_item_id>` `[free]` — details.
- `orbiads line-items list-by-order <order_id> [--limit N] [--offset N]` `[free]` — by order.
- `orbiads line-items approve <line_item_id> [--yes]` `[free]` — draft → approved.
- `orbiads line-items activate|pause|archive <job_id> [--yes]` `[free]` — bulk on all LIs of a job.
- `orbiads line-items update <job_id> <line_item_id> --file <body.json>` `[free]` — under job context.
- `orbiads line-items update-targeting <campaign_id> <line_item_id> --file <tgt.json>` `[free]` — PATCH the targeting.
- `orbiads line-items duplicate <line_item_id>` `[free]` — duplicate.
- `orbiads line-items verify <job_id>` `[free]` — read-only health check.
- `orbiads line-items private-deals [--limit N] [--offset N]` `[free]` — list programmatic deals.
- `orbiads line-items create-adexchange|create-open-bidding|create-preferred-deal --file <body.json>` `[free]` — programmatic line items (Story 62.3a).

## Jobs (deploy pipeline state)

- `orbiads jobs list [--limit N] [--status <s>]` `[free]` — list jobs (filter by status).
- `orbiads jobs get <job_id>` `[free]` — full job state.
- `orbiads jobs duplicate <job_id>` `[free]` — create a new draft from an existing job.

## Status polling pattern

```bash
orbiads campaigns deploy cmp_abc123 --yes --json   # → job_id
orbiads jobs get $JOB_ID --json                    # poll until status=succeeded|failed
orbiads reporting delivery-status $JOB_ID --json   # post-deploy delivery check
```

## Post-deploy reporting

- `orbiads reporting run --dimensions DATE,LINE_ITEM_NAME --metrics IMPRESSIONS,CLICKS --start <YYYY-MM-DD> --end <YYYY-MM-DD>` `[free]` — custom delivery report.
- `orbiads reporting delivery-report <job_id>` `[free]` — fetch the delivery report for a job.
- `orbiads reporting delivery-status <job_id>` `[free]` — delivery status.
- `orbiads reporting alerts-underdelivery` `[free]` — under-delivery alerts across campaigns.
- `orbiads reporting alerts-budget <campaign_id>` `[free]` — budget alerts.
