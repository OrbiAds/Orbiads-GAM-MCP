---
name: adops-admin
description: GAM network administration — teams, sites, labels, custom fields, network settings, feature flags. Exposed via the MCP surface only (no CLI equivalent for gam_admin actions).
argument-hint: "<teams|sites|labels|custom-fields|features|settings|network> [action]"
allowed-tools: mcp__orbiads__gam_admin,mcp__orbiads__network,mcp__orbiads__settings,mcp__orbiads__gam_features,mcp__orbiads__tenant_catalog
model: sonnet
---

# GAM Network Administration

Always confirm the tenant first: `get_my_tenant_id`. All read operations are free.

Load the `orbiads` orchestrator skill on first use; this command then delegates to the `admin` consolidated skill for detailed action guidance.

> **MCP-only surface**: `gam_admin` actions have no CLI equivalent in `orbiads-cli`. If a user is working in a terminal-only context, they must use the MCP server for these operations.

## teams

Read: `gam_admin(action="teams.list")` — returns all teams with their roles and ad unit/order access. `gam_admin(action="teams.get", params={team_id})` for detail.

Write (requires `confirmation_token`):
1. Preview: `gam_admin(action="teams.create", params={name, description, ..., dry_run: true})`.
2. Show `ExecutionPlan` — team name, member list, permissions scope. Wait for user confirmation.
3. Execute: `gam_admin(action="teams.create", params={..., confirmation_token: "<token>"})`.

Update: `gam_admin(action="teams.patch", params={team_id, ..., dry_run: true})` → confirm → execute.

## sites

Read: `gam_admin(action="sites.list")` — site records with their associated ad units and networks.

Write: `gam_admin(action="sites.create", params={name, url, ..., dry_run: true})` → confirm → execute.

## labels

Read: `gam_admin(action="labels.list")` — network labels and their applied-to counts.

Write: `gam_admin(action="labels.create", params={name, description, ..., dry_run: true})` → confirm → execute.

Labels can be applied to ad units, line items, and orders — surface current application counts before deletion.

## custom-fields

Read: `gam_admin(action="custom_fields.list")` — custom field definitions (name, type, entity type).

Write: `gam_admin(action="custom_fields.create", params={name, entity_type, data_type, ..., dry_run: true})` → confirm → execute.

Before creating a new field, check for duplicates: `gam_admin(action="custom_fields.list")` filtered by entity type.

## features

Read: `gam_features(action="get_gam_features")` — active beta and system feature flags on the network. Free, no confirmation needed.

Use this to verify feature availability before proposing operations that depend on optional GAM capabilities (e.g., first-look, roadblocking, native styles).

## settings

Read: `settings(action="get_naming_conventions")` — naming templates for orders, line items, creatives, placements.

Write: `settings(action="update_naming_conventions", params={...})` — requires `confirmation_token`. Naming convention changes affect the entire network; surface the diff clearly before executing.

## network

List accessible networks: `network(action="list_accessible_networks")` — free. Switch context: `network(action="switch_network", params={network_code})`.

Read network metadata: `network(action="get_network_info")` — GAM network code, display name, currency, time zone. Use this before any write to confirm the right network is active.

---

## Hard rules

- `gam_admin` has no CLI equivalent — always use the MCP surface for these operations.
- Never modify team permissions, labels, or custom fields without a dry-run preview approved by the user.
- Never switch the active network without confirming with the user — all subsequent reads and writes use the new context.
- Deleting a label applied to live inventory causes silent data loss in reports — always check application counts before proposing deletion.
- Never invent a `tenantId` or `networkCode`.
