# Allowed Tools

## Read-First Tools

- `list_ad_units` `[free]` — list active ad units in the network.
- `search_ad_units` `[free]` — search by name with pagination.
- `get_ad_unit_tree` `[free]` — rebuild the full hierarchy and detect orphaned nodes.
- `audit_inventory` `[variable]` — detect structure, naming, or placement-overload issues.
- `find_inactive_ad_units` `[free]` — identify cleanup candidates.

## Preparation Without Writes

- `generate_inventory_blueprint` `[variable]` — generate a consistent blueprint before any real creation.

## Writes with Mandatory Preview

- `create_ad_units_batch` `[free]` — create a batch of ad units with `dry_run=True`, then `confirmation_token`.
- `push_inventory_blueprint` `[variable]` — push a blueprint after preview and human validation.

## Destructive Boundary

- no bulk archive tool is currently documented here; keep cleanup to candidate discovery with `find_inactive_ad_units` until an approved archive path is exposed.