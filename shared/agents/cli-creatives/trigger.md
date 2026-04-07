# Agent Trigger — cli-creatives

## Enter when

- the user asks to list, upload, or manage creatives via CLI;
- a workflow needs creative IDs for association with line items.

## Do not enter when

- creative IDs are already confirmed in the session — pass them to the next skill;
- the request is about native image creatives via MCP — route to `native-image` instead;
- the request is about orders or line items only — route to `cli-orders`.

## Disambiguation

- "list creatives" → read path only, no write;
- "upload creative" → confirm file path and destination before proceeding;
- "check creative status" → read path only.