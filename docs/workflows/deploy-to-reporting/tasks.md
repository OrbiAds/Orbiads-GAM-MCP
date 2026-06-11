# Tasks

## QA and Approval Gate

- validate creative coverage using the `campaigns` skill before activation;
- review preview URLs at the smallest useful scope;
- validate SSL and compliance findings before real writes.

## Controlled Campaign Action

- choose the requested action: deploy, update, pause, archive, rollback, or report only;
- run the `campaign(action="dry_run")` preview path first (the `campaigns` skill handles this);
- keep archive and rollback as exceptional actions with explicit human approval.

## Reporting and Audit

- re-read delivery state immediately after the action using `reporting(action="check_delivery_status")`;
- run standard, template-based, or custom reporting via the `reporting` skill only at the needed depth;
- include audit logs, alerts, and the recommended next action in the handoff packet.