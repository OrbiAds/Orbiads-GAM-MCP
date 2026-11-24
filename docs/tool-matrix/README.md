<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo
  (MCP tool definitions + billing_guard.CREDIT_COSTS + transport routes).
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds MCP Tool Matrix

Single-source-of-truth catalogue of OrbiAds MCP parent tools, with their sub-actions, costs, and per-action access classification (`read` / `write` / `destructive`). Generated from the backend source (no hand-edit).

> MCP annotations (`readOnlyHint`, `destructiveHint`) are per **tool**, so a parent mixing reads and writes cannot carry a precise hint: the per-action **Access** column below is the authoritative classification. `readOnlyHint=true` is set only on tools whose actions are all `read`; `destructiveHint=true` on tools holding at least one `destructive` action.

## Summary

- **36 parent tools** (catalogue refactor cible Epic 68 / 76)
- **14 standalone tools** (non-parent / non-deprecated: auth, jobs, etc.)
- **50 tools total** exposed via MCP (36 parents + 14 standalone), covering **511 GAM operations**
- _241 legacy child wrappers_ remain as **soft-deprecated** aliases (scheduled for sunset, Epic 68.4) — hidden at runtime, not counted in the totals above; see legacy mapping

## Parent tools — overview

| Parent | Epic | # Actions | Mode | read / write / destructive | Source |
|---|---|---|---|---|---|
| `ad_review_center` | — | 3 | ✍️ mixed/write | 1 / 2 / 0 | `ad_review.py:124` |
| `audiences` | 68.2 | 8 | ✍️ mixed/write | 3 / 5 / 0 | `audiences.py:342` |
| `audit` | 117 | 3 | 📖 read | 3 / 0 / 0 | `audit.py:141` |
| `audit_skill` | 65.0a | 8 | 📖 read | 8 / 0 / 0 | `audit_skill.py:269` |
| `billing` | 68.5 | 2 | 📖 read | 2 / 0 / 0 | `billing.py:77` |
| `blueprint` | 78.13 | 20 | ✍️ mixed/write | 10 / 10 / 0 | `blueprint.py:387` |
| `campaign` | 110.1 | 16 | ✍️ mixed/write | 3 / 10 / 3 | `campaign_ops.py:694` |
| `companies` | 118 | 23 | ✍️ mixed/write | 13 / 9 / 1 | `advertisers.py:724` |
| `creative_assets` | 68.7d | 22 | ✍️ mixed/write | 1 / 21 / 0 | `creatives.py:1247` |
| `creative_qa` | 68.6 | 7 | 📖 read | 7 / 0 / 0 | `creative_qa.py:213` |
| `creative_wrapper_skill` | 76.1 | 13 | ✍️ mixed/write | 5 / 7 / 1 | `creative_wrappers.py:346` |
| `creatives` | 68.7d | 34 | ✍️ mixed/write | 19 / 11 / 4 | `creatives.py:1213` |
| `dai_skill` | 98 | 14 | ✍️ mixed/write | 4 / 8 / 2 | `dai_skill.py:190` |
| `deals` | 64 | 41 | ✍️ mixed/write | 14 / 23 / 4 | `deals.py:1202` |
| `formats` | 78.2 | 9 | ✍️ mixed/write | 4 / 4 / 1 | `formats.py:150` |
| `gam_admin` | 65 | 61 | ✍️ mixed/write | 18 / 41 / 2 | `gam_admin.py:188` |
| `gam_features` | 68.5 | 3 | 📖 read | 3 / 0 / 0 | `gam_features.py:121` |
| `gam_jobs` | 82 | 4 | ✍️ mixed/write | 2 / 2 / 0 | `jobs_async.py:268` |
| `inventory` | 68.6 | 15 | ✍️ mixed/write | 11 / 3 / 1 | `inventory.py:713` |
| `jobs` | 68.2 | 3 | ✍️ mixed/write | 2 / 1 / 0 | `jobs.py:151` |
| `line_items` | 68 | 19 | ✍️ mixed/write | 6 / 12 / 1 | `line_items.py:419` |
| `live_stream` | 98 | 13 | ✍️ mixed/write | 4 / 6 / 3 | `live_stream.py:98` |
| `mcm` | 88.1 | 8 | ✍️ mixed/write | 3 / 4 / 1 | `mcm.py:306` |
| `network` | 68.5 | 6 | ✍️ mixed/write | 3 / 3 / 0 | `network.py:268` |
| `orders` | 68 | 11 | ✍️ mixed/write | 6 / 4 / 1 | `orders.py:231` |
| `placements` | 68.6 | 6 | ✍️ mixed/write | 1 / 4 / 1 | `placements.py:276` |
| `pql` | 68.2 | 3 | 📖 read | 3 / 0 / 0 | `pql.py:369` |
| `prebid_skill` | 70 | 6 | ✍️ mixed/write | 2 / 3 / 1 | `prebid_skill.py:449` |
| `preview` | 68.2 | 3 | 📖 read | 3 / 0 / 0 | `preview.py:754` |
| `products` | 68.8 | 7 | ✍️ mixed/write | 4 / 2 / 1 | `products.py:535` |
| `reporting` | 68.7b | 33 | ✍️ mixed/write | 26 / 5 / 2 | `reporting.py:2802` |
| `settings` | 68.1 | 26 | ✍️ mixed/write | 11 / 14 / 1 | `settings.py:668` |
| `targeting` | 68.6 | 28 | ✍️ mixed/write | 14 / 11 / 3 | `targeting.py:937` |
| `tenant_catalog` | 78.1 | 4 | ✍️ mixed/write | 2 / 2 / 0 | `tenant_catalog.py:131` |
| `video_ops` | 98 | 10 | ✍️ mixed/write | 3 / 6 / 1 | `video_ops.py:145` |
| `yield_skill` | 98 | 5 | ✍️ mixed/write | 3 / 2 / 0 | `yield_skill.py:119` |

