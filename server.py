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

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

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

SERVER_INFO = {
    "name": "OrbiAds Google Ad Manager MCP",
    "status": "ok",
    "auth_required_for_gam": True,
    "transport": "streamable-http",
    "docs": "https://orbiads.com/docs/mcp",
    "tools_total": 50,
    "operations_total": 290,
}

# ── Schema helpers ─────────────────────────────────────────────────────────────

def _actions_desc(actions: list[tuple[str, str]]) -> str:
    """Format action descriptions as a readable list."""
    lines = ["Sub-operation to perform:"]
    for name, desc in actions:
        lines.append(f"  • {name}: {desc}")
    return "\n".join(lines)


def _t(name: str, description: str, actions: list[tuple[str, str]], extra: dict | None = None) -> dict:
    """Build a parent tool definition with a discriminator action enum."""
    action_names = [a[0] for a in actions]
    props: dict = {
        "action": {
            "type": "string",
            "enum": action_names,
            "description": _actions_desc(actions),
        },
        "network_code": {
            "type": "integer",
            "description": "GAM network code (e.g. 12345678). Required for all network-scoped operations. Obtain via select_gam_network or list_accessible_networks.",
        },
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


# ── Tool catalogue ─────────────────────────────────────────────────────────────

TOOLS: list[dict] = [
    _standalone(
        "server_info",
        "Public health and catalogue summary. Real Google Ad Manager operations require OAuth.",
        {},
    ),

    # -- ad_review_center ------------------------------------------------------
    _t(
        "ad_review_center",
        """Search and moderate Ad Exchange creatives in GAM Ad Review Center.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: search = 0 credits. allow_batch/block_batch are write operations.
OUTPUT: search returns Ad Review creative results. Batch actions return moderation summaries.
WHEN TO USE: Use ad_review_center to find, allow, or block marketplace creatives before they serve on publisher inventory.""",
        [
            ("search", "Search Ad Review Center creatives by web property, status, advertiser, or review filters."),
            ("allow_batch", "Allow multiple reviewed ads in one write operation. Requires ad IDs."),
            ("block_batch", "Block multiple reviewed ads in one write operation. Requires ad IDs and a block reason."),
        ],
    ),

    # -- dai_skill -----------------------------------------------------------------
    _t(
        "dai_skill",
        """DAI (Dynamic Ad Insertion) and broadcasting operations.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: read = 0 credits.
OUTPUT: Results for DAI entities.
WHEN TO USE: Use for managing Dynamic Ad Insertion auth keys and encoding profiles.""",
        [
            ("create_cdn_configuration", "Create a CDN configuration."),
            ("create_dai_auth_key", "Create a DAI authentication key."),
            ("create_dai_encoding_profile", "Create a DAI encoding profile."),
            ("delete_cdn_configuration", "Delete a CDN configuration."),
            ("delete_dai_encoding_profile", "Delete a DAI encoding profile."),
            ("perform_dai_auth_key_action", "Perform an action on a DAI authentication key."),
            ("register_sessions", "Register sessions."),
            ("update_cdn_configuration", "Update a CDN configuration."),
            ("update_dai_auth_key", "Update a DAI authentication key."),
            ("update_dai_encoding_profile", "Update a DAI encoding profile."),
            ("get_stream_activity", "Get stream activity."),
            ("list_cdn_configurations", "List CDN configurations."),
            ("list_dai_auth_keys", "List DAI authentication keys."),
            ("list_dai_encoding_profiles", "List DAI encoding profiles."),
        ],
    ),

    # -- live_stream -----------------------------------------------------------
    _t(
        "live_stream",
        """Manage live stream ad breaks for GAM video workflows.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: list/get = 0 credits. create/patch/delete are write operations.
OUTPUT: Returns live stream ad break objects scoped by event, asset key, or custom asset key.
WHEN TO USE: Use live_stream to inspect, create, update, or delete ad breaks for live video events.""",
        [
            ("list", "List ad breaks for an event_id, asset_key, or custom_asset_key."),
            ("get", "Get a specific ad break by identifier."),
            ("create", "Create a new live stream ad break."),
            ("patch", "Update an existing live stream ad break by asset key."),
            ("delete", "Delete an existing live stream ad break by asset key."),
        ],
    ),

    # -- video_ops -----------------------------------------------------------------
    _t(
        "video_ops",
        """Video monetization: ad rule management, content metadata, and content bundle operations.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: read = 0 credits.
OUTPUT: Results for video ops entities.
WHEN TO USE: Use for managing Ad Rules, Content metadata, and Content bundles.""",
        [
            ("create_ad_rules", "Create ad rules."),
            ("create_content_bundles", "Create content bundles."),
            ("perform_ad_rule_action", "Perform an action on ad rules."),
            ("perform_content_action", "Perform an action on content."),
            ("perform_content_bundle_action", "Perform an action on content bundles."),
            ("update_ad_rules", "Update ad rules."),
            ("update_content_bundles", "Update content bundles."),
            ("get_ad_rules_by_statement", "Get ad rules by statement."),
            ("get_content_bundles_by_statement", "Get content bundles by statement."),
            ("get_content_by_statement", "Get content by statement."),
        ],
    ),

    # -- mcm -------------------------------------------------------------------
    _t(
        "mcm",
        """Read Multi-Customer Management earnings for parent publishers.

MODE: read-only
AUTH: OAuth 2.0 required with MCM principal access
CREDITS: 0 credits
OUTPUT: Returns monthly MCM earnings for the requested month and year.
WHEN TO USE: Use mcm for publisher revenue reporting across MCM child networks.""",
        [
            ("earnings_fetch", "Fetch monthly MCM earnings for a given month and year."),
        ],
    ),

    # -- prebid_skill ----------------------------------------------------------
    _t(
        "prebid_skill",
        """Plan and operate Prebid.js / header bidding setup for GAM.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: preview and inspect reads are free. Generation/update actions may charge credits when they create or mutate GAM entities.
OUTPUT: Returns targeting-key plans, line item generation summaries, cleanup previews, or update results.
WHEN TO USE: Use prebid_skill to generate Prebid targeting keys, create or update Prebid line items, preview batches, inspect existing setup, or clean up generated artifacts.""",
        [
            ("preview_batch", "Preview a Prebid batch plan without mutating GAM."),
            ("generate_targeting_keys", "Generate GAM custom targeting keys and values for Prebid."),
            ("generate_line_items", "Generate Prebid line items from bucket and placement configuration."),
            ("update_line_items", "Update existing Prebid line items."),
            ("inspect_existing_setup", "Inspect existing GAM targeting keys, values, and line items for Prebid readiness."),
            ("cleanup", "Preview or run cleanup for generated Prebid artifacts."),
        ],
    ),

    # ── audiences ──────────────────────────────────────────────────────────────
    _t(
        "audiences",
        """Manage GAM first-party audience segments.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required — call initiate_gam_auth first
CREDITS: list/get = 0 credits (free). create_audience_segment = 0.5 credits and requires a confirmation_token.
OUTPUT: Returns audience segment objects with id, name, status, membershipExpirationDays, and eligibilityCriteria.
SIDE EFFECTS: create/update modify GAM network data. perform_audience_segment_action can activate or deactivate segments.
WHEN TO USE: Use this tool for managing first-party data segments (CRM lists, pixel-based audiences). For targeting existing segments on line items, use the targeting tool instead.""",
        [
            ("list_audience_segments", "List all audience segments on the network. Read-only, free. Returns paginated list with id, name, type, and status."),
            ("get_audience_segment", "Get a specific audience segment by ID. Read-only, free. Requires segment_id parameter."),
            ("create_audience_segment", "Create a new first-party audience segment. Write operation, costs 0.5 credits, requires confirmation_token. Returns the created segment with its new ID."),
            ("update_audience_segment", "Update an existing audience segment's name, description, or membership rules. Write, free. Requires segment_id."),
            ("perform_audience_segment_action", "Activate or deactivate a segment. Write, free. Requires segment_id and action type (ACTIVATE or DEACTIVATE)."),
        ],
    ),

    # ── audit ──────────────────────────────────────────────────────────────────
    _t(
        "audit",
        """Query the GAM audit log for change history.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns a list of AuditEvent objects with entityId, entityType, changeType, userId, timestamp, and a diff of changed fields.
WHEN TO USE: Use audit when you need to trace who changed what and when on a specific GAM entity (order, line item, creative, ad unit).
NOT the same as audit_skill: audit queries the GAM change log; audit_skill runs proactive quality/compliance checks.
NOT the same as gam_audit: gam_audit runs a full network-wide compliance report; audit queries history for a specific entity.""",
        [
            ("query_audit_log", "Execute a filtered query against the GAM audit log. Filterable by entityId, entityType, userId, and date range. Returns a paginated list of audit events."),
        ],
    ),

    # ── audit_skill ────────────────────────────────────────────────────────────
    _t(
        "audit_skill",
        """OrbiAds proactive audit suite — six sub-actions for quality and compliance analysis.

MODE: read-only (all actions are non-destructive analysis)
AUTH: OAuth 2.0 required
CREDITS: 0 (all actions free)
OUTPUT: Returns a structured markdown report with findings, severity levels (CRITICAL/WARNING/INFO), and recommended remediations.
WHEN TO USE: Use audit_skill to proactively detect problems before they impact delivery.
  • Use hygiene_check for routine health checks (orphaned creatives, stalled orders, mismatched budgets).
  • Use standards_baseline to verify compliance against a named framework (ISO 27001 ad-ops, IAB, NIST).
  • Use wrapper_coverage to audit creative wrapper deployment across ad units.
  • Use estimate_cost to preview credit costs before running expensive operations.
NOT the same as audit: audit queries GAM change history; audit_skill analyzes current state.
NOT the same as gam_audit: gam_audit is a convenience wrapper combining hygiene_check + ops_diagnostic + standards_baseline in one call.""",
        [
            ("hygiene_check", "Scan the network for hygiene issues: orphaned creatives, line items past end date still active, orders with no live line items, creative-line item association gaps. Returns severity-tagged findings."),
            ("ops_diagnostic", "Diagnose operational delivery problems: underdelivery, pacing issues, targeting conflicts, creative disapprovals. Correlates data across orders/line items/creatives."),
            ("standards_baseline", "Evaluate the network against a named compliance framework. Requires framework parameter: orbiads_baseline | iso27001_adops | iab_anti_tampering | nist_csf. Returns a pass/fail checklist per control."),
            ("wrapper_coverage", "Audit CreativeWrapper coverage across ad units and placements. Detects missing wrappers, double-wrapping, and wrapper misconfiguration."),
            ("estimate_cost", "Preview the credit cost of an operation before executing it. Requires operation_name and parameters. Returns cost in credits and explanation."),
            ("export_authoring", "Export an authoring-audit CSV of GAM entities (teams, users, custom fields, labels) for governance and compliance reporting. Returns a download URL or inline CSV."),
        ],
        extra={
            "framework": {
                "type": "string",
                "enum": ["orbiads_baseline", "iso27001_adops", "iab_anti_tampering", "nist_csf"],
                "description": "Compliance framework for standards_baseline action. Required when action=standards_baseline.",
            },
        },
    ),

    # ── billing ────────────────────────────────────────────────────────────────
    _t(
        "billing",
        """Inspect OrbiAds account billing — credit balance and transaction history.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: get_credit_balance returns {balance: float, plan: string, monthly_allowance: int}. list_transactions returns paginated list of {date, type, amount, description, balance_after}.
WHEN TO USE: Call get_credit_balance before write operations to confirm sufficient credits. Use list_transactions for usage auditing.""",
        [
            ("get_credit_balance", "Return the current credit balance, plan type, and monthly allowance for the authenticated tenant."),
            ("list_transactions", "List credit transaction history (debits for write operations, credits for plan renewal/top-ups). Filterable by date range."),
        ],
    ),

    # ── blueprint ──────────────────────────────────────────────────────────────
    _t(
        "blueprint",
        """Manage the tenant inventory blueprint — the canonical definition of ad formats, positions, key-values, and brand settings used to generate GAM campaigns.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes (save_blueprint, save_preferences, add/remove operations) = 0 credits but modify persistent tenant configuration.
OUTPUT: get_active_blueprint returns the full blueprint JSON with formats, positions, keyValues, brand. list_templates returns available campaign templates.
SIDE EFFECTS: Changes to the blueprint affect all future campaign deployments that reference it. Removing a format or position does not remove existing GAM line items.
WHEN TO USE: Use blueprint to define or update the standard inventory structure before running campaign. Use formats tool for the Custom Format Registry (creative format recipes, not inventory positions).""",
        [
            ("get_active_preferences", "Read the current tenant preferences (naming conventions, default targeting, delivery settings)."),
            ("get_active_blueprint", "Read the full active inventory blueprint JSON."),
            ("save_blueprint", "Replace the full blueprint with a new version. Write. Validate with a dry-run before saving to production."),
            ("save_preferences", "Update tenant preferences. Write."),
            ("add_format", "Add a creative format to the blueprint. Write. Requires format_code and size parameters."),
            ("remove_format", "Remove a creative format from the blueprint. Write. Does not remove existing GAM creatives."),
            ("add_position", "Add an inventory position (ad unit + targeting combination) to the blueprint. Write."),
            ("remove_position", "Remove an inventory position from the blueprint. Write. Does not archive existing ad units."),
            ("add_key_value", "Add a custom targeting key-value definition to the blueprint. Write."),
            ("remove_key_value", "Remove a key-value definition from the blueprint. Write."),
            ("update_brand", "Update brand metadata (name, logo, primary color) attached to the blueprint. Write."),
            ("update_platforms", "Update the list of target platforms (desktop, mobile_web, app_ios, app_android) in the blueprint. Write."),
            ("list_templates", "List all available campaign templates (display, native, video presets). Read-only."),
        ],
    ),

    # ── campaign ───────────────────────────────────────────────────────────────
    _t(
        "campaign",
        """Orchestrate GAM campaign lifecycle — the primary write surface for creating and managing campaigns.

MODE: write-heavy (most actions modify GAM data)
AUTH: OAuth 2.0 required
CREDITS: deploy = 2–5 credits depending on line item count. Other write operations = 0.5–1 credit. Reads = 0.
CONFIRMATION TOKEN: create_draft, deploy and rollback require a confirmation_token obtained from a prior dry-run preview. This prevents accidental deployment.
DEPLOY WORKFLOW: create_draft creates a Firestore campaigns/{campaignId} document from MCP. deploy accepts either campaignId (modern campaigns/{id}) or jobId (legacy jobs/{id}). For direct GAM-only display trafficking, use create_display.
OUTPUT: deploy returns {campaign_id, order_id, line_item_ids[], creative_ids[], status}. rollback returns {reverted_to_version, entities_affected}.
SIDE EFFECTS: deploy creates Order + LineItems + Creatives + LICAs in GAM — irreversible without rollback. rollback archives the current version and restores the previous one.
WHEN TO USE: Use campaign for end-to-end campaign creation from a blueprint. Use line_items or orders for surgical updates to existing campaigns.
DESTRUCTIVE: rollback and archive are non-trivial — they modify live GAM entities.""",
        [
            ("deploy", "Deploy a complete campaign to GAM: accepts campaignId from create_draft/REST or legacy jobId, plus confirmation_token. Creates Order, LineItems, Creatives, and LICAs."),
            ("create_draft", "Create an OrbiAds campaigns/{campaignId} draft from MCP without using the web UI. Write, requires confirmation_token."),
            ("update", "Update an existing campaign's metadata, budget, or targeting without full redeployment. Write."),
            ("ensure_template", "Ensure a native ad template exists in GAM, creating it if absent. Idempotent write."),
            ("create_native_style", "Create a GAM native ad style for use in native campaigns. Write."),
            ("create_line_items_batch", "Create multiple line items under an existing order in one call. Write. Faster than individual line item creation."),
            ("create_licas", "Create LineItem-Creative Associations (LICAs) to link creatives to line items. Write."),
            ("create_display", "Create a standard display ad campaign (order + line items + creatives) from a template. Write, requires confirmation_token."),
            ("rollback", "Revert a campaign to its previous deployed version. Destructive write — archives current version. Requires confirmation_token."),
            ("pause", "Pause all active line items in a campaign. Write."),
            ("archive", "Archive a campaign (order + line items). Destructive — removes from active serving. Requires confirmation_token."),
        ],
        extra={
            "campaign_id": {
                "type": "string",
                "description": "OrbiAds campaigns/{campaignId} identifier, accepted by deploy and campaign lifecycle actions.",
            },
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token from a prior estimate/preview call. Required for deploy, rollback, archive.",
            },
            "jobId": {
                "type": "string",
                "description": "Legacy Firestore jobs/{jobId} document. deploy also accepts modern campaignId.",
            },
        },
    ),

    # ── companies ──────────────────────────────────────────────────────────────
    _t(
        "companies",
        """Manage GAM companies — advertisers, agencies, and contacts.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes (create, update, archive) = 0.5 credits.
OUTPUT: Returns Company objects with id, name, type (ADVERTISER/AGENCY/HOUSE_ADVERTISER), creditStatus, address, and associated contacts.
SIDE EFFECTS: archive_advertiser deactivates the company and prevents new orders from being created under it. Does not delete historical data.
WHEN TO USE: Use companies to manage the advertiser/agency entities required before creating orders. An order must be linked to an advertiser.""",
        [
            ("list_advertisers", "List all advertiser companies on the network. Read-only, paginated."),
            ("get_advertiser", "Get a specific advertiser by ID. Read-only. Requires company_id."),
            ("create_advertiser", "Create a new advertiser company. Write, 0.5 credits. Requires name and optionally creditStatus, address."),
            ("update_advertiser", "Update an existing advertiser's name, credit status, or address. Write."),
            ("archive_advertiser", "Archive (deactivate) an advertiser. Destructive write — prevents new orders. Requires company_id."),
            ("list_agencies", "List all agency companies on the network. Read-only."),
            ("get_agency", "Get a specific agency by ID. Read-only."),
            ("create_agency", "Create a new agency company. Write, 0.5 credits."),
            ("update_agency", "Update an existing agency. Write."),
            ("list_contacts", "List contacts associated with a company. Read-only. Requires company_id."),
            ("get_contact", "Get a specific contact by ID. Read-only."),
            ("update_contact", "Update a contact's details. Write."),
        ],
        extra={
            "company_id": {
                "type": "integer",
                "description": "GAM Company ID (required for get/update/archive operations).",
            },
        },
    ),

    # ── creative_assets ────────────────────────────────────────────────────────
    _t(
        "creative_assets",
        """Upload and create GAM creative asset files — images, HTML5, video, audio, and companion ads.

MODE: write (all actions upload or create assets)
AUTH: OAuth 2.0 required
CREDITS: 0.5 credits per upload/create action.
OUTPUT: Returns CreativeAsset objects with assetId, fileName, fileSize, mimeType, and a preview URL.
SIDE EFFECTS: Assets are stored in GAM and consume storage quota. compress_image modifies the asset file in-place.
WHEN TO USE: Use creative_assets for asset file management (uploading raw files). Use creatives for full Creative entity management (associate assets with creative templates). Use creative_qa to validate assets after upload.""",
        [
            ("bulk_upload", "Upload multiple asset files in one call. Returns list of assetId per file. Preferred over individual uploads for batch workflows."),
            ("upload_from_url", "Download a file from a URL and upload it to GAM as an asset. Write. Requires source_url and file_name."),
            ("upload_and_associate", "Upload an asset and immediately associate it with an existing creative. Write."),
            ("upload_html5_zip", "Upload an HTML5 ZIP package and validate its structure before storage. Returns assetId and a list of validation warnings."),
            ("create_image", "Create an image asset from raw bytes or a local file path. Write."),
            ("create_html5", "Create an HTML5 asset from inline HTML/CSS/JS content. Write."),
            ("create_html5_from_files", "Create an HTML5 asset by bundling multiple local files. Write."),
            ("create_video", "Create a video creative asset (VAST URL or inline video). Write."),
            ("create_audio", "Create an audio creative asset. Write."),
            ("create_vast_redirect", "Create a VAST redirect creative that points to an external VAST URL. Write."),
            ("create_companion", "Create a companion ad asset associated with a video creative. Write."),
            ("create_third_party", "Create a third-party tag creative asset (JavaScript or iframe snippet). Write."),
            ("create_classic_native", "Create a classic native ad asset with headline, body, image, and CTA fields. Write."),
            ("compress_image", "Compress an existing image asset to reduce file size. Modifies asset in-place. Write."),
            ("get_video_transcode_status", "Check the status of a video transcode job. Read-only. Returns status: PENDING | PROCESSING | COMPLETE | FAILED."),
        ],
    ),

    # ── creative_qa ────────────────────────────────────────────────────────────
    _t(
        "creative_qa",
        """Creative quality assurance — validate, scan, and pre-check creatives before and after trafficking.

MODE: read-only (all actions are non-destructive analysis)
AUTH: OAuth 2.0 required
CREDITS: 0 (all free)
OUTPUT: Returns a QA report with pass/fail status per check, severity (CRITICAL/WARNING/INFO), and specific issue descriptions with remediation guidance.
WHEN TO USE: Run creative_qa after uploading creative assets and before activating line items. Use pre_archive_check before archiving a creative to detect active associations.
NOT the same as audit_skill: audit_skill checks network-wide operational health; creative_qa focuses specifically on individual creative compliance.""",
        [
            ("scan_creative_compliance", "Scan a creative for policy violations, prohibited content, missing click-through URLs, and size non-compliance. Returns a compliance report per check."),
            ("validate_creative_ssl", "Verify that all URLs in a creative (click-throughs, image src, tracking pixels) are HTTPS. Critical for modern GAM requirements."),
            ("validate_creative_ssl_batch", "Run SSL validation on multiple creatives in one call. Returns a per-creative summary."),
            ("audit_creative_tracking", "Verify all impression and click tracking pixels are reachable and return 200. Detects broken trackers."),
            ("audit_order_tracking", "Audit tracking pixels across all creatives associated with an order. Returns a per-creative, per-tracker report."),
            ("validate_tag_snippet", "Validate a third-party ad tag snippet for syntax errors, unsafe JS, and missing required macros (%%CLICK_URL%%, etc.)."),
            ("pre_archive_check", "Check whether a creative has active LICA associations before archiving. Returns list of active line items that would be affected."),
        ],
    ),

    # ── creative_wrapper_skill ─────────────────────────────────────────────────
    _t(
        "creative_wrapper_skill",
        """Manage GAM CreativeWrapper entities — wrappers that inject scripts around all creatives served on an ad unit or placement.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns CreativeWrapper objects with id, name, adUnitId or placementId, headerHtmlSnippet, footerHtmlSnippet, and ordering.
SIDE EFFECTS: Active CreativeWrappers apply globally to every creative served on the targeted ad unit/placement. Misconfigured wrappers can break ad serving. Test in a staging network first.
WHEN TO USE: Use for injecting site-wide measurement scripts, viewability tags, or brand safety layers. Use presets for reusable wrapper templates.""",
        [
            ("list", "List all CreativeWrappers on the network. Read-only."),
            ("get", "Get a specific CreativeWrapper by ID. Read-only."),
            ("create", "Create a new CreativeWrapper. Write. Requires adUnitId or placementId, and headerHtmlSnippet or footerHtmlSnippet."),
            ("update", "Update an existing wrapper's snippet or targeting. Write."),
            ("activate", "Activate a paused wrapper. Write."),
            ("deactivate", "Deactivate an active wrapper without deleting it. Write. Preferred over archive for temporary suspension."),
            ("archive", "Archive a wrapper permanently. Destructive write."),
            ("set_data_declaration", "Set the data usage declaration for a wrapper (required for GDPR/CCPA compliance). Write."),
            ("list_rich_media_ads_companies", "List GAM-certified rich media companies available for wrapper configuration. Read-only."),
            ("find_third_party_company", "Search for a third-party company by name to use in a wrapper. Read-only."),
            ("create_preset", "Save a wrapper configuration as a reusable preset. Write."),
            ("list_wrapper_presets", "List all saved wrapper presets. Read-only."),
            ("provision", "Apply a preset to a set of ad units or placements. Bulk write."),
        ],
    ),

    # ── creatives ──────────────────────────────────────────────────────────────
    _t(
        "creatives",
        """Manage GAM Creative entities and native styles — full lifecycle from list to archive, plus LICA management.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits. Bulk operations = 0.5 credits flat.
OUTPUT: Returns Creative objects with id, name, type, size, previewUrl, and associated assetIds. Preview URLs expire after 24h.
WHEN TO USE: Use creatives for Creative entity management (metadata, associations, lifecycle). Use creative_assets for raw asset file uploads. Use creative_qa for compliance validation.
NOTE: A Creative entity in GAM wraps one or more creative_assets. A LICA (LineItem-Creative Association) links a Creative to a LineItem for serving.""",
        [
            ("list_creatives_by_advertiser", "List all creatives for a given advertiser ID. Read-only."),
            ("list_creatives_by_line_item", "List all creatives associated with a line item. Read-only."),
            ("list_creatives_by_network", "List all creatives on the network with optional filters. Read-only."),
            ("get_creative", "Get a single creative by ID. Read-only."),
            ("update_creative", "Update a creative's name, size, or snippet. Write."),
            ("archive_creative", "Archive a creative. Destructive write — removes from active serving. Run pre_archive_check first."),
            ("duplicate_creative", "Duplicate an existing creative to use as a starting point. Write."),
            ("get_creative_preview_url", "Generate a preview URL for a creative. Read-only. URL expires after 24h."),
            ("get_native_style_preview_urls", "Generate preview URLs for a native style across all sizes. Read-only."),
            ("get_campaign_preview_links", "Get all preview links for a campaign (all creatives + all placements). Read-only."),
            ("get_video_transcode_status", "Check transcode status for a video creative. Read-only."),
            ("list_native_styles", "List all native ad styles. Read-only."),
            ("get_native_style", "Get a specific native style by ID. Read-only."),
            ("update_native_style", "Update a native style's template or CSS. Write."),
            ("archive_native_style", "Archive a native style. Destructive write."),
            ("duplicate_native_style", "Duplicate a native style. Write."),
            ("ensure_classic_native_template", "Ensure a classic native template exists, creating it if absent. Idempotent write."),
            ("list_creative_templates", "List all creative templates available on the network. Read-only."),
            ("get_creative_template", "Get a specific creative template by ID. Read-only."),
            ("discover_native_formats", "Discover available native ad formats and their required fields. Read-only."),
            ("associate_creative", "Create a LICA between one creative and one line item. Write."),
            ("bulk_associate_creatives", "Create multiple LICAs in one call. Write."),
            ("get_licas_by_line_item", "List all LICAs for a line item. Read-only."),
            ("get_licas_batch", "Retrieve multiple LICAs by ID. Read-only."),
            ("deactivate_lica", "Deactivate a LICA without deleting it. Write."),
            ("update_lica", "Update a LICA's weight or start/end date. Write."),
            ("delete_licas", "Delete LICAs permanently. Destructive write."),
        ],
    ),

    # ── deals ──────────────────────────────────────────────────────────────────
    _t(
        "deals",
        """Author and manage programmatic deals — PMP, PG/PD proposals, ADCP deal flows, and auction packages.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Write operations = 0.5–2 credits. ADCP create = 2 credits.
OUTPUT: Returns Deal or Proposal objects with id, status, buyerId, floorPrice, targeting, and negotiation state.
SIDE EFFECTS: Proposals go through a negotiation workflow — state transitions (reserve, request_buyer_acceptance) trigger buyer notifications. terminate_proposal_negotiations is irreversible.
WHEN TO USE: Use deals for programmatic direct (PG/PD), private marketplace (PMP), and ADCP deal creation. For standard direct-sold campaigns, use campaign tool instead.""",
        [
            ("list_deals", "List all programmatic deals on the network. Read-only."),
            ("get_deal", "Get a specific deal by ID. Read-only."),
            ("create_deal", "Create a new programmatic deal. Write."),
            ("update_deal", "Update a deal's floor price or targeting. Write."),
            ("list_auctions", "List auction packages. Read-only."),
            ("get_auction", "Get a specific auction package. Read-only."),
            ("create_auction", "Create an auction package. Write."),
            ("update_auction", "Update an auction package. Write."),
            ("list_buyers", "List all programmatic buyers on the network. Read-only."),
            ("get_buyer", "Get a specific buyer by ID. Read-only."),
            ("get_proposal", "Get a proposal by ID including its negotiation history. Read-only."),
            ("create_proposal", "Create a new PG/PD proposal. Write."),
            ("update_proposal", "Update a proposal's terms, targeting, or pricing. Write."),
            ("archive_proposal", "Archive a proposal. Destructive write."),
            ("request_buyer_acceptance", "Send a proposal to the buyer for acceptance. Write — triggers buyer notification."),
            ("reserve_proposal", "Reserve inventory for a proposal (locks availability). Write."),
            ("edit_proposal_for_negotiation", "Reopen an accepted proposal for renegotiation. Write."),
            ("terminate_proposal_negotiations", "Permanently terminate negotiations. Irreversible destructive write."),
            ("get_marketplace_comments", "Retrieve buyer/seller comments on a proposal. Read-only."),
            ("list_proposal_line_items", "List line items within a proposal. Read-only."),
            ("create_proposal_line_items", "Create line items within a proposal. Write."),
            ("update_proposal_line_items", "Update proposal line items' targeting or pricing. Write."),
            ("archive_proposal_line_items", "Archive proposal line items. Destructive write."),
            ("create_makegoods", "Create makegood line items to compensate for underdelivered campaigns. Write."),
            ("estimate_deal_cost", "Preview the credit cost of a deal operation. Read-only."),
            ("adcp_validate", "Validate an ADCP deal configuration before creation. Read-only."),
            ("adcp_preview", "Preview an ADCP deal's reach and estimated delivery. Read-only."),
            ("adcp_create", "Create an ADCP deal. Write, 2 credits, requires confirmation_token."),
        ],
    ),

    # ── formats ────────────────────────────────────────────────────────────────
    _t(
        "formats",
        """Manage the Custom Format Registry — reusable creative format recipes with multi-site scope.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0 credits (config changes only).
OUTPUT: Returns Format recipe objects with id, name, dimensions, creative_type, and applicable_sites.
WHEN TO USE: Use formats to define reusable creative format specifications (e.g., a 300x250 standard display recipe) that can be applied across multiple GAM networks.
NOT the same as blueprint: blueprint defines inventory positions; formats defines creative format specifications.
NOT the same as creative_assets: creative_assets manages uploaded files; formats manages format metadata.""",
        [
            ("list_recipes", "List all registered creative format recipes. Read-only."),
            ("list_suggested_recipes", "List AI-suggested format recipes based on the network's inventory. Read-only."),
            ("accept_suggested_recipe", "Accept and register a suggested recipe. Write."),
            ("reject_suggested_recipe", "Reject a suggested recipe so it is not shown again. Write."),
            ("register_recipe", "Register a new custom format recipe. Write."),
            ("update_recipe", "Update a recipe's dimensions, creative type, or scope. Write."),
            ("delete_recipe", "Delete a format recipe. Destructive write — does not affect existing creatives."),
            ("resolve", "Resolve conflicts between formats across sites. Write."),
            ("detect_conflicts", "Detect format conflicts across registered sites without resolving them. Read-only."),
        ],
    ),

    # ── gam_admin ──────────────────────────────────────────────────────────────
    _t(
        "gam_admin",
        """GAM admin orchestration — 48 operations across 7 administrative areas: Teams, Sites, Mobile Apps, Custom Fields, Labels, Publisher Provided Signals, and Users.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required — user must have Network Admin role for write operations
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns administrative entity objects specific to the sub-area (Team, Site, MobileApp, CustomField, Label, PublisherProvidedSignalsConfig, User objects).
SIDE EFFECTS: User management operations (deactivate, remove) affect access control. Label and custom field changes propagate to existing entities. Team changes affect inventory access rights.
WHEN TO USE: Use gam_admin for network configuration and governance tasks (team structure, user management, custom metadata). Use targeting for custom targeting key-values used in ad serving.""",
        [
            ("list_teams", "List all teams on the network. Read-only."),
            ("get_team", "Get a team by ID. Read-only."),
            ("create_team", "Create a new team. Write."),
            ("update_team", "Update a team's name or description. Write."),
            ("delete_team", "Delete a team. Destructive write — removes team membership associations."),
            ("add_team_members", "Add users to a team. Write."),
            ("remove_team_members", "Remove users from a team. Write."),
            ("list_sites", "List all sites on the network. Read-only."),
            ("get_site", "Get a site by ID. Read-only."),
            ("create_site", "Create a new site. Write."),
            ("update_site", "Update a site. Write."),
            ("delete_site", "Delete a site. Destructive write."),
            ("list_mobile_apps", "List mobile apps registered on the network. Read-only."),
            ("get_mobile_app", "Get a mobile app by ID. Read-only."),
            ("create_mobile_app", "Register a new mobile app. Write."),
            ("update_mobile_app", "Update a mobile app's details. Write."),
            ("list_custom_fields", "List all custom fields defined on the network. Read-only."),
            ("get_custom_field", "Get a custom field by ID. Read-only."),
            ("create_custom_field", "Create a custom field for orders, line items, or creatives. Write."),
            ("update_custom_field", "Update a custom field's name or options. Write."),
            ("deactivate_custom_field", "Deactivate a custom field. Soft delete — preserves existing values."),
            ("list_custom_field_options", "List options for a custom field of type SELECT. Read-only."),
            ("create_custom_field_option", "Add a new option to a SELECT custom field. Write."),
            ("update_custom_field_option", "Update a custom field option. Write."),
            ("deactivate_custom_field_option", "Deactivate a custom field option. Write."),
            ("list_labels", "List all labels. Read-only."),
            ("get_label", "Get a label by ID. Read-only."),
            ("create_label", "Create a new label. Write."),
            ("update_label", "Update a label. Write."),
            ("deactivate_label", "Deactivate a label. Write."),
            ("list_pps_configs", "List Publisher Provided Signals configurations. Read-only."),
            ("get_pps_config", "Get a PPS config by ID. Read-only."),
            ("create_pps_config", "Create a PPS configuration. Write."),
            ("update_pps_config", "Update a PPS configuration. Write."),
            ("delete_pps_config", "Delete a PPS configuration. Destructive write."),
            ("list_users", "List all users on the network. Read-only."),
            ("get_user", "Get a user by ID. Read-only."),
            ("get_current_user", "Get the currently authenticated user's profile. Read-only."),
            ("create_user", "Create a new user account. Write."),
            ("update_user", "Update a user's role or email. Write."),
            ("deactivate_user", "Deactivate a user account. Write — revokes network access."),
            ("perform_user_action", "Perform a lifecycle action on a user (ACTIVATE, DEACTIVATE). Write."),
            ("list_roles", "List all roles available on the network. Read-only."),
            ("list_team_memberships", "List team memberships for a user. Read-only."),
            ("get_user_record", "Get a user's full record including role and team assignments. Read-only."),
            ("get_salesperson_record", "Get salesperson metadata for a user. Read-only."),
            ("get_trafficker_record", "Get trafficker metadata for a user. Read-only."),
            ("audit_user_access", "Audit user access rights: roles, teams, and accessible inventory. Read-only."),
        ],
    ),

    # ── gam_features ───────────────────────────────────────────────────────────
    _t(
        "gam_features",
        """Inspect GAM network features — discover which beta features and capabilities are enabled.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns a list of NetworkFeature objects with featureName, enabled (boolean), and description.
WHEN TO USE: Call before using advanced GAM features to verify they are enabled on the network. Use probe_gam_features when you need to test a specific capability live.""",
        [
            ("get_gam_features", "Return the cached list of features enabled on the network."),
            ("probe_gam_features", "Live-probe the network for feature availability (slower but always current)."),
            ("refresh_gam_features", "Force-refresh the feature cache. Call after a GAM admin enables new features."),
        ],
    ),

    # ── gam_jobs ───────────────────────────────────────────────────────────────
    _t(
        "gam_jobs",
        """Poll and manage async GAM background jobs.

MODE: read-only (polling only — jobs are created by other tools)
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns Job objects with id, type, status (PENDING | RUNNING | COMPLETE | FAILED), progress (0–100), result_url or result_data, and error if failed.
WHEN TO USE: Use after starting a long-running operation (e.g., large inventory scan, bulk line item creation) that returns a job_id. Poll until status = COMPLETE or FAILED.""",
        [
            ("poll", "Poll a job's current status and progress. Returns status and progress percentage. Recommended polling interval: 5 seconds."),
            ("get", "Get a completed job's full result. Returns result_data or result_url for download."),
            ("list", "List recent jobs for the current tenant. Read-only."),
            ("cancel", "Cancel a running job. Write — interrupts the background operation."),
        ],
        extra={
            "job_id": {
                "type": "string",
                "description": "Async job identifier returned by a previous long-running operation.",
            },
        },
    ),

    # ── inventory ──────────────────────────────────────────────────────────────
    _t(
        "inventory",
        """Manage GAM ad unit inventory — tree traversal, audit, batch creation, ads.txt, and blueprint sync.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5–1 credit.
OUTPUT: get_ad_unit_tree returns a hierarchical JSON of ad units. audit_inventory returns an analysis report. create_ad_units_batch returns a list of {requested_name, created_id, status}.
SIDE EFFECTS: push_inventory_blueprint creates or updates ad units in GAM based on the stored blueprint. archive_inactive_ad_units is destructive and cannot be undone.
WHEN TO USE: Use inventory for ad unit structure management. Use targeting for custom targeting keys. Use blueprint for the canonical format/position definition that drives inventory creation.""",
        [
            ("get_ad_unit_tree", "Return the full ad unit hierarchy as a nested JSON tree. Read-only."),
            ("audit_inventory", "Analyze the inventory for structural issues: orphaned ad units, duplicate sizes, missing placements. Read-only."),
            ("create_ad_units_batch", "Create multiple ad units in one call from a specification list. Write."),
            ("generate_ads_json", "Generate an ads.json / app-ads.json file from the current inventory. Read-only."),
            ("generate_inventory_blueprint", "Generate a blueprint JSON from existing GAM inventory (reverse-engineering). Read-only."),
            ("push_inventory_blueprint", "Push the stored blueprint to GAM, creating or updating ad units. Write, 1 credit."),
            ("get_ad_units_by_ids", "Retrieve multiple ad units by ID in one call. Read-only."),
            ("find_inactive_ad_units", "Find ad units with no recent impressions. Read-only."),
            ("archive_inactive_ad_units", "Archive ad units flagged as inactive. Destructive write. Run find_inactive_ad_units first."),
            ("list_ad_unit_sizes", "List all sizes used across ad units on the network. Read-only."),
        ],
    ),

    # ── jobs ───────────────────────────────────────────────────────────────────
    _t(
        "jobs",
        """Manage OrbiAds campaign deployment jobs — distinct from GAM background jobs (use gam_jobs for those).

MODE: read + limited write
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns OrbiAds Job objects with id, campaign_id, status, created_at, and deployment log.
WHEN TO USE: Use jobs to check the status of an OrbiAds campaign deployment job. Use gam_jobs to poll GAM-native background operations.
NOT the same as gam_jobs: jobs tracks OrbiAds deployment pipelines; gam_jobs tracks GAM server-side async jobs.""",
        [
            ("get_job", "Get an OrbiAds deployment job by ID. Returns status, progress, and deployment log."),
            ("list_jobs", "List recent OrbiAds deployment jobs for the tenant. Read-only."),
            ("duplicate_job", "Duplicate a completed job configuration to re-run a similar deployment. Write."),
        ],
        extra={
            "job_id": {
                "type": "string",
                "description": "OrbiAds deployment job identifier.",
            },
        },
    ),

    # ── line_items ─────────────────────────────────────────────────────────────
    _t(
        "line_items",
        """Non-lifecycle Line Item operations — get, list, update, duplicate, verify, and create programmatic types.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns LineItem objects with id, name, type, startDateTime, endDateTime, costType, unitsBought, targeting, and deliveryIndicator.
WHEN TO USE: Use line_items for individual line item CRUD and programmatic line item creation. Use campaign for full campaign orchestration. Use line_item_lifecycle for status transitions (activate/pause/archive).
NOT the same as line_item_lifecycle: line_items handles data updates; line_item_lifecycle handles status transitions.""",
        [
            ("get", "Get a single line item by ID. Read-only."),
            ("list_by_order", "List all line items under an order. Read-only. Requires order_id."),
            ("update", "Update a line item's name, targeting, dates, or budget. Write."),
            ("update_targeting", "Update only the targeting of a line item. Write. More efficient than full update for targeting-only changes."),
            ("duplicate", "Duplicate a line item to create a copy. Write."),
            ("verify", "Verify that a line item configuration is valid before activation. Read-only."),
            ("approve", "Approve a line item for delivery. Write."),
            ("archive", "Archive a line item. Destructive write."),
            ("create_batch", "Create multiple standard line items under an order. Write."),
            ("activate_batch", "Activate multiple line items in one call. Write."),
            ("pause_batch", "Pause multiple line items in one call. Write."),
            ("create_adexchange", "Create an Ad Exchange line item. Write. Requires adExchangeEnvironment and targeting."),
            ("create_open_bidding", "Create an Open Bidding line item. Write. Requires yieldGroupIds."),
            ("create_preferred_deal", "Create a Preferred Deal line item. Write. Requires fixedCpm and buyerId."),
            ("list_private_deals", "List Private Marketplace deals associated with line items. Read-only."),
        ],
        extra={
            "line_item_id": {
                "type": "integer",
                "description": "GAM Line Item ID (required for single-entity operations).",
            },
            "order_id": {
                "type": "integer",
                "description": "GAM Order ID (required for list_by_order and create_batch).",
            },
        },
    ),

    # ── network ────────────────────────────────────────────────────────────────
    _t(
        "network",
        """GAM network management — get info, switch active network, list accessible networks, update settings.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. update_network = 0.5 credits.
OUTPUT: get_network_info returns {networkCode, displayName, currencyCode, timeZone, effectiveRootAdUnit}. list_accessible_networks returns all networks the authenticated user can access.
WHEN TO USE: Use network to discover and switch between multiple GAM networks. Call list_accessible_networks after authentication to find available networks, then switch_network to set the active one.""",
        [
            ("get_network_info", "Return metadata about the current active GAM network."),
            ("switch_network", "Set a different network as the active one for subsequent operations. Requires network_code of the target network."),
            ("list_accessible_networks", "List all GAM networks accessible to the authenticated Google account."),
            ("update_network", "Update network-level settings (display name, currency). Write, requires Network Admin role."),
        ],
    ),

    # ── orders ─────────────────────────────────────────────────────────────────
    _t(
        "orders",
        """Non-lifecycle Order operations — list, get, create, update, and manage orders.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns Order objects with id, name, status, advertiserId, agencyId, salespersonId, secondarySalespersonIds, traffickerId, customFieldValues, totalBudget, and startDateTime/endDateTime.
WHEN TO USE: Use orders for Order entity management. Use campaign for full campaign orchestration that includes Order + LineItems. Use order_lifecycle for status transitions.
NOT the same as order_lifecycle: orders handles data; order_lifecycle handles approve/archive/disapprove transitions.""",
        [
            ("list_delivering", "List orders currently in delivery. Read-only."),
            ("get", "Get a single order by ID. Read-only."),
            ("list", "List orders with optional filters (advertiser, status, date range). Read-only."),
            ("create", "Create a new order. Write. Requires advertiserId, name, and traffickerId."),
            ("archive", "Archive an order. Destructive write — stops delivery."),
            ("approve", "Approve an order for delivery. Write."),
            ("verify_setup", "Verify an order's setup (targeting, creative associations) before activation. Read-only."),
            ("update", "Update an order's name, salespersonId, secondarySalespersonIds, customFieldValues, or notes. Write."),
            ("find_or_create", "Find an existing order matching the criteria or create a new one if not found. Idempotent write."),
            ("list_users", "List users (salespeople, traffickers) associated with an order. Read-only."),
            ("list_roles", "List available order roles. Read-only."),
        ],
        extra={
            "order_id": {
                "type": "integer",
                "description": "GAM Order ID (required for single-entity operations).",
            },
        },
    ),

    # ── placements ─────────────────────────────────────────────────────────────
    _t(
        "placements",
        """Manage GAM placements — named groups of ad units used for targeting.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns Placement objects with id, name, description, targetedAdUnitIds, and status.
WHEN TO USE: Use placements to create named groupings of ad units for targeting in line items. Placements are referenced in line item targeting via the targeting tool. Use inventory for individual ad unit management.""",
        [
            ("list_placements", "List all placements on the network. Read-only."),
            ("create_placement", "Create a new placement grouping ad units. Write. Requires name and targetedAdUnitIds."),
            ("update_placement", "Update a placement's name or ad unit membership. Write."),
            ("archive_placement", "Archive a placement. Destructive write — removes from targeting options."),
        ],
    ),

    # -- yield_skill ---------------------------------------------------------------
    _t(
        "yield_skill",
        """Yield optimization group management and forecast governance.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: read = 0 credits.
OUTPUT: Results for yield groups and forecast adjustments.
WHEN TO USE: Use for managing yield groups and reading forecast adjustments.""",
        [
            ("create_yield_group", "Create a yield group."),
            ("update_yield_group", "Update a yield group."),
            ("list_forecast_adjustments", "List forecast adjustments."),
            ("list_forecast_segments", "List forecast segments."),
            ("list_yield_groups", "List yield groups."),
        ],
    ),

    # ── pql ────────────────────────────────────────────────────────────────────
    _t(
        "pql",
        """Execute PQL (Publisher Query Language) queries against GAM reporting tables.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns a ResultSet with column definitions and rows. Each row is an array of values matching the column order.
WHEN TO USE: Use pql for ad-hoc data extraction not covered by the reporting tool's structured reports.
LIMITATIONS: Not all PQL tables are available on all networks (some require beta features). The Language and Device_Category tables have known limitations. For structured delivery/inventory reports, use reporting instead.""",
        [
            ("run_query", "Execute a PQL SELECT statement. Example: SELECT Id, Name FROM Order WHERE Status = 'DELIVERING'. Returns rows up to 1000 per call."),
        ],
        extra={
            "pql_query": {
                "type": "string",
                "description": "PQL SELECT statement. Supported tables: Order, LineItem, Creative, AdUnit, Placement, Company, User, and others. Max 1000 rows returned.",
            },
        },
    ),

    # ── preview ────────────────────────────────────────────────────────────────
    _t(
        "preview",
        """Generate creative and campaign preview URLs and validate creative coverage.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns preview URLs (expire after 24h) and coverage reports listing which line items have zero or insufficient creative associations.
WHEN TO USE: Use preview before launching a campaign to verify all creatives render correctly and coverage is complete.""",
        [
            ("get_preview_urls", "Generate preview URLs for a single creative across its associated ad sizes."),
            ("get_campaign_preview_urls", "Generate preview URLs for all creatives in a campaign. Returns a per-line-item, per-creative list."),
            ("check_creative_coverage", "Check that all line items in a campaign have at least one active creative. Returns a coverage report."),
        ],
    ),

    # ── products ───────────────────────────────────────────────────────────────
    _t(
        "products",
        """Manage GAM Products and Product Packages for programmatic direct deals.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns Product objects with id, name, type, rateType, rate, targeting, and status.
WHEN TO USE: Use products to manage the GAM product catalogue for Programmatic Direct (PD) deals. Products define the inventory packages offered to buyers. For creating deals from products, use the deals tool.""",
        [
            ("create", "Create a new GAM product. Write. Requires name, productTemplateId, and rate."),
            ("list", "List all products on the network with optional filters. Read-only."),
            ("get", "Get a product by ID. Read-only."),
            ("update", "Update a product's rate, targeting, or description. Write."),
            ("archive", "Archive a product. Destructive write — removes from buyer-facing catalogue."),
            ("get_adcp", "Get the ADCP (Automated Direct Campaign Pricing) configuration for a product. Read-only."),
            ("pricing_suggestion", "Get a pricing suggestion for a product based on historical delivery data. Read-only."),
        ],
        extra={
            "product_id": {
                "type": "integer",
                "description": "GAM Product ID (required for single-entity operations).",
            },
        },
    ),

    # ── reporting ──────────────────────────────────────────────────────────────
    _t(
        "reporting",
        """Full GAM and GA4 reporting — delivery reports, custom reports, forecasting, traffic data, billing, and report management.

MODE: mixed (read + write)
  READ: all report-run, forecast, list, get, and discovery actions (majority of actions)
  WRITE: save_report_template (creates), update_report_template (mutates), duplicate_report_template (creates), delete_report_template (destructive), create_gam_report (creates in GAM), update_gam_report (mutates in GAM), delete_gam_report (destructive soft-delete — PATCH visibility=HIDDEN)
AUTH: OAuth 2.0 required
CREDITS: 0 (all actions free)
OUTPUT: Delivery/custom reports return rows of dimension+metric values. Forecasts return estimated_impressions, estimated_clicks, and confidence intervals. Template/GAM report actions return the object after mutation.
SIDE EFFECTS:
  • delete_report_template permanently removes the template from the tenant — irreversible.
  • delete_gam_report uses soft-delete (PATCH visibility=HIDDEN on the GAM REST API) — the report is hidden from the UI but not purged; there is no DELETE endpoint on GAM reports.
  • save_report_template and create_gam_report persist new entities that count against quotas.
WHEN TO USE: Use reporting for all data extraction and analysis. Use reporting_skill for high-level multi-step reporting workflows described in natural language.
  • Delivery analysis: check_delivery_status or fetch_delivery_report.
  • Custom ad-hoc reports: run_custom_report.
  • Forecasting: get_standalone_forecast or get_delivery_forecast_by_line_item. For pre-flight feasibility, pass sizes/creativeSizes, geo/geoTargeting, priority, frequencyCaps, lineItemType and cpmMicroAmount so the estimate is constrained like the planned Line Item.
  • GA4 data: run_ga_report.
  • Reusable reports: save_report_template / run_report_from_template.
LIMITATIONS: Some SOAP-era metrics (TOTAL_*, AD_SERVER_ALL_REVENUE) and dimensions (MONTH_AND_YEAR, CREATIVE_SIZE) are rejected by the REST API. Use get_report_dimensions/get_report_metrics to discover valid options.""",
        [
            ("check_delivery_status", "Check delivery status (actual vs booked) for an order or line item. Returns pacing indicator."),
            ("fetch_delivery_report", "Fetch a delivery report for a date range. Returns impressions, clicks, CTR by line item."),
            ("run_custom_report", "Run an ad-hoc report with specified dimensions and metrics. Returns result rows."),
            ("fetch_inventory_report", "Fetch an inventory forecast report for ad units. Returns available impressions."),
            ("get_report_result", "Retrieve the result of a previously run report by report_id."),
            ("export_report_csv", "Export a report result as a CSV download URL."),
            ("get_report_dimensions", "List valid dimension names for custom reports. Use to discover available breakdown options."),
            ("get_report_metrics", "List valid metric names for custom reports. Use to discover available measurements."),
            ("get_report_date_ranges", "List valid relative date range strings (LAST_7_DAYS, LAST_MONTH, etc.)."),
            ("get_standalone_forecast", "Get a constrained forecast for a prospective line item. Accepts adUnitIds, startDate, endDate, sizes/creativeSizes, geo/geoTargeting, priority, frequencyCaps, lineItemType and cpmMicroAmount."),
            ("get_delivery_forecast_by_line_item", "Get a delivery forecast for one or more existing line items."),
            ("get_prospective_delivery_forecast", "Get a prospective forecast for a hypothetical line item configuration."),
            ("get_traffic_data", "Get historical traffic data (impressions available) for targeting criteria."),
            ("list_report_templates", "List saved report templates. Read-only."),
            ("save_report_template", "Save a report configuration as a reusable template. Write."),
            ("delete_report_template", "Delete a report template. Destructive write."),
            ("duplicate_report_template", "Duplicate a report template. Write."),
            ("update_report_template", "Update a saved report template. Write."),
            ("run_report_from_template", "Run a report using a saved template. Returns report_id for async result retrieval."),
            ("list_gam_reports", "List reports saved in the GAM UI. Read-only."),
            ("get_gam_report", "Get a specific GAM report by ID. Read-only."),
            ("create_gam_report", "Create a new report in GAM. Write."),
            ("update_gam_report", "Update a GAM report configuration. Write."),
            ("delete_gam_report", "Delete a GAM report. Destructive write — uses soft-delete (PATCH visibility=HIDDEN)."),
            ("run_gam_report", "Run a GAM report and return result rows."),
            ("run_ga_report", "Run a GA4 report for connected Google Analytics data."),
            ("get_ga_dimensions", "List valid GA4 dimension names."),
            ("get_ga_metrics", "List valid GA4 metric names."),
            ("check_underdelivery_alerts", "Check for active underdelivery alerts across all line items. Returns affected line items with severity."),
            ("check_budget_alerts", "Check for budget pacing alerts. Returns line items at risk of overspending."),
            ("generate_billing_report", "Generate a billing summary report for a date range. Returns revenue by advertiser and line item."),
        ],
    ),

    # ── settings ───────────────────────────────────────────────────────────────
    _t(
        "settings",
        """Manage OrbiAds tenant settings — naming conventions, delivery defaults, and configuration presets.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0 credits (configuration only).
OUTPUT: Returns settings objects with key-value pairs for naming patterns, delivery parameters, and preset configurations.
WHEN TO USE: Use settings to configure tenant-level defaults that apply across all campaigns. For network-level GAM settings, use the network tool.""",
        [
            ("list_presets", "List all saved configuration presets. Read-only."),
            ("create_preset", "Save current settings as a named preset. Write."),
            ("delete_preset", "Delete a preset. Destructive write."),
            ("get_tenant_settings", "Get all tenant-level settings. Read-only."),
            ("update_tenant_settings", "Update tenant settings. Write."),
            ("get_naming_conventions", "Get configured naming convention patterns for orders, line items, and creatives."),
            ("update_naming_conventions", "Update naming convention patterns. Write."),
            ("get_delivery_defaults", "Get default delivery settings (pacing, priority, roadblocking) applied to new line items."),
            ("update_delivery_defaults", "Update delivery defaults. Write."),
        ],
    ),

    # ── targeting ──────────────────────────────────────────────────────────────
    _t(
        "targeting",
        """Manage GAM custom targeting keys, values, and ad unit targeting configuration.

MODE: mixed (read + write)
AUTH: OAuth 2.0 required
CREDITS: Reads = 0. Writes = 0.5 credits.
OUTPUT: Returns CustomTargetingKey objects with id, name, type (PREDEFINED/FREEFORM), and associated values. get_available_countries/languages/devices return canonical lists for geographic/device targeting.
WHEN TO USE: Use targeting to manage the custom targeting vocabulary (keys and values) used in line item targeting. Use line_items to apply targeting to line items. Use inventory for ad unit structure.
NOTE: get_inventory_forecast takes targeting criteria and returns estimated available impressions — useful before creating a line item to verify reach.""",
        [
            ("list_ad_units", "List all ad units with their sizes and status. Read-only. For full hierarchy, use inventory get_ad_unit_tree."),
            ("validate_fluid", "Validate a fluid targeting expression for syntax and reference errors. Read-only."),
            ("list_custom_targeting_keys", "List all custom targeting keys on the network. Read-only."),
            ("get_inventory_forecast", "Get estimated available impressions for a targeting specification. Read-only. Use before creating a line item to validate reach."),
            ("create_custom_targeting_key", "Create a new custom targeting key. Write."),
            ("create_custom_targeting_values", "Create one or more values for an existing key. Write."),
            ("update_custom_targeting_key", "Update a key's name or type. Write."),
            ("delete_custom_targeting_key", "Delete a targeting key and all its values. Destructive write."),
            ("update_custom_targeting_value", "Update a targeting value's name or display name. Write."),
            ("perform_custom_targeting_value_action", "Activate or deactivate a targeting value. Write."),
            ("search_ad_units", "Search ad units by name or path. Read-only."),
            ("update_ad_unit", "Update an ad unit's name, description, or size. Write."),
            ("archive_ad_unit", "Archive an ad unit. Destructive write. Run inventory find_inactive_ad_units first."),
            ("get_custom_targeting_values", "Get all values for a specific targeting key. Read-only."),
            ("search_custom_targeting", "Search targeting keys and values by text. Read-only."),
            ("get_available_countries", "Return the canonical list of countries for geographic targeting (ISO 3166-1 alpha-2 codes)."),
            ("get_available_languages", "Return the canonical list of language codes for language targeting."),
            ("get_device_categories", "Return the canonical list of device categories (DESKTOP, MOBILE, TABLET, CONNECTED_TV)."),
        ],
    ),

    # ── tenant_catalog ─────────────────────────────────────────────────────────
    _t(
        "tenant_catalog",
        """Scan and cache the tenant's GAM inventory catalog for fast downstream operations.

MODE: read (scan triggers a background read job)
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: get_active_catalog returns a JSON catalog of ad units, placements, and key-values. get_scan_status returns {status: IDLE|RUNNING|COMPLETE, progress, last_updated}.
WHEN TO USE: Run scan_network once after connecting a new GAM network, then call refresh periodically (daily) to keep the catalog current. Other tools use the catalog for fast lookups without hitting the GAM API on every call.""",
        [
            ("scan_network", "Trigger a background scan of the GAM network to build the inventory catalog. Returns a scan job ID. Poll with get_scan_status."),
            ("get_scan_status", "Get the status of the most recent catalog scan. Returns status, progress, and last_updated timestamp."),
            ("get_active_catalog", "Return the current cached inventory catalog (ad units, placements, targeting keys). May be stale if not refreshed recently."),
            ("refresh", "Trigger an incremental catalog refresh to pick up recent GAM changes without a full rescan."),
        ],
    ),

    # ── Standalone tools ───────────────────────────────────────────────────────
    _standalone(
        "get_my_tenant_id",
        """Return the OrbiAds tenant ID for the authenticated session.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns {tenant_id: string}
WHEN TO USE: Call this first in any workflow to resolve your tenant_id. The tenant_id is required by some internal operations and for multi-tenant debugging.""",
        {},
    ),

    _standalone(
        "initiate_gam_auth",
        """Start the OAuth 2.0 authorization flow to link a GAM network to the OrbiAds tenant.

MODE: write (creates a pending auth session)
AUTH: Partially authenticated (OrbiAds session required, GAM auth not yet established)
CREDITS: 0 (free)
OUTPUT: Returns {auth_url: string, session_id: string}. Open auth_url in a browser and authorize. Then poll poll_auth_status with the session_id.
WHEN TO USE: Call when a GAM network has not yet been authorized (check_credentials returns false). Do not call if credentials are already valid.""",
        {
            "network_code": {
                "type": "integer",
                "description": "The GAM network code to authorize. Obtain from the GAM UI or list_accessible_networks after a Google sign-in.",
            },
        },
        required=["network_code"],
    ),

    _standalone(
        "poll_auth_status",
        """Poll the OAuth authorization status after initiating a GAM auth flow.

MODE: read-only
AUTH: OrbiAds session required
CREDITS: 0 (free)
OUTPUT: Returns {status: 'pending'|'authorized'|'failed', error?: string}
WHEN TO USE: Call repeatedly (every 2–5 seconds) after initiate_gam_auth until status = 'authorized' or 'failed'.""",
        {
            "session_id": {
                "type": "string",
                "description": "Auth session ID returned by initiate_gam_auth.",
            },
        },
        required=["session_id"],
    ),

    _standalone(
        "select_gam_network",
        """Set the active GAM network for the current session when the tenant has multiple linked networks.

MODE: write (session state change)
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns {network_code: int, display_name: string, currency: string}
WHEN TO USE: Call after authentication when the tenant has more than one GAM network linked. All subsequent tool calls will use this network_code unless overridden per-call.""",
        {
            "network_code": {
                "type": "integer",
                "description": "GAM network code to set as active.",
            },
        },
        required=["network_code"],
    ),

    _standalone(
        "line_item_lifecycle",
        """Perform lifecycle status transitions on a GAM Line Item (activate, pause, archive, resume).

MODE: write
AUTH: OAuth 2.0 required
CREDITS: 0.5 credits. Confirmation token required for archive.
OUTPUT: Returns {line_item_id, previous_status, new_status}
WHEN TO USE: Use this for status transitions only. For data updates (targeting, budget, dates), use the line_items update action.
DESTRUCTIVE: archive cannot be undone from the API.""",
        {
            "line_item_id": {"type": "integer", "description": "GAM Line Item ID."},
            "lifecycle_action": {
                "type": "string",
                "enum": ["activate", "pause", "archive", "resume"],
                "description": "activate: start delivery. pause: stop delivery temporarily. resume: restart a paused line item. archive: permanently remove from serving (destructive).",
            },
            "network_code": {"type": "integer", "description": "GAM network code."},
            "confirmation_token": {
                "type": "string",
                "description": "Required for lifecycle_action=archive. Obtain from a prior estimate_cost call.",
            },
        },
        required=["line_item_id", "lifecycle_action", "network_code"],
    ),

    _standalone(
        "order_lifecycle",
        """Perform lifecycle status transitions on a GAM Order (approve, archive, disapprove).

MODE: write
AUTH: OAuth 2.0 required
CREDITS: 0.5 credits. Confirmation token required for archive.
OUTPUT: Returns {order_id, previous_status, new_status}
WHEN TO USE: Use this for order status transitions. For data updates, use the orders update action.
DESTRUCTIVE: archive stops all line item delivery under the order.""",
        {
            "order_id": {"type": "integer", "description": "GAM Order ID."},
            "lifecycle_action": {
                "type": "string",
                "enum": ["approve", "archive", "disapprove"],
                "description": "approve: allow delivery. disapprove: block delivery. archive: permanently deactivate (destructive).",
            },
            "network_code": {"type": "integer", "description": "GAM network code."},
            "confirmation_token": {
                "type": "string",
                "description": "Required for lifecycle_action=archive.",
            },
        },
        required=["order_id", "lifecycle_action", "network_code"],
    ),

    _standalone(
        "reporting_skill",
        """High-level reporting orchestration — describe a reporting goal in natural language and get results.

MODE: read-only (orchestrates multiple reporting tool calls internally)
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns a formatted report with dimensions, metrics, and data rows. May include charts or summary analysis.
WHEN TO USE: Use reporting_skill when the reporting goal is clear but the exact dimension/metric combination is unknown. It internally calls get_report_dimensions, get_report_metrics, and run_custom_report.
  Example: "weekly revenue by ad unit for last month" → selects AD_UNIT_NAME + TOTAL_LINE_ITEM_LEVEL_REVENUE automatically.
NOT the same as reporting: reporting gives direct access to individual report operations; reporting_skill is a higher-level orchestrator.""",
        {
            "network_code": {"type": "integer", "description": "GAM network code."},
            "goal": {
                "type": "string",
                "description": "Plain-language description of the reporting goal. Example: 'top 10 advertisers by revenue last quarter' or 'daily CTR for line items in order 12345'.",
            },
        },
        required=["network_code", "goal"],
    ),

    _standalone(
        "check_credentials",
        """Verify that the GAM OAuth credentials for a network are still valid and have required scopes.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns {valid: boolean, scopes: string[], expires_at: datetime, error?: string}
WHEN TO USE: Call at the start of a session to verify credentials before running operations. If valid=false, call initiate_gam_auth to re-authorize.""",
        {
            "network_code": {"type": "integer", "description": "GAM network code to check."},
        },
        required=["network_code"],
    ),

    _standalone(
        "disconnect_gam",
        """Revoke and permanently remove the GAM OAuth credentials for a network from the tenant.

MODE: write (destructive)
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns {network_code, disconnected_at}
SIDE EFFECTS: All OrbiAds operations requiring this network will fail after disconnection. The network must be re-authorized via initiate_gam_auth to restore access.
WHEN TO USE: Use when intentionally removing a network from the tenant (e.g., end of contract). Confirmation token required — this action is irreversible via API.""",
        {
            "network_code": {"type": "integer", "description": "GAM network code to disconnect."},
            "confirmation_token": {
                "type": "string",
                "description": "Write-confirmation token. Required — disconnection is irreversible.",
            },
        },
        required=["network_code", "confirmation_token"],
    ),

    _standalone(
        "gam_audit",
        """Run a full GAM network compliance audit combining hygiene, diagnostics, and a standards baseline in one call.

MODE: read-only
AUTH: OAuth 2.0 required
CREDITS: 0 (free)
OUTPUT: Returns a comprehensive markdown report with: (1) hygiene findings, (2) operational diagnostics, (3) standards baseline results per framework control. Overall pass/fail verdict included.
WHEN TO USE: Use gam_audit for a complete one-shot network audit. For individual audit components, use audit_skill with the specific action.
NOT the same as audit: audit queries change history; gam_audit analyzes current state.
NOT the same as audit_skill: gam_audit is a convenience wrapper that calls hygiene_check + ops_diagnostic + standards_baseline in sequence.""",
        {
            "network_code": {"type": "integer", "description": "GAM network code."},
            "framework": {
                "type": "string",
                "enum": ["orbiads_baseline", "iso27001_adops", "iab_anti_tampering", "nist_csf"],
                "description": "Compliance framework for the standards baseline section. Defaults to orbiads_baseline if omitted.",
            },
        },
        required=["network_code"],
    ),
]


