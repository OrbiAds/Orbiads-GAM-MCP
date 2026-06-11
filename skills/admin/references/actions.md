---
name: orbiads-admin-actions
description: Full action catalogue for the orbiads-admin skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Network Administration & Settings: Action Catalogue

Full per-tool action reference for the [`orbiads-admin`](../SKILL.md) skill. 87 actions across 5 parent tool(s); CLI coverage 13/87 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:gam_admin` (Epic 65)

_GAM admin orchestration — single entry point for 54 ops over 7 areas._

- **Mode:** mixed · **Actions:** 58 (19 writes, 39 reads)
- **Surfaces:** MCP ✅ · CLI 0/58 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `applications.create` | 0 | yes | — | MCP-only |
| `applications.patch` | 0 | yes | — | MCP-only |
| `custom_fields.create` | 0 | yes | — | MCP-only |
| `custom_fields.patch` | 0 | yes | — | MCP-only |
| `entity_signals.create` | 0 | yes | — | MCP-only |
| `entity_signals.patch` | 0 | yes | — | MCP-only |
| `labels.create` | 0 | yes | — | MCP-only |
| `labels.patch` | 0 | yes | — | MCP-only |
| `sites.create` | 0 | yes | — | MCP-only |
| `sites.patch` | 0 | yes | — | MCP-only |
| `teams.create` | 0 | yes | — | MCP-only |
| `teams.patch` | 0 | yes | — | MCP-only |
| `user_team_associations.create` | 0 | yes | — | MCP-only |
| `user_team_associations.delete` | 0 | yes | — | MCP-only |
| `user_team_associations.update` | 0 | yes | — | MCP-only |
| `users.activate` | 0 | yes | — | MCP-only |
| `users.create` | 0 | yes | — | MCP-only |
| `users.deactivate` | 0 | yes | — | MCP-only |
| `users.update` | 0 | yes | — | MCP-only |
| `applications.batch_archive` | 0 | — | — | MCP-only |
| `applications.batch_create` | 0 | — | — | MCP-only |
| `applications.batch_unarchive` | 0 | — | — | MCP-only |
| `applications.batch_update` | 0 | — | — | MCP-only |
| `applications.get` | 0 | — | — | MCP-only |
| `applications.list` | 0 | — | — | MCP-only |
| `custom_fields.batch_activate` | 0 | — | — | MCP-only |
| `custom_fields.batch_create` | 0 | — | — | MCP-only |
| `custom_fields.batch_deactivate` | 0 | — | — | MCP-only |
| `custom_fields.batch_update` | 0 | — | — | MCP-only |
| `custom_fields.get` | 0 | — | — | MCP-only |
| `custom_fields.list` | 0 | — | — | MCP-only |
| `entity_signals.batch_create` | 0 | — | — | MCP-only |
| `entity_signals.batch_update` | 0 | — | — | MCP-only |
| `entity_signals.get` | 0 | — | — | MCP-only |
| `entity_signals.list` | 0 | — | — | MCP-only |
| `labels.batch_activate` | 0 | — | — | MCP-only |
| `labels.batch_create` | 0 | — | — | MCP-only |
| `labels.batch_deactivate` | 0 | — | — | MCP-only |
| `labels.batch_update` | 0 | — | — | MCP-only |
| `labels.get` | 0 | — | — | MCP-only |
| `labels.list` | 0 | — | — | MCP-only |
| `sites.batch_create` | 0 | — | — | MCP-only |
| `sites.batch_deactivate` | 0 | — | — | MCP-only |
| `sites.batch_submit_for_approval` | 0 | — | — | MCP-only |
| `sites.batch_update` | 0 | — | — | MCP-only |
| `sites.get` | 0 | — | — | MCP-only |
| `sites.list` | 0 | — | — | MCP-only |
| `teams.batch_activate` | 0 | — | — | MCP-only |
| `teams.batch_create` | 0 | — | — | MCP-only |
| `teams.batch_deactivate` | 0 | — | — | MCP-only |
| `teams.batch_update` | 0 | — | — | MCP-only |
| `teams.get` | 0 | — | — | MCP-only |
| `teams.list` | 0 | — | — | MCP-only |
| `user_team_associations.list` | 0 | — | — | MCP-only |
| `users.current` | 0 | — | — | MCP-only |
| `users.get` | 0 | — | — | MCP-only |
| `users.get_roles` | 0 | — | — | MCP-only |
| `users.list` | 0 | — | — | MCP-only |

### `orbiads:gam_features` (Epic 68.5)

_Parent gam_features tool for the Epic 68.5 catalogue refactor batch._

- **Mode:** read-only · **Actions:** 3 (0 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 0/3 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 3 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `get_gam_features` | 0 | — | — | MCP-only |
| `probe_gam_features` | 0.5 | — | — | MCP-only |
| `refresh_gam_features` | 0 | — | — | MCP-only |

### `orbiads:network` (Epic 68.5)

_Parent network tool for the Epic 68.5 catalogue refactor batch._

- **Mode:** mixed · **Actions:** 6 (3 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 4/6 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 4 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `set_preview_url_library` | 0 | yes | — | MCP-only |
| `switch_network` | 0 | yes | — | `orbiads network switch` |
| `update_network` | 0 | yes | — | `orbiads network update` |
| `get_network_info` | 0 | — | — | `orbiads network gam-info` |
| `get_preview_url_library` | 0 | — | — | MCP-only |
| `list_accessible_networks` | 0 | — | — | `orbiads network list` |

### `orbiads:settings` (Epic 68.1)

_Parent settings tool for the Epic 68.1 catalogue refactor POC._

- **Mode:** mixed · **Actions:** 16 (7 writes, 9 reads)
- **Surfaces:** MCP ✅ · CLI 9/16 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 9 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `accept_preset_suggestion` | 0 | yes | — | MCP-only |
| `create_preset` | 0 | yes | — | `orbiads settings presets create` |
| `delete_preset` | 0 | yes | — | `orbiads settings presets delete` |
| `update_delivery_defaults` | 0 | yes | — | `orbiads settings delivery-defaults set` |
| `update_naming_conventions` | 0 | yes | — | `orbiads settings naming set` |
| `update_preset` | 0 | yes | — | MCP-only |
| `update_tenant_settings` | 0 | yes | — | `orbiads settings general set` |
| `dismiss_preset_suggestion` | 0 | — | — | MCP-only |
| `get_delivery_defaults` | 0 | — | — | `orbiads settings delivery-defaults get` |
| `get_multilang_matrix` | 0 | — | — | MCP-only |
| `get_naming_conventions` | 0 | — | — | `orbiads settings naming get` |
| `get_tenant_settings` | 0 | — | — | `orbiads settings general get` |
| `list_preset_suggestions` | 0 | — | — | MCP-only |
| `list_presets` | 0 | — | — | `orbiads settings presets list` |
| `list_preview_matrices` | 0 | — | — | MCP-only |
| `recompute_preset_suggestions` | 0 | — | — | MCP-only |

### `orbiads:tenant_catalog` (Epic 78.1)

_Parent tenant_catalog MCP tool — scan + read tenant inventory catalog (Story 78.1)._

- **Mode:** mixed · **Actions:** 4 (2 writes, 2 reads)
- **Surfaces:** MCP ✅ · CLI 0/4 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `refresh` | 1 | yes | required | MCP-only |
| `scan_network` | 1 | yes | required | MCP-only |
| `get_active_catalog` | 0 | — | — | MCP-only |
| `get_scan_status` | 0 | — | — | MCP-only |

