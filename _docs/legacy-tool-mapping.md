<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo
  (@deprecated_tool decorators in the MCP tool definitions).
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# Legacy Tool Mapping — OrbiAds MCP Catalogue

OrbiAds Epic 68 / 76 refactored the MCP catalogue from a flat list of ~270 tools to a parent>child design with 36 parent tools. The 241 pre-refactor child tools are kept as **soft-deprecated wrappers, scheduled for sunset (Epic 68.4)** — they route to their parent and emit a `deprecated_tool_called` analytics event on use. They are hidden at runtime and are **not counted** as part of the public tool/operation surface (which is the parent + standalone tools only).

**Migration recommendation:** Update integrations to call the parent tool with `action: <child_name>` instead. Schedule: parents stable from Epic 68 (2026 Q2). Sunset of legacy wrappers TBD per usage telemetry.

## Replacement summary

| Parent tool | Legacy wrappers count |
|---|---|
| `audiences` | 5 |
| `audit` | 1 |
| `audit_skill` | 2 |
| `billing` | 2 |
| `campaign` | 13 |
| `companies` | 12 |
| `creative_assets` | 18 |
| `creative_qa` | 7 |
| `creatives` | 27 |
| `deals` | 29 |
| `gam_features` | 3 |
| `inventory` | 10 |
| `jobs` | 3 |
| `line_items` | 16 |
| `network` | 4 |
| `orders` | 11 |
| `placements` | 4 |
| `pql` | 1 |
| `preview` | 3 |
| `products` | 9 |
| `reporting` | 31 |
| `settings` | 9 |
| `targeting` | 21 |

## Detailed mapping

### → `audiences` (5 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `create_audience_segment` | `create_audience_segment` | `audiences.py` |
| `get_audience_segment` | `get_audience_segment` | `audiences.py` |
| `list_audience_segments` | `list_audience_segments` | `audiences.py` |
| `perform_audience_segment_action` | `perform_audience_segment_action` | `audiences.py` |
| `update_audience_segment` | `update_audience_segment` | `audiences.py` |

### → `audit` (1 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `query_audit_log` | `query_audit_log` | `audit.py` |

### → `audit_skill` (2 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `audit_skill_estimate_cost` | `estimate_cost` | `audit_estimator.py` |
| `export_authoring_audit` | `export_authoring` | `export_authoring_audit.py` |

### → `billing` (2 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `get_credit_balance` | `get_credit_balance` | `billing.py` |
| `list_transactions` | `list_transactions` | `billing.py` |

### → `campaign` (13 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_campaign` | `archive` | `campaign_ops.py` |
| `archive_eligible_campaigns` | `archive_eligible` | `campaign_ops.py` |
| `create_display_campaign` | `create_display` | `campaign_ops.py` |
| `create_licas` | `create_licas` | `campaign_ops.py` |
| `create_line_items_batch` | `create_line_items_batch` | `campaign_ops.py` |
| `create_native_style` | `create_native_style` | `campaign_ops.py` |
| `deploy_campaign` | `deploy` | `campaign_ops.py` |
| `deploy_media_action` | `deploy_media` | `campaign_ops.py` |
| `ensure_template` | `ensure_template` | `campaign_ops.py` |
| `pause_campaign` | `pause` | `campaign_ops.py` |
| `plan_deployment_action` | `plan_deployment` | `campaign_ops.py` |
| `rollback_resources` | `rollback` | `campaign_ops.py` |
| `update_campaign` | `update` | `campaign_ops.py` |

### → `companies` (12 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `create_advertiser` | `advertisers.create` | `advertisers.py` |
| `create_agency` | `agencies.create` | `advertisers.py` |
| `create_contact` | `contacts.create` | `orders.py` |
| `find_advertiser` | `advertisers.find` | `advertisers.py` |
| `find_or_create_advertiser` | `advertisers.find_or_create` | `advertisers.py` |
| `get_advertiser` | `advertisers.get` | `advertisers.py` |
| `get_agencies` | `agencies.list` | `advertisers.py` |
| `get_contacts` | `contacts.list` | `orders.py` |
| `list_advertisers` | `advertisers.list` | `advertisers.py` |
| `update_advertiser` | `advertisers.update` | `advertisers.py` |
| `update_agency` | `agencies.update` | `advertisers.py` |
| `update_contact` | `contacts.update` | `orders.py` |