# ── Prompts catalogue ─────────────────────────────────────────────────────────

PROMPTS: list[dict] = [
    {
        "name": "adops_audit",
        "description": (
            "Run a structured GAM network audit. Guides through hygiene check, "
            "operational diagnostics, and compliance baseline in sequence. "
            "Use when you want a comprehensive health report on a GAM network."
        ),
        "arguments": [
            {
                "name": "network_code",
                "description": "GAM network code (integer). Obtain via list_accessible_networks if unknown.",
                "required": True,
            },
            {
                "name": "framework",
                "description": (
                    "Compliance framework for the standards baseline. "
                    "One of: orbiads_baseline | iso27001_adops | iab_anti_tampering | nist_csf. "
                    "Defaults to orbiads_baseline."
                ),
                "required": False,
            },
        ],
    },
    {
        "name": "adops_campaign",
        "description": (
            "Step-by-step campaign creation workflow: verify credentials → select blueprint → "
            "preview credit cost → confirm → deploy. Includes rollback instructions if deployment fails. "
            "Use when launching a new ad campaign in GAM."
        ),
        "arguments": [
            {
                "name": "network_code",
                "description": "GAM network code (integer).",
                "required": True,
            },
            {
                "name": "campaign_name",
                "description": "Advertiser-facing campaign name. Will be used as the GAM Order name.",
                "required": True,
            },
            {
                "name": "advertiser_id",
                "description": "GAM Advertiser ID. Use advertisers list_advertisers if unknown.",
                "required": False,
            },
        ],
    },
    {
        "name": "adops_report",
        "description": (
            "Build and run a GAM performance report. Guides through dimension/metric selection, "
            "date range, and optional template save. Returns formatted data rows. "
            "Use when you need delivery, revenue, or inventory data from GAM."
        ),
        "arguments": [
            {
                "name": "network_code",
                "description": "GAM network code (integer).",
                "required": True,
            },
            {
                "name": "goal",
                "description": (
                    "Plain-language reporting goal. Examples: "
                    "'top 10 advertisers by revenue last month', "
                    "'daily CTR for order 12345 last 7 days', "
                    "'inventory availability by ad unit this week'."
                ),
                "required": True,
            },
        ],
    },
    {
        "name": "adops_onboarding",
        "description": (
            "Onboard a new GAM network: get tenant ID → start OAuth flow → "
            "poll for authorization → scan inventory catalog → verify credentials. "
            "Use when connecting OrbiAds to a GAM network for the first time."
        ),
        "arguments": [
            {
                "name": "network_code",
                "description": "GAM network code to connect. Found in GAM Admin > Networks.",
                "required": True,
            },
        ],
    },
    {
        "name": "adops_line_item_troubleshoot",
        "description": (
            "Diagnose and fix a line item delivery problem: check delivery status → "
            "run ops_diagnostic → inspect targeting conflicts → check creative associations → "
            "suggest remediations. Use when a line item is underdelivering or not serving."
        ),
        "arguments": [
            {
                "name": "network_code",
                "description": "GAM network code (integer).",
                "required": True,
            },
            {
                "name": "line_item_id",
                "description": "GAM Line Item ID to diagnose.",
                "required": True,
            },
        ],
    },
]


