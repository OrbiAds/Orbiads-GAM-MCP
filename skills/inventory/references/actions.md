---
name: orbiads-inventory-actions
description: Full action catalogue for the orbiads-inventory skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Inventory & Targeting Management: Action Catalogue

Full per-tool action reference for the [`orbiads-inventory`](../SKILL.md) skill. 85 actions across 6 parent tool(s); CLI coverage 37/85 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:audiences` (Epic 68.2)

_Parent audiences tool for the Epic 68.2 catalogue refactor batch._

- **Mode:** mixed · **Actions:** 8 (5 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 5/8 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 5 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create_audience_segment` | 0.5 | yes | required | `orbiads audiences create` |
| `perform_audience_segment_action` | 0 | yes | — | `orbiads audiences action` |
| `perform_segment_population_action` | 0 | yes | — | MCP-only |
| `update_audience_segment` | 0 | yes | — | `orbiads audiences update` |
| `update_segment_memberships` | 0.5 | yes | required | MCP-only |
| `get_audience_segment` | 0 | — | — | `orbiads audiences get` |
| `get_segment_population_results` | 0 | — | — | MCP-only |
| `list_audience_segments` | 0 | — | — | `orbiads audiences list` |

### `orbiads:blueprint` (Epic 78.13)

_Parent blueprint MCP tool — CRUD on tenant inventory blueprint (Story 78.13)._

- **Mode:** mixed · **Actions:** 20 (7 writes, 13 reads)
- **Surfaces:** MCP ✅ · CLI 0/20 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `remove_format` | 0.25 | yes | required | MCP-only |
| `remove_key_value` | 0.25 | yes | required | MCP-only |
| `remove_position` | 0.25 | yes | required | MCP-only |
| `save_blueprint` | 0.25 | yes | required | MCP-only |
| `save_preferences` | 0.25 | yes | required | MCP-only |
| `update_brand` | 0.25 | yes | required | MCP-only |
| `update_platforms` | 0.25 | yes | required | MCP-only |
| `add_format` | 0.25 | — | — | MCP-only |
| `add_key_value` | 0.25 | — | — | MCP-only |
| `add_position` | 0.25 | — | — | MCP-only |
| `get_active_blueprint` | 0 | — | — | MCP-only |
| `get_active_preferences` | 0 | — | — | MCP-only |
| `get_block_version` | 0 | — | — | MCP-only |
| `get_diff` | 0 | — | — | MCP-only |
| `get_preview_url` | 0 | — | — | MCP-only |
| `get_v2` | 0 | — | — | MCP-only |
| `list_block_versions` | 0 | — | — | MCP-only |
| `list_drafts` | 0 | — | — | MCP-only |
| `list_packages` | 0 | — | — | MCP-only |
| `list_templates` | 0 | — | — | MCP-only |

### `orbiads:inventory` (Epic 68.6)

_Parent inventory tool for Story 68.6._

- **Mode:** mixed · **Actions:** 14 (3 writes, 11 reads)
- **Surfaces:** MCP ✅ · CLI 10/14 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 10 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `archive_inactive_ad_units` | 0 | yes | — | `orbiads inventory archive-inactive` |
| `create_ad_units_batch` | 0.5 | yes | required | `orbiads inventory save-adunits` |
| `push_inventory_blueprint` | 0.5 | yes | required | `orbiads inventory blueprint-push` |
| `audit_inventory` | 0 | — | — | `orbiads inventory audit` |
| `blueprint_starter` | 0 | — | — | MCP-only |
| `find_inactive_ad_units` | 0.25 | — | — | `orbiads inventory list-inactive` |
| `generate_ads_json` | 0 | — | — | `orbiads inventory ads-json` |
| `generate_inventory_blueprint` | 0 | — | — | `orbiads inventory blueprint-generate` |
| `get_ad_unit_tree` | 0 | — | — | `orbiads inventory ad-units` |
| `get_ad_units_by_ids` | 0 | — | — | `orbiads inventory ad-units-by-ids` |
| `get_catalog` | 0 | — | — | MCP-only |
| `list_ad_unit_sizes` | 0 | — | — | `orbiads inventory sizes` |
| `list_line_item_templates` | 0 | — | — | MCP-only |
| `list_suggested_ad_units` | 0 | — | — | MCP-only |

