# Allowed Tools

## Placement Reads and Writes

- `list_placements` `[free]` — inspect the current placement catalog.
- `create_placement` `[free]` — create a new placement for the approved ad-unit subset.
- `update_placement` `[free]` — revise an existing placement.
- `archive_placement` `[free]` — exceptional placement deactivation.

## Targeting Taxonomy Reads

- `list_custom_targeting_keys` `[free]` — list targeting keys and attached values.
- `get_custom_targeting_values` `[free]` — re-read the values of one targeting key.
- `search_custom_targeting` `[free]` — search the taxonomy by name.
- `get_available_countries` `[free]` — inspect country targeting choices.
- `get_available_languages` `[free]` — inspect language targeting choices.
- `get_device_categories` `[free]` — inspect device targeting choices.
- `search_ad_units` `[free]` — re-read or refine the ad-unit subset from targeting work.

## Compatibility and Supply Checks

- `validate_fluid` `[free]` — confirm Native / Fluid compatibility on the selected ad units.
- `get_inventory_forecast` `[variable]` — estimate the impact of a constrained targeting scope.

## Targeting and Inventory Writes

- `create_custom_targeting_key` `[free]` — create a new targeting key.
- `create_custom_targeting_values` `[free]` — create values under a targeting key.
- `update_custom_targeting_key` `[free]` — revise key metadata.
- `delete_custom_targeting_key` `[free]` — exceptional taxonomy deletion.
- `update_ad_unit` `[free]` — revise ad-unit metadata when targeting alignment requires it.
- `archive_ad_unit` `[free]` — exceptional inventory cleanup after explicit review.