### → `creative_assets` (18 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `bulk_upload_creatives` | `bulk_upload` | `creatives.py` |
| `compress_image_creative` | `compress_image` | `creatives.py` |
| `create_audio_creative` | `create_audio` | `creatives.py` |
| `create_classic_native_creative` | `create_classic_native` | `creatives.py` |
| `create_click_tracking_creative` | `create_click_tracking` | `creatives.py` |
| `create_companion_creative` | `create_companion` | `creatives.py` |
| `create_custom_creative` | `create_custom` | `creatives.py` |
| `create_html5_creative` | `create_html5` | `creatives.py` |
| `create_html5_creative_from_files` | `create_html5_from_files` | `creatives.py` |
| `create_image_creative` | `create_image` | `creatives.py` |
| `create_image_redirect_creative` | `create_image_redirect` | `creatives.py` |
| `create_internal_redirect_creative` | `create_internal_redirect` | `creatives.py` |
| `create_third_party_creative` | `create_third_party` | `creatives.py` |
| `create_vast_redirect_creative` | `create_vast_redirect` | `creatives.py` |
| `create_video_creative` | `create_video` | `creatives.py` |
| `upload_and_associate_creative` | `upload_and_associate` | `creatives.py` |
| `upload_creative_from_url` | `upload_from_url` | `creatives.py` |
| `upload_html5_zip_creative` | `upload_html5_zip` | `creatives.py` |

### → `creative_qa` (7 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `audit_creative_tracking` | `audit_creative_tracking` | `creative_qa.py` |
| `audit_order_tracking` | `audit_order_tracking` | `creative_qa.py` |
| `pre_archive_check` | `pre_archive_check` | `creative_qa.py` |
| `scan_creative_compliance` | `scan_creative_compliance` | `creative_qa.py` |
| `validate_creative_ssl` | `validate_creative_ssl` | `creative_qa.py` |
| `validate_creative_ssl_batch` | `validate_creative_ssl_batch` | `creative_qa.py` |
| `validate_tag_snippet` | `validate_tag_snippet` | `creative_qa.py` |

### → `creatives` (27 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_creative` | `archive_creative` | `creatives.py` |
| `archive_native_style` | `archive_native_style` | `creatives.py` |
| `associate_creative` | `associate_creative` | `creatives.py` |
| `bulk_associate_creatives` | `bulk_associate_creatives` | `creatives.py` |
| `deactivate_lica` | `deactivate_lica` | `creatives.py` |
| `delete_licas` | `delete_licas` | `creatives.py` |
| `discover_native_formats` | `discover_native_formats` | `creatives.py` |
| `duplicate_creative` | `duplicate_creative` | `creatives.py` |
| `duplicate_native_style` | `duplicate_native_style` | `creatives.py` |
| `ensure_classic_native_template` | `ensure_classic_native_template` | `creatives.py` |
| `get_campaign_preview_links` | `get_campaign_preview_links` | `creatives.py` |
| `get_creative` | `get_creative` | `creatives.py` |
| `get_creative_preview_url` | `get_creative_preview_url` | `creatives.py` |
| `get_creative_template` | `get_creative_template` | `creatives.py` |
| `get_licas_batch` | `get_licas_batch` | `creatives.py` |
| `get_licas_by_line_item` | `get_licas_by_line_item` | `creatives.py` |
| `get_native_style` | `get_native_style` | `creatives.py` |
| `get_native_style_preview_urls` | `get_native_style_preview_urls` | `creatives.py` |
| `get_video_transcode_status` | `get_video_transcode_status` | `creatives.py` |
| `list_creative_templates` | `list_creative_templates` | `creatives.py` |
| `list_creatives_by_advertiser` | `list_creatives_by_advertiser` | `creatives.py` |
| `list_creatives_by_line_item` | `list_creatives_by_line_item` | `creatives.py` |
| `list_creatives_by_network` | `list_creatives_by_network` | `creatives.py` |
| `list_native_styles` | `list_native_styles` | `creatives.py` |
| `update_creative` | `update_creative` | `creatives.py` |
| `update_lica` | `update_lica` | `creatives.py` |
| `update_native_style` | `update_native_style` | `creatives.py` |