## Parent tools — details

### `ad_review_center`

_Ad Review Center - search, allow, or block Ad Exchange creatives._

**Server-side implementation:** `ad_review.py` · **Actions:** 3 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `search` | 0 | 📖 read | — |
| `allow_batch` | 0.5 | ✍️ write | ✅ required |
| `block_batch` | 0.5 | ✍️ write | ✅ required |

### `audiences` — Epic 68.2

_Parent audiences tool for the Epic 68.2 catalogue refactor batch._

**Server-side implementation:** `audiences.py` · **Actions:** 8 · **Mode:** mixed (read + write)

**Legacy wrappers:** 5 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_audience_segments` | 0 | 📖 read | — |
| `get_audience_segment` | 0 | 📖 read | — |
| `create_audience_segment` | 0.5 | ✍️ write | ✅ required |
| `update_audience_segment` | 0 | ✍️ write | — |
| `perform_audience_segment_action` | 0 | ✍️ write | — |
| `update_segment_memberships` | 0.5 | ✍️ write | ✅ required |
| `get_segment_population_results` | 0 | 📖 read | — |
| `perform_segment_population_action` | 0 | ✍️ write | — |

### `audit` — Epic 117

_Parent audit tool: OrbiAds audit journal + GAM change history (read-only)._

**Server-side implementation:** `audit.py` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 1 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `query_audit_log` | 0 | 📖 read | — |
| `list_change_events` | 0 | 📖 read | — |
| `get_change_event` | 0 | 📖 read | — |

### `audit_skill` — Epic 65.0a

_OrbiAds audit suite — single entry point for audit sub-actions._

**Server-side implementation:** `audit_skill.py` · **Actions:** 8 · **Mode:** read-only

**Legacy wrappers:** 2 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `hygiene_check` | 0.5 | 📖 read | — |
| `ops_diagnostic` | 1 | 📖 read | — |
| `standards_baseline` | 0 | 📖 read | — |
| `wrapper_coverage` | 1 | 📖 read | — |
| `estimate_cost` | 0 | 📖 read | — |
| `export_authoring` | 0 | 📖 read | — |
| `export_xlsx` | 0 | 📖 read | — |
| `inventory_extended` | 2 | 📖 read | — |

### `billing` — Epic 68.5

_Parent billing tool for the Epic 68.5 catalogue refactor batch._

**Server-side implementation:** `billing.py` · **Actions:** 2 · **Mode:** read-only

**Legacy wrappers:** 2 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_credit_balance` | 0 | 📖 read | — |
| `list_transactions` | 0 | 📖 read | — |

### `blueprint` — Epic 78.13

_Parent blueprint MCP tool — CRUD on tenant inventory blueprint (Story 78.13)._

