# CLI Orders — Advertisers & Orders

## Purpose

- Look up or create advertisers in GAM.
- Create and manage orders for campaign trafficking.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.

## Expected Output

- Confirmed advertiser (existing or newly created).
- Confirmed order ready for line-item creation.

## Guardrails

- Always use `--json` flag for structured output.
- Search for existing advertisers before creating new ones.
- Advertiser creation costs 1 credit; order creation costs 1 credit.
- Do not create orders without explicit user confirmation.
