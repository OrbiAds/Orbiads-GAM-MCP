---
description: "Manage GAM advertisers and orders via CLI. Use when creating or finding advertisers and orders."
---

# OrbiAds CLI — Orders

Find or create GAM advertisers and orders, which are required before building campaigns.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## User Configuration Note

Naming conventions from tenant settings are applied automatically by the backend. The advertiser and order names you provide in `--name` flags will be used as macro values for the configured naming templates (e.g., `{advertiser}`, `{campaign}` macros in `orderTemplate`). If no naming template is configured, the `--name` value is used as-is.

## Commands

- `orbiads advertisers list --json` `[free]` — list all advertisers
- `orbiads advertisers list --search "<name>" --json` `[free]` — search advertisers by name
- `orbiads advertisers create --name "<name>" --json` `[1 credit]` — create a new advertiser
- `orbiads orders list --json` `[free]` — list all orders
- `orbiads orders list --advertiser <id> --json` `[free]` — list orders for a specific advertiser
- `orbiads orders create --advertiser <id> --name "<name>" --json` `[1 credit]` — create a new order
- `orbiads orders get --id <id> --json` `[free]` — get a specific order by ID

## Steps

1. [start] Run `orbiads advertisers list --search "<name>" --json` to find an existing advertiser.
2. [depends: step 1] If not found, run `orbiads advertisers create --name "<name>" --json` after user confirmation (costs 1 credit).
3. [depends: steps 1/2] Run `orbiads orders list --advertiser <id> --json` to check existing orders.
4. [depends: step 3] If no suitable order exists, run `orbiads orders create --advertiser <id> --name "<name>" --json` after user confirmation (costs 1 credit).
5. [depends: step 4] Return confirmed advertiser ID and order ID.

## Abort Conditions

- User declines advertiser or order creation.
- Insufficient credits (advertiser costs 1, order costs 1).
- No network connected: route to cli-bootstrap skill first.

## Output

Confirmed advertiser ID and order ID, ready for campaign creation.
