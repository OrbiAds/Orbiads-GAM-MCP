<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo
  (MCP tool definitions + billing_guard.CREDIT_COSTS + transport routes).
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds MCP Tool Matrix

Single-source-of-truth catalogue of OrbiAds MCP parent tools, with their sub-actions, costs, and write/read classification. Generated from the backend source (no hand-edit).

## Summary

- **36 parent tools** (catalogue refactor cible Epic 68 / 76)
- **241 legacy child wrappers** (soft-deprecated, still routing to parents — see legacy mapping)
- **14 standalone tools** (non-parent / non-deprecated: auth, jobs, etc.)
- **291 tools total** exposed via MCP

## Parent tools — overview

| Parent | Epic | # Actions | Mode | Source |
|---|---|---|---|---|
| `ad_review_center` | — | 3 | 📖 read | `ad_review.py:124` |
| `audiences` | 68.2 | 8 | ✍️ mixed/write | `audiences.py:341` |
| `audit` | 68.5 | 1 | 📖 read | `audit.py:81` |
| `audit_skill` | 65.0a | 8 | 📖 read | `audit_skill.py:267` |
| `billing` | 68.5 | 2 | 📖 read | `billing.py:77` |
| `blueprint` | 78.13 | 20 | ✍️ mixed/write | `blueprint.py:364` |
| `campaign` | 20.1 | 16 | ✍️ mixed/write | `campaign_ops.py:564` |
| `companies` | — | 15 | ✍️ mixed/write | `advertisers.py:303` |
| `creative_assets` | 68.7d | 22 | ✍️ mixed/write | `creatives.py:934` |
| `creative_qa` | 68.6 | 7 | 📖 read | `creative_qa.py:159` |
| `creative_wrapper_skill` | 76.1 | 13 | ✍️ mixed/write | `creative_wrappers.py:341` |
| `creatives` | 68.7d | 30 | ✍️ mixed/write | `creatives.py:898` |
| `dai_skill` | 98 | 14 | ✍️ mixed/write | `dai_skill.py:192` |
| `deals` | 64 | 28 | ✍️ mixed/write | `deals.py:588` |
| `formats` | 78.2 | 9 | ✍️ mixed/write | `formats.py:154` |
| `gam_admin` | 65 | 58 | ✍️ mixed/write | `gam_admin.py:162` |
| `gam_features` | 68.5 | 3 | 📖 read | `gam_features.py:121` |
| `gam_jobs` | 82 | 4 | 📖 read | `jobs_async.py:282` |
| `inventory` | 68.6 | 14 | ✍️ mixed/write | `inventory.py:544` |
| `jobs` | 68.2 | 3 | ✍️ mixed/write | `jobs.py:143` |
| `line_items` | 68 | 18 | ✍️ mixed/write | `line_items.py:360` |
| `live_stream` | 98 | 13 | ✍️ mixed/write | `live_stream.py:95` |
| `mcm` | — | 1 | 📖 read | `mcm.py:42` |
| `network` | 68.5 | 6 | ✍️ mixed/write | `network.py:240` |
| `orders` | 68 | 11 | ✍️ mixed/write | `orders.py:161` |
| `placements` | 68.6 | 6 | ✍️ mixed/write | `placements.py:245` |
| `pql` | 68.2 | 3 | 📖 read | `pql.py:348` |
| `prebid_skill` | 70 | 6 | ✍️ mixed/write | `prebid_skill.py:458` |
| `preview` | 68.2 | 3 | ✍️ mixed/write | `preview.py:665` |
| `products` | 68.8 | 7 | ✍️ mixed/write | `products.py:504` |
| `reporting` | 68.7b | 32 | ✍️ mixed/write | `reporting.py:1518` |
| `settings` | 68.1 | 20 | ✍️ mixed/write | `settings.py:618` |
| `targeting` | 68.6 | 27 | ✍️ mixed/write | `targeting.py:870` |
| `tenant_catalog` | 78.1 | 4 | ✍️ mixed/write | `tenant_catalog.py:134` |
| `video_ops` | 98 | 10 | ✍️ mixed/write | `video_ops.py:141` |
| `yield_skill` | 98 | 5 | ✍️ mixed/write | `yield_skill.py:123` |

## Parent tools — details

### `ad_review_center`

_Ad Review Center - search, allow, or block Ad Exchange creatives._

**Source (private monorepo):** `backend/src/mcp/tools/ad_review.py:124` · **Actions:** 3 · **Mode:** read-only

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `search` | 0 | — | — |
| `allow_batch` | 0 | — | — |
| `block_batch` | 0 | — | — |

### `audiences` — Epic 68.2

