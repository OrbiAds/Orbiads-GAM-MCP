# Deploy & reporting

## Purpose

- Prepare a controlled push with preview and coverage checks.
- Execute campaign actions with guardrails.
- Monitor delivery and produce post-push reports.

## Prerequisites

- `bootstrap` has been completed;
- a `jobId`, `orderId`, or the required campaign resources are available;
- creatives and business configuration were validated by humans before any real push.

## Inputs

- `tenantId`;
- `jobId` for `deploy_campaign`, `update_campaign`, `pause_campaign`, or `archive_campaign`;
- `orderId`, `lineItemIds`, or `creativeIds` for preview and coverage;
- optionally reporting inputs: dimensions, metrics, template, dates, filters.

## Expected Output

- preview and coverage packet ready for validation;
- action preview or confirmed execution with clear status;
- usable delivery indicators and reports;
- audit trace and recommended next action.

## Guardrails

- verify preview and coverage before any real deployment;
- use `dry_run=True` for `deploy_campaign`, `update_campaign`, `pause_campaign`, `archive_campaign`, and `rollback_resources`;
- never archive or roll back without explicit human validation;
- distinguish read-only reporting from reporting that consumes credits;
- review audit logs after any important action.

## Handoff

- pass the execution status, previews, reporting results, and risks;
- route next to optimization, pause, update, audit, or recurring reporting.