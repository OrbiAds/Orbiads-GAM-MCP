# Handoff

## The Skill Must Return

- confirmed `tenantId`;
- active `networkCode`;
- `authStatus`: `completed`, `pending`, `select_network`, or `expired`;
- `networkInitialized` indicator;
- optional useful context: balance, settings, delivery defaults.

## Open Risks to Surface

- browser authentication not completed;
- network selection still pending;
- network context not initialized;
- billing or settings not reviewed before a billed tool.

## Next Logical Step

- move to `inventory-ad-units` to explore or create inventory;
- or move to `availability-forecast` if the ad units are already known.