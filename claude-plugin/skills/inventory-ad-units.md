# Claude Skill Wrapper — inventory-ad-units

- load `../../shared/agents/inventory-ad-units/`;
- execute `../../shared/skills/inventory-ad-units/`;
- use this skill for inventory audits, blueprint prep, and ad-unit batch creation.

## Claude-Specific Hints

- render the ad-unit tree as a collapsible artifact when the hierarchy has more than 10 nodes;
- use `<handoff>` tags to pass `selectedAdUnitIds` and `auditFindings` to the next skill;
- always show the dry_run preview as an artifact before asking for confirmation;
- surface naming anomalies as a numbered list — one issue per line for easy human review.
