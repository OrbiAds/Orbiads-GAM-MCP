# Agent Trigger — bootstrap

## Enter when

- the user mentions auth, tenant setup, network selection, or readiness checks;
- no confirmed `tenantId` or `networkCode` is available for the session;
- the user asks to refresh or switch network context.

## Do not enter when

- `tenantId` and `networkCode` are already confirmed in the session packet — reuse them instead;
- the user says "refresh" but a `networkCode` is already active — call `switch_network` directly, skip full bootstrap;
- the request is about inventory, placements, or creatives — route to the appropriate skill after confirming session state.

## Disambiguation

- "connect" or "reconnect" → full bootstrap;
- "switch network" with active session → `switch_network` call only, not full bootstrap;
- "check auth before creating…" → bootstrap first, then hand off to the named skill;
- "which network am I on?" → `get_network_info` only, not full bootstrap.
