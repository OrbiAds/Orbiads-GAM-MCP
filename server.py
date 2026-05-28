#!/usr/bin/env python3
"""
OrbiAds MCP Server — local stub for Glama registry indexing and security scanning.

This stub runs fully offline and serves the OrbiAds tool catalogue via stdio MCP.
No network calls are made. All tool invocations return an auth-required message.

Production server (real GAM data): https://orbiads.com/mcp
Requires OAuth 2.0 authentication (Google / GAM account).
"""
import json
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("orbiads-stub")

SERVER_NAME = "orbiads"
SERVER_VERSION = "1.8.41"
PROTOCOL_VERSION = "2024-11-05"

AUTH_MSG = (
    "Authentication required. This is the OrbiAds MCP discovery stub. "
    "To perform real GAM operations connect to https://orbiads.com/mcp "
    "using OAuth 2.0 (Google account linked to your GAM network). "
    "See https://orbiads.com/docs/quickstart for setup instructions."
)

NETWORK_CODE_PROP = {
    "network_code": {
        "type": "integer",
        "description": "GAM network code (e.g. 12345678). Required for all network-scoped operations.",
    }
}

TENANT_PROP = {
    "tenant_id": {
        "type": "string",
        "description": "OrbiAds tenant identifier. Resolved automatically from the authenticated session.",
    }
}


def _t(name: str, description: str, actions: list[str], extra: dict | None = None) -> dict:
    """Build a parent tool definition with an action discriminator and optional extra properties."""
    props: dict = {
        "action": {
            "type": "string",
            "enum": actions,
            "description": f"Sub-operation to perform. One of: {', '.join(actions)}.",
        },
        **NETWORK_CODE_PROP,
        **(extra or {}),
    }
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": props,
            "required": ["action"],
            "additionalProperties": True,
        },
    }


def _standalone(name: str, description: str, props: dict, required: list[str] | None = None) -> dict:
    """Build a standalone (non-parent) tool definition."""
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": props,
            "required": required or [],
            "additionalProperties": False,
        },
    }


