---
name: adops-inventory
description: Browse and manage GAM ad units, placements, targeting taxonomy, and network blueprints. Read-heavy; blueprint and placement writes use preview→confirm→execute gate.
argument-hint: "<list-units|list-placements|targeting|forecast|blueprint|audit> [scope]"
allowed-tools: mcp__orbiads__inventory,mcp__orbiads__placements,mcp__orbiads__targeting,mcp__orbiads__blueprint,mcp__orbiads__reporting,mcp__orbiads__audiences
model: sonnet
---

# GAM Inventory, Placements, and Targeting

Always confirm the tenant first: `get_my_tenant_id`. All read operations are free.

Load the `orbiads` orchestrator skill on first use; this command then delegates to the `inventory` consolidated skill for detailed action guidance.

## list-units `[parent-id]`

`targeting(action="list_ad_units")` — returns the full ad unit tree. Pass `parent_ad_unit_id` to scope to a subtree. For targeted lookup: `targeting(action="search_ad_units", params={query})`. For bulk fetch by IDs: `inventory(action="get_ad_units_by_ids", params={ids: [...]})`.

Always list before any placement or targeting write — the business scope must be frozen first.

## list-placements `[name-filter]`

`placements(action="list_placements")` — returns all placements with their constituent ad unit IDs.

Before creating or updating: read current state. Before proposing names or grouping changes, call `settings(action="get_naming_conventions")` and apply the returned pattern.

## targeting

Reads (all free):
- `targeting(action="list_custom_targeting_keys")` — all custom targeting keys.
- `targeting(action="get_custom_targeting_values", params={key_id})` — values for a key.
- `targeting(action="get_available_countries")` — country lookups.
- `targeting(action="get_device_categories")` — device families.
- `targeting(action="get_browsers")` / `targeting(action="get_operating_systems")` — browser/OS lists.
- `targeting(action="get_content_labels")` — Google content categories.

Writes (require `confirmation_token` from dry-run preview):
- `targeting(action="create_custom_targeting_key", params={name, display_name, type, dry_run: true})` — preview first; then execute with `confirmation_token`.
- `targeting(action="create_custom_targeting_values", params={key_id, name, display_name, dry_run: true})`.
- `targeting(action="perform_custom_targeting_value_action", params={value_ids, action_type, dry_run: true})` — surface impact before acting on values.

Validate Native/Fluid targeting compatibility with `targeting(action="validate_fluid", params={ad_unit_id})`.

## forecast `[ad-unit-id]`

Before any write that changes supply, run an availability check via the `reporting` skill:

`reporting(action="get_standalone_forecast", params={targeting, line_item_type, start_date_time, end_date_time, units_bought})` — free. Present `available_units` vs. `units_bought` to the user.

If supply is tight or targeting is highly constrained, run `reporting(action="get_traffic_data", params={targeting, date_range})` for sizing context.

## blueprint `[generate|push|get]`

Read blueprint state: `blueprint(action="get_active_blueprint")` — free.

Generate a new blueprint: `inventory(action="generate_inventory_blueprint", params={network_code, ...})` — free, returns a draft blueprint.

Push blueprint to network (costs credits, requires `confirmation_token`):
1. Call `inventory(action="push_inventory_blueprint", params={..., dry_run: true})` — returns `ExecutionPlan` with mutations + estimated cost.
2. Show the plan to the user. Wait for explicit confirmation.
3. Call `inventory(action="push_inventory_blueprint", params={..., confirmation_token: "<token>"})`.

## audit

Run an inventory health check: `inventory(action="audit_inventory")` — free, returns anomalies, orphaned units, and structural issues. Follow with `inventory(action="find_inactive_ad_units")` (0.25 cr) to surface unused ad units.

For first-party audience health: `audiences(action="list_audience_segments")`.

---

## Hard rules

- Never freeze an ad unit subset before reading current state with `list_ad_units`.
- Never create a placement or targeting key without checking naming conventions first.
- Never run a blueprint push without a dry-run `ExecutionPlan` preview approved by the user.
- Targeting writes are destructive if values are in use — always surface which line items reference a key/value before deletion.
- Never invent a `tenantId` or `networkCode`.