def _get_prompt_messages(name: str, args: dict) -> list[dict]:
    """Return the message sequence for a named prompt."""
    nc = args.get("network_code", "<network_code>")
    if name == "adops_audit":
        fw = args.get("framework", "orbiads_baseline")
        return [{"role": "user", "content": {"type": "text", "text": (
            f"Run a full GAM network audit on network {nc}.\n\n"
            f"Step 1 — Hygiene check:\n"
            f"  Call audit_skill with action=hygiene_check and network_code={nc}.\n\n"
            f"Step 2 — Operational diagnostics:\n"
            f"  Call audit_skill with action=ops_diagnostic and network_code={nc}.\n\n"
            f"Step 3 — Standards baseline ({fw}):\n"
            f"  Call audit_skill with action=standards_baseline, network_code={nc}, framework={fw}.\n\n"
            "Summarise findings by severity (CRITICAL → WARNING → INFO). "
            "List top 3 recommended remediations."
        )}}]
    if name == "adops_campaign":
        cname = args.get("campaign_name", "<campaign_name>")
        return [{"role": "user", "content": {"type": "text", "text": (
            f"Create a new GAM campaign on network {nc}.\n\n"
            f"Step 1 — Verify credentials:\n"
            f"  Call check_credentials with network_code={nc}. If invalid, call initiate_gam_auth.\n\n"
            f"Step 2 — Fetch active blueprint:\n"
            f"  Call blueprint with action=get_active_blueprint and network_code={nc}.\n\n"
            f"Step 3 — Estimate cost:\n"
            f"  Call audit_skill with action=estimate_cost, operation_name=deploy_campaign, "
            f"network_code={nc}.\n\n"
            f"Step 4 — Deploy (after user confirms):\n"
            f"  Call campaigns with action=deploy, network_code={nc}, campaign_name='{cname}'. "
            f"Include the confirmation_token from step 3.\n\n"
            "If deployment fails, report the error code and suggest remediation."
        )}}]
    if name == "adops_report":
        goal = args.get("goal", "<goal>")
        return [{"role": "user", "content": {"type": "text", "text": (
            f"Build and run a GAM report on network {nc}.\n\n"
            f"Goal: {goal}\n\n"
            f"Step 1 — Discover available dimensions/metrics:\n"
            f"  Call reporting with action=get_report_dimensions, network_code={nc}.\n"
            f"  Call reporting with action=get_report_metrics, network_code={nc}.\n\n"
            f"Step 2 — Select the best dimensions and metrics for the goal above.\n\n"
            f"Step 3 — Run the report:\n"
            f"  Call reporting_skill with network_code={nc}, goal='{goal}'.\n\n"
            "Format the result as a markdown table. Highlight the top 5 rows by the primary metric."
        )}}]
    if name == "adops_onboarding":
        return [{"role": "user", "content": {"type": "text", "text": (
            f"Onboard GAM network {nc} to OrbiAds.\n\n"
            "Step 1 — Get tenant ID:\n"
            "  Call get_my_tenant_id.\n\n"
            f"Step 2 — Start OAuth flow:\n"
            f"  Call initiate_gam_auth with network_code={nc}. "
            "Open the returned auth_url in a browser and authorize.\n\n"
            "Step 3 — Poll for completion:\n"
            "  Call poll_auth_status every 3 seconds until status='authorized'.\n\n"
            f"Step 4 — Scan inventory catalog:\n"
            f"  Call tenant_catalog with action=scan_network, network_code={nc}. "
            "Poll get_scan_status until COMPLETE.\n\n"
            f"Step 5 — Verify:\n"
            f"  Call check_credentials with network_code={nc}. Report valid=true to confirm success."
        )}}]
    if name == "adops_line_item_troubleshoot":
        li = args.get("line_item_id", "<line_item_id>")
        return [{"role": "user", "content": {"type": "text", "text": (
            f"Troubleshoot delivery issue for line item {li} on network {nc}.\n\n"
            f"Step 1 — Check delivery status:\n"
            f"  Call reporting with action=check_delivery_status, network_code={nc}, "
            f"line_item_id={li}.\n\n"
            f"Step 2 — Run ops diagnostic:\n"
            f"  Call audit_skill with action=ops_diagnostic, network_code={nc}.\n\n"
            f"Step 3 — Inspect the line item:\n"
            f"  Call line_items with action=get, network_code={nc}, line_item_id={li}.\n\n"
            f"Step 4 — Check creative associations:\n"
            f"  Call creatives with action=list_by_line_item, network_code={nc}, line_item_id={li}.\n\n"
            "Based on findings, explain the root cause and list 3 concrete remediation steps."
        )}}]
    return [{"role": "user", "content": {"type": "text", "text": f"Run the {name} workflow."}}]


