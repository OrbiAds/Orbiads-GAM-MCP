# Agent Trigger — cli-orders

## Enter when

- the user asks to look up or create advertisers, orders, or line items via CLI;
- a workflow needs a confirmed `orderId` or `advertiserId` for downstream skills.

## Do not enter when

- `orderId` and `advertiserId` are already confirmed — pass them directly;
- the request is about creatives only — route to `cli-creatives`;
- the request is about deployment — route to `cli-deploy`.

## Disambiguation

- "find advertiser" → search path only, no write;
- "create order" → confirm advertiser first, then create;
- "list my orders" → read path with `--json`.