_Parent audiences tool for the Epic 68.2 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/audiences.py:341` · **Actions:** 8 · **Mode:** mixed (read + write)

**Legacy wrappers:** 5 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_audience_segments` | 0 | — | — |
| `get_audience_segment` | 0 | — | — |
| `create_audience_segment` | 0.5 | ✅ | ✅ required |
| `update_audience_segment` | 0 | ✅ | — |
| `perform_audience_segment_action` | 0 | ✅ | — |
| `update_segment_memberships` | 0.5 | ✅ | ✅ required |
| `get_segment_population_results` | 0 | — | — |
| `perform_segment_population_action` | 0 | ✅ | — |

### `audit` — Epic 68.5

_Parent audit tool for the Epic 68.5 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/audit.py:81` · **Actions:** 1 · **Mode:** read-only

**Legacy wrappers:** 1 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `query_audit_log` | 0 | — | — |

### `audit_skill` — Epic 65.0a

_OrbiAds audit suite — single entry point for audit sub-actions._

**Source (private monorepo):** `backend/src/mcp/tools/audit_skill.py:267` · **Actions:** 8 · **Mode:** read-only

**Legacy wrappers:** 2 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `hygiene_check` | 0 | — | — |
| `ops_diagnostic` | 0 | — | — |
| `standards_baseline` | 0 | — | — |
| `wrapper_coverage` | 0 | — | — |
| `estimate_cost` | 0 | — | — |
| `export_authoring` | 0 | — | — |
| `export_xlsx` | 0 | — | — |
| `inventory_extended` | 0 | — | — |

### `billing` — Epic 68.5

_Parent billing tool for the Epic 68.5 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/billing.py:77` · **Actions:** 2 · **Mode:** read-only

**Legacy wrappers:** 2 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_credit_balance` | 0 | — | — |
| `list_transactions` | 0 | — | — |

### `blueprint` — Epic 78.13

_Parent blueprint MCP tool — CRUD on tenant inventory blueprint (Story 78.13)._

**Source (private monorepo):** `backend/src/mcp/tools/blueprint.py:364` · **Actions:** 20 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_active_preferences` | 0 | — | — |
| `get_active_blueprint` | 0 | — | — |
| `save_blueprint` | 0.25 | ✅ | ✅ required |
| `save_preferences` | 0.25 | ✅ | ✅ required |
| `add_format` | 0.25 | — | — |
| `remove_format` | 0.25 | ✅ | ✅ required |
| `add_position` | 0.25 | — | — |
| `remove_position` | 0.25 | ✅ | ✅ required |
| `add_key_value` | 0.25 | — | — |
| `remove_key_value` | 0.25 | ✅ | ✅ required |
| `update_brand` | 0.25 | ✅ | ✅ required |
| `update_platforms` | 0.25 | ✅ | ✅ required |
| `list_templates` | 0 | — | — |
| `get_v2` | 0 | — | — |
| `list_drafts` | 0 | — | — |
| `get_diff` | 0 | — | — |
| `list_block_versions` | 0 | — | — |
| `get_block_version` | 0 | — | — |
| `list_packages` | 0 | — | — |
| `get_preview_url` | 0 | — | — |

### `campaign` — Epic 20.1

_Parent campaign tool for deployment, update, rollback, and lifecycle orchestration._

**Source (private monorepo):** `backend/src/mcp/tools/campaign_ops.py:564` · **Actions:** 16 · **Mode:** mixed (read + write)

**Legacy wrappers:** 13 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `read` | 0 | — | — |
| `dry_run` | 0 | — | — |
| `deploy` | 0 | ✅ | — |
| `create_draft` | 0 | ✅ | — |
| `update` | 0 | ✅ | — |
| `ensure_template` | 0 | — | — |
| `create_native_style` | 0.5 | ✅ | ✅ required |
| `create_line_items_batch` | 1 | ✅ | ✅ required |
| `create_licas` | 0 | ✅ | — |
| `create_display` | 0 | ✅ | — |
| `plan_deployment` | 0 | — | — |
| `deploy_media` | 1 | ✅ | ✅ required |
| `rollback` | 0 | ✅ | — |
| `pause` | 0 | ✅ | — |
| `archive` | 0 | ✅ | — |
| `archive_eligible` | 0 | ✅ | — |

### `companies`

_Companies dispatcher — single entry point for advertisers, agencies, contacts, and rich media partners._

**Source (private monorepo):** `backend/src/mcp/tools/advertisers.py:303` · **Actions:** 15 · **Mode:** mixed (read + write)

