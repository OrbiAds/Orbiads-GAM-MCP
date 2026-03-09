# Steps

1. [start] Verify that `bootstrap` is complete and reuse the selected inventory scope when available.
2. [depends: step 1] Read the current placement state with `list_placements`.
3. [depends: step 1] Read the current targeting taxonomy with key, value, geo, language, and device lookups; these reads are `[parallel-safe]`.
4. [depends: steps 2-3] Re-read or refine the ad-unit subset with `search_ad_units` if needed.
5. [depends: step 4] Run `validate_fluid` for any Native or Fluid path.
6. [depends: steps 3-5] Run `get_inventory_forecast` only when tighter targeting could materially change supply.
7. [depends: steps 2-6] Execute placement, targeting, or ad-unit writes only after explicit approval of names, scope, and destructive impact.
8. [depends: steps 2-7] Hand off the placement and targeting packet to the next trafficking workflow.

## Abort Conditions

- stop if the selected ad-unit scope is still ambiguous;
- stop before taxonomy deletion, ad-unit archive, or placement archive without approval;
- stop if targeting constraints and supply expectations clearly conflict.