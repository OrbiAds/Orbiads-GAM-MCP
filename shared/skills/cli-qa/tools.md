# Available CLI Commands

## Campaign + job inspection

- `orbiads campaigns get <campaign_id>` `[free]` — full campaign config and status.
- `orbiads jobs get <job_id>` `[free]` — full pipeline state, including failure reason.
- `orbiads line-items verify <job_id>` `[free]` — read-only health check on the line items of a job.

## Creative QA (compliance, SSL, tracking)

- `orbiads creative-qa scan-compliance --file <cr.json>` `[free]` — scan a creative payload for compliance issues.
- `orbiads creative-qa validate-ssl <creative_id> [--follow-redirects]` `[free]` — SSL/HTTPS check on a creative's tag URLs.
- `orbiads creative-qa validate-ssl-batch --file <ids.json>` `[free]` — batch SSL check.
- `orbiads creative-qa validate-tag --file <tag.json>` `[free]` — validate a third-party tag snippet (macros, safety, format).
- `orbiads creative-qa audit-tracking <creative_id>` `[free]` — audit a creative's tracking pixels & macros.
- `orbiads creative-qa audit-order-tracking <order_id>` `[free]` — tracking audit across every line-item creative of an order.
- `orbiads creative-qa pre-archive-check --file <body.json>` `[free]` — pre-archive safety checks before retiring a creative.

## Inventory QA

- `orbiads inventory validate-fluid --file <req.json>` `[free]` — Fluid-sizing support on selected ad units.
- `orbiads inventory audit [--file <body.json>]` `[free]` — full inventory audit.

## Preview & coverage

- `orbiads preview campaign <job_id> [--file <body.json>]` `[free]` — GAM preview links for a campaign's creatives.
- `orbiads preview share --file <body.json>` `[free]` — generate a shareable preview token / URL.
- `orbiads preview coverage --file <req.json>` `[free]` — check creative coverage across an inventory selection.

## Audit trail

- `orbiads audit log [--limit N]` `[free]` — tenant audit log (who did what when).
