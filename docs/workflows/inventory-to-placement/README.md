# Inventory to Placement

## Goal

- Start from a validated tenant and active GAM network.
- Qualify the inventory scope, compare current placement coverage, and align targeting.
- End with either executed placement updates or an approved placement handoff packet.

## Skill Composition

- `orbiads` (orchestrator — auth context and tenant confirmation)
- `inventory` (ad unit discovery, audit, fluid validation)
- `orbiads` → `inventory` (placement and targeting reads and writes)
- `reporting` (availability forecast when targeting pressure must be checked before trafficking)

## Entry Conditions

- `tenantId` and `networkCode` are known.
- The business scope is known: audit, expansion, placement review, or targeting preparation.
- Naming rules for ad units, placements, and custom targeting are available.

## Exit States

- inventory scope reviewed and documented;
- placement CRUD executed or explicitly deferred;
- targeting packet ready for advertiser, order, and line-item work.