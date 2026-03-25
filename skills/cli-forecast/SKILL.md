---
description: "Run GAM availability forecasts via CLI. Use when checking impression supply or delivery capacity."
---

# OrbiAds CLI — Forecast

Run GAM availability forecasts to check whether enough impressions are available for a campaign before committing.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Commands

- `orbiads reporting run --type forecast --ad-units <ids> --start <date> --end <date> --json` `[free]` — run an availability forecast
- `orbiads inventory ad-units --json` `[free]` — list all ad units
- `orbiads inventory ad-units --id <id> --json` `[free]` — get a specific ad unit by ID

## Steps

1. [start] Confirm ad unit IDs with the user. If unknown, run `orbiads inventory ad-units --json` to discover them.
2. [depends: step 1] Run `orbiads reporting run --type forecast --ad-units <ids> --start <date> --end <date> --json`.
3. [depends: step 2] Analyze the results: available impressions, matched impressions, possible impressions, contending line items.
4. [depends: step 3] Summarize findings and recommend whether the impression goal is achievable.

## Abort Conditions

- No ad unit IDs provided or found: route to cli-inventory skill first.
- No network connected: route to cli-bootstrap skill first.

## Output

Forecast summary: available vs. requested impressions, contention analysis, and a go/no-go recommendation for the campaign goal.
