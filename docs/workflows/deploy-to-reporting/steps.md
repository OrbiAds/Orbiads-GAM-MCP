# Steps

1. Use the `orbiads` skill to confirm the active tenant and network instead of repeating auth checks.
2. Use the `campaigns` skill to run QA first: `creative_qa(action="scan_creative_compliance")`, `creative_qa(action="validate_creative_ssl")`, and `creatives(action="get_creative_preview_url")` for preview URLs.
3. Stop immediately if previews, SSL, or coverage are not acceptable.
4. Use the `campaigns` skill to run `campaign(action="dry_run")` for the requested action to produce a signed `ExecutionPlan`.
5. Ask for explicit human approval before any real deploy, update, pause, archive, or rollback.
6. Execute the approved action with the `confirmation_token` and re-read delivery state immediately after with `reporting(action="check_delivery_status")`.
7. Use the `reporting` skill to run the smallest reporting path that answers the business question.
8. Return the delivery, reporting, alert, and audit packet with the next recommended action.