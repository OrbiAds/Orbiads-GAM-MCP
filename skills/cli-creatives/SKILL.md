---
description: "List, inspect, and upload GAM creatives via CLI. Use when managing creative assets."
---

# OrbiAds CLI — Creatives

List, inspect, and upload GAM creatives for use in campaigns.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## User Configuration Note

Creative naming template from tenant settings is applied automatically by the backend. The `--name` value you provide is used as macro values for the configured `creativeTemplate` (e.g., `{advertiser}`, `{format}`, `{size}` macros). If no naming template is configured, the `--name` value is used as-is.

## Commands

- `orbiads creatives list --json` `[free]` — list all creatives
- `orbiads creatives list --search "<name>" --json` `[free]` — search creatives by name
- `orbiads creatives get --id <id> --json` `[free]` — get a specific creative by ID
- `orbiads creatives upload --file <path> --name "<name>" --advertiser <id> --json` `[5 credits]` — upload a new creative

## Steps

1. [start] Run `orbiads creatives list --json` or add `--search "<name>"` to filter.
2. [depends: step 1] If a new creative is needed, confirm file path, name, and advertiser ID with the user.
3. [depends: step 2] Run `orbiads creatives upload --file <path> --name "<name>" --advertiser <id> --json` after user confirmation (costs 5 credits).
4. [depends: step 3] Run `orbiads creatives get --id <id> --json` to verify the creative was created successfully.

## Abort Conditions

- File not found at the specified path.
- Insufficient credits (upload costs 5 credits).
- User declines the upload.
- No network connected: route to cli-bootstrap skill first.

## Output

Creative ID, name, dimensions, and status. Ready for use in campaign line items.
