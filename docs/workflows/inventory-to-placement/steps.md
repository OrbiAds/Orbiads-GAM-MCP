# Steps

1. Reuse the `bootstrap` handoff instead of re-running authentication or network discovery.
2. Scope the inventory with `inventory-ad-units` using `search_ad_units`, `list_ad_units`, `get_ad_units_by_ids`, and `audit_inventory`.
3. Freeze the approved ad unit subset before any placement or targeting write.
4. Read the current placement and targeting state with `placements-targeting` using `list_placements`, targeting taxonomy reads, and device / geo / language lookups.
5. Run `validate_fluid` when Native or Fluid delivery is in scope.
6. Execute placement or taxonomy writes only after business approval of names, grouping rules, and destructive impact.
7. Run `availability-forecast` only when the new placement or targeting plan could materially change supply.
8. Return a packet containing selected ad units, placement state, targeting state, and the recommended trafficking path.