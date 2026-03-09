---
description: Align GAM placements with qualified ad units, maintain targeting taxonomy, and validate Native/Fluid compatibility.
---

# OrbiAds — placements-targeting

Align placement structure with the selected ad-unit scope. Maintain the targeting taxonomy and audience-facing constraints.

## When to Use

- Placement creation, update, or review requests.
- Targeting keys, values, geo, language, or device preparation.
- Native delivery requires Fluid compatibility confirmation.

**Do not use** if `adUnitIds` are not yet qualified — run `inventory-ad-units` first.

## Steps

1. Verify bootstrap complete, reuse inventory scope when available.
2. `list_placements` — read current state. `[free]`
3. `list_custom_targeting_keys` + `get_custom_targeting_values` + geo/language/device lookups. `[free]`
4. Re-read or refine ad-unit subset with `search_ad_units` if needed. `[free]`
5. `validate_fluid` for any Native or Fluid path. `[free]`
6. `get_inventory_forecast` if tighter targeting could materially change supply. `[variable]`
7. Execute placement / targeting / ad-unit writes only after explicit approval of names, scope, and destructive impact.
8. Hand off placement and targeting packet.

## Key Tools

- `list_placements`, `list_custom_targeting_keys`, `get_custom_targeting_values`, `validate_fluid` — `[free]`
- `create_placement`, `update_placement` — writes, confirm naming and ad-unit grouping first
- `create_custom_targeting_key`, `create_custom_targeting_values` — writes, confirm taxonomy first
- `delete_custom_targeting_key` — destructive, explicit confirmation required
- `archive_placement`, `archive_ad_unit` — destructive, human review required

## Abort Conditions

- Stop if Native delivery is requested but `validate_fluid` has not passed.
- Surface destructive operations (key deletion, ad-unit archive) as a separate confirmation block — never bundle with safe writes.

## Output

Render placement coverage gap as an artifact table (existing vs. missing vs. proposed).

```
<handoff>
selectedAdUnitIds: [...]
placementIds: [...]
targetingKeyIds: [...]
fluidCompatible: true | false
nextRecommendedSkill: advertiser-order-line-items
</handoff>
```

Use extended thinking when taxonomy changes have downstream impact on existing line items.
