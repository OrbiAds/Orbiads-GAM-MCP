# Agent Trigger — placements-targeting

## Enter when

- the user asks to create, update, or review placements;
- targeting keys, values, geo, language, or device preparation is needed;
- Native delivery requires Fluid compatibility confirmation.

## Do not enter when

- `adUnitIds` are not yet qualified — route to `inventory-ad-units` first;
- the request is about line-item targeting already set on existing line items — use `update_line_item_targeting` directly via `advertiser-order-line-items`;
- the user is asking about supply only — route to `availability-forecast`.

## Disambiguation

- "check if these ad units support Native/Fluid" → `validate_fluid` only, not a full placement review;
- "create a placement for this inventory" → read existing placements first, confirm naming before write;
- "what targeting values exist?" → `list_custom_targeting_keys` read path, no write;
- "delete a targeting key" → exceptional — requires explicit confirmation, never silent.
