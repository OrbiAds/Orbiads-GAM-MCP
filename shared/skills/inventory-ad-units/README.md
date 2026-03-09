# Inventory & ad units

## Purpose

- Explore the existing GAM inventory.
- Qualify the ad units needed for a business workflow.
- Create or push new ad units in a controlled way.

## Prerequisites

- `bootstrap` has been completed;
- an active network is available;
- the business goal is known: read, audit, batch creation, blueprint, or cleanup.

## Inputs

- `tenantId`;
- optionally a list of `adUnitIds` to re-read;
- optionally a `units` batch for `create_ad_units_batch`;
- optionally the inputs for `generate_inventory_blueprint`: `brand`, `platforms`, `pageTypes`, `positions`, `formats`.

## Expected Output

- qualified inventory tree;
- selected ad units ready for targeting, forecast, or trafficking;
- creation preview or blueprint ready for confirmation;
- list of anomalies and recommended actions.

## Guardrails

- start by reading the current state before any write;
- use `audit_inventory` before a significant creation step;
- use `dry_run=True` for `create_ad_units_batch`, `push_inventory_blueprint`, and `archive_inactive_ad_units`;
- confirm a write only after human validation of names, parents, sizes, and volumes;
- do not archive inactive ad units without prior manual review.

## Handoff

- pass the selected or created `adUnitIds`;
- pass along any remaining inventory anomalies;
- route next to `availability-forecast`, `placements-targeting`, or creative production.