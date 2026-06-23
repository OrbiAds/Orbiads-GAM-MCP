---
name: orbiads-campaigns-actions
description: Full action catalogue for the orbiads-campaigns skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Campaign Operations & Creative QA: Action Catalogue

Full per-tool action reference for the [`orbiads-campaigns`](../SKILL.md) skill. 149 actions across 12 parent tool(s); CLI coverage 106/149 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:ad_review_center`

_Ad Review Center - search, allow, or block Ad Exchange creatives._

- **Mode:** read-only · **Actions:** 3 (0 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 3/3 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `allow_batch` | 0 | — | — | `orbiads ad-review allow` |
| `block_batch` | 0 | — | — | `orbiads ad-review block` |
| `search` | 0 | — | — | `orbiads ad-review search` |

### `orbiads:campaign` (Epic 20.1)

_Parent campaign tool for deployment, update, rollback, and lifecycle orchestration._

- **Mode:** mixed · **Actions:** 16 (12 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 11/16 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 13 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `archive` | 0 | yes | — | `orbiads campaigns archive` |
| `archive_eligible` | 0 | yes | — | MCP-only |
| `create_display` | 0 | yes | — | MCP-only |
| `create_draft` | 0 | yes | — | MCP-only |
| `create_licas` | 0 | yes | — | `orbiads campaigns attach-creatives` |
| `create_line_items_batch` | 1 | yes | required | `orbiads campaigns add-line-items` |
| `create_native_style` | 0.5 | yes | required | MCP-only |
| `deploy` | 0 | yes | — | `orbiads campaigns deploy` |
| `deploy_media` | 1 | yes | required | `orbiads campaigns deploy-media` |
| `pause` | 0 | yes | — | `orbiads campaigns pause` |
| `rollback` | 0 | yes | — | `orbiads campaigns recover` |
| `update` | 0 | yes | — | `orbiads campaigns update` |
| `dry_run` | 0 | — | — | `orbiads campaigns dry-run` |
| `ensure_template` | 0 | — | — | MCP-only |
| `plan_deployment` | 0 | — | — | `orbiads campaigns plan-deployment` |
| `read` | 0 | — | — | `orbiads campaigns read` |

### `orbiads:creative_assets` (Epic 68.7d)

_Parent creative asset tool for upload/create/compress/transcode actions._

- **Mode:** mixed · **Actions:** 22 (19 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 18/22 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 18 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create_aspect_ratio_image` | 0 | yes | — | MCP-only |
| `create_audio` | 0 | yes | — | `orbiads creatives upload-audio` |
| `create_classic_native` | 0 | yes | — | `orbiads creatives upload-native-classic` |
| `create_click_tracking` | 0 | yes | — | `orbiads creatives upload-click-tracking` |
| `create_companion` | 0 | yes | — | `orbiads creatives upload-companion` |
| `create_custom` | 0 | yes | — | `orbiads creatives upload-custom` |
| `create_hosted_audio` | 0 | yes | — | MCP-only |
| `create_hosted_video` | 0 | yes | — | MCP-only |
| `create_html5` | 0 | yes | — | `orbiads creatives upload-html5` |
| `create_html5_from_files` | 0 | yes | — | `orbiads creatives upload-html5` |
| `create_image` | 0 | yes | — | `orbiads creatives upload-images` |
| `create_image_redirect` | 0 | yes | — | `orbiads creatives upload-image-redirect` |
| `create_internal_redirect` | 0 | yes | — | `orbiads creatives upload-internal-redirect` |
| `create_third_party` | 0 | yes | — | `orbiads creatives upload-third-party` |
| `create_vast_redirect` | 0 | yes | — | `orbiads creatives upload-vast-redirect` |
| `create_video` | 0 | yes | — | `orbiads creatives upload-video` |
| `upload_and_associate` | 0 | yes | — | `orbiads creatives upload` |
| `upload_from_url` | 0 | yes | — | `orbiads creatives upload-url` |
| `upload_html5_zip` | 0 | yes | — | `orbiads creatives upload-html5` |
| `bulk_upload` | 0 | — | — | `orbiads creatives upload-images` |
| `compress_image` | 0 | — | — | `orbiads creatives compress-image` |
| `get_video_transcode_status` | 0 | — | — | MCP-only |

### `orbiads:creative_qa` (Epic 68.6)

_Parent creative QA tool for Story 68.6._

- **Mode:** read-only · **Actions:** 7 (0 writes, 7 reads)
- **Surfaces:** MCP ✅ · CLI 7/7 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 7 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `audit_creative_tracking` | 0.5 | — | — | `orbiads creative-qa audit-tracking` |
| `audit_order_tracking` | 0.5 | — | — | `orbiads creative-qa audit-order-tracking` |
| `pre_archive_check` | 0.5 | — | — | `orbiads creative-qa pre-archive-check` |
| `scan_creative_compliance` | 0 | — | — | `orbiads creative-qa scan-compliance` |
| `validate_creative_ssl` | 0 | — | — | `orbiads creative-qa validate-ssl` |
| `validate_creative_ssl_batch` | 0 | — | — | `orbiads creative-qa validate-ssl-batch` |
| `validate_tag_snippet` | 0 | — | — | `orbiads creative-qa validate-tag` |