# ── Resources catalogue ───────────────────────────────────────────────────────

RESOURCES: list[dict] = [
    {
        "uri": "orbiads://docs/quickstart",
        "name": "OrbiAds Quickstart Guide",
        "description": (
            "Step-by-step guide to connect OrbiAds to a GAM network via OAuth 2.0 "
            "and run the first tool call. Covers authentication, network selection, "
            "and credit usage basics."
        ),
        "mimeType": "text/markdown",
    },
    {
        "uri": "orbiads://docs/credit-costs",
        "name": "Credit Cost Reference",
        "description": (
            "Complete table of OrbiAds credit costs per operation. "
            "Read operations cost 0 credits. Write operations cost 0.5–2 credits "
            "depending on complexity. Campaign deploy costs 2 credits."
        ),
        "mimeType": "text/markdown",
    },
    {
        "uri": "orbiads://docs/compliance-frameworks",
        "name": "Compliance Frameworks Reference",
        "description": (
            "Documentation for the four audit compliance frameworks supported by audit_skill: "
            "orbiads_baseline (internal best practices), iso27001_adops (ISO 27001 ad-ops subset), "
            "iab_anti_tampering (IAB anti-fraud controls), nist_csf (NIST Cybersecurity Framework subset)."
        ),
        "mimeType": "text/markdown",
    },
    {
        "uri": "orbiads://tools/catalogue",
        "name": "Tool Catalogue Summary",
        "description": (
            "Summary of all 39 OrbiAds MCP tools grouped by domain: "
            "campaign management, inventory, targeting, reporting, audit, billing, and auth. "
            "Includes read/write classification and credit cost per tool."
        ),
        "mimeType": "text/markdown",
    },
]