**Server-side implementation:** `blueprint.py` · **Actions:** 20 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_active_preferences` | 0 | 📖 read | — |
| `get_active_blueprint` | 0 | 📖 read | — |
| `save_blueprint` | 0.25 | ✍️ write | ✅ required |
| `save_preferences` | 0.25 | ✍️ write | ✅ required |
| `add_format` | 0.25 | ✍️ write | ✅ required |
| `remove_format` | 0.25 | ✍️ write | ✅ required |
| `add_position` | 0.25 | ✍️ write | ✅ required |
| `remove_position` | 0.25 | ✍️ write | ✅ required |
| `add_key_value` | 0.25 | ✍️ write | ✅ required |
| `remove_key_value` | 0.25 | ✍️ write | ✅ required |
| `update_brand` | 0.25 | ✍️ write | ✅ required |
| `update_platforms` | 0.25 | ✍️ write | ✅ required |
| `list_templates` | 0 | 📖 read | — |
| `get_v2` | 0 | 📖 read | — |
| `list_drafts` | 0 | 📖 read | — |
| `get_diff` | 0 | 📖 read | — |
| `list_block_versions` | 0 | 📖 read | — |
| `get_block_version` | 0 | 📖 read | — |
| `list_packages` | 0 | 📖 read | — |
| `get_preview_url` | 0 | 📖 read | — |

### `campaign` — Epic 110.1

_Parent campaign tool for deployment, update, rollback, and lifecycle orchestration._

**Server-side implementation:** `campaign_ops.py` · **Actions:** 16 · **Mode:** mixed (read + write)

**Legacy wrappers:** 13 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `read` | 0 | 📖 read | — |
| `dry_run` | 0 | 📖 read | — |
| `deploy` | 0 | ✍️ write | — |
| `create_draft` | 0 | ✍️ write | — |
| `update` | 0 | ✍️ write | — |
| `ensure_template` | 0 | ✍️ write | — |
| `create_native_style` | 0.5 | ✍️ write | ✅ required |
| `create_line_items_batch` | 1 | ✍️ write | ✅ required |
| `create_licas` | 0 | ✍️ write | — |
| `create_display` | 0 | ✍️ write | — |
| `plan_deployment` | 0 | 📖 read | — |
| `deploy_media` | 1 | ✍️ write | ✅ required |
| `rollback` | 0 | ⚠️ destructive | — |
| `pause` | 0 | ✍️ write | — |
| `archive` | 0 | ⚠️ destructive | — |
| `archive_eligible` | 0 | ⚠️ destructive | — |

### `companies` — Epic 118

_Companies dispatcher — single entry point for advertisers, agencies, contacts, and rich media partners._

**Server-side implementation:** `advertisers.py` · **Actions:** 23 · **Mode:** mixed (read + write)

**Legacy wrappers:** 12 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `advertisers.list` | 0 | 📖 read | — |
| `advertisers.get` | 0 | 📖 read | — |
| `advertisers.find` | 0 | 📖 read | — |
| `advertisers.create` | 0 | ✍️ write | — |
| `advertisers.update` | 0 | ✍️ write | — |
| `advertisers.find_or_create` | 0 | ✍️ write | — |
| `advertisers.archive_advertiser` | 0.5 | ⚠️ destructive | ✅ required |
| `agencies.list` | 0 | 📖 read | — |
| `agencies.create` | 0 | ✍️ write | — |
| `agencies.update` | 0 | ✍️ write | — |
| `contacts.list` | 0 | 📖 read | — |
| `contacts.create` | 0 | ✍️ write | — |
| `contacts.update` | 0 | ✍️ write | — |
| `rich_media.list` | 0 | 📖 read | — |
| `rich_media.get` | 0 | 📖 read | — |
| `third_party.list` | 0 | 📖 read | — |
| `third_party.get` | 0 | 📖 read | — |
| `all.list` | 0 | 📖 read | — |
| `all.get` | 0 | 📖 read | — |
| `all.create` | 0.5 | ✍️ write | ✅ required |
| `partners.list` | 0 | 📖 read | — |
| `partners.get` | 0 | 📖 read | — |
| `partners.update` | 0 | ✍️ write | — |

### `creative_assets` — Epic 68.7d

_Parent creative asset tool for upload/create/compress/transcode actions._

**Server-side implementation:** `creatives.py` · **Actions:** 22 · **Mode:** mixed (read + write)

**Legacy wrappers:** 18 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `bulk_upload` | 0 | ✍️ write | — |
| `upload_from_url` | 0 | ✍️ write | — |
| `upload_and_associate` | 0 | ✍️ write | — |
| `upload_html5_zip` | 0 | ✍️ write | — |
| `create_image` | 0 | ✍️ write | — |
| `create_html5` | 0 | ✍️ write | — |
| `create_html5_from_files` | 0 | ✍️ write | — |
| `create_video` | 0 | ✍️ write | — |
| `create_audio` | 0 | ✍️ write | — |
| `create_hosted_video` | 0 | ✍️ write | — |
| `create_hosted_audio` | 0 | ✍️ write | — |
| `create_vast_redirect` | 0 | ✍️ write | — |
| `create_internal_redirect` | 0 | ✍️ write | — |
| `create_image_redirect` | 0 | ✍️ write | — |
| `create_click_tracking` | 0 | ✍️ write | — |
| `create_custom` | 0 | ✍️ write | — |
| `create_aspect_ratio_image` | 0 | ✍️ write | — |
| `create_companion` | 0 | ✍️ write | — |
| `create_third_party` | 0 | ✍️ write | — |
| `create_classic_native` | 0 | ✍️ write | — |
| `compress_image` | 0 | ✍️ write | — |
| `get_video_transcode_status` | 0 | 📖 read | — |

### `creative_qa` — Epic 68.6

_Parent creative QA tool for Story 68.6._

**Server-side implementation:** `creative_qa.py` · **Actions:** 7 · **Mode:** read-only

**Legacy wrappers:** 7 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `scan_creative_compliance` | 0 | 📖 read | — |
| `validate_creative_ssl` | 0 | 📖 read | — |
| `validate_creative_ssl_batch` | 0 | 📖 read | — |
| `audit_creative_tracking` | 0.5 | 📖 read | — |
| `audit_order_tracking` | 0.5 | 📖 read | — |
| `validate_tag_snippet` | 0 | 📖 read | — |
| `pre_archive_check` | 0.5 | 📖 read | — |

### `creative_wrapper_skill` — Epic 76.1

_Manage GAM CreativeWrapper entities (AdUnit/Placement level wrapping) through one parent tool._

**Server-side implementation:** `creative_wrappers.py` · **Actions:** 13 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list` | 0 | 📖 read | — |
| `get` | 0 | 📖 read | — |
| `create` | 0.5 | ✍️ write | ✅ required |
| `update` | 0.5 | ✍️ write | ✅ required |
| `activate` | 0.25 | ✍️ write | ✅ required |
| `deactivate` | 0.25 | ✍️ write | ✅ required |
| `archive` | 0 | ⚠️ destructive | — |
| `set_data_declaration` | 0.5 | ✍️ write | ✅ required |
| `list_rich_media_ads_companies` | 0 | 📖 read | — |
| `find_third_party_company` | 0 | 📖 read | — |
| `create_preset` | 0.5 | ✍️ write | ✅ required |
| `list_wrapper_presets` | 0 | 📖 read | — |
| `provision` | 2 | ✍️ write | ✅ required |

### `creatives` — Epic 68.7d

_Parent creatives tool for the Epic 68.7d catalogue refactor batch._

**Server-side implementation:** `creatives.py` · **Actions:** 34 · **Mode:** mixed (read + write)

**Legacy wrappers:** 27 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_creatives_by_advertiser` | 0 | 📖 read | — |
| `list_creatives_by_line_item` | 0 | 📖 read | — |
| `list_creatives_by_network` | 0 | 📖 read | — |
| `list_creatives` | 0 | 📖 read | — |
| `get_creative` | 0 | 📖 read | — |
| `update_creative` | 0 | ✍️ write | — |
| `archive_creative` | 0 | ⚠️ destructive | — |
| `duplicate_creative` | 0.5 | ✍️ write | ✅ required |
| `get_creative_preview_url` | 0 | 📖 read | — |
| `get_native_style_preview_urls` | 0 | 📖 read | — |
| `get_campaign_preview_links` | 0 | 📖 read | — |
| `get_video_transcode_status` | 0 | 📖 read | — |
| `list_native_styles` | 0 | 📖 read | — |
| `get_native_style` | 0 | 📖 read | — |
| `update_native_style` | 0 | ✍️ write | — |
| `archive_native_style` | 0 | ⚠️ destructive | — |
| `duplicate_native_style` | 0.5 | ✍️ write | ✅ required |
| `ensure_classic_native_template` | 0 | ✍️ write | — |
| `list_creative_templates` | 0 | 📖 read | — |
| `get_creative_template` | 0 | 📖 read | — |
| `discover_native_formats` | 0.5 | 📖 read | — |
| `associate_creative` | 0 | ✍️ write | — |
| `bulk_associate_creatives` | 0 | ✍️ write | — |
| `get_licas_by_line_item` | 0 | 📖 read | — |
| `get_licas_by_creative` | 0 | 📖 read | — |
| `list_licas` | 0 | 📖 read | — |
| `get_licas_batch` | 0 | 📖 read | — |
| `deactivate_lica` | 0 | ✍️ write | — |
| `update_lica` | 0 | ✍️ write | — |
| `delete_licas` | 0 | ⚠️ destructive | — |
| `delete_lica_permanently` | 0 | ⚠️ destructive | — |
| `list_creative_sets` | 0 | 📖 read | — |
| `create_creative_set` | 0.5 | ✍️ write | ✅ required |
| `update_creative_set` | 0 | ✍️ write | — |

### `dai_skill` — Epic 98

_DAI (Dynamic Ad Insertion) and broadcasting operations._

**Server-side implementation:** `dai_skill.py` · **Actions:** 14 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_stream_activity` | 0 | 📖 read | — |
| `register_sessions` | 0 | ✍️ write | — |
| `list_cdn_configurations` | 0 | 📖 read | — |
| `create_cdn_configuration` | 0.5 | ✍️ write | ✅ required |
| `update_cdn_configuration` | 0.5 | ✍️ write | ✅ required |
| `delete_cdn_configuration` | 0.5 | ⚠️ destructive | ✅ required |
| `list_dai_auth_keys` | 0 | 📖 read | — |
| `create_dai_auth_key` | 0.5 | ✍️ write | ✅ required |
| `update_dai_auth_key` | 0.5 | ✍️ write | ✅ required |
| `perform_dai_auth_key_action` | 0.5 | ✍️ write | ✅ required |
| `list_dai_encoding_profiles` | 0 | 📖 read | — |
| `create_dai_encoding_profile` | 0.5 | ✍️ write | ✅ required |
| `update_dai_encoding_profile` | 0.5 | ✍️ write | ✅ required |
| `delete_dai_encoding_profile` | 0.5 | ⚠️ destructive | ✅ required |

### `deals` — Epic 64

_Parent MCP tool for PMP, PG/PD proposal authoring, and ADCP deal flows._

**Server-side implementation:** `deals.py` · **Actions:** 41 · **Mode:** mixed (read + write)

**Legacy wrappers:** 29 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_deals` | 0 | 📖 read | — |
| `get_deal` | 0 | 📖 read | — |
| `create_deal` | 0 | ✍️ write | — |
| `update_deal` | 0 | ✍️ write | — |
| `list_auctions` | 0 | 📖 read | — |
| `get_auction` | 0 | 📖 read | — |
| `create_auction` | 0 | ✍️ write | — |
| `update_auction` | 0 | ✍️ write | — |
| `list_buyers` | 0 | 📖 read | — |
| `get_buyer` | 0 | 📖 read | — |
| `get_proposal` | 0 | 📖 read | — |
| `list_proposals` | 0 | 📖 read | — |
| `create_proposal` | 5 | ✍️ write | ✅ required |
| `update_proposal` | 2 | ✍️ write | ✅ required |
| `archive_proposal` | 0 | ⚠️ destructive | — |
| `request_buyer_acceptance` | 0 | ✍️ write | — |
| `reserve_proposal` | 0 | ✍️ write | — |
| `edit_proposal_for_negotiation` | 0 | ✍️ write | — |
| `terminate_proposal_negotiations` | 0 | ⚠️ destructive | — |
| `pause_proposal` | 0 | ✍️ write | — |
| `resume_proposal` | 0 | ✍️ write | — |
| `unarchive_proposal` | 0 | ✍️ write | — |
| `discard_proposal_drafts` | 0 | ⚠️ destructive | — |
| `request_buyer_review` | 0 | ✍️ write | — |
| `push_proposal_to_order` | 0 | ✍️ write | — |
| `get_marketplace_comments` | 0 | 📖 read | — |
| `list_proposal_line_items` | 0 | 📖 read | — |
| `create_proposal_line_items` | 3 | ✍️ write | ✅ required |
| `update_proposal_line_items` | 1 | ✍️ write | ✅ required |
| `archive_proposal_line_items` | 0 | ⚠️ destructive | — |
| `get_proposal_line_item` | 0 | 📖 read | — |
| `pause_proposal_line_items` | 0 | ✍️ write | — |
| `resume_proposal_line_items` | 0 | ✍️ write | — |
| `reserve_proposal_line_items` | 0 | ✍️ write | — |
| `release_proposal_line_items` | 0 | ✍️ write | — |
| `unarchive_proposal_line_items` | 0 | ✍️ write | — |
| `create_makegoods` | 3 | ✍️ write | ✅ required |
| `estimate_deal_cost` | 0 | 📖 read | — |
| `adcp_validate` | 0 | 📖 read | — |
| `adcp_preview` | 0 | 📖 read | — |
| `adcp_create` | 0 | ✍️ write | — |

### `formats` — Epic 78.2

_Parent formats MCP tool — Custom Format Registry avec scope multi-site (Story 78.2)._

**Server-side implementation:** `formats.py` · **Actions:** 9 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_recipes` | 0 | 📖 read | — |
| `list_suggested_recipes` | 0 | 📖 read | — |
| `accept_suggested_recipe` | 0.25 | ✍️ write | ✅ required |
| `reject_suggested_recipe` | 0.25 | ✍️ write | ✅ required |
| `register_recipe` | 0.25 | ✍️ write | ✅ required |
| `update_recipe` | 0.25 | ✍️ write | ✅ required |
| `delete_recipe` | 0.25 | ⚠️ destructive | ✅ required |
| `resolve` | 0 | 📖 read | — |
| `detect_conflicts` | 0 | 📖 read | — |

### `gam_admin` — Epic 65

_GAM admin orchestration — single entry point for 54 ops over 7 areas._

**Server-side implementation:** `gam_admin.py` · **Actions:** 61 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `teams.list` | 0 | 📖 read | — |
| `teams.get` | 0 | 📖 read | — |
| `teams.create` | 0.5 | ✍️ write | ✅ required |
| `teams.batch_create` | 0.5 | ✍️ write | ✅ required |
| `teams.patch` | 0 | ✍️ write | — |
| `teams.batch_update` | 0 | ✍️ write | — |
| `teams.batch_activate` | 0 | ✍️ write | — |
| `teams.batch_deactivate` | 0 | ✍️ write | — |
| `sites.list` | 0 | 📖 read | — |
| `sites.get` | 0 | 📖 read | — |
| `sites.create` | 0.5 | ✍️ write | ✅ required |
| `sites.batch_create` | 0.5 | ✍️ write | ✅ required |
| `sites.patch` | 0 | ✍️ write | — |
| `sites.batch_update` | 0 | ✍️ write | — |
| `sites.batch_deactivate` | 0 | ✍️ write | — |
| `sites.batch_submit_for_approval` | 0 | ✍️ write | — |
| `applications.list` | 0 | 📖 read | — |
| `applications.get` | 0 | 📖 read | — |
| `applications.create` | 0.5 | ✍️ write | ✅ required |
| `applications.batch_create` | 0.5 | ✍️ write | ✅ required |
| `applications.patch` | 0 | ✍️ write | — |
| `applications.batch_update` | 0 | ✍️ write | — |
| `applications.batch_archive` | 0 | ⚠️ destructive | — |
| `applications.batch_unarchive` | 0 | ✍️ write | — |
| `custom_fields.list` | 0 | 📖 read | — |
| `custom_fields.get` | 0 | 📖 read | — |
| `custom_fields.create` | 0.5 | ✍️ write | ✅ required |
| `custom_fields.batch_create` | 0.5 | ✍️ write | ✅ required |
| `custom_fields.patch` | 0 | ✍️ write | — |
| `custom_fields.batch_update` | 0 | ✍️ write | — |
| `custom_fields.batch_activate` | 0 | ✍️ write | — |
| `custom_fields.batch_deactivate` | 0 | ✍️ write | — |
| `custom_fields.create_dropdown_options` | 0.5 | ✍️ write | ✅ required |
| `custom_fields.update_dropdown_options` | 0 | ✍️ write | — |
| `custom_fields.get_dropdown_option` | 0 | 📖 read | — |
| `labels.list` | 0 | 📖 read | — |
| `labels.get` | 0 | 📖 read | — |
| `labels.create` | 0.5 | ✍️ write | ✅ required |
| `labels.batch_create` | 0.5 | ✍️ write | ✅ required |
| `labels.patch` | 0 | ✍️ write | — |
| `labels.batch_update` | 0 | ✍️ write | — |
| `labels.batch_activate` | 0 | ✍️ write | — |
| `labels.batch_deactivate` | 0 | ✍️ write | — |
| `entity_signals.list` | 0 | 📖 read | — |
| `entity_signals.get` | 0 | 📖 read | — |
| `entity_signals.create` | 0.5 | ✍️ write | ✅ required |
| `entity_signals.batch_create` | 0.5 | ✍️ write | ✅ required |
| `entity_signals.patch` | 0 | ✍️ write | — |
| `entity_signals.batch_update` | 0 | ✍️ write | — |
| `users.list` | 0 | 📖 read | — |
| `users.get` | 0 | 📖 read | — |
| `users.current` | 0 | 📖 read | — |
| `users.get_roles` | 0 | 📖 read | — |
| `users.create` | 0.5 | ✍️ write | ✅ required |
| `users.update` | 0.5 | ✍️ write | ✅ required |
| `users.activate` | 0 | ✍️ write | — |
| `users.deactivate` | 0 | ✍️ write | — |
| `user_team_associations.list` | 0 | 📖 read | — |
| `user_team_associations.create` | 0.5 | ✍️ write | ✅ required |
| `user_team_associations.update` | 0 | ✍️ write | — |
| `user_team_associations.delete` | 0 | ⚠️ destructive | — |

### `gam_features` — Epic 68.5

_Parent gam_features tool for the Epic 68.5 catalogue refactor batch._

**Server-side implementation:** `gam_features.py` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_gam_features` | 0 | 📖 read | — |
| `probe_gam_features` | 0.5 | 📖 read | — |
| `refresh_gam_features` | 0 | 📖 read | — |

### `gam_jobs` — Epic 82

_Async job dispatcher (parent>child pattern, Epic 82)._

**Server-side implementation:** `jobs_async.py` · **Actions:** 4 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `image-optimize` | 0 | 📖 read | — |
| `blueprint-generate` | 0 | ✍️ write | — |
| `audit-export` | 0 | ✍️ write | — |
| `poll` | 0 | 📖 read | — |

### `inventory` — Epic 68.6

_Parent inventory tool for Story 68.6._

**Server-side implementation:** `inventory.py` · **Actions:** 15 · **Mode:** mixed (read + write)

**Legacy wrappers:** 10 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_ad_unit_tree` | 0 | 📖 read | — |
| `audit_inventory` | 0 | 📖 read | — |
| `create_ad_units_batch` | 0.5 | ✍️ write | ✅ required |
| `generate_ads_json` | 0 | 📖 read | — |
| `generate_inventory_blueprint` | 0 | 📖 read | — |
| `push_inventory_blueprint` | 0.5 | ✍️ write | ✅ required |
| `get_ad_units_by_ids` | 0 | 📖 read | — |
| `find_inactive_ad_units` | 0.25 | 📖 read | — |
| `archive_inactive_ad_units` | 0 | ⚠️ destructive | — |
| `list_ad_unit_sizes` | 0 | 📖 read | — |
| `blueprint_starter` | 0 | ✍️ write | — |
| `get_catalog` | 0 | 📖 read | — |
| `list_line_item_templates` | 0 | 📖 read | — |
| `list_suggested_ad_units` | 0 | 📖 read | — |
| `list_ad_units` | 0 | 📖 read | — |

### `jobs` — Epic 68.2

_Parent jobs tool for the Epic 68.2 catalogue refactor batch._

**Server-side implementation:** `jobs.py` · **Actions:** 3 · **Mode:** mixed (read + write)

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_job` | 0 | 📖 read | — |
| `list_jobs` | 0 | 📖 read | — |
| `duplicate_job` | 0 | ✍️ write | — |

### `line_items` — Epic 68

_Parent line_items tool for non-lifecycle Line Item operations._

**Server-side implementation:** `line_items.py` · **Actions:** 19 · **Mode:** mixed (read + write)

**Legacy wrappers:** 16 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get` | 0 | 📖 read | — |
| `get_full` | 0 | 📖 read | — |
| `list_by_order` | 0 | 📖 read | — |
| `list` | 0 | 📖 read | — |
| `update` | 0 | ✍️ write | — |
| `update_batch` | 0 | ✍️ write | — |
| `update_targeting` | 0 | ✍️ write | — |
| `duplicate` | 0 | ✍️ write | — |
| `verify` | 0 | 📖 read | — |
| `approve` | 0 | ✍️ write | — |
| `archive` | 0 | ⚠️ destructive | — |
| `create_batch` | 0 | ✍️ write | — |
| `activate_batch` | 0 | ✍️ write | — |
| `pause_batch` | 0 | ✍️ write | — |
| `create` | 0 | ✍️ write | — |
| `create_adexchange` | 0 | ✍️ write | — |
| `create_open_bidding` | 0 | ✍️ write | — |
| `create_preferred_deal` | 0 | ✍️ write | — |
| `list_private_deals` | 0 | 📖 read | — |

### `live_stream` — Epic 98

_Live stream ad breaks + event/slate management._

**Server-side implementation:** `live_stream.py` · **Actions:** 13 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list` | 0 | 📖 read | — |
| `get` | 0 | 📖 read | — |
| `create` | 0.5 | ✍️ write | ✅ required |
| `patch` | 0.5 | ✍️ write | ✅ required |
| `delete` | 0.5 | ⚠️ destructive | ✅ required |
| `list_live_stream_events` | 0 | 📖 read | — |
| `create_live_stream_event` | 0.5 | ✍️ write | ✅ required |
| `update_live_stream_event` | 0 | ✍️ write | — |
| `delete_live_stream_event` | 0 | ⚠️ destructive | — |
| `list_live_stream_slates` | 0 | 📖 read | — |
| `create_live_stream_slate` | 0.5 | ✍️ write | ✅ required |
| `update_live_stream_slate` | 0 | ✍️ write | — |
| `delete_live_stream_slate` | 0 | ⚠️ destructive | — |

### `mcm` — Epic 88.1

_Multi-Customer Management: earnings, child publishers and their agreements._

**Server-side implementation:** `mcm.py` · **Actions:** 8 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `earnings_fetch` | 0 | 📖 read | — |
| `list_child_publishers` | 0 | 📖 read | — |
| `get_child_publisher` | 0 | 📖 read | — |
| `invite_child_publisher` | 0.5 | ✍️ write | ✅ required |
| `update_child_publisher` | 0 | ✍️ write | — |
| `withdraw_child_publisher` | 0 | ⚠️ destructive | — |
| `renegotiate_child_publisher` | 0 | ✍️ write | — |
| `resend_child_publisher_invitation` | 0 | ✍️ write | — |

### `network` — Epic 68.5

_Parent network tool for the Epic 68.5 catalogue refactor batch._

**Server-side implementation:** `network.py` · **Actions:** 6 · **Mode:** mixed (read + write)

**Legacy wrappers:** 4 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_network_info` | 0 | 📖 read | — |
| `switch_network` | 0 | ✍️ write | — |
| `list_accessible_networks` | 0 | 📖 read | — |
| `update_network` | 0 | ✍️ write | — |
| `get_preview_url_library` | 0 | 📖 read | — |
| `set_preview_url_library` | 0 | ✍️ write | — |

### `orders` — Epic 68

_Parent orders tool for non-lifecycle Order operations._

**Server-side implementation:** `orders.py` · **Actions:** 11 · **Mode:** mixed (read + write)

**Legacy wrappers:** 11 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_delivering` | 0 | 📖 read | — |
| `get` | 0 | 📖 read | — |
| `list` | 0 | 📖 read | — |
| `create` | 0 | ✍️ write | — |
| `archive` | 0 | ⚠️ destructive | — |
| `approve` | 0 | ✍️ write | — |
| `verify_setup` | 0 | 📖 read | — |
| `update` | 0 | ✍️ write | — |
| `find_or_create` | 0 | ✍️ write | — |
| `list_users` | 0 | 📖 read | — |
| `list_roles` | 0 | 📖 read | — |

### `placements` — Epic 68.6

_Parent placements tool for Story 68.6._

**Server-side implementation:** `placements.py` · **Actions:** 6 · **Mode:** mixed (read + write)

**Legacy wrappers:** 4 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_placements` | 0 | 📖 read | — |
| `create_placement` | 0.5 | ✍️ write | ✅ required |
| `update_placement` | 0 | ✍️ write | — |
| `activate_placement` | 0 | ✍️ write | — |
| `deactivate_placement` | 0 | ✍️ write | — |
| `archive_placement` | 0 | ⚠️ destructive | — |

### `pql` — Epic 68.2

_Parent pql tool for the Epic 68.2 catalogue refactor batch._

**Server-side implementation:** `pql.py` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 1 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `run_query` | 0 | 📖 read | — |
| `validate_query` | 0 | 📖 read | — |
| `list_tables` | 0 | 📖 read | — |

### `prebid_skill` — Epic 70

_Dispatch Prebid.js / Header Bidding sub-actions through one MCP tool._

**Server-side implementation:** `prebid_skill.py` · **Actions:** 6 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `generate_line_items` | 10 | ✍️ write | ✅ required |
| `generate_targeting_keys` | 1 | ✍️ write | ✅ required |
| `update_line_items` | 5 | ✍️ write | ✅ required |
| `inspect_existing_setup` | 0 | 📖 read | — |
| `preview_batch` | 0 | 📖 read | — |
| `cleanup` | 0 | ⚠️ destructive | — |

### `preview` — Epic 68.2

_Parent preview tool for the Epic 68.2 catalogue refactor batch._

**Server-side implementation:** `preview.py` · **Actions:** 3 · **Mode:** read-only

**Legacy wrappers:** 3 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `get_preview_urls` | 0.25 | 📖 read | — |
| `get_campaign_preview_urls` | 0.25 | 📖 read | — |
| `check_creative_coverage` | 0 | 📖 read | — |

### `products` — Epic 68.8

_Parent products tool for the Epic 68.8 catalogue refactor batch._

**Server-side implementation:** `products.py` · **Actions:** 7 · **Mode:** mixed (read + write)

**Legacy wrappers:** 9 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `create` | 0 | ✍️ write | — |
| `list` | 0 | 📖 read | — |
| `get` | 0 | 📖 read | — |
| `update` | 0 | ✍️ write | — |
| `archive` | 0 | ⚠️ destructive | — |
| `get_adcp` | 0 | 📖 read | — |
| `pricing_suggestion` | 0 | 📖 read | — |

### `reporting` — Epic 68.7b

_Parent reporting tool for the Epic 68.7b catalogue refactor batch._

**Server-side implementation:** `reporting.py` · **Actions:** 33 · **Mode:** mixed (read + write)

**Legacy wrappers:** 31 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `check_delivery_status` | 0 | 📖 read | — |
| `fetch_delivery_report` | 0 | 📖 read | — |
| `run_custom_report` | 0.5 | 📖 read | — |
| `fetch_inventory_report` | 0.5 | 📖 read | — |
| `get_report_result` | 0 | 📖 read | — |
| `export_report_csv` | 0.5 | 📖 read | — |
| `get_report_download_link` | 0 | 📖 read | — |
| `get_report_dimensions` | 0 | 📖 read | — |
| `get_report_metrics` | 0 | 📖 read | — |
| `get_report_date_ranges` | 0 | 📖 read | — |
| `get_standalone_forecast` | 0 | 📖 read | — |
| `get_delivery_forecast_by_line_item` | 0 | 📖 read | — |
| `get_availability_forecast_by_line_item` | 0 | 📖 read | — |
| `get_prospective_delivery_forecast` | 0 | 📖 read | — |
| `get_traffic_data` | 0 | 📖 read | — |
| `list_report_templates` | 0 | 📖 read | — |
| `save_report_template` | 0 | ✍️ write | — |
| `delete_report_template` | 0 | ⚠️ destructive | — |
| `duplicate_report_template` | 0 | ✍️ write | — |
| `update_report_template` | 0 | ✍️ write | — |
| `run_report_from_template` | 0.5 | 📖 read | — |
| `list_gam_reports` | 0 | 📖 read | — |
| `get_gam_report` | 0 | 📖 read | — |
| `create_gam_report` | 0 | ✍️ write | — |
| `update_gam_report` | 0 | ✍️ write | — |
| `delete_gam_report` | 0 | ⚠️ destructive | — |
| `run_gam_report` | 0 | 📖 read | — |
| `run_ga_report` | 0.5 | 📖 read | — |
| `get_ga_dimensions` | 0 | 📖 read | — |
| `get_ga_metrics` | 0 | 📖 read | — |
| `check_underdelivery_alerts` | 0.25 | 📖 read | — |
| `check_budget_alerts` | 0.25 | 📖 read | — |
| `generate_billing_report` | 0.5 | 📖 read | — |

### `settings` — Epic 68.1

_Parent settings tool for the Epic 68.1 catalogue refactor POC._

**Server-side implementation:** `settings.py` · **Actions:** 26 · **Mode:** mixed (read + write)

