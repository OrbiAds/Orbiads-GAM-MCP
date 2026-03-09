# Tool Matrix

## Purpose

- Map each business objective to:
  - shared skills;
  - MCP tools;
  - guardrails;
  - expected output.

## Matrix

| Objective | Shared skill | Primary MCP tools | Guardrails | Expected output |
| --- | --- | --- | --- | --- |
| Bootstrap auth and network context | `bootstrap` | `get_my_tenant_id`, `initiate_gam_auth`, `poll_auth_status`, `check_credentials`, `select_gam_network`, `get_network_info`, `list_accessible_networks`, `get_credit_balance`, `get_tenant_settings`, `get_delivery_defaults` | stop on missing auth or ambiguous network context | session packet with `tenantId`, `networkCode`, blockers, and next skill |
| Audit or shape inventory | `inventory-ad-units` | `list_ad_units`, `search_ad_units`, `get_ad_unit_tree`, `audit_inventory`, `generate_inventory_blueprint`, `push_inventory_blueprint`, `create_ad_units_batch`, `find_inactive_ad_units` | read audit first, confirm before batch writes or cleanup | inventory packet, blueprint, or created ad-unit IDs |
| Manage placements and targeting | `placements-targeting` | `list_placements`, `create_placement`, `update_placement`, `archive_placement`, `validate_fluid`, `list_custom_targeting_keys`, `get_custom_targeting_values`, `search_custom_targeting`, `get_available_countries`, `get_available_languages`, `get_device_categories` | validate fluid before Native paths and confirm taxonomy before writes | placement IDs and targeting packet |
| Validate supply before trafficking | `availability-forecast` | `get_standalone_forecast`, `get_delivery_forecast_by_line_item`, `get_inventory_forecast` | warn about cost-sensitive reads and stop when inputs are incomplete | forecast summary with risk and recommendation |
| Prepare advertiser, order, and line items | `advertiser-order-line-items` | `list_advertisers`, `get_advertiser`, `create_advertiser`, `find_advertiser`, `list_orders`, `get_order`, `update_order`, `verify_order_setup`, `create_line_items`, `list_line_items_by_order`, `get_line_item`, `update_line_item`, `verify_line_item_setup`, `activate_line_items` | do not document `find_or_create_order`; treat `create_open_bidding_line_item` as a boundary only | trafficking packet with advertiser, order, and line-item state |
| Build Classic Native image creatives | `native-image` | `create_image_creative`, `ensure_classic_native_template`, `create_classic_native_creative`, `associate_creative`, `get_creative` | require approved asset, naming context, and downstream QA | creative IDs and Native-ready creative packet |
| Run QA and preview gates | `qa-preview` | `scan_creative_compliance`, `validate_creative_ssl`, `validate_creative_ssl_batch`, `get_preview_urls`, `get_campaign_preview_urls`, `check_creative_coverage`, `get_creative_preview_url` | compliance, SSL, preview, and human go/no-go required before launch | QA verdict, preview URLs, and blockers |
| Deploy, monitor, report, or rollback | `deploy-reporting` | `deploy_campaign`, `update_campaign`, `pause_campaign`, `archive_campaign`, `rollback_resources`, `check_delivery_status`, `fetch_delivery_report`, `run_custom_report`, `fetch_inventory_report`, `get_report_result`, `export_report_csv`, `check_underdelivery_alerts`, `check_budget_alerts`, `query_audit_log` | separate `dry_run`, approval, execution, and post-launch monitoring | deployment summary, alerts, report handles, or rollback plan |

## Rule

- wrappers should surface the shared skill first and only expose low-level tools through the shared contracts.