_RESOURCE_CONTENT: dict[str, str] = {
    "orbiads://docs/quickstart": """# OrbiAds Quickstart

## Prerequisites
- An active OrbiAds account (sign up at https://orbiads.com)
- A Google Ad Manager network with Admin or API access

## Step 1 — Get your tenant ID
```
get_my_tenant_id()
```

## Step 2 — Start OAuth authorization
```
initiate_gam_auth(network_code=<YOUR_NETWORK_CODE>)
```
Open the returned `auth_url` in a browser and authorize with the Google account that has GAM access.

## Step 3 — Poll for completion
```
poll_auth_status(session_id=<SESSION_ID>)
```
Repeat every 3 seconds until `status = "authorized"`.

## Step 4 — Scan your inventory
```
tenant_catalog(action="scan_network", network_code=<YOUR_NETWORK_CODE>)
```
Poll `get_scan_status` until `COMPLETE`. This builds a local cache for fast lookups.

## Step 5 — Verify and start using OrbiAds
```
check_credentials(network_code=<YOUR_NETWORK_CODE>)
```
All tools are now available. Read operations are free; write operations cost credits.
""",

    "orbiads://docs/credit-costs": """# OrbiAds Credit Cost Reference

## Free operations (0 credits)
All read operations, list operations, forecast queries, audit reports,
credential checks, tenant catalog scans, and configuration reads.

## Write operations

| Operation | Credits | Notes |
|-----------|---------|-------|
| Campaign deploy | 2.0 | Requires confirmation_token |
| Line item create | 0.5 | Requires confirmation_token |
| Line item update | 0.5 | |
| Line item lifecycle (archive) | 0.5 | Irreversible |
| Order lifecycle (archive) | 0.5 | Irreversible |
| Creative create | 0.5 | |
| Audience segment create | 0.5 | |
| Custom targeting key create | 0.5 | |
| Custom targeting values create | 0.5 | |
| Ad unit update/archive | 0.5 | Archive is irreversible |
| Placement create/update | 0.5 | |
| disconnect_gam | 0 | Irreversible — requires confirmation_token |

## Confirmation tokens
Write operations that can cause irreversible changes require a `confirmation_token`.
Call `audit_skill(action="estimate_cost")` to preview cost and receive the token.
Tokens expire after 5 minutes.
""",

    "orbiads://docs/compliance-frameworks": """# OrbiAds Compliance Frameworks

Use `audit_skill(action="standards_baseline", framework=<NAME>)` to evaluate your GAM network.

## orbiads_baseline
OrbiAds internal best practices for GAM networks. Covers:
- Naming convention consistency (orders, line items, creatives)
- Creative association completeness
- Orphaned entity detection
- Budget pacing configuration
- Targeting overlap analysis

## iso27001_adops
ISO 27001 controls adapted for ad operations. Covers:
- Access control (GAM user roles and permissions)
- Data classification (audience segment handling)
- Change management (audit log completeness)
- Incident response (delivery alert coverage)

## iab_anti_tampering
IAB Tech Lab anti-fraud and anti-tampering controls. Covers:
- Creative wrapper integrity
- Viewability measurement tag presence
- Brand safety targeting configuration
- Invalid traffic mitigation settings

## nist_csf
NIST Cybersecurity Framework subset for ad tech. Covers:
- Identify: asset inventory completeness (ad units, placements, creatives)
- Protect: permission boundaries and credential hygiene
- Detect: audit log and alert coverage
- Respond: incident workflow readiness
""",

    "orbiads://tools/catalogue": """# OrbiAds Tool Catalogue

39 tools across 29 parent tools and 10 standalone tools.

## Authentication & Setup (read/write, 0 credits)
- `get_my_tenant_id` — resolve authenticated tenant ID
- `initiate_gam_auth` — start OAuth 2.0 GAM authorization flow
- `poll_auth_status` — poll OAuth completion status
- `select_gam_network` — set active network for session
- `check_credentials` — verify GAM credentials validity
- `disconnect_gam` — revoke GAM credentials (irreversible, requires token)

## Campaign Management (write, 2 credits for deploy)
- `campaigns` — full campaign lifecycle: deploy, list, get, pause, resume, archive
- `order_lifecycle` — order status transitions: approve, disapprove, archive
- `line_item_lifecycle` — line item status transitions: activate, pause, resume, archive

## Inventory & Targeting (read/write, 0–0.5 credits)
- `inventory` — ad units, placements, size mappings: list, get, create, update, archive
- `targeting` — custom targeting keys/values, ad unit targeting, inventory forecast
- `audiences` — first-party audience segments: list, get, create, update, activate
- `placements` — placement management: list, get, create, update, archive
- `tenant_catalog` — inventory catalog: scan, refresh, get_active_catalog

## Line Items & Orders (read/write, 0–0.5 credits)
- `line_items` — full line item CRUD + lifecycle
- `orders` — order CRUD

## Creatives (read/write, 0–0.5 credits)
- `creatives` — creative lifecycle: get, update, archive, duplicate
- `creative_assets` — upload and manage creative assets (images, HTML5)
- `creative_qa` — validate creatives before association

## Reporting (read-only, 0 credits)
- `reporting` — 25+ operations: custom reports, GAM reports, GA4 reports, forecasts, alerts
- `reporting_skill` — natural-language reporting orchestrator

## Audit & Compliance (read-only, 0 credits)
- `audit` — query GAM change log by entity
- `audit_skill` — proactive audit: hygiene_check, ops_diagnostic, standards_baseline, wrapper_coverage
- `gam_audit` — one-shot full network audit (convenience wrapper)

## Network Admin (read/write)
- `network` — network settings, timezone, currency
- `gam_admin` — user management, team configuration, role assignments
- `settings` — OrbiAds tenant settings, naming conventions, delivery defaults

## Blueprints & Formats (read/write, 0 credits)
- `blueprint` — inventory blueprint: formats, positions, key-values, brand settings
- `formats` — Custom Format Registry: creative format recipes

## Products & Pricing (read/write, 0–0.5 credits)
- `products` — Product Catalog: list, get, create, update, archive
- `pricing` — Rate Card management: get, update rates

## Deals (read/write, 0–0.5 credits)
- `deals` — programmatic deals: PG, PD, PA deal management
""",
}


