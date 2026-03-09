# Agent Trigger — deploy-reporting

## Enter when

- the user asks to deploy, update, pause, archive, monitor, or report on a campaign;
- QA has returned a go decision and the next step is live activation;
- post-push signals — delivery, alerts, or audit — must be reviewed.

## Do not enter when

- QA has not run yet — route to `qa-preview` first and block deployment;
- the request is about creative production or line-item setup — route to the appropriate upstream skill;
- the user only wants a forecast — route to `availability-forecast` instead.

## Disambiguation

- "deploy this job" → always dry_run first, then explicit confirmation before real deploy;
- "pause this campaign" → `pause_campaign` with dry_run preview, not a silent call;
- "archive this order" → exceptional — requires blast-radius summary and explicit approval;
- "show me delivery stats" → `check_delivery_status` + `fetch_delivery_report`, read-only, no confirmation needed;
- "rollback" → `rollback_resources` is exceptional — summarize impact, require explicit approval.
