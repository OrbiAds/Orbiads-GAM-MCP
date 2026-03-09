# Claude Skill Wrapper — deploy-reporting

- load `../../shared/agents/deploy-reporting/`;
- execute `../../shared/skills/deploy-reporting/`;
- use this skill for dry-run deployment, live actions, delivery monitoring, and reporting.

## Claude-Specific Hints

- always render the dry_run summary as an artifact before asking for deployment confirmation;
- use `<handoff>` tags to pass execution status, delivery alerts, and report handles to any follow-up skill;
- format the post-push monitoring summary as a structured artifact: delivery status, underdelivery alerts, budget alerts, audit tail;
- never include a real deployment call and a rollback suggestion in the same turn — keep them as separate decisions.

## Example

- see `../examples/reporting-follow-up.md`.