**Legacy wrappers:** 12 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `advertisers.list` | 0 | — | — |
| `advertisers.get` | 0 | — | — |
| `advertisers.find` | 0 | — | — |
| `advertisers.create` | 0 | ✅ | — |
| `advertisers.update` | 0 | ✅ | — |
| `advertisers.find_or_create` | 0 | — | — |
| `advertisers.archive_advertiser` | 0.5 | ✅ | ✅ required |
| `agencies.list` | 0 | — | — |
| `agencies.create` | 0 | ✅ | — |
| `agencies.update` | 0 | ✅ | — |
| `contacts.list` | 0 | — | — |
| `contacts.create` | 0 | ✅ | — |
| `contacts.update` | 0 | ✅ | — |
| `rich_media.list` | 0 | — | — |
| `rich_media.get` | 0 | — | — |

### `creative_assets` — Epic 68.7d

_Parent creative asset tool for upload/create/compress/transcode actions._

**Source (private monorepo):** `backend/src/mcp/tools/creatives.py:934` · **Actions:** 22 · **Mode:** mixed (read + write)

**Legacy wrappers:** 18 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `bulk_upload` | 0 | — | — |
| `upload_from_url` | 0 | ✅ | — |
| `upload_and_associate` | 0 | ✅ | — |
| `upload_html5_zip` | 0 | ✅ | — |
| `create_image` | 0 | ✅ | — |
| `create_html5` | 0 | ✅ | — |
| `create_html5_from_files` | 0 | ✅ | — |
| `create_video` | 0 | ✅ | — |
| `create_audio` | 0 | ✅ | — |
| `create_hosted_video` | 0 | ✅ | — |
| `create_hosted_audio` | 0 | ✅ | — |
| `create_vast_redirect` | 0 | ✅ | — |
| `create_internal_redirect` | 0 | ✅ | — |
| `create_image_redirect` | 0 | ✅ | — |
| `create_click_tracking` | 0 | ✅ | — |
| `create_custom` | 0 | ✅ | — |
| `create_aspect_ratio_image` | 0 | ✅ | — |
| `create_companion` | 0 | ✅ | — |
| `create_third_party` | 0 | ✅ | — |
| `create_classic_native` | 0 | ✅ | — |
| `compress_image` | 0 | — | — |
| `get_video_transcode_status` | 0 | — | — |

### `creative_qa` — Epic 68.6

_Parent creative QA tool for Story 68.6._

**Source (private monorepo):** `backend/src/mcp/tools/creative_qa.py:159` · **Actions:** 7 · **Mode:** read-only

**Legacy wrappers:** 7 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `scan_creative_compliance` | 0 | — | — |
| `validate_creative_ssl` | 0 | — | — |
| `validate_creative_ssl_batch` | 0 | — | — |
| `audit_creative_tracking` | 0.5 | — | — |
| `audit_order_tracking` | 0.5 | — | — |
| `validate_tag_snippet` | 0 | — | — |
| `pre_archive_check` | 0.5 | — | — |

### `creative_wrapper_skill` — Epic 76.1

_Manage GAM CreativeWrapper entities (AdUnit/Placement level wrapping) through one parent tool._

**Source (private monorepo):** `backend/src/mcp/tools/creative_wrappers.py:341` · **Actions:** 13 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list` | 0 | — | — |
| `get` | 0 | — | — |
| `create` | 0 | ✅ | — |
| `update` | 0 | ✅ | — |
| `activate` | 0 | ✅ | — |
| `deactivate` | 0 | ✅ | — |
| `archive` | 0 | ✅ | — |
| `set_data_declaration` | 0 | ✅ | — |
| `list_rich_media_ads_companies` | 0 | — | — |
| `find_third_party_company` | 0 | — | — |
| `create_preset` | 0 | ✅ | — |
| `list_wrapper_presets` | 0 | — | — |
| `provision` | 0 | — | — |

### `creatives` — Epic 68.7d

_Parent creatives tool for the Epic 68.7d catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/creatives.py:898` · **Actions:** 30 · **Mode:** mixed (read + write)