### `orbiads:creative_wrapper_skill` (Epic 76.1)

_Manage GAM CreativeWrapper entities (AdUnit/Placement level wrapping) through one parent tool._

- **Mode:** mixed · **Actions:** 13 (7 writes, 6 reads)
- **Surfaces:** MCP ✅ · CLI 10/13 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `activate` | 0 | yes | — | `orbiads creative-wrappers activate` |
| `archive` | 0 | yes | — | MCP-only |
| `create` | 0 | yes | — | `orbiads creative-wrappers create` |
| `create_preset` | 0 | yes | — | MCP-only |
| `deactivate` | 0 | yes | — | `orbiads creative-wrappers deactivate` |
| `set_data_declaration` | 0 | yes | — | `orbiads creative-wrappers set-data-declaration` |
| `update` | 0 | yes | — | `orbiads creative-wrappers update` |
| `find_third_party_company` | 0 | — | — | `orbiads creative-wrappers find-company` |
| `get` | 0 | — | — | `orbiads creative-wrappers get` |
| `list` | 0 | — | — | `orbiads creative-wrappers list` |
| `list_rich_media_ads_companies` | 0 | — | — | `orbiads creative-wrappers list-companies` |
| `list_wrapper_presets` | 0 | — | — | MCP-only |
| `provision` | 0 | — | — | `orbiads creative-wrappers provision` |

### `orbiads:creatives` (Epic 68.7d)

_Parent creatives tool for the Epic 68.7d catalogue refactor batch._

- **Mode:** mixed · **Actions:** 30 (13 writes, 17 reads)
- **Surfaces:** MCP ✅ · CLI 27/30 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 27 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `archive_creative` | 0 | yes | — | `orbiads creatives archive` |
| `archive_native_style` | 0 | yes | — | `orbiads native-styles archive` |
| `associate_creative` | 0 | yes | — | `orbiads campaigns attach-creatives` |
| `bulk_associate_creatives` | 0 | yes | — | `orbiads campaigns attach-creatives` |
| `create_creative_set` | 0 | yes | — | MCP-only |
| `deactivate_lica` | 0 | yes | — | `orbiads licas deactivate` |
| `delete_licas` | 0 | yes | — | `orbiads licas delete` |
| `duplicate_creative` | 0.5 | yes | required | `orbiads creatives duplicate` |
| `duplicate_native_style` | 0.5 | yes | required | `orbiads native-styles duplicate` |
| `update_creative` | 0 | yes | — | `orbiads creatives update` |
| `update_creative_set` | 0 | yes | — | MCP-only |
| `update_lica` | 0 | yes | — | `orbiads licas update` |
| `update_native_style` | 0 | yes | — | `orbiads native-styles update` |
| `discover_native_formats` | 0.5 | — | — | `orbiads creative-templates list` |
| `ensure_classic_native_template` | 0 | — | — | `orbiads creative-templates ensure-classic-native` |
| `get_campaign_preview_links` | 0 | — | — | `orbiads preview campaign` |
| `get_creative` | 0 | — | — | `orbiads creatives get` |
| `get_creative_preview_url` | 0 | — | — | `orbiads creatives preview-url` |
| `get_creative_template` | 0 | — | — | `orbiads creative-templates get` |
| `get_licas_batch` | 0 | — | — | `orbiads licas batch` |
| `get_licas_by_line_item` | 0 | — | — | `orbiads licas list-by-line-item` |
| `get_native_style` | 0 | — | — | `orbiads native-styles get` |
| `get_native_style_preview_urls` | 0 | — | — | `orbiads creatives native-style-previews` |
| `get_video_transcode_status` | 0 | — | — | `orbiads creatives transcode-status` |
| `list_creative_sets` | 0 | — | — | MCP-only |
| `list_creative_templates` | 0 | — | — | `orbiads creative-templates list` |
| `list_creatives_by_advertiser` | 0 | — | — | `orbiads creatives list` |
| `list_creatives_by_line_item` | 0 | — | — | `orbiads creatives list-by-line-item` |
| `list_creatives_by_network` | 0 | — | — | `orbiads creatives list-by-network` |
| `list_native_styles` | 0 | — | — | `orbiads native-styles list` |

### `orbiads:formats` (Epic 78.2)

_Parent formats MCP tool — Custom Format Registry avec scope multi-site (Story 78.2)._

