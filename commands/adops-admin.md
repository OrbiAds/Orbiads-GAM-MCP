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

> **Call convention & write model — read this first.** `gam_admin` takes **two** discriminators: `area` and `action` (NOT a dotted `action="teams.create"`). Signature: `gam_admin(area="<area>", action="<action>", params={...})`.
> Areas: `teams`, `sites`, `applications`, `custom_fields`, `labels`, `entity_signals` (PPS), `users`, `user_team_associations`.
> **`gam_admin` writes execute immediately** — it has **no `dry_run` preview and no `confirmation_token`** flow (unlike `campaign`/`creatives`). Always surface exactly what will change and get the user's explicit go-ahead *before* calling a write action, because there is no server-side preview step to fall back on.

## teams

Read: `gam_admin(area="teams", action="list")` — returns all teams with their roles and ad unit/order access. `gam_admin(area="teams", action="get", params={team_id})` for detail.

Write (executes immediately — confirm with the user first):
1. Summarize the intended change — team name, member list, permissions scope. Wait for user confirmation.
2. Execute: `gam_admin(area="teams", action="create", params={name, description, ...})`.

Update: `gam_admin(area="teams", action="patch", params={team_id, ...})` — confirm with the user, then execute.

## sites

Read: `gam_admin(area="sites", action="list")` — site records with their associated ad units and networks.

Write: `gam_admin(area="sites", action="create", params={name, url, ...})` — confirm with the user first (executes immediately).

## labels

Read: `gam_admin(area="labels", action="list")` — network labels and their applied-to counts.

Write: `gam_admin(area="labels", action="create", params={name, description, ...})` — confirm with the user first (executes immediately).

Labels can be applied to ad units, line items, and orders — surface current application counts before deletion.

## custom-fields

Read: `gam_admin(area="custom_fields", action="list")` — custom field definitions (name, type, entity type).

Write: `gam_admin(area="custom_fields", action="create", params={name, entity_type, data_type, ...})` — confirm with the user first (executes immediately).

Before creating a new field, check for duplicates: `gam_admin(area="custom_fields", action="list")` filtered by entity type.

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
- `gam_admin` takes `area` + `action` (e.g. `area="teams", action="create"`), never a dotted `action="teams.create"`.
- `gam_admin` writes execute immediately — there is no `dry_run`/`confirmation_token` step. Never modify team permissions, labels, or custom fields without first getting the user's explicit approval of the exact change.
- Never switch the active network without confirming with the user — all subsequent reads and writes use the new context.
- Deleting a label applied to live inventory causes silent data loss in reports — always check application counts before proposing deletion.
- Never invent a `tenantId` or `networkCode`.
