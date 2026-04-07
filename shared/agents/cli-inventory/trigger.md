# Agent Trigger — cli-inventory

## Enter when

- the user asks to list, search, or audit ad units via CLI;
- a workflow needs confirmed `adUnitIds` before targeting, forecasting, or orders.

## Do not enter when

- `adUnitIds` are already confirmed in the session — pass them directly;
- the request is about placements or targeting — route to `cli-targeting`;
- the request is about forecasting — route to `cli-forecast` with existing IDs.

## Disambiguation

- "list ad units" or "show inventory" → read path, filtered by search;
- "which sizes are available?" → ad-unit detail query;
- "find ad units for…" → filtered search, then return IDs.