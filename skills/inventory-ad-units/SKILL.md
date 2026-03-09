---
description: Audit, explore, blueprint, and batch-create GAM ad units with mandatory dry_run gates.
---

# OrbiAds — inventory-ad-units

Explore the existing GAM inventory, qualify the ad units needed for a workflow, and create or push new ad units in a controlled way.

## When to Use

- Inventory audit, ad-unit lookup, naming cleanup, or batch creation.
- A workflow needs confirmed `adUnitIds` before placements, targeting, or forecasting.

**Do not use** if `adUnitIds` are already confirmed — pass them directly to the next skill.

## Steps

1. Verify bootstrap is complete and active network is initialized.
2. `list_ad_units` + `search_ad_units` + `get_ad_unit_tree` + `audit_inventory` — read first. `[free]`
3. If specific subset needed → `get_ad_units_by_ids`. `[free]`
4. Choose path: read-only review / direct creation / blueprint generation.
5. Always `dry_run=True` first for any write batch.
6. Ask human validation of names, parents, sizes, volumes.
7. Execute only after explicit confirmation.
8. Hand off `adUnitIds` and residual risks.

## Key Tools

- `list_ad_units`, `search_ad_units`, `get_ad_unit_tree`, `audit_inventory`, `find_inactive_ad_units` — `[free]`
- `generate_inventory_blueprint` — preview without write `[free]`
- `create_ad_units_batch` — write, requires `dry_run=True` then confirmation token
- `push_inventory_blueprint` — write after human validation
- `archive_inactive_ad_units` — destructive, human review required

## Abort Conditions

- Stop before any write if `dry_run` preview has not been shown and approved.
- Stop if naming conflicts or missing parent are unresolved.

## Output

Render the ad-unit tree as a collapsible artifact when hierarchy > 10 nodes.
Show the dry_run preview as an artifact before asking for confirmation.

```
<handoff>
selectedAdUnitIds: [...]
auditFindings: [...]
confirmationNeeded: true | false
nextRecommendedSkill: placements-targeting | availability-forecast
</handoff>
```
