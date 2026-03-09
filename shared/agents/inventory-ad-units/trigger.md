# Agent Trigger — inventory-ad-units

## Enter when

- the user asks for inventory audit, ad-unit lookup, naming cleanup, or batch creation;
- a workflow needs confirmed `adUnitIds` before placements, targeting, or forecasting.

## Do not enter when

- `adUnitIds` are already confirmed in the session packet — pass them directly to the next skill;
- the request is about placements or targeting only — route to `placements-targeting` instead;
- the request is a supply check — route to `availability-forecast` with the existing `adUnitIds`.

## Disambiguation

- "list my ad units" → read path only, no write;
- "create ad units" → always starts with audit, then blueprint, then dry_run batch — never direct write;
- "clean up inactive ad units" → `find_inactive_ad_units` first, human review required before any archive;
- "show me the inventory tree" → `get_ad_unit_tree`, single read call, no downstream routing needed.