**Legacy wrappers:** 27 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_creatives_by_advertiser` | 0 | — | — |
| `list_creatives_by_line_item` | 0 | — | — |
| `list_creatives_by_network` | 0 | — | — |
| `get_creative` | 0 | — | — |
| `update_creative` | 0 | ✅ | — |
| `archive_creative` | 0 | ✅ | — |
| `duplicate_creative` | 0.5 | ✅ | ✅ required |
| `get_creative_preview_url` | 0 | — | — |
| `get_native_style_preview_urls` | 0 | — | — |
| `get_campaign_preview_links` | 0 | — | — |
| `get_video_transcode_status` | 0 | — | — |
| `list_native_styles` | 0 | — | — |
| `get_native_style` | 0 | — | — |
| `update_native_style` | 0 | ✅ | — |
| `archive_native_style` | 0 | ✅ | — |
| `duplicate_native_style` | 0.5 | ✅ | ✅ required |
| `ensure_classic_native_template` | 0 | — | — |
| `list_creative_templates` | 0 | — | — |
| `get_creative_template` | 0 | — | — |
| `discover_native_formats` | 0.5 | — | — |
| `associate_creative` | 0 | ✅ | — |
| `bulk_associate_creatives` | 0 | ✅ | — |
| `get_licas_by_line_item` | 0 | — | — |
| `get_licas_batch` | 0 | — | — |
| `deactivate_lica` | 0 | ✅ | — |
| `update_lica` | 0 | ✅ | — |
| `delete_licas` | 0 | ✅ | — |
| `list_creative_sets` | 0 | — | — |
| `create_creative_set` | 0 | ✅ | — |
| `update_creative_set` | 0 | ✅ | — |

### `dai_skill` — Epic 98

_DAI (Dynamic Ad Insertion) and broadcasting operations._

**Source (private monorepo):** `backend/src/mcp/tools/dai_skill.py:192` · **Actions:** 14 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_stream_activity` | 0 | — | — |
| `register_sessions` | 0 | ✅ | — |
| `list_cdn_configurations` | 0 | — | — |
| `create_cdn_configuration` | 0 | ✅ | — |
| `update_cdn_configuration` | 0 | ✅ | — |
| `delete_cdn_configuration` | 0 | ✅ | — |
| `list_dai_auth_keys` | 0 | — | — |
| `create_dai_auth_key` | 0 | ✅ | — |
| `update_dai_auth_key` | 0 | ✅ | — |
| `perform_dai_auth_key_action` | 0 | ✅ | — |
| `list_dai_encoding_profiles` | 0 | — | — |
| `create_dai_encoding_profile` | 0 | ✅ | — |
| `update_dai_encoding_profile` | 0 | ✅ | — |
| `delete_dai_encoding_profile` | 0 | ✅ | — |

### `deals` — Epic 64

_Parent MCP tool for PMP, PG/PD proposal authoring, and ADCP deal flows._

**Source (private monorepo):** `backend/src/mcp/tools/deals.py:588` · **Actions:** 28 · **Mode:** mixed (read + write)

**Legacy wrappers:** 29 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_deals` | 0 | — | — |
| `get_deal` | 0 | — | — |
| `create_deal` | 0 | ✅ | — |
| `update_deal` | 0 | ✅ | — |
| `list_auctions` | 0 | — | — |
| `get_auction` | 0 | — | — |
| `create_auction` | 0 | ✅ | — |
| `update_auction` | 0 | ✅ | — |
| `list_buyers` | 0 | — | — |
| `get_buyer` | 0 | — | — |
| `get_proposal` | 0 | — | — |
| `create_proposal` | 5 | ✅ | ✅ required |
| `update_proposal` | 2 | ✅ | ✅ required |
| `archive_proposal` | 0 | ✅ | — |
| `request_buyer_acceptance` | 0 | ✅ | — |
| `reserve_proposal` | 0 | ✅ | — |
| `edit_proposal_for_negotiation` | 0 | ✅ | — |
| `terminate_proposal_negotiations` | 0 | ✅ | — |
| `get_marketplace_comments` | 0 | — | — |
| `list_proposal_line_items` | 0 | — | — |
| `create_proposal_line_items` | 3 | ✅ | ✅ required |
| `update_proposal_line_items` | 1 | ✅ | ✅ required |
| `archive_proposal_line_items` | 0 | ✅ | — |
| `create_makegoods` | 3 | ✅ | ✅ required |
| `estimate_deal_cost` | 0 | — | — |
| `adcp_validate` | 0 | — | — |
| `adcp_preview` | 0 | — | — |
| `adcp_create` | 0 | — | — |

### `formats` — Epic 78.2

_Parent formats MCP tool — Custom Format Registry avec scope multi-site (Story 78.2)._

**Source (private monorepo):** `backend/src/mcp/tools/formats.py:154` · **Actions:** 9 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_recipes` | 0 | — | — |
| `list_suggested_recipes` | 0 | — | — |
| `accept_suggested_recipe` | 0.25 | ✅ | ✅ required |
| `reject_suggested_recipe` | 0.25 | ✅ | ✅ required |
| `register_recipe` | 0.25 | ✅ | ✅ required |
| `update_recipe` | 0.25 | ✅ | ✅ required |
| `delete_recipe` | 0.25 | ✅ | ✅ required |
| `resolve` | 0 | — | — |
| `detect_conflicts` | 0 | — | — |

### `gam_admin` — Epic 65

_GAM admin orchestration — single entry point for 54 ops over 7 areas._