- **Mode:** mixed · **Actions:** 9 (5 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 0/9 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `accept_suggested_recipe` | 0.25 | yes | required | MCP-only |
| `delete_recipe` | 0.25 | yes | required | MCP-only |
| `register_recipe` | 0.25 | yes | required | MCP-only |
| `reject_suggested_recipe` | 0.25 | yes | required | MCP-only |
| `update_recipe` | 0.25 | yes | required | MCP-only |
| `detect_conflicts` | 0 | — | — | MCP-only |
| `list_recipes` | 0 | — | — | MCP-only |
| `list_suggested_recipes` | 0 | — | — | MCP-only |
| `resolve` | 0 | — | — | MCP-only |

### `orbiads:gam_jobs` (Epic 82)

_Async job dispatcher (parent>child pattern, Epic 82)._

- **Mode:** read-only · **Actions:** 4 (0 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 0/4 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `audit-export` | 0 | — | — | MCP-only |
| `blueprint-generate` | 0 | — | — | MCP-only |
| `image-optimize` | 0 | — | — | MCP-only |
| `poll` | 0 | — | — | MCP-only |

### `orbiads:jobs` (Epic 68.2)

_Parent jobs tool for the Epic 68.2 catalogue refactor batch._

- **Mode:** mixed · **Actions:** 3 (1 writes, 2 reads)
- **Surfaces:** MCP ✅ · CLI 3/3 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 3 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `duplicate_job` | 0 | yes | — | `orbiads jobs duplicate` |
| `get_job` | 0 | — | — | `orbiads jobs get` |
| `list_jobs` | 0 | — | — | `orbiads jobs list` |

### `orbiads:line_items` (Epic 68)

_Parent line_items tool for non-lifecycle Line Item operations._

- **Mode:** mixed · **Actions:** 18 (13 writes, 5 reads)
- **Surfaces:** MCP ✅ · CLI 16/18 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 16 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `activate_batch` | 0 | yes | — | `orbiads line-items activate` |
| `approve` | 0 | yes | — | `orbiads line-items approve` |
| `archive` | 0 | yes | — | `orbiads line-items archive` |
| `create` | 0 | yes | — | `orbiads campaigns add-line-items` |
| `create_adexchange` | 0 | yes | — | `orbiads line-items create-adexchange` |
| `create_batch` | 0 | yes | — | `orbiads campaigns add-line-items` |
| `create_open_bidding` | 0 | yes | — | `orbiads line-items create-open-bidding` |
| `create_preferred_deal` | 0 | yes | — | `orbiads line-items create-preferred-deal` |
| `duplicate` | 0 | yes | — | `orbiads line-items duplicate` |
| `pause_batch` | 0 | yes | — | `orbiads line-items pause` |
| `update` | 0 | yes | — | `orbiads line-items update` |
| `update_batch` | 0 | yes | — | MCP-only |
| `update_targeting` | 0 | yes | — | `orbiads line-items update-targeting` |
| `get` | 0 | — | — | `orbiads line-items get` |
| `get_full` | 0 | — | — | MCP-only |
| `list_by_order` | 0 | — | — | `orbiads line-items list-by-order` |
| `list_private_deals` | 0 | — | — | `orbiads line-items private-deals` |
| `verify` | 0 | — | — | `orbiads line-items verify` |

### `orbiads:live_stream` (Epic 98)

_Live stream ad breaks + event/slate management._

- **Mode:** mixed · **Actions:** 13 (9 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 0/13 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create` | 0 | yes | — | MCP-only |
| `create_live_stream_event` | 0 | yes | — | MCP-only |
| `create_live_stream_slate` | 0 | yes | — | MCP-only |
| `delete` | 0 | yes | — | MCP-only |
| `delete_live_stream_event` | 0 | yes | — | MCP-only |
| `delete_live_stream_slate` | 0 | yes | — | MCP-only |
| `patch` | 0 | yes | — | MCP-only |
| `update_live_stream_event` | 0 | yes | — | MCP-only |
| `update_live_stream_slate` | 0 | yes | — | MCP-only |
| `get` | 0 | — | — | MCP-only |
| `list` | 0 | — | — | MCP-only |
| `list_live_stream_events` | 0 | — | — | MCP-only |
| `list_live_stream_slates` | 0 | — | — | MCP-only |

### `orbiads:orders` (Epic 68)

_Parent orders tool for non-lifecycle Order operations._

- **Mode:** mixed · **Actions:** 11 (4 writes, 7 reads)
- **Surfaces:** MCP ✅ · CLI 11/11 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 11 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `approve` | 0 | yes | — | `orbiads orders approve` |
| `archive` | 0 | yes | — | `orbiads orders archive` |
| `create` | 0 | yes | — | `orbiads orders create` |
| `update` | 0 | yes | — | `orbiads orders update` |
| `find_or_create` | 0 | — | — | `orbiads orders create` |
| `get` | 0 | — | — | `orbiads orders get` |
| `list` | 0 | — | — | `orbiads orders list` |
| `list_delivering` | 0 | — | — | `orbiads orders list-delivering` |
| `list_roles` | 0 | — | — | `orbiads roles list` |
| `list_users` | 0 | — | — | `orbiads users list` |
| `verify_setup` | 0 | — | — | `orbiads line-items verify` |
