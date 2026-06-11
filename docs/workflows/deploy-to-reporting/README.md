# Deploy to Reporting

## Goal

- Validate creative coverage and previews before any real campaign action.
- Execute deploy, update, pause, archive, or rollback with clear approval gates.
- End with delivery, reporting, and audit outputs that support the next business decision.

## Skill Composition

- `orbiads` (orchestrator — auth context and tenant confirmation)
- `campaigns` (QA, deploy, pause, archive, rollback — creative compliance and preview gates)
- `reporting` (delivery status, underdelivery alerts, custom reporting, forecasts)
- `campaigns` (order/line-item remediation when needed before activation)

## Entry Conditions

- the relevant campaign identifiers are known: `jobId`, `orderId`, `lineItemIds`, `creativeIds`, depending on the action;
- creatives and targeting were already business-approved;
- the operator knows whether the goal is preview only, deploy, update, pause, archive, rollback, or reporting.

## Exit States

- preview packet accepted or rejected;
- real campaign action executed or explicitly deferred;
- delivery and reporting packet ready for optimization, incident handling, or recurring reporting.