**Source (private monorepo):** `backend/src/mcp/tools/gam_admin.py:162` · **Actions:** 58 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `teams.list` | 0 | — | — |
| `teams.get` | 0 | — | — |
| `teams.create` | 0 | ✅ | — |
| `teams.batch_create` | 0 | — | — |
| `teams.patch` | 0 | ✅ | — |
| `teams.batch_update` | 0 | — | — |
| `teams.batch_activate` | 0 | — | — |
| `teams.batch_deactivate` | 0 | — | — |
| `sites.list` | 0 | — | — |
| `sites.get` | 0 | — | — |
| `sites.create` | 0 | ✅ | — |
| `sites.batch_create` | 0 | — | — |
| `sites.patch` | 0 | ✅ | — |
| `sites.batch_update` | 0 | — | — |
| `sites.batch_deactivate` | 0 | — | — |
| `sites.batch_submit_for_approval` | 0 | — | — |
| `applications.list` | 0 | — | — |
| `applications.get` | 0 | — | — |
| `applications.create` | 0 | ✅ | — |
| `applications.batch_create` | 0 | — | — |
| `applications.patch` | 0 | ✅ | — |
| `applications.batch_update` | 0 | — | — |
| `applications.batch_archive` | 0 | — | — |
| `applications.batch_unarchive` | 0 | — | — |
| `custom_fields.list` | 0 | — | — |
| `custom_fields.get` | 0 | — | — |
| `custom_fields.create` | 0 | ✅ | — |
| `custom_fields.batch_create` | 0 | — | — |
| `custom_fields.patch` | 0 | ✅ | — |
| `custom_fields.batch_update` | 0 | — | — |
| `custom_fields.batch_activate` | 0 | — | — |
| `custom_fields.batch_deactivate` | 0 | — | — |
| `labels.list` | 0 | — | — |
| `labels.get` | 0 | — | — |
| `labels.create` | 0 | ✅ | — |
| `labels.batch_create` | 0 | — | — |
| `labels.patch` | 0 | ✅ | — |
| `labels.batch_update` | 0 | — | — |
| `labels.batch_activate` | 0 | — | — |
| `labels.batch_deactivate` | 0 | — | — |
| `entity_signals.list` | 0 | — | — |
| `entity_signals.get` | 0 | — | — |
| `entity_signals.create` | 0 | ✅ | — |
| `entity_signals.batch_create` | 0 | — | — |
| `entity_signals.patch` | 0 | ✅ | — |
| `entity_signals.batch_update` | 0 | — | — |
| `users.list` | 0 | — | — |
| `users.get` | 0 | — | — |
| `users.current` | 0 | — | — |
| `users.get_roles` | 0 | — | — |
| `users.create` | 0 | ✅ | — |
| `users.update` | 0 | ✅ | — |
| `users.activate` | 0 | ✅ | — |
| `users.deactivate` | 0 | ✅ | — |
| `user_team_associations.list` | 0 | — | — |
| `user_team_associations.create` | 0 | ✅ | — |
| `user_team_associations.update` | 0 | ✅ | — |
| `user_team_associations.delete` | 0 | ✅ | — |

### `gam_features` — Epic 68.5

_Parent gam_features tool for the Epic 68.5 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/gam_features.py:121` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_gam_features` | 0 | — | — |
| `probe_gam_features` | 0.5 | — | — |
| `refresh_gam_features` | 0 | — | — |

### `gam_jobs` — Epic 82

_Async job dispatcher (parent>child pattern, Epic 82)._

**Source (private monorepo):** `backend/src/mcp/tools/jobs_async.py:282` · **Actions:** 4 · **Mode:** read-only

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `image-optimize` | 0 | — | — |
| `blueprint-generate` | 0 | — | — |
| `audit-export` | 0 | — | — |
| `poll` | 0 | — | — |

### `inventory` — Epic 68.6

_Parent inventory tool for Story 68.6._

**Source (private monorepo):** `backend/src/mcp/tools/inventory.py:544` · **Actions:** 14 · **Mode:** mixed (read + write)

