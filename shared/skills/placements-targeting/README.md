# Placements & targeting

## Purpose

- Align placement structure with the selected ad-unit scope.
- Maintain the targeting taxonomy and audience-facing constraints.
- Produce a trafficking-ready packet for order and line-item execution.

## Prerequisites

- `bootstrap` has been completed;
- the relevant `adUnitIds` are known or reusable from `inventory-ad-units`;
- naming rules for placements and custom targeting are approved.

## Inputs

- `tenantId`;
- selected `adUnitIds` or an inventory search scope;
- placement create / update / archive intent when applicable;
- custom targeting key / value intent when applicable;
- geo, language, device, and Native / Fluid constraints.

## Expected Output

- qualified placement summary;
- current targeting taxonomy and approved changes;
- compatibility checks for Native / Fluid and constrained inventory;
- handoff packet for advertiser, order, and line-item work.

## Guardrails

- read placements and targeting taxonomy before any write;
- validate Native / Fluid compatibility before promising Native delivery;
- confirm custom targeting deletion and placement archive operations explicitly;
- use inventory forecast when tighter targeting could materially reduce supply;
- surface destructive ad-unit changes instead of hiding them in a mixed batch.

## Handoff

- pass the selected `adUnitIds`, `placementIds`, key or value identifiers, and constraint summary;
- pass any forecast signal that changes the trafficking plan;
- route next to `advertiser-order-line-items`, `native-image`, or preview / deployment flows.