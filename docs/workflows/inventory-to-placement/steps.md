# Steps

1. Use the `orbiads` skill to confirm the active tenant and network (`auth check_credentials`, `get_my_tenant_id`) instead of re-running authentication from scratch.
2. Scope the inventory with the `inventory` skill using `targeting(action="search_ad_units")`, `targeting(action="list_ad_units")`, `inventory(action="get_ad_units_by_ids")`, and `inventory(action="audit_inventory")`.
3. Freeze the approved ad unit subset before any placement or targeting write.
4. Read the current placement and targeting state using `placements(action="list_placements")`, targeting taxonomy reads via `targeting(action="list_custom_targeting_keys")` and `targeting(action="get_custom_targeting_values")`, and device / geo / language lookups.
5. Run `targeting(action="validate_fluid", params={ad_unit_id})` when Native or Fluid delivery is in scope.
6. Execute placement or taxonomy writes only after business approval of names, grouping rules, and destructive impact. All writes use the preview → confirm → execute gate.
7. Use the `reporting` skill (`reporting(action="get_standalone_forecast")`) only when the new placement or targeting plan could materially change supply.
8. Return a packet containing selected ad units, placement state, targeting state, and the recommended trafficking path.