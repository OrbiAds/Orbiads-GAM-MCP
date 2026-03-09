# Steps

1. Reuse the `bootstrap` handoff instead of repeating auth checks.
2. Run `qa-preview` first to check creative coverage, preview URLs, SSL, and compliance.
3. Stop immediately if previews, SSL, or coverage are not acceptable.
4. Run `deploy-reporting` in `dry_run=True` mode for the requested action whenever the tool supports preview.
5. Ask for explicit human approval before any real deploy, update, pause, archive, or rollback.
6. Execute the approved action and re-read delivery state immediately after execution.
7. Run the smallest reporting path that answers the business question.
8. Return the delivery, reporting, alert, and audit packet with the next recommended action.