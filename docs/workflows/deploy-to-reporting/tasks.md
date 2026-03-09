# Tasks

## QA and Approval Gate

- validate creative coverage before activation;
- review preview URLs at the smallest useful scope;
- validate SSL and compliance findings before real writes.

## Controlled Campaign Action

- choose the requested action: deploy, update, pause, archive, rollback, or report only;
- run the preview path first when the write tool supports `dry_run=True`;
- keep archive and rollback as exceptional actions with explicit human approval.

## Reporting and Audit

- re-read delivery state immediately after the action;
- run standard, template-based, or custom reporting only at the needed depth;
- include audit logs, alerts, and the recommended next action in the handoff packet.