**Legacy wrappers:** 10 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_ad_unit_tree` | 0 | — | — |
| `audit_inventory` | 0 | — | — |
| `create_ad_units_batch` | 0.5 | ✅ | ✅ required |
| `generate_ads_json` | 0 | — | — |
| `generate_inventory_blueprint` | 0 | — | — |
| `push_inventory_blueprint` | 0.5 | ✅ | ✅ required |
| `get_ad_units_by_ids` | 0 | — | — |
| `find_inactive_ad_units` | 0.25 | — | — |
| `archive_inactive_ad_units` | 0 | ✅ | — |
| `list_ad_unit_sizes` | 0 | — | — |
| `blueprint_starter` | 0 | — | — |
| `get_catalog` | 0 | — | — |
| `list_line_item_templates` | 0 | — | — |
| `list_suggested_ad_units` | 0 | — | — |

### `jobs` — Epic 68.2

_Parent jobs tool for the Epic 68.2 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/jobs.py:143` · **Actions:** 3 · **Mode:** mixed (read + write)

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_job` | 0 | — | — |
| `list_jobs` | 0 | — | — |
| `duplicate_job` | 0 | ✅ | — |

### `line_items` — Epic 68

_Parent line_items tool for non-lifecycle Line Item operations._

**Source (private monorepo):** `backend/src/mcp/tools/line_items.py:360` · **Actions:** 18 · **Mode:** mixed (read + write)

**Legacy wrappers:** 16 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get` | 0 | — | — |
| `get_full` | 0 | — | — |
| `list_by_order` | 0 | — | — |
| `update` | 0 | ✅ | — |
| `update_batch` | 0 | ✅ | — |
| `update_targeting` | 0 | ✅ | — |
| `duplicate` | 0 | ✅ | — |
| `verify` | 0 | — | — |
| `approve` | 0 | ✅ | — |
| `archive` | 0 | ✅ | — |
| `create_batch` | 0 | ✅ | — |
| `activate_batch` | 0 | ✅ | — |
| `pause_batch` | 0 | ✅ | — |
| `create` | 0 | ✅ | — |
| `create_adexchange` | 0 | ✅ | — |
| `create_open_bidding` | 0 | ✅ | — |
| `create_preferred_deal` | 0 | ✅ | — |
| `list_private_deals` | 0 | — | — |

### `live_stream` — Epic 98

_Live stream ad breaks + event/slate management._

**Source (private monorepo):** `backend/src/mcp/tools/live_stream.py:95` · **Actions:** 13 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list` | 0 | — | — |
| `get` | 0 | — | — |
| `create` | 0 | ✅ | — |
| `patch` | 0 | ✅ | — |
| `delete` | 0 | ✅ | — |
| `list_live_stream_events` | 0 | — | — |
| `create_live_stream_event` | 0 | ✅ | — |
| `update_live_stream_event` | 0 | ✅ | — |
| `delete_live_stream_event` | 0 | ✅ | — |
| `list_live_stream_slates` | 0 | — | — |
| `create_live_stream_slate` | 0 | ✅ | — |
| `update_live_stream_slate` | 0 | ✅ | — |
| `delete_live_stream_slate` | 0 | ✅ | — |

### `mcm`

_MCM read-only operations._

**Source (private monorepo):** `backend/src/mcp/tools/mcm.py:42` · **Actions:** 1 · **Mode:** read-only

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `earnings_fetch` | 0 | — | — |

### `network` — Epic 68.5

_Parent network tool for the Epic 68.5 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/network.py:240` · **Actions:** 6 · **Mode:** mixed (read + write)

**Legacy wrappers:** 4 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_network_info` | 0 | — | — |
| `switch_network` | 0 | ✅ | — |
| `list_accessible_networks` | 0 | — | — |
| `update_network` | 0 | ✅ | — |
| `get_preview_url_library` | 0 | — | — |
| `set_preview_url_library` | 0 | ✅ | — |

### `orders` — Epic 68

_Parent orders tool for non-lifecycle Order operations._

**Source (private monorepo):** `backend/src/mcp/tools/orders.py:161` · **Actions:** 11 · **Mode:** mixed (read + write)

**Legacy wrappers:** 11 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_delivering` | 0 | — | — |
| `get` | 0 | — | — |
| `list` | 0 | — | — |
| `create` | 0 | ✅ | — |
| `archive` | 0 | ✅ | — |
| `approve` | 0 | ✅ | — |
| `verify_setup` | 0 | — | — |
| `update` | 0 | ✅ | — |
| `find_or_create` | 0 | — | — |
| `list_users` | 0 | — | — |
| `list_roles` | 0 | — | — |

### `placements` — Epic 68.6

_Parent placements tool for Story 68.6._

**Source (private monorepo):** `backend/src/mcp/tools/placements.py:245` · **Actions:** 6 · **Mode:** mixed (read + write)

**Legacy wrappers:** 4 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_placements` | 0 | — | — |
| `create_placement` | 0.5 | ✅ | ✅ required |
| `update_placement` | 0 | ✅ | — |
| `activate_placement` | 0 | ✅ | — |
| `deactivate_placement` | 0 | ✅ | — |
| `archive_placement` | 0 | ✅ | — |

### `pql` — Epic 68.2

_Parent pql tool for the Epic 68.2 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/pql.py:348` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 1 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `run_query` | 0 | — | — |
| `validate_query` | 0 | — | — |
| `list_tables` | 0 | — | — |

### `prebid_skill` — Epic 70

_Dispatch Prebid.js / Header Bidding sub-actions through one MCP tool._

**Source (private monorepo):** `backend/src/mcp/tools/prebid_skill.py:458` · **Actions:** 6 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `generate_line_items` | 0 | — | — |
| `generate_targeting_keys` | 0 | — | — |
| `update_line_items` | 0 | ✅ | — |
| `inspect_existing_setup` | 0 | — | — |
| `preview_batch` | 0 | — | — |
| `cleanup` | 0 | — | — |