# ── MCP JSON-RPC over stdio ────────────────────────────────────────────────────
# Protocol: newline-delimited JSON (one message per line, no Content-Length)
# Ref: https://spec.modelcontextprotocol.io/specification/basic/transports/#stdio

def _read_message() -> dict | None:
    """Read one JSON-RPC message from stdin (newline-delimited)."""
    line = sys.stdin.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    return json.loads(line)


def _write_message(obj: dict) -> None:
    """Write one JSON-RPC message to stdout (newline-delimited)."""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _handle(req: dict) -> dict | None:
    method = req.get("method", "")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {"listChanged": False},
                    "prompts": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                },
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": (
                    "OrbiAds MCP — Google Ad Manager automation for publishers and agencies. "
                    "Authenticate at https://orbiads.com to link your GAM network via OAuth 2.0. "
                    "Start with get_my_tenant_id, then initiate_gam_auth to connect your network. "
                    "Use prompts (adops_audit, adops_campaign, adops_report, adops_onboarding, "
                    "adops_line_item_troubleshoot) for guided multi-step workflows. "
                    "Use resources for credit cost reference, compliance framework docs, and tool catalogue."
                ),
            },
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        }

    if method == "tools/call":
        params = req.get("params", {}) or {}
        if params.get("name") == "server_info":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(SERVER_INFO)}],
                    "structuredContent": SERVER_INFO,
                    "isError": False,
                },
            }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": AUTH_MSG}],
                "isError": False,
            },
        }

    if method == "prompts/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"prompts": PROMPTS},
        }

    if method == "prompts/get":
        params = req.get("params", {})
        name = params.get("name", "")
        args = params.get("arguments", {}) or {}
        prompt = next((p for p in PROMPTS if p["name"] == name), None)
        if prompt is None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Prompt not found: {name}"},
            }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "description": prompt["description"],
                "messages": _get_prompt_messages(name, args),
            },
        }

    if method == "resources/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"resources": RESOURCES},
        }

    if method == "resources/read":
        params = req.get("params", {})
        uri = params.get("uri", "")
        content = _RESOURCE_CONTENT.get(uri)
        if content is None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": f"Resource not found: {uri}"},
            }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "contents": [{"uri": uri, "mimeType": "text/markdown", "text": content}]
            },
        }

    if method == "ping":
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}

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
