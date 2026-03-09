---
description: Deploy, monitor, and report on GAM campaigns with mandatory dry_run gates and post-push audit trails.
---

# OrbiAds — deploy-reporting

Prepare a controlled push with preview and coverage checks. Execute campaign actions with guardrails. Monitor delivery and produce post-push reports.

## When to Use

- Deploy, update, pause, archive, monitor, or report on a campaign.
- QA has returned a go decision and next step is live activation.
- Post-push signals — delivery, alerts, or audit — must be reviewed.

**Do not use** if QA has not run yet — route to `qa-preview` first.

## Steps

1. Verify bootstrap complete and campaign resources (`jobId`, `orderId`, line items, creatives) known.
2. `check_creative_coverage` + `get_preview_urls` — coverage and preview before any push. `[free]`
3. Campaign action with `dry_run=True` → show preview artifact → ask explicit human confirmation.
4. Execute real action only after approval.
5. `check_delivery_status` + `fetch_delivery_report` after execution. `[free]`
6. Run appropriate reporting path (template / custom / inventory / GAM / GA4).
7. `check_underdelivery_alerts` + `check_budget_alerts` + `query_audit_log`. `[free]`
8. Return delivery / reporting / alert / audit packet.

## Key Tools

- `check_creative_coverage`, `get_preview_urls`, `get_campaign_preview_urls` — `[free]`
- `check_delivery_status`, `fetch_delivery_report`, `query_audit_log` — `[free]`
- `check_underdelivery_alerts`, `check_budget_alerts` — `[free]`
- `deploy_campaign`, `update_campaign`, `pause_campaign` — `dry_run=True` required, then confirmation
- `archive_campaign`, `rollback_resources` — exceptional, blast-radius summary required

## Abort Conditions

- Never deploy without prior dry_run shown and approved.
- Never include a real deployment call and a rollback suggestion in the same turn.
- Stop before archive or rollback without explicit blast-radius summary and user approval.

## Output

Always render the dry_run summary as an artifact before asking for deployment confirmation.

```
<handoff>
campaignActionStatus: dry_run | executed | paused | archived
deliveryStatus: delivering | underdelivering | paused
underdeliveryAlerts: [...]
budgetAlerts: [...]
reportHandles: [...]
nextRecommendedSkill: null | deploy-reporting (follow-up)
</handoff>
```

Format post-push monitoring summary as a structured artifact: delivery status, underdelivery alerts, budget alerts, audit tail.
