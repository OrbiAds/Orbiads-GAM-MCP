# Skill Chain

## Dependency Graph

```text
bootstrap
    │
    ▼
inventory-ad-units ─────────────────────────────┐
    │                                            │
    ▼                                            ▼
placements-targeting                  availability-forecast
    │                                            │
    └──────────────────┬─────────────────────────┘
                       │
                       ▼
           advertiser-order-line-items
                       │
           ┌───────────┴────────────┐
           │                        │
           ▼                        ▼
      native-image            (direct to qa)
           │                        │
           └───────────┬────────────┘
                       │
                       ▼
                  qa-preview
                       │
                       ▼
              deploy-reporting
```

## Canonical Progression

1. `bootstrap`
2. `inventory-ad-units`
3. `placements-targeting`
4. `availability-forecast`
5. `advertiser-order-line-items`
6. `native-image`
7. `qa-preview`
8. `deploy-reporting`

## Alternate Entries

- start at `availability-forecast` when the user already has a stable inventory packet;
- start at `advertiser-order-line-items` when the network, advertiser, and trafficking scope are already known;
- start at `deploy-reporting` for live-campaign monitoring or rollback analysis.

## Parallel Branches

- `placements-targeting` and `availability-forecast` can run independently once `inventory-ad-units` has confirmed `adUnitIds`;
- `native-image` and direct-to-qa paths converge at `qa-preview` — both require confirmed `lineItemIds`.

## Rule

- wrappers should route through the orchestrator first, then enter the smallest useful skill from this chain.