TOOLS: list[dict] = [
    # ── Parent tools (29) ─────────────────────────────────────────────────────
    _t(
        "audiences",
        "Manage GAM audience segments — create, list, get, update, and perform "
        "lifecycle actions on first-party audience data.",
        [
            "list_audience_segments",
            "get_audience_segment",
            "create_audience_segment",
            "update_audience_segment",
            "perform_audience_segment_action",
        ],
    ),
    _t(
        "audit",
        "Query the GAM audit log to retrieve change history across network objects "
        "(orders, line items, creatives, ad units, etc.).",
        ["query_audit_log"],
    ),
    _t(
        "audit_skill",
        "OrbiAds audit suite — single entry point for six audit sub-actions covering "
        "hygiene, operational diagnostics, security baseline, creative wrapper coverage, "
        "cost estimation, and authoring exports.",
        [
            "hygiene_check",
            "ops_diagnostic",
            "standards_baseline",
            "wrapper_coverage",
            "estimate_cost",
            "export_authoring",
        ],
        extra={
            "framework": {
                "type": "string",
                "enum": ["orbiads_baseline", "iso27001_adops", "iab_anti_tampering", "nist_csf"],
                "description": "Compliance framework for standards_baseline action.",
            }
        },
    ),
    _t(
        "billing",
        "Inspect OrbiAds billing — credit balance and transaction history.",
        ["get_credit_balance", "list_transactions"],
    ),
    _t(
        "blueprint",
        "CRUD operations on the tenant inventory blueprint — preferences, formats, "
        "positions, key-values, brand settings, and platform configuration.",
        [
            "get_active_preferences",
            "get_active_blueprint",
            "save_blueprint",
            "save_preferences",
            "add_format",
            "remove_format",
            "add_position",
            "remove_position",
            "add_key_value",
            "remove_key_value",
            "update_brand",
            "update_platforms",
            "list_templates",
        ],
    ),
    _t(
        "campaign",
        "Orchestrate GAM campaign lifecycle — deploy, update, rollback, pause, archive, "
        "and manage native styles and line item batches.",
        [
            "deploy",
            "update",
            "ensure_template",
            "create_native_style",
            "create_line_items_batch",
            "create_licas",
            "create_display",
            "rollback",
            "pause",
            "archive",
        ],
        extra={
            "campaign_id": {
                "type": "string",
                "description": "OrbiAds campaign identifier (required for update/rollback/pause/archive).",
            },
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token (required for deploy and rollback).",
            },
        },
    ),
    _t(
        "companies",
        "Manage GAM companies — advertisers, agencies, and contacts — with full CRUD support.",
        [
            "list_advertisers",
            "get_advertiser",
            "create_advertiser",
            "update_advertiser",
            "archive_advertiser",
            "list_agencies",
            "get_agency",
            "create_agency",
            "update_agency",
            "list_contacts",
            "get_contact",
            "update_contact",
        ],
    ),
    _t(
        "creative_assets",
        "Upload and manage GAM creative assets — images, HTML5 ZIPs, video, audio, "
        "VAST redirects, companions, classic native creatives, and compression tasks.",
        [
            "bulk_upload",
            "upload_from_url",
            "upload_and_associate",
            "upload_html5_zip",
            "create_image",
            "create_html5",
            "create_html5_from_files",
            "create_video",
            "create_audio",
            "create_vast_redirect",
            "create_companion",
            "create_third_party",
            "create_classic_native",
            "compress_image",
            "get_video_transcode_status",
        ],
    ),
    _t(
        "creative_qa",
        "Creative quality assurance — SSL validation, compliance scanning, tracking audits, "
        "tag snippet validation, and pre-archive checks.",
        [
            "scan_creative_compliance",
            "validate_creative_ssl",
            "validate_creative_ssl_batch",
            "audit_creative_tracking",
            "audit_order_tracking",
            "validate_tag_snippet",
            "pre_archive_check",
        ],
    ),
    _t(
        "creative_wrapper_skill",
        "Manage GAM CreativeWrapper entities at AdUnit or Placement level — list, get, "
        "create, update, activate, deactivate, archive, provision, and manage presets.",
        [
            "list",
            "get",
            "create",
            "update",
            "activate",
            "deactivate",
            "archive",
            "set_data_declaration",
            "list_rich_media_ads_companies",
            "find_third_party_company",
            "create_preset",
            "list_wrapper_presets",
            "provision",
        ],
    ),
    _t(
        "creatives",
        "Full creative lifecycle — list, get, update, archive, duplicate, preview URLs, "
        "native style management, creative templates, LICA association, and native format discovery.",
        [
            "list_creatives_by_advertiser",
            "list_creatives_by_line_item",
            "list_creatives_by_network",
            "get_creative",
            "update_creative",
            "archive_creative",
            "duplicate_creative",
            "get_creative_preview_url",
            "get_native_style_preview_urls",
            "get_campaign_preview_links",
            "get_video_transcode_status",
            "list_native_styles",
            "get_native_style",
            "update_native_style",
            "archive_native_style",
            "duplicate_native_style",
            "ensure_classic_native_template",
            "list_creative_templates",
            "get_creative_template",
            "discover_native_formats",
            "associate_creative",
            "bulk_associate_creatives",
            "get_licas_by_line_item",
            "get_licas_batch",
            "deactivate_lica",
            "update_lica",
            "delete_licas",
        ],
    ),
    _t(
        "deals",
        "Author and manage programmatic deals — PMP, PG/PD proposals, ADCP flows, "
        "auction packages, buyer management, marketplace comments, makegoods, and cost estimation.",
        [
            "list_deals",
            "get_deal",
            "create_deal",
            "update_deal",
            "list_auctions",
            "get_auction",
            "create_auction",
            "update_auction",
            "list_buyers",
            "get_buyer",
            "get_proposal",
            "create_proposal",
            "update_proposal",
            "archive_proposal",
            "request_buyer_acceptance",
            "reserve_proposal",
            "edit_proposal_for_negotiation",
            "terminate_proposal_negotiations",
            "get_marketplace_comments",
            "list_proposal_line_items",
            "create_proposal_line_items",
            "update_proposal_line_items",
            "archive_proposal_line_items",
            "create_makegoods",
            "estimate_deal_cost",
            "adcp_validate",
            "adcp_preview",
            "adcp_create",
        ],
    ),
    _t(
        "formats",
        "Manage the Custom Format Registry with multi-site scope — register, update, delete, "
        "resolve conflicts, and browse suggested recipes.",
        [
            "list_recipes",
            "list_suggested_recipes",
            "accept_suggested_recipe",
            "reject_suggested_recipe",
            "register_recipe",
            "update_recipe",
            "delete_recipe",
            "resolve",
            "detect_conflicts",
        ],
    ),
    _t(
        "gam_admin",
        "GAM admin orchestration — single entry point for 48 operations across 7 areas: "
        "Teams, Sites, Mobile Apps, Custom Fields, Labels, Publisher Provided Signals, and Users.",
        [
            "list_teams", "get_team", "create_team", "update_team", "delete_team",
            "add_team_members", "remove_team_members",
            "list_sites", "get_site", "create_site", "update_site", "delete_site",
            "list_mobile_apps", "get_mobile_app", "create_mobile_app", "update_mobile_app",
            "list_custom_fields", "get_custom_field", "create_custom_field",
            "update_custom_field", "deactivate_custom_field",
            "list_custom_field_options", "create_custom_field_option",
            "update_custom_field_option", "deactivate_custom_field_option",
            "list_labels", "get_label", "create_label", "update_label", "deactivate_label",
            "list_pps_configs", "get_pps_config", "create_pps_config",
            "update_pps_config", "delete_pps_config",
            "list_users", "get_user", "get_current_user", "create_user",
            "update_user", "deactivate_user", "perform_user_action",
            "list_roles", "list_team_memberships",
            "get_user_record", "get_salesperson_record",
            "get_trafficker_record", "audit_user_access",
        ],
    ),
    _t(
        "gam_features",
        "Inspect and refresh the GAM features available on the network (beta features, "
        "enabled capabilities, real-time probing).",
        ["get_gam_features", "probe_gam_features", "refresh_gam_features"],
    ),
    _t(
        "gam_jobs",
        "Async GAM job dispatcher — poll status, list and retrieve results for "
        "long-running background operations (Epic 82 pattern).",
        ["poll", "get", "list", "cancel"],
        extra={
            "job_id": {
                "type": "string",
                "description": "Async job identifier returned by a previous long-running operation.",
            }
        },
    ),
    _t(
        "inventory",
        "Manage GAM ad unit inventory — tree traversal, audit, batch creation, "
        "ads.txt generation, blueprint push/pull, and inactive unit cleanup.",
        [
            "get_ad_unit_tree",
            "audit_inventory",
            "create_ad_units_batch",
            "generate_ads_json",
            "generate_inventory_blueprint",
            "push_inventory_blueprint",
            "get_ad_units_by_ids",
            "find_inactive_ad_units",
            "archive_inactive_ad_units",
            "list_ad_unit_sizes",
        ],
    ),
    _t(
        "jobs",
        "Manage OrbiAds campaign deployment jobs — get status, list history, and duplicate.",
        ["get_job", "list_jobs", "duplicate_job"],
        extra={
            "job_id": {
                "type": "string",
                "description": "OrbiAds job identifier.",
            }
        },
    ),
    _t(
        "line_items",
        "Non-lifecycle Line Item operations — get, list, update, targeting, duplicate, "
        "verify, approve, archive, batch create, and programmatic types.",
        [
            "get",
            "list_by_order",
            "update",
            "update_targeting",
            "duplicate",
            "verify",
            "approve",
            "archive",
            "create_batch",
            "activate_batch",
            "pause_batch",
            "create_adexchange",
            "create_open_bidding",
            "create_preferred_deal",
            "list_private_deals",
        ],
        extra={
            "line_item_id": {
                "type": "integer",
                "description": "GAM Line Item ID (required for single-entity operations).",
            },
            "order_id": {
                "type": "integer",
                "description": "GAM Order ID (required for list_by_order).",
            },
        },
    ),
    _t(
        "network",
        "GAM network management — get info, switch active network, list all accessible "
        "networks, and update network settings.",
        ["get_network_info", "switch_network", "list_accessible_networks", "update_network"],
    ),
    _t(
        "orders",
        "Non-lifecycle Order operations — list, get, create, update, archive, approve, "
        "verify setup, find-or-create, and manage users and roles.",
        [
            "list_delivering",
            "get",
            "list",
            "create",
            "archive",
            "approve",
            "verify_setup",
            "update",
            "find_or_create",
            "list_users",
            "list_roles",
        ],
        extra={
            "order_id": {
                "type": "integer",
                "description": "GAM Order ID (required for single-entity operations).",
            }
        },
    ),
    _t(
        "placements",
        "Manage GAM placements — list, create, update, and archive placement targeting groups.",
        ["list_placements", "create_placement", "update_placement", "archive_placement"],
    ),
    _t(
        "pql",
        "Execute PQL (Publisher Query Language) queries against GAM reporting tables "
        "for ad-hoc data extraction.",
        ["run_query"],
        extra={
            "pql_query": {
                "type": "string",
                "description": "PQL SELECT statement (e.g. SELECT Id, Name FROM Order WHERE ...).",
            }
        },
    ),
    _t(
        "preview",
        "Generate creative and campaign preview URLs and check creative coverage "
        "across line items.",
        ["get_preview_urls", "get_campaign_preview_urls", "check_creative_coverage"],
    ),
    _t(
        "products",
        "Manage GAM Products and Product Packages — create, list, get, update, archive, "
        "inspect ADCP configuration, and get pricing suggestions.",
        [
            "create",
            "list",
            "get",
            "update",
            "archive",
            "get_adcp",
            "pricing_suggestion",
        ],
        extra={
            "product_id": {
                "type": "integer",
                "description": "GAM Product ID (required for single-entity operations).",
            }
        },
    ),
    _t(
        "reporting",
        "Full GAM and GA4 reporting — custom reports, delivery reports, inventory reports, "
        "forecasting, traffic data, report templates, alert checks, and billing reports.",
        [
            "check_delivery_status",
            "fetch_delivery_report",
            "run_custom_report",
            "fetch_inventory_report",
            "get_report_result",
            "export_report_csv",
            "get_report_dimensions",
            "get_report_metrics",
            "get_report_date_ranges",
            "get_standalone_forecast",
            "get_delivery_forecast_by_line_item",
            "get_prospective_delivery_forecast",
            "get_traffic_data",
            "list_report_templates",
            "save_report_template",
            "delete_report_template",
            "duplicate_report_template",
            "update_report_template",
            "run_report_from_template",
            "list_gam_reports",
            "get_gam_report",
            "create_gam_report",
            "update_gam_report",
            "delete_gam_report",
            "run_gam_report",
            "run_ga_report",
            "get_ga_dimensions",
            "get_ga_metrics",
            "check_underdelivery_alerts",
            "check_budget_alerts",
            "generate_billing_report",
        ],
    ),
    _t(
        "settings",
        "Manage OrbiAds tenant settings — naming conventions, delivery defaults, "
        "presets (create/list/delete), and global tenant configuration.",
        [
            "list_presets",
            "create_preset",
            "delete_preset",
            "get_tenant_settings",
            "update_tenant_settings",
            "get_naming_conventions",
            "update_naming_conventions",
            "get_delivery_defaults",
            "update_delivery_defaults",
        ],
    ),
    _t(
        "targeting",
        "Manage GAM custom targeting keys and values — create, update, delete, search, "
        "inspect ad units, validate fluid targeting, and fetch available country/language/device lists.",
        [
            "list_ad_units",
            "validate_fluid",
            "list_custom_targeting_keys",
            "get_inventory_forecast",
            "create_custom_targeting_key",
            "create_custom_targeting_values",
            "update_custom_targeting_key",
            "delete_custom_targeting_key",
            "update_custom_targeting_value",
            "perform_custom_targeting_value_action",
            "search_ad_units",
            "update_ad_unit",
            "archive_ad_unit",
            "get_custom_targeting_values",
            "search_custom_targeting",
            "get_available_countries",
            "get_available_languages",
            "get_device_categories",
        ],
    ),
    _t(
        "tenant_catalog",
        "Scan and read the tenant inventory catalog — network scanning, scan status polling, "
        "catalog refresh, and active catalog retrieval.",
        ["scan_network", "get_scan_status", "get_active_catalog", "refresh"],
    ),
    # ── Standalone tools (10) ──────────────────────────────────────────────────
    _standalone(
        "get_my_tenant_id",
        "Return the OrbiAds tenant ID associated with the authenticated session. "
        "Call this first to resolve your tenant_id before any scoped operations.",
        {},
    ),
    _standalone(
        "initiate_gam_auth",
        "Start the OAuth 2.0 authorization flow to link a GAM network to your OrbiAds tenant. "
        "Returns an authorization URL to open in the browser.",
        {
            "network_code": {
                "type": "integer",
                "description": "The GAM network code to authorize.",
            }
        },
        required=["network_code"],
    ),
    _standalone(
        "poll_auth_status",
        "Poll the OAuth authorization status after initiating a GAM auth flow. "
        "Returns 'pending', 'authorized', or 'failed'.",
        {
            "session_id": {
                "type": "string",
                "description": "Auth session ID returned by initiate_gam_auth.",
            }
        },
        required=["session_id"],
    ),
    _standalone(
        "select_gam_network",
        "Set the active GAM network code for the current session when the tenant has "
        "multiple linked networks.",
        {
            "network_code": {
                "type": "integer",
                "description": "GAM network code to activate.",
            }
        },
        required=["network_code"],
    ),
    _standalone(
        "line_item_lifecycle",
        "Lifecycle operations on a Line Item — activate, pause, archive, or resume — "
        "with optional confirmation token for write-gated actions.",
        {
            "line_item_id": {"type": "integer", "description": "GAM Line Item ID."},
            "lifecycle_action": {
                "type": "string",
                "enum": ["activate", "pause", "archive", "resume"],
                "description": "Lifecycle transition to apply.",
            },
            "network_code": {"type": "integer", "description": "GAM network code."},
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token (required for destructive transitions).",
            },
        },
        required=["line_item_id", "lifecycle_action", "network_code"],
    ),
    _standalone(
        "order_lifecycle",
        "Lifecycle operations on an Order — approve, archive, or disapprove — "
        "with optional confirmation token.",
        {
            "order_id": {"type": "integer", "description": "GAM Order ID."},
            "lifecycle_action": {
                "type": "string",
                "enum": ["approve", "archive", "disapprove"],
                "description": "Lifecycle transition to apply.",
            },
            "network_code": {"type": "integer", "description": "GAM network code."},
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token (required for approve/archive).",
            },
        },
        required=["order_id", "lifecycle_action", "network_code"],
    ),
    _standalone(
        "reporting_skill",
        "High-level reporting skill — orchestrates multi-step GAM and GA4 report workflows, "
        "combining dimension/metric discovery, report creation, and result export into one call.",
        {
            "network_code": {"type": "integer", "description": "GAM network code."},
            "goal": {
                "type": "string",
                "description": "Plain-language reporting goal (e.g. 'weekly revenue by ad unit for last month').",
            },
        },
        required=["network_code", "goal"],
    ),
    _standalone(
        "check_credentials",
        "Verify that the GAM OAuth credentials linked to the tenant are still valid "
        "and have the required scopes.",
        {
            "network_code": {"type": "integer", "description": "GAM network code to check."},
        },
        required=["network_code"],
    ),
    _standalone(
        "disconnect_gam",
        "Revoke and remove the GAM OAuth credentials for a specific network from the tenant.",
        {
            "network_code": {"type": "integer", "description": "GAM network code to disconnect."},
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token (required — this action is irreversible).",
            },
        },
        required=["network_code", "confirmation_token"],
    ),
    _standalone(
        "gam_audit",
        "Run a comprehensive GAM network audit covering security baseline, hygiene checks, "
        "and operational diagnostics in a single call.",
        {
            "network_code": {"type": "integer", "description": "GAM network code."},
            "framework": {
                "type": "string",
                "enum": ["orbiads_baseline", "iso27001_adops", "iab_anti_tampering", "nist_csf"],
                "description": "Compliance framework to evaluate against.",
            },
        },
        required=["network_code"],
    ),
]


