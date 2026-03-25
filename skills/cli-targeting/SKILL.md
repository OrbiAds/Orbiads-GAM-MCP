---
description: "Explore and validate GAM targeting configuration via CLI. Use when building targeting for campaigns."
---

# OrbiAds CLI — Targeting

Explore available targeting keys and validate ad unit compatibility to build targeting configurations for campaigns.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Campaign Presets & Pre-configured Targeting

**Check campaign presets for pre-configured targeting key-values.** The user may have campaign presets that include pre-selected targeting configurations:

- `__builtin_homepage` — Pack Homepage (may include page-type key-values)
- `__builtin_ros` — Pack Run of Site (may include broad targeting)
- `__builtin_interstitiel` — Pack Interstitiel (may include interstitial-specific key-values)
- Custom user presets may include specific `keyValues` targeting

If a preset matches the campaign goal, its targeting key-values are already defined and can be applied directly. Presets are configured at orbiads.com/settings and applied via the MCP `list_presets` tool or visible in `orbiads network info --json`.

## Commands

- `orbiads inventory keys --json` `[free]` — list all targeting keys and their values
- `orbiads inventory keys --key "<name>" --json` `[free]` — get values for a specific targeting key
- `orbiads inventory ad-units --search "<name>" --json` `[free]` — search ad units by name
- `orbiads inventory ad-units --id <id> --json` `[free]` — get a specific ad unit with targeting details

## Steps

1. [start] Check if a campaign preset includes pre-configured targeting key-values for this campaign. If yes, use the preset's targeting and skip to step 4.
2. [fallback] Run `orbiads inventory keys --json` to list all targeting keys and values.
3. [depends: step 2] Select the relevant keys for the campaign scope.
4. [depends: steps 1-3] Run `orbiads inventory ad-units --id <id> --json` for each target ad unit to validate targeting compatibility.
5. [depends: step 4] Summarize the targeting configuration and confirm with the user.

## Abort Conditions

- No targeting keys available: new keys may need to be created via web UI or MCP.
- Ad units incompatible with the desired targeting.
- No network connected: route to cli-bootstrap skill first.

## Output

Validated targeting configuration: selected keys with values, compatible ad unit IDs, and confirmation from the user.