### `orbiads:placements` (Epic 68.6)

_Parent placements tool for Story 68.6._

- **Mode:** mixed · **Actions:** 6 (5 writes, 1 reads)
- **Surfaces:** MCP ✅ · CLI 4/6 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 4 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `activate_placement` | 0 | yes | — | MCP-only |
| `archive_placement` | 0 | yes | — | `orbiads inventory placement-archive` |
| `create_placement` | 0.5 | yes | required | `orbiads inventory placement-create` |
| `deactivate_placement` | 0 | yes | — | MCP-only |
| `update_placement` | 0 | yes | — | `orbiads inventory placement-update` |
| `list_placements` | 0 | — | — | `orbiads inventory placements` |

### `orbiads:targeting` (Epic 68.6)

_Parent targeting tool for Story 68.6._

- **Mode:** mixed · **Actions:** 27 (13 writes, 14 reads)
- **Surfaces:** MCP ✅ · CLI 18/27 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 21 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `activate_ad_unit` | 0 | yes | — | MCP-only |
| `archive_ad_unit` | 0 | yes | — | `orbiads inventory archive-ad-unit` |
| `create_custom_targeting_key` | 0.5 | yes | required | `orbiads inventory create-key` |
| `create_custom_targeting_values` | 0.5 | yes | required | `orbiads custom-targeting-values create` |
| `create_targeting_preset` | 0.5 | yes | required | MCP-only |
| `deactivate_ad_unit` | 0 | yes | — | MCP-only |
| `delete_custom_targeting_key` | 0 | yes | — | `orbiads inventory delete-key` |
| `delete_targeting_preset` | 0 | yes | — | MCP-only |
| `perform_custom_targeting_value_action` | 0 | yes | — | `orbiads custom-targeting-values action` |
| `update_ad_unit` | 0 | yes | — | `orbiads inventory update-ad-unit` |
| `update_custom_targeting_key` | 0 | yes | — | `orbiads inventory update-key` |
| `update_custom_targeting_value` | 0 | yes | — | `orbiads custom-targeting-values update` |
| `update_targeting_preset` | 0 | yes | — | MCP-only |
| `get_available_countries` | 0 | — | — | `orbiads inventory countries` |
| `get_available_languages` | 0 | — | — | `orbiads inventory languages` |
| `get_browsers` | 0 | — | — | MCP-only |
| `get_content_labels` | 0 | — | — | MCP-only |
| `get_custom_targeting_values` | 0 | — | — | `orbiads custom-targeting-values list` |
| `get_device_categories` | 0 | — | — | `orbiads inventory device-categories` |
| `get_inventory_forecast` | 0 | — | — | `orbiads inventory forecast` |
| `get_operating_systems` | 0 | — | — | MCP-only |
| `list_ad_units` | 0 | — | — | `orbiads inventory ad-units` |
| `list_custom_targeting_keys` | 0 | — | — | `orbiads inventory keys` |
| `list_targeting_presets` | 0 | — | — | MCP-only |
| `search_ad_units` | 0 | — | — | `orbiads inventory search-ad-units` |
| `search_custom_targeting` | 0 | — | — | `orbiads inventory search-custom-targeting` |
| `validate_fluid` | 0 | — | — | `orbiads inventory validate-fluid` |

### `orbiads:video_ops` (Epic 98)

_Video monetization: ad rule management, content metadata, and content bundle operations._

- **Mode:** mixed · **Actions:** 10 (7 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 0/10 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `activate_content_bundle` | 0 | yes | — | MCP-only |
| `create_ad_rule` | 0 | yes | — | MCP-only |
| `create_content_bundle` | 0 | yes | — | MCP-only |
| `deactivate_content_bundle` | 0 | yes | — | MCP-only |
| `delete_ad_rule` | 0 | yes | — | MCP-only |
| `update_ad_rule` | 0 | yes | — | MCP-only |
| `update_content_bundle` | 0 | yes | — | MCP-only |
| `list_ad_rules` | 0 | — | — | MCP-only |
| `list_content` | 0 | — | — | MCP-only |
| `list_content_bundles` | 0 | — | — | MCP-only |