### `preview` — Epic 68.2

_Parent preview tool for the Epic 68.2 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/preview.py:665` · **Actions:** 3 · **Mode:** mixed (read + write)

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `get_preview_urls` | 0.25 | ✅ | ✅ required |
| `get_campaign_preview_urls` | 0.25 | ✅ | ✅ required |
| `check_creative_coverage` | 0 | — | — |

### `products` — Epic 68.8

_Parent products tool for the Epic 68.8 catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/products.py:504` · **Actions:** 7 · **Mode:** mixed (read + write)

**Legacy wrappers:** 9 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `create` | 0 | ✅ | — |
| `list` | 0 | — | — |
| `get` | 0 | — | — |
| `update` | 0 | ✅ | — |
| `archive` | 0 | ✅ | — |
| `get_adcp` | 0 | — | — |
| `pricing_suggestion` | 0 | — | — |

### `reporting` — Epic 68.7b

_Parent reporting tool for the Epic 68.7b catalogue refactor batch._

**Source (private monorepo):** `backend/src/mcp/tools/reporting.py:1518` · **Actions:** 32 · **Mode:** mixed (read + write)

**Legacy wrappers:** 31 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `check_delivery_status` | 0 | — | — |
| `fetch_delivery_report` | 0 | — | — |
| `run_custom_report` | 0.5 | — | — |
| `fetch_inventory_report` | 0.5 | — | — |
| `get_report_result` | 0 | — | — |
| `export_report_csv` | 0.5 | — | — |
| `get_report_download_link` | 0 | — | — |
| `get_report_dimensions` | 0 | — | — |
| `get_report_metrics` | 0 | — | — |
| `get_report_date_ranges` | 0 | — | — |
| `get_standalone_forecast` | 0 | — | — |
| `get_delivery_forecast_by_line_item` | 0 | — | — |
| `get_prospective_delivery_forecast` | 0 | — | — |
| `get_traffic_data` | 0 | — | — |
| `list_report_templates` | 0 | — | — |
| `save_report_template` | 0 | ✅ | — |
| `delete_report_template` | 0 | ✅ | — |
| `duplicate_report_template` | 0 | ✅ | — |
| `update_report_template` | 0 | ✅ | — |
| `run_report_from_template` | 0.5 | — | — |
| `list_gam_reports` | 0 | — | — |
| `get_gam_report` | 0 | — | — |
| `create_gam_report` | 0 | ✅ | — |
| `update_gam_report` | 0 | ✅ | — |
| `delete_gam_report` | 0 | ✅ | — |
| `run_gam_report` | 0 | — | — |
| `run_ga_report` | 0.5 | — | — |
| `get_ga_dimensions` | 0 | — | — |
| `get_ga_metrics` | 0 | — | — |
| `check_underdelivery_alerts` | 0.25 | — | — |
| `check_budget_alerts` | 0.25 | — | — |
| `generate_billing_report` | 0.5 | — | — |

### `settings` — Epic 68.1

_Parent settings tool for the Epic 68.1 catalogue refactor POC._

**Source (private monorepo):** `backend/src/mcp/tools/settings.py:618` · **Actions:** 20 · **Mode:** mixed (read + write)

