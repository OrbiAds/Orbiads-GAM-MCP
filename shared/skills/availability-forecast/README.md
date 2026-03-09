# Availability & forecast

## Purpose

- Verify availability before creating, duplicating, or activating delivery.
- Compare several targeting hypotheses without writing into GAM.
- Produce an actionable recommendation before trafficking or deployment.

## Prerequisites

- `bootstrap` has been completed;
- qualified `adUnitIds` or an existing `lineItemId` are available;
- the delivery window is known and, for display, the target creative sizes are known.

## Inputs

- `tenantId`;
- either `adUnitIds` + dates + targeting for `get_standalone_forecast` or `get_inventory_forecast`;
- or `lineItemId` for `get_delivery_forecast_by_line_item`;
- optionally country IDs, language IDs, device IDs, and `creativeSizes`.

## Expected Output

- forecast packet with estimated availability;
- pressure or risk level;
- documented targeting assumptions;
- go / adjust / stop recommendation before the next step.

## Guardrails

- prefer `get_standalone_forecast` for a still-theoretical scenario;
- use `get_delivery_forecast_by_line_item` for an already existing line item;
- keep `get_inventory_forecast` as a lower-level variant;
- specify `creativeSizes` for every display scenario to avoid misleading forecasts;
- remind users that a forecast is not a contractual delivery guarantee.

## Handoff

- pass the assumptions, key numbers, and risks to the next skill;
- route next to line-item creation/editing, creative production, or deployment.