# Agent Trigger — cli-targeting

## Enter when

- the user asks to explore targeting keys, values, or placements via CLI;
- a workflow needs a validated targeting packet for line-item creation.

## Do not enter when

- targeting is already confirmed in the session — pass it directly;
- the request is about inventory discovery — route to `cli-inventory`;
- the request is about forecasting — route to `cli-forecast`.

## Disambiguation

- "show targeting keys" → read path only;
- "set targeting for line item" → validate ad units, then build packet;
- "which placements are available?" → targeting key lookup.