**Legacy wrappers:** 9 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_presets` | 0 | 📖 read | — |
| `create_preset` | 0 | ✍️ write | — |
| `update_preset` | 0 | ✍️ write | — |
| `delete_preset` | 0 | ⚠️ destructive | — |
| `list_preset_suggestions` | 0 | 📖 read | — |
| `accept_preset_suggestion` | 0 | ✍️ write | — |
| `dismiss_preset_suggestion` | 0 | ✍️ write | — |
| `recompute_preset_suggestions` | 0 | ✍️ write | — |
| `get_tenant_settings` | 0 | 📖 read | — |
| `update_tenant_settings` | 0 | ✍️ write | — |
| `get_naming_conventions` | 0 | 📖 read | — |
| `update_naming_conventions` | 0 | ✍️ write | — |
| `get_delivery_defaults` | 0 | 📖 read | — |
| `update_delivery_defaults` | 0 | ✍️ write | — |
| `get_network_delivery_defaults` | 0 | 📖 read | — |
| `update_network_delivery_defaults` | 0 | ✍️ write | — |
| `reset_network_delivery_defaults` | 0 | ✍️ write | — |
| `get_network_naming_conventions` | 0 | 📖 read | — |
| `update_network_naming_conventions` | 0 | ✍️ write | — |
| `reset_network_naming_conventions` | 0 | ✍️ write | — |
| `get_multilang_matrix` | 0 | 📖 read | — |
| `get_global_multilang_matrix` | 0 | 📖 read | — |
| `save_global_multilang_matrix` | 0 | ✍️ write | — |
| `apply_multilang_to_networks` | 0 | ✍️ write | — |
| `resolve_multilang_matrix` | 0 | 📖 read | — |
| `list_preview_matrices` | 0 | 📖 read | — |

### `targeting` — Epic 68.6

_Parent targeting tool for Story 68.6._

**Server-side implementation:** `targeting.py` · **Actions:** 28 · **Mode:** mixed (read + write)

**Legacy wrappers:** 21 deprecated child tool(s) still in catalogue and routing to this parent — see [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md).

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_ad_units` | 0 | 📖 read | — |
| `validate_fluid` | 0 | 📖 read | — |
| `list_custom_targeting_keys` | 0 | 📖 read | — |
| `get_inventory_forecast` | 0 | 📖 read | — |
| `create_custom_targeting_key` | 0.5 | ✍️ write | ✅ required |
| `create_custom_targeting_values` | 0.5 | ✍️ write | ✅ required |
| `update_custom_targeting_key` | 0 | ✍️ write | — |
| `delete_custom_targeting_key` | 0 | ⚠️ destructive | — |
| `activate_custom_targeting_keys` | 0 | ✍️ write | — |
| `update_custom_targeting_value` | 0 | ✍️ write | — |
| `perform_custom_targeting_value_action` | 0 | ✍️ write | — |
| `search_ad_units` | 0 | 📖 read | — |
| `update_ad_unit` | 0 | ✍️ write | — |
| `activate_ad_unit` | 0 | ✍️ write | — |
| `deactivate_ad_unit` | 0 | ✍️ write | — |
| `archive_ad_unit` | 0 | ⚠️ destructive | — |
| `get_custom_targeting_values` | 0 | 📖 read | — |
| `search_custom_targeting` | 0 | 📖 read | — |
| `get_available_countries` | 0 | 📖 read | — |
| `get_available_languages` | 0 | 📖 read | — |
| `get_device_categories` | 0 | 📖 read | — |
| `get_browsers` | 0 | 📖 read | — |
| `get_operating_systems` | 0 | 📖 read | — |
| `get_content_labels` | 0 | 📖 read | — |
| `list_targeting_presets` | 0 | 📖 read | — |
| `create_targeting_preset` | 0.5 | ✍️ write | ✅ required |
| `update_targeting_preset` | 0 | ✍️ write | — |
| `delete_targeting_preset` | 0 | ⚠️ destructive | — |

### `tenant_catalog` — Epic 78.1

_Parent tenant_catalog MCP tool — scan + read tenant inventory catalog (Story 78.1)._

**Server-side implementation:** `tenant_catalog.py` · **Actions:** 4 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `scan_network` | 1 | ✍️ write | ✅ required |
| `get_scan_status` | 0 | 📖 read | — |
| `get_active_catalog` | 0 | 📖 read | — |
| `refresh` | 1 | ✍️ write | ✅ required |

### `video_ops` — Epic 98

_Video monetization: ad rule management, content metadata, and content bundle operations._

**Server-side implementation:** `video_ops.py` · **Actions:** 10 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_ad_rules` | 0 | 📖 read | — |
| `create_ad_rule` | 0.5 | ✍️ write | ✅ required |
| `update_ad_rule` | 0.5 | ✍️ write | ✅ required |
| `delete_ad_rule` | 0.5 | ⚠️ destructive | ✅ required |
| `list_content` | 0 | 📖 read | — |
| `list_content_bundles` | 0 | 📖 read | — |
| `create_content_bundle` | 0.5 | ✍️ write | ✅ required |
| `update_content_bundle` | 0.5 | ✍️ write | ✅ required |
| `activate_content_bundle` | 0.5 | ✍️ write | ✅ required |
| `deactivate_content_bundle` | 0.5 | ✍️ write | ✅ required |

### `yield_skill` — Epic 98

_Yield optimization group management and forecast governance._

**Server-side implementation:** `yield_skill.py` · **Actions:** 5 · **Mode:** mixed (read + write)

| Action | Cost (credits) | Access | Confirmation token? |
|---|---|---|---|
| `list_yield_groups` | 0 | 📖 read | — |
| `create_yield_group` | 0.5 | ✍️ write | ✅ required |
| `update_yield_group` | 0.5 | ✍️ write | ✅ required |
| `list_forecast_adjustments` | 0 | 📖 read | — |
| `list_forecast_segments` | 0 | 📖 read | — |

## Standalone tools

Tools that are neither parents nor deprecated wrappers (auth flow, async jobs, internal helpers).

| Tool | Module | Cost | Access |
|---|---|---|---|
| `check_credentials` | `auth.py:699` | 0 | 📖 read |
| `disconnect_gam` | `auth.py:762` | 0 | ⚠️ destructive |
| `gam_audit` | `gam_audit.py:116` | 0 | 📖 read |
| `get_my_tenant_id` | `auth.py:309` | 0 | 📖 read |
| `get_premium_rate` | `pricing.py:71` | 0 | 📖 read |
| `initiate_gam_auth` | `auth.py:408` | 0 | ✍️ write |
| `line_item_lifecycle` | `line_items.py:1665` | 0 | ⚠️ destructive |
| `list_premium_rates` | `pricing.py:50` | 0 | 📖 read |
| `list_rate_cards` | `pricing.py:30` | 0 | 📖 read |
| `order_lifecycle` | `orders.py:1028` | 0 | ⚠️ destructive |
| `poll_auth_status` | `auth.py:492` | 0 | 📖 read |
| `reporting_skill` | `reporting.py:4052` | 0 | ✍️ write |
| `select_gam_network` | `auth.py:613` | 0 | ✍️ write |
| `server_info` | `server_info.py:16` | 0 | 📖 read |

## See also

- [`_docs/legacy-tool-mapping.md`](../../_docs/legacy-tool-mapping.md) — the 241 legacy wrappers and their parent dispatch targets
- [`cli/parity-matrix.json`](../../cli/parity-matrix.json) — CLI command coverage per MCP tool
- [`.claude-plugin/plugin.json`](../../.claude-plugin/plugin.json) — Claude Code plugin manifest
