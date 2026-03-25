---
description: "Explore GAM ad units, placements, and targeting keys via CLI. Use when browsing inventory or finding ad units."
---

# OrbiAds CLI — Inventory

Explore GAM ad units, placements, and targeting keys to identify where ads can run and what targeting is available.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Campaign Presets

**Check campaign presets first** before manual ad unit discovery. The user may have pre-configured campaign presets that bundle ad units and targeting together:

- `__builtin_homepage` — Pack Homepage (homepage ad units pre-selected)
- `__builtin_ros` — Pack Run of Site (run-of-site ad units pre-selected)
- `__builtin_interstitiel` — Pack Interstitiel (interstitial ad units pre-selected)
- Plus custom user presets with specific advertiserId, orderId, adUnitIds, and keyValues

If a preset matches the campaign goal (e.g., the user wants a homepage takeover), the ad units are already selected and you can skip manual inventory browsing. Presets are configured at orbiads.com/settings and applied via the MCP `list_presets` tool or visible in `orbiads network info --json`.

## Commands

- `orbiads inventory ad-units --json` `[free]` — list all ad units
- `orbiads inventory ad-units --search "<name>" --json` `[free]` — search ad units by name
- `orbiads inventory ad-units --id <id> --json` `[free]` — get a specific ad unit by ID
- `orbiads inventory placements --json` `[free]` — list all placements
- `orbiads inventory placements --search "<name>" --json` `[free]` — search placements by name
- `orbiads inventory keys --json` `[free]` — list all targeting keys
- `orbiads inventory keys --key "<name>" --json` `[free]` — get values for a specific targeting key

## Steps

1. [start] Check if a campaign preset matches the user's goal. If yes, use the preset's ad units and skip to step 5.
2. [fallback] Run `orbiads inventory ad-units --json` or add `--search "<name>"` to filter.
3. [depends: step 2] Identify relevant ad units, note their IDs and sizes.
4. [depends: step 2] Run `orbiads inventory placements --json` if placements are needed.
5. [depends: steps 1-4] Run `orbiads inventory keys --json` to discover available targeting keys.
6. [depends: steps 1-5] Return selected adUnitIds, sizes, and targeting keys.

## Abort Conditions

- No matches found: broaden the search term or list all.
- No network connected: route to cli-bootstrap skill first.

## Output

List of ad unit IDs, their sizes, placement IDs, and available targeting keys relevant to the user's request.
