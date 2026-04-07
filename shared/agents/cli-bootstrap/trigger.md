# Agent Trigger — cli-bootstrap

## Enter when

- the user wants to verify CLI installation or authentication;
- no confirmed `tenantId` or `networkCode` is available for the CLI session;
- the user asks to switch or refresh network context via CLI.

## Do not enter when

- `tenantId` and `networkCode` are already confirmed — reuse them instead;
- the request is about inventory, creatives, or orders — route to the appropriate CLI skill after confirming session state.

## Disambiguation

- "check CLI" or "orbiads status" → full bootstrap;
- "switch network" with active session → network switch only, not full bootstrap;
- "am I authenticated?" → `orbiads auth status --json` only.