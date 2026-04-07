# Agent Trigger — cli-deploy

## Enter when

- the user asks to deploy a campaign via CLI;
- a workflow needs to push a campaign live after QA validation;
- the user asks for post-deployment delivery reports.

## Do not enter when

- QA has not been run yet — route to `cli-qa` first;
- the request is about campaign creation only — route to `cli-orders`;
- the request is about forecast or supply check — route to `cli-forecast`.

## Disambiguation

- "deploy campaign" → confirm dry-run passed, then deploy;
- "check deployment status" → poll with `--json` only;
- "delivery report" → post-deploy reporting path.