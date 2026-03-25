---
description: "Validate GAM campaigns before deployment via CLI. Use for readiness checks or dry-runs."
---

# OrbiAds CLI — QA

Validate a GAM campaign configuration before deployment by inspecting its setup, checking creatives, and running a dry-run.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Commands

- `orbiads campaigns get <id> --json` `[free]` — inspect campaign configuration
- `orbiads creatives get --id <id> --json` `[free]` — inspect a creative by ID
- `orbiads campaigns deploy <id> --dry-run --json` `[free]` — simulate deployment without spending credits

## Steps

1. [start] Run `orbiads campaigns get <id> --json` to inspect the campaign configuration.
2. [depends: step 1] **Verify naming conventions applied correctly.** Check that entity names (order, line items, creatives) match the configured naming templates. If the user has configured `orderTemplate`, `lineItemTemplate`, or `creativeTemplate` in tenant settings, the names should follow those patterns. Flag any names that look like they used fallback defaults when a template was expected, or vice versa.
3. [depends: step 1] Verify each creative. Run `orbiads creatives get --id <id> --json` for each creative referenced in the campaign. Check compliance and SSL status.
4. [depends: step 3] Run `orbiads campaigns deploy <id> --dry-run --json` to simulate deployment.
5. [depends: step 4] Summarize results: list blocking issues, warnings, naming convention compliance, and provide a go/no-go recommendation.

## Abort Conditions

- Campaign does not exist or has no line items.
- Dry-run returns blocking errors that must be fixed first.
- No network connected: route to cli-bootstrap skill first.

## Output

QA summary: blocking issues, warnings, creative compliance status, naming convention compliance, and a clear go/no-go recommendation for deployment.