### → `deals` (29 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_proposal` | `archive_proposal` | `deals.py` |
| `archive_proposal_line_items` | `archive_proposal_line_items` | `deals.py` |
| `create_deal` | `create_deal` | `deals.py` |
| `create_makegoods` | `create_makegoods` | `deals.py` |
| `create_media_buy_from_adcp` | `adcp_create` | `adcp.py` |
| `create_pmp_deal` | `create_deal` | `deals.py` |
| `create_private_auction` | `create_auction` | `deals.py` |
| `create_proposal` | `create_proposal` | `deals.py` |
| `create_proposal_line_items` | `create_proposal_line_items` | `deals.py` |
| `edit_proposal_for_negotiation` | `edit_proposal_for_negotiation` | `deals.py` |
| `estimate_deal_cost` | `estimate_deal_cost` | `deals.py` |
| `get_marketplace_comments` | `get_marketplace_comments` | `deals.py` |
| `get_pmp_deal` | `get_deal` | `deals.py` |
| `get_private_auction` | `get_auction` | `deals.py` |
| `get_programmatic_buyer` | `get_buyer` | `deals.py` |
| `get_proposal` | `get_proposal` | `deals.py` |
| `list_pmp_deals` | `list_deals` | `deals.py` |
| `list_private_auctions` | `list_auctions` | `deals.py` |
| `list_programmatic_buyers` | `list_buyers` | `deals.py` |
| `list_proposal_line_items` | `list_proposal_line_items` | `deals.py` |
| `preview_media_buy_from_adcp` | `adcp_preview` | `adcp.py` |
| `request_buyer_acceptance` | `request_buyer_acceptance` | `deals.py` |
| `reserve_proposal` | `reserve_proposal` | `deals.py` |
| `terminate_proposal_negotiations` | `terminate_proposal_negotiations` | `deals.py` |
| `update_pmp_deal` | `update_deal` | `deals.py` |
| `update_private_auction` | `update_auction` | `deals.py` |
| `update_proposal` | `update_proposal` | `deals.py` |
| `update_proposal_line_items` | `update_proposal_line_items` | `deals.py` |
| `validate_adcp_request` | `adcp_validate` | `adcp.py` |

### → `gam_features` (3 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `get_gam_features` | `get_gam_features` | `gam_features.py` |
| `probe_gam_features` | `probe_gam_features` | `gam_features.py` |
| `refresh_gam_features` | `refresh_gam_features` | `gam_features.py` |

### → `inventory` (10 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_inactive_ad_units` | `archive_inactive_ad_units` | `inventory.py` |
| `audit_inventory` | `audit_inventory` | `inventory.py` |
| `create_ad_units_batch` | `create_ad_units_batch` | `inventory.py` |
| `find_inactive_ad_units` | `find_inactive_ad_units` | `inventory.py` |
| `generate_ads_json` | `generate_ads_json` | `inventory.py` |
| `generate_inventory_blueprint` | `generate_inventory_blueprint` | `inventory.py` |
| `get_ad_unit_tree` | `get_ad_unit_tree` | `inventory.py` |
| `get_ad_units_by_ids` | `get_ad_units_by_ids` | `inventory.py` |
| `list_ad_unit_sizes` | `list_ad_unit_sizes` | `inventory.py` |
| `push_inventory_blueprint` | `push_inventory_blueprint` | `inventory.py` |

### → `jobs` (3 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `duplicate_job` | `duplicate_job` | `jobs.py` |
| `get_job` | `get_job` | `jobs.py` |
| `list_jobs` | `list_jobs` | `jobs.py` |