**Legacy wrappers:** 9 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_presets` | 0 | — | — |
| `create_preset` | 0 | ✅ | — |
| `update_preset` | 0 | ✅ | — |
| `delete_preset` | 0 | ✅ | — |
| `list_preset_suggestions` | 0 | — | — |
| `accept_preset_suggestion` | 0 | ✅ | — |
| `dismiss_preset_suggestion` | 0 | — | — |
| `recompute_preset_suggestions` | 0 | — | — |
| `get_tenant_settings` | 0 | — | — |
| `update_tenant_settings` | 0 | ✅ | — |
| `get_naming_conventions` | 0 | — | — |
| `update_naming_conventions` | 0 | ✅ | — |
| `get_delivery_defaults` | 0 | — | — |
| `update_delivery_defaults` | 0 | ✅ | — |
| `get_multilang_matrix` | 0 | — | — |
| `get_global_multilang_matrix` | 0 | — | — |
| `save_global_multilang_matrix` | 0 | ✅ | — |
| `apply_multilang_to_networks` | 0 | — | — |
| `resolve_multilang_matrix` | 0 | — | — |
| `list_preview_matrices` | 0 | — | — |

### `targeting` — Epic 68.6

_Parent targeting tool for Story 68.6._

**Source (private monorepo):** `backend/src/mcp/tools/targeting.py:870` · **Actions:** 27 · **Mode:** mixed (read + write)

**Legacy wrappers:** 21 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_ad_units` | 0 | — | — |
| `validate_fluid` | 0 | — | — |
| `list_custom_targeting_keys` | 0 | — | — |
| `get_inventory_forecast` | 0 | — | — |
| `create_custom_targeting_key` | 0.5 | ✅ | ✅ required |
| `create_custom_targeting_values` | 0.5 | ✅ | ✅ required |
| `update_custom_targeting_key` | 0 | ✅ | — |
| `delete_custom_targeting_key` | 0 | ✅ | — |
| `update_custom_targeting_value` | 0 | ✅ | — |
| `perform_custom_targeting_value_action` | 0 | ✅ | — |
| `search_ad_units` | 0 | — | — |
| `update_ad_unit` | 0 | ✅ | — |
| `activate_ad_unit` | 0 | ✅ | — |
| `deactivate_ad_unit` | 0 | ✅ | — |
| `archive_ad_unit` | 0 | ✅ | — |
| `get_custom_targeting_values` | 0 | — | — |
| `search_custom_targeting` | 0 | — | — |
| `get_available_countries` | 0 | — | — |
| `get_available_languages` | 0 | — | — |
| `get_device_categories` | 0 | — | — |
| `get_browsers` | 0 | — | — |
| `get_operating_systems` | 0 | — | — |
| `get_content_labels` | 0 | — | — |
| `list_targeting_presets` | 0 | — | — |
| `create_targeting_preset` | 0.5 | ✅ | ✅ required |
| `update_targeting_preset` | 0 | ✅ | — |
| `delete_targeting_preset` | 0 | ✅ | — |

### `tenant_catalog` — Epic 78.1

_Parent tenant_catalog MCP tool — scan + read tenant inventory catalog (Story 78.1)._

**Source (private monorepo):** `backend/src/mcp/tools/tenant_catalog.py:134` · **Actions:** 4 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `scan_network` | 1 | ✅ | ✅ required |
| `get_scan_status` | 0 | — | — |
| `get_active_catalog` | 0 | — | — |
| `refresh` | 1 | ✅ | ✅ required |

### `video_ops` — Epic 98

_Video monetization: ad rule management, content metadata, and content bundle operations._

**Source (private monorepo):** `backend/src/mcp/tools/video_ops.py:141` · **Actions:** 10 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_ad_rules` | 0 | — | — |
| `create_ad_rule` | 0 | ✅ | — |
| `update_ad_rule` | 0 | ✅ | — |
| `delete_ad_rule` | 0 | ✅ | — |
| `list_content` | 0 | — | — |
| `list_content_bundles` | 0 | — | — |
| `create_content_bundle` | 0 | ✅ | — |
| `update_content_bundle` | 0 | ✅ | — |
| `activate_content_bundle` | 0 | ✅ | — |
| `deactivate_content_bundle` | 0 | ✅ | — |

### `yield_skill` — Epic 98

_Yield optimization group management and forecast governance._

**Source (private monorepo):** `backend/src/mcp/tools/yield_skill.py:123` · **Actions:** 5 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Write? | Confirmation token? |
|---|---|---|---|
| `list_yield_groups` | 0 | — | — |
| `create_yield_group` | 0 | ✅ | — |
| `update_yield_group` | 0 | ✅ | — |
| `list_forecast_adjustments` | 0 | — | — |
| `list_forecast_segments` | 0 | — | — |

## Standalone tools

Tools that are neither parents nor deprecated wrappers (auth flow, async jobs, internal helpers).

| Tool | Module | Cost | Write? |
|---|---|---|---|
| `check_credentials` | `auth.py:549` | 0 | — |
| `disconnect_gam` | `auth.py:609` | 0 | ✅ |
| `gam_audit` | `gam_audit.py:121` | 0 | — |
| `get_my_tenant_id` | `auth.py:166` | 0 | — |
| `get_premium_rate` | `pricing.py:53` | 0 | — |
| `initiate_gam_auth` | `auth.py:265` | 0 | ✅ |
| `line_item_lifecycle` | `line_items.py:1088` | 0 | ✅ |
| `list_premium_rates` | `pricing.py:39` | 0 | — |
| `list_rate_cards` | `pricing.py:25` | 0 | — |
| `order_lifecycle` | `orders.py:713` | 0 | ✅ |
| `poll_auth_status` | `auth.py:349` | 0 | — |
| `reporting_skill` | `reporting.py:1949` | 0 | — |
| `select_gam_network` | `auth.py:475` | 0 | ✅ |
| `server_info` | `server_info.py:16` | 0 | — |

## See also

- [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md) — the 241 legacy wrappers and their parent dispatch targets
- [`cli/parity-matrix.json`](../../cli/parity-matrix.json) — CLI command coverage per MCP tool
- [`.claude-plugin/plugin.json`](../../.claude-plugin/plugin.json) — Claude Code plugin manifest