# ── MCP JSON-RPC over stdio ────────────────────────────────────────────────────
# Protocol: Content-Length framing (same as LSP / JSON-RPC 2.0 over stdio)
# Ref: https://spec.modelcontextprotocol.io/specification/basic/transports/#stdio

def _read_message() -> dict | None:
    """Read one JSON-RPC message from stdin (Content-Length framed)."""
    headers: dict[str, str] = {}
    while True:
        raw = sys.stdin.buffer.readline()
        if not raw:
            return None
        line = raw.decode("utf-8").rstrip("\r\n")
        if not line:
            break
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v

    length = int(headers.get("content-length", 0))
    if not length:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def _write_message(obj: dict) -> None:
    """Write one JSON-RPC message to stdout (Content-Length framed)."""
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8")
    sys.stdout.buffer.write(header + body)
    sys.stdout.buffer.flush()


def _handle(req: dict) -> dict | None:
    method = req.get("method", "")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": (
                    "OrbiAds MCP Server — Google Ad Manager automation via natural language. "
                    "Authenticate at https://orbiads.com to connect your GAM network."
                ),
            },
        }

    if method == "notifications/initialized":
        return None  # notification — no response

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": AUTH_MSG}],
                "isError": False,
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

    # Unknown method
    if req_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    return None


def main() -> None:
    logger.info("OrbiAds MCP stub v%s — listening on stdio", SERVER_VERSION)
    while True:
        try:
            msg = _read_message()
            if msg is None:
                break
            response = _handle(msg)
            if response is not None:
                _write_message(response)
        except json.JSONDecodeError as exc:
            logger.error("JSON decode error: %s", exc)
        except Exception as exc:  # noqa: BLE001
            logger.error("Unhandled error: %s", exc)


if __name__ == "__main__":
    main()