### → `line_items` (16 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `activate_line_items` | `activate_batch` | `line_items.py` |
| `approve_line_item` | `approve` | `line_items.py` |
| `archive_line_item` | `archive` | `line_items.py` |
| `create_adexchange_line_item` | `create_adexchange` | `line_items.py` |
| `create_line_item` | `create` | `line_items.py` |
| `create_line_items` | `create_batch` | `line_items.py` |
| `create_open_bidding_line_item` | `create_open_bidding` | `line_items.py` |
| `create_preferred_deal_line_item` | `create_preferred_deal` | `line_items.py` |
| `duplicate_line_item` | `duplicate` | `line_items.py` |
| `get_line_item` | `get` | `line_items.py` |
| `list_line_items_by_order` | `list_by_order` | `line_items.py` |
| `list_private_deals` | `list_private_deals` | `line_items.py` |
| `pause_line_items` | `pause_batch` | `line_items.py` |
| `update_line_item` | `update` | `line_items.py` |
| `update_line_item_targeting` | `update_targeting` | `line_items.py` |
| `verify_line_item_setup` | `verify` | `line_items.py` |

### → `network` (4 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `get_network_info` | `get_network_info` | `network.py` |
| `list_accessible_networks` | `list_accessible_networks` | `network.py` |
| `switch_network` | `switch_network` | `network.py` |
| `update_network` | `update_network` | `network.py` |

### → `orders` (11 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `approve_order` | `approve` | `orders.py` |
| `archive_order` | `archive` | `orders.py` |
| `create_order` | `create` | `orders.py` |
| `find_or_create_order` | `find_or_create` | `advertisers.py` |
| `get_order` | `get` | `orders.py` |
| `list_delivering_orders` | `list_delivering` | `orders.py` |
| `list_orders` | `list` | `orders.py` |
| `list_roles` | `list_roles` | `orders.py` |
| `list_users` | `list_users` | `orders.py` |
| `update_order` | `update` | `orders.py` |
| `verify_order_setup` | `verify_setup` | `orders.py` |

### → `placements` (4 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_placement` | `archive_placement` | `placements.py` |
| `create_placement` | `create_placement` | `placements.py` |
| `list_placements` | `list_placements` | `placements.py` |
| `update_placement` | `update_placement` | `placements.py` |

### → `pql` (1 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `run_pql_query` | `run_query` | `pql.py` |

### → `preview` (3 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `check_creative_coverage` | `check_creative_coverage` | `preview.py` |
| `get_campaign_preview_urls` | `get_campaign_preview_urls` | `preview.py` |
| `get_preview_urls` | `get_preview_urls` | `preview.py` |

### → `products` (9 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_product` | `archive` | `products.py` |
| `create_premium_rate` | `pricing_create_premium_rate` | `pricing.py` |
| `create_product` | `create` | `products.py` |
| `get_pricing_suggestion` | `pricing_suggestion` | `products.py` |
| `get_product` | `get` | `products.py` |
| `get_products_adcp` | `get_adcp` | `products.py` |
| `list_products` | `list` | `products.py` |
| `update_premium_rate` | `pricing_update_premium_rate` | `pricing.py` |
| `update_product` | `update` | `products.py` |

### → `reporting` (31 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `check_budget_alerts` | `check_budget_alerts` | `reporting.py` |
| `check_delivery_status` | `check_delivery_status` | `reporting.py` |
| `check_underdelivery_alerts` | `check_underdelivery_alerts` | `reporting.py` |
| `create_gam_report` | `create_gam_report` | `reporting.py` |
| `delete_gam_report` | `delete_gam_report` | `reporting.py` |
| `delete_report_template` | `delete_report_template` | `reporting.py` |
| `duplicate_report_template` | `duplicate_report_template` | `reporting.py` |
| `export_report_csv` | `export_report_csv` | `reporting.py` |
| `fetch_delivery_report` | `fetch_delivery_report` | `reporting.py` |
| `fetch_inventory_report` | `fetch_inventory_report` | `reporting.py` |
| `generate_billing_report` | `generate_billing_report` | `reporting.py` |
| `get_delivery_forecast_by_line_item` | `get_delivery_forecast_by_line_item` | `reporting.py` |
| `get_ga_dimensions` | `get_ga_dimensions` | `reporting.py` |
| `get_ga_metrics` | `get_ga_metrics` | `reporting.py` |
| `get_gam_report` | `get_gam_report` | `reporting.py` |
| `get_prospective_delivery_forecast` | `get_prospective_delivery_forecast` | `reporting.py` |
| `get_report_date_ranges` | `get_report_date_ranges` | `reporting.py` |
| `get_report_dimensions` | `get_report_dimensions` | `reporting.py` |
| `get_report_metrics` | `get_report_metrics` | `reporting.py` |
| `get_report_result` | `get_report_result` | `reporting.py` |
| `get_standalone_forecast` | `get_standalone_forecast` | `reporting.py` |
| `get_traffic_data` | `get_traffic_data` | `reporting.py` |
| `list_gam_reports` | `list_gam_reports` | `reporting.py` |
| `list_report_templates` | `list_report_templates` | `reporting.py` |
| `run_custom_report` | `run_custom_report` | `reporting.py` |
| `run_ga_report` | `run_ga_report` | `reporting.py` |
| `run_gam_report` | `run_gam_report` | `reporting.py` |
| `run_report_from_template` | `run_report_from_template` | `reporting.py` |
| `save_report_template` | `save_report_template` | `reporting.py` |
| `update_gam_report` | `update_gam_report` | `reporting.py` |
| `update_report_template` | `update_report_template` | `reporting.py` |

### → `settings` (9 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `create_preset` | `create_preset` | `settings.py` |
| `delete_preset` | `delete_preset` | `settings.py` |
| `get_delivery_defaults` | `get_delivery_defaults` | `settings.py` |
| `get_naming_conventions` | `get_naming_conventions` | `settings.py` |
| `get_tenant_settings` | `get_tenant_settings` | `settings.py` |
| `list_presets` | `list_presets` | `settings.py` |
| `update_delivery_defaults` | `update_delivery_defaults` | `settings.py` |
| `update_naming_conventions` | `update_naming_conventions` | `settings.py` |
| `update_tenant_settings` | `update_tenant_settings` | `settings.py` |

### → `targeting` (21 legacy wrappers)

| Legacy tool | Replacement action | Module |
|---|---|---|
| `archive_ad_unit` | `archive_ad_unit` | `targeting.py` |
| `create_custom_targeting_key` | `create_custom_targeting_key` | `targeting.py` |
| `create_custom_targeting_values` | `create_custom_targeting_values` | `targeting.py` |
| `delete_custom_targeting_key` | `delete_custom_targeting_key` | `targeting.py` |
| `get_available_countries` | `get_available_countries` | `targeting.py` |
| `get_available_languages` | `get_available_languages` | `targeting.py` |
| `get_browsers` | `get_browsers` | `targeting.py` |
| `get_content_labels` | `get_content_labels` | `targeting.py` |
| `get_custom_targeting_values` | `get_custom_targeting_values` | `targeting.py` |
| `get_device_categories` | `get_device_categories` | `targeting.py` |
| `get_inventory_forecast` | `get_inventory_forecast` | `targeting.py` |
| `get_operating_systems` | `get_operating_systems` | `targeting.py` |
| `list_ad_units` | `list_ad_units` | `targeting.py` |
| `list_custom_targeting_keys` | `list_custom_targeting_keys` | `targeting.py` |
| `perform_custom_targeting_value_action` | `perform_custom_targeting_value_action` | `targeting.py` |
| `search_ad_units` | `search_ad_units` | `targeting.py` |
| `search_custom_targeting` | `search_custom_targeting` | `targeting.py` |
| `update_ad_unit` | `update_ad_unit` | `targeting.py` |
| `update_custom_targeting_key` | `update_custom_targeting_key` | `targeting.py` |
| `update_custom_targeting_value` | `update_custom_targeting_value` | `targeting.py` |
| `validate_fluid` | `validate_fluid` | `targeting.py` |
