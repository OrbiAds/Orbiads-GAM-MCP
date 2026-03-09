# Agent Trigger — availability-forecast

## Enter when

- the user asks whether supply is sufficient for a delivery goal;
- viability or underdelivery risk must be checked before activation;
- tighter targeting may materially reduce available inventory.

## Do not enter when

- `adUnitIds` are not yet qualified — route to `inventory-ad-units` first;
- the request is about line-item creation or trafficking — that belongs in `advertiser-order-line-items`;
- the user just wants to list ad units without a supply question.

## Disambiguation

- "is there enough inventory for X impressions?" → `get_standalone_forecast`;
- "check the forecast for this line item" → `get_delivery_forecast_by_line_item`;
- "will tighter geo targeting hurt supply?" → `get_inventory_forecast` with constrained targeting;
- "what country IDs do I need?" → reference data calls only, not a full forecast run.
