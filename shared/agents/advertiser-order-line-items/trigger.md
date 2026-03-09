# Agent Trigger — advertiser-order-line-items

## Enter when

- the user asks to resolve an advertiser, create or update an order, or manage line items;
- a workflow is ready to move from inventory and targeting into trafficking.

## Do not enter when

- advertiser, order, and line-item IDs are already confirmed — pass them directly to `native-image` or `qa-preview`;
- the request is about placements or targeting only — route to `placements-targeting` first;
- the user just wants to check supply — route to `availability-forecast` instead.

## Disambiguation

- "find or create the advertiser for brand X" → `find_or_create_advertiser`, read-first;
- "create line items for this order" → always job-backed batch, never direct low-level create;
- "activate line items" → requires `verify_line_item_setup` and explicit confirmation before activation;
- "set up a preferred deal line item" → valid path but requires a confirmed deal ID first;
- "open bidding line item" → capability boundary only, return NOT_IMPLEMENTED clearly.
