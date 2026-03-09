---
description: Check GAM supply viability before activation — run standalone or line-item forecasts with explicit credit warnings.
---

# OrbiAds — availability-forecast

Verify availability before creating, duplicating, or activating delivery. Compare targeting hypotheses without writing into GAM.

## When to Use

- User asks whether supply is sufficient for a delivery goal.
- Viability or underdelivery risk must be checked before activation.
- Tighter targeting may materially reduce available inventory.

**Do not use** if `adUnitIds` are not yet qualified — run `inventory-ad-units` first.

## Steps

1. Confirm active network and qualified `adUnitIds` or `lineItemId` are known.
2. Resolve targeting IDs: `get_available_countries`, `get_available_languages`, `get_device_categories`. `[free]`
3. Choose path:
   - New scenario → `get_standalone_forecast` `[variable]`
   - Existing line item → `get_delivery_forecast_by_line_item` `[variable]`
   - Direct inventory targeting → `get_inventory_forecast` `[variable]`
4. Run with explicit dates, creative sizes, and targeting assumptions.
5. Interpret `availableUnits`, `forecastUnits`, `possibleUnits`, pressure level.
6. Produce go / adjust / stop recommendation.
7. Hand off assumptions and risks.

## Abort Conditions

- Stop if `adUnitIds` are not confirmed — redirect to `inventory-ad-units`.
- Warn before every `[variable]` forecast call — state the credit cost implication first.
- Stop if creative sizes are missing for a display scenario.

## Output

Render as a structured artifact:

```
<handoff>
scenarioType: standalone | line-item | inventory
availableUnits: ...
pressureLevel: low | medium | high
recommendation: go | adjust-targeting | reduce-goal | stop
nextRecommendedSkill: advertiser-order-line-items
</handoff>
```

Apply extended thinking when comparing multiple targeting scenarios before choosing which forecast to run.
