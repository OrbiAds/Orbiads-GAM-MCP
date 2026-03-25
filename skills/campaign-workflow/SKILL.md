---
description: "Full campaign setup in Google Ad Manager — from advertiser to live delivery. Guides the LLM through the correct entity creation order, naming conventions, and QA checks. Use when the user wants to create, traffic, or deploy a complete campaign."
---

# OrbiAds — Campaign Workflow (Master)

Orchestrate a complete GAM campaign from scratch to live delivery. This skill chains sub-skills in the correct order, enforces GAM best practices, and ensures nothing is skipped.

## GAM Entity Hierarchy

Every campaign in Google Ad Manager follows this strict hierarchy. Each entity depends on its parent existing first.

```
Network
  └── Company (Advertiser)
        └── Order
              └── Line Item
                    ├── Inventory Targeting (ad units or placements)
                    ├── Audience Targeting (geo, device, key-values)
                    ├── Creative Placeholders (expected sizes)
                    └── Creative Assignments (LICAs)
                          └── Creative (image, native, video...)
```

**Rule: you cannot skip levels.** A Line Item requires an Order. An Order requires an Advertiser. A Creative Assignment requires both a Line Item and a Creative with matching sizes.

## User Configuration

The user may have configured naming conventions, delivery defaults, campaign presets, and tenant settings. **Always read these before creating any entity.** The configuration is tenant-level and applies to all campaigns.

### Naming Conventions (MCP: `get_naming_conventions`)

Templates with macros that control how entities are named:
- `orderTemplate`: e.g. `{YYYY}{MM}-{advertiser}-{campaign}`
- `lineItemTemplate`: e.g. `{order}-{format}-{placement}`
- `creativeTemplate`: e.g. `{advertiser}-{format}-{size}`
- `nativeStyleTemplate`: e.g. `{advertiser}-NS-{format}`
- `reportNameTemplate`: e.g. `{report_type}-{YYYY}{MM}{DD}-{date_range}`

Available macros: `{YYYY}`, `{MM}`, `{DD}`, `{advertiser}`, `{campaign}`, `{order}`, `{type}`, `{format}`, `{size}`, `{placement}`, `{name}`, `{start_YYYY}`, `{start_MM}`, `{start_DD}`, `{end_YYYY}`, `{end_MM}`, `{end_DD}`

When a template is `null`, GAM auto-generates the name.

### Delivery Defaults (MCP: `get_delivery_defaults`)

Tenant-level defaults applied when creating line items:
- `lineItemType`, `deliveryRateType`, `creativeRotationType`
- `costType`, `currencyCode`, `microAmount` (CPM in micros, 1000000 = 1.00)
- `priority`, `frequencyCapImpressions`, `frequencyCapPeriod`
- `roadblockingType`, `timeZoneId`
- `startDateTimeType` (IMMEDIATELY or ONE_HOUR_FROM_NOW)
- `unlimitedEndDateTime` (boolean)

### Campaign Presets (MCP: `list_presets`)

Pre-configured ad unit + targeting combos:
- `__builtin_homepage` — Pack Homepage
- `__builtin_ros` — Pack Run of Site
- `__builtin_interstitiel` — Pack Interstitiel
- Plus custom user presets with advertiserId, orderId, adUnitIds, keyValues

### Tenant Settings (MCP: `get_tenant_settings`)

- `autoArchivalEnabled` + `archivalDelayDays`
- `ga4PropertyId` (for GA4 reports)
- `previewPages` (for in-context preview URLs)

### Fallback Naming Conventions

If `get_naming_conventions` returns null templates (user has not configured naming), use these defaults:

| Entity | Default Pattern | Example |
|--------|----------------|---------|
| **Advertiser** | `{BrandName}` | `Renault` |
| **Order** | `{BrandName} — {Campaign} — {Month YYYY}` | `Renault — Spring Launch — Apr 2026` |
| **Line Item** | `{BrandName} — {Format} — {Targeting} — {Type}` | `Renault — MPU 300x250 — FR Desktop — Standard` |
| **Creative** | `{BrandName} — {Format} — {Version}` | `Renault — MPU 300x250 — v1` |
| **Placement** | `{SiteName} — {Section} — {Position}` | `LeMonde — Homepage — Leaderboard` |

**Rules:**
- Use `—` (em dash) as separator, not `-` (hyphen)
- Keep names unique across the network (GAM enforces this for Orders)
- Include the size in Line Item and Creative names for quick identification
- Add version numbers to creatives when A/B testing

## Workflow Steps

### Phase 0 — Bootstrap & Configuration

**Pre-condition:** Active network with confirmed `tenantId` and `networkCode`.

If not confirmed, run `/orbiads:bootstrap` first.

**Read tenant configuration** — call these MCP tools before any entity creation:

1. `get_naming_conventions` — understand how the user wants entities named
2. `get_delivery_defaults` — understand the user's default line item settings (type, CPM, pacing, etc.)
3. `list_presets` — check if pre-configured campaign presets exist (may skip manual inventory discovery)
4. `get_tenant_settings` — read archival settings, GA4 property, and preview pages

Store the results for use in subsequent phases. If any call fails, proceed with the fallback defaults documented above.

### Phase 1 — Inventory & Targeting

**Goal:** Identify where the ads will serve and what targeting to apply.

**Check presets first.** If `list_presets` returned presets that match the campaign brief (e.g., user wants a homepage takeover and `__builtin_homepage` exists), use the preset's `adUnitIds` and `keyValues` directly. This skips manual ad unit discovery.

If no preset matches, proceed with manual discovery:

1. **Discover ad units** — Browse the inventory to find relevant ad units by name, section, or size.
   - MCP: uses `list_ad_units`, `search_ad_units`, `get_ad_unit_tree`
   - CLI: `orbiads inventory ad-units --json` or `--search "<name>"`

2. **Check placements** — See if ad units are already grouped into placements.
   - MCP: uses `list_placements`
   - CLI: `orbiads inventory placements --json`

3. **Review targeting keys** — List custom key-values available for audience targeting.
   - MCP: uses `list_custom_targeting_keys`, `get_custom_targeting_values`
   - CLI: `orbiads inventory keys --json`

4. **Validate Native/Fluid** (if native campaign) — Check if selected ad units support Native format.
   - MCP: uses `validate_fluid`

**Output:** List of `adUnitIds`, available sizes, targeting keys. Pass to Phase 2.

### Phase 2 — Availability Forecast

**Goal:** Verify enough inventory exists before committing to a campaign.

1. **Run forecast** with the selected ad units, date range, and creative sizes.
   - MCP: uses `get_standalone_forecast` or `get_delivery_forecast_by_line_item`
   - CLI: `orbiads reporting run --type forecast --ad-units <ids> --start <date> --end <date> --json`

2. **Interpret results:**
   - `availableUnits` > campaign goal — **safe to proceed**
   - `availableUnits` between 50-100% of goal — **proceed with caution**, may need broader targeting
   - `availableUnits` < 50% of goal — **stop and adjust** (broader targeting, more ad units, or lower goal)

3. **Check competitive pressure** — review contending line items that compete for the same inventory.

**GAM best practice:** Always forecast before creating line items. A forecast is free and prevents overbooking.

**Output:** Forecast summary with go/adjust/stop recommendation. Pass to Phase 3.

### Phase 3 — Advertiser & Order

**Goal:** Create or resolve the advertiser and order that will contain the line items.

1. **Find or create advertiser:**
   - Search existing advertisers by name first — avoid duplicates.
   - MCP: uses `find_or_create_advertiser`
   - CLI: `orbiads advertisers list --search "<name>" --json`, then `orbiads advertisers create --name "<name>" --json` if not found
   - **GAM rule:** `advertiserId` on an Order must point to a Company with `type=ADVERTISER`. Using an agency ID causes an error.

2. **Create order:**
   - Apply the user's `orderTemplate` from `get_naming_conventions` if configured. Provide the macro values (advertiser name, campaign name, dates) and the backend will expand the template. If no template is configured, use the fallback pattern: `{Brand} — {Campaign} — {Month YYYY}`
   - Set `traffickerId` to the user's GAM user ID
   - MCP: uses `create_order` (within `advertiser-order-line-items` tools)
   - CLI: `orbiads orders create --advertiser <id> --name "<name>" --json`
   - **GAM rule:** Order names must be unique across the entire network.

**Output:** Confirmed `advertiserId` and `orderId`. Pass to Phase 4.

### Phase 4 — Line Items

**Goal:** Create line items with correct type, pricing, dates, targeting, and creative placeholders.

**Read delivery defaults first.** Apply the user's delivery defaults from `get_delivery_defaults` (loaded in Phase 0). The user may have configured custom line item type, CPM rate, pacing, frequency caps, etc. Only override these defaults when the campaign brief explicitly specifies different values.

1. **Choose line item type** based on the campaign brief (or use the user's default `lineItemType` if not specified in the brief):

   | Campaign goal | Line Item Type | Priority |
   |--------------|----------------|----------|
   | Guaranteed impressions (direct sold) | `STANDARD` | 6-10 |
   | Share of voice / takeover | `SPONSORSHIP` | 4 |
   | Backfill / remnant | `PRICE_PRIORITY` | 12 |
   | Self-promotional | `HOUSE` | 16 |
   | Ad network / exchange | `NETWORK` | 12 |

2. **Set mandatory fields:**
   - `orderId` — from Phase 3
   - `name` — Apply the user's `lineItemTemplate` from `get_naming_conventions` if configured. Provide macro values (order name, format, placement, size). If no template is configured, use the fallback pattern: `{Brand} — {Size} — {Targeting} — {Type}`
   - `startDateTime` / `endDateTime` — must match the campaign brief. Use the user's `timeZoneId` from delivery defaults (or network timezone).
   - `costType` + `costPerUnit` — Use the user's default `costType` and `microAmount` from delivery defaults. `CPM` requires `unitType=IMPRESSIONS`, `CPC` requires `unitType=CLICKS`. Override only if the brief specifies a different rate.
   - `primaryGoal` — impression or click goal
   - `creativePlaceholders` — list of expected sizes (e.g., `300x250`, `728x90`). **Must match creative sizes exactly.**
   - `targeting.inventoryTargeting` — at least one ad unit or placement. **Mandatory.**
   - `creativeRotationType` — Use the user's default from delivery defaults (typically `OPTIMIZED`). Override with `EVEN` for explicit A/B testing.

3. **Set delivery options:**
   - `deliveryRateType`: Use the user's default from delivery defaults. Common values: `EVENLY` (recommended), `FRONTLOADED` (launch events), `AS_FAST_AS_POSSIBLE` (remnant only)
   - `frequencyCaps`: Use the user's default `frequencyCapImpressions` and `frequencyCapPeriod`. Combine short-term (1/hour) with long-term (10/week) caps if needed.
   - `priority`: Use the user's default priority from delivery defaults unless the brief requires a different value.
   - `roadblockingType`: Use the user's default from delivery defaults.

4. **Apply targeting:**
   - Inventory: ad units or placements (mandatory) — if using a preset, these are already set
   - Geo: country/region/city IDs
   - Device: device category, OS, browser
   - Custom: key-value pairs — if using a preset, check for pre-configured `keyValues`
   - Day-parting: if required by the brief

**GAM best practices:**
- Start targeting broad, narrow incrementally. Over-targeting = underdelivery.
- Use include-targeting (whitelist ad units) over exclude-targeting.
- Always include `creativePlaceholders` — a line item without them gets stuck in `NEEDS_CREATIVES` state.

**Output:** Created `lineItemIds` with targeting configured. Pass to Phase 5.

### Phase 5 — Creatives & Assignment

**Goal:** Create creatives and assign them to line items.

1. **Create creatives** matching the line item's `creativePlaceholders` sizes:
   - Apply the user's `creativeTemplate` from `get_naming_conventions` if configured. Provide macro values (advertiser name, format, size). If no template is configured, use the fallback pattern: `{Brand} — {Format} — {Version}`
   - MCP: uses `create_image_creative`, `create_classic_native_creative`
   - CLI: `orbiads creatives upload --file <path> --name "<name>" --advertiser <id> --json`
   - **GAM rule (v202502+):** `CreativeAssetService` is removed. Image bytes must be inlined in `createCreatives`.

2. **Assign creatives to line items (LICA):**
   - Creative size **must exactly match** one of the line item's `creativePlaceholders`. Size mismatch is the #1 API error.
   - MCP: uses `associate_creative`
   - **GAM rule:** A line item can have multiple creatives (rotation). A creative can be shared across line items.

3. **Verify assignment:**
   - After assignment, the line item status should move from `NEEDS_CREATIVES` to `READY`.
   - If still `NEEDS_CREATIVES`, a size is missing or the assignment failed.

**Output:** Created `creativeIds`, confirmed assignments. Pass to Phase 6.

### Phase 6 — QA & Preview

**Goal:** Last quality gate before going live. Never skip this phase.

1. **Compliance scan** — check creative content for policy violations.
   - MCP: uses `scan_creative_compliance`

2. **SSL validation** — verify all creative assets load over HTTPS.
   - MCP: uses `validate_creative_ssl` or `validate_creative_ssl_batch`
   - CLI: `orbiads creatives get --id <id> --json` (check SSL fields)

3. **Dry-run deployment** — simulate without executing.
   - MCP: uses `deploy_campaign` with `dry_run=True`
   - CLI: `orbiads campaigns deploy <id> --dry-run --json`

4. **Creative coverage check** — verify every line item has at least one matching creative.
   - MCP: uses `check_creative_coverage`

5. **Preview URLs** — generate visual previews for human review.
   - MCP: uses `get_preview_urls` or `get_campaign_preview_urls`
   - Include `previewPages` from tenant settings (loaded in Phase 0) for in-context preview. If `previewPages` is configured, the preview URLs will render creatives within the user's actual site pages, giving a realistic view of how ads will appear in production.

6. **QA Checklist:**
   - [ ] Order name matches brief (and follows the configured `orderTemplate` if set)
   - [ ] Correct advertiser assigned
   - [ ] Line item dates match brief
   - [ ] CPM/CPC rates match brief (and align with delivery defaults)
   - [ ] Impression/click goals match brief
   - [ ] All creatives assigned with matching sizes
   - [ ] Targeting matches brief (geo, device, ad units)
   - [ ] Frequency caps set if required (check against delivery defaults)
   - [ ] Delivery pacing matches requirements
   - [ ] No overbooking warnings
   - [ ] SSL validation passed
   - [ ] Preview renders correctly (use previewPages for in-context check)
   - [ ] Dry-run returns no blocking errors

**Decision:**
- All checks pass — **GO** — proceed to Phase 7
- Blocking issues found — **STOP** — report issues, fix, re-run QA
- Warnings only — **GO with caution** — note the warnings

**Output:** Go/no-go decision with findings. Pass to Phase 7 if GO.

### Phase 7 — Deploy & Monitor

**Goal:** Push the campaign live and verify delivery.

1. **Approve the order** — required before line items can deliver.
   - MCP: uses `approve_order`

2. **Deploy the campaign:**
   - MCP: uses `deploy_campaign` (without `dry_run`)
   - CLI: `orbiads campaigns deploy <id> --yes --json`
   - **Requires explicit user confirmation.** Never auto-deploy.

3. **Monitor initial delivery** (first 24h):
   - Check delivery status after 1 hour, then at 24 hours
   - MCP: uses `check_delivery_status`, `fetch_delivery_report`
   - CLI: `orbiads campaigns get <id> --json`, `orbiads reporting run --type delivery --campaign <id> --json`

4. **Check alerts:**
   - MCP: uses `check_underdelivery_alerts`, `check_budget_alerts`

5. **Line item status lifecycle:**
   ```
   DRAFT → NEEDS_CREATIVES → READY → DELIVERING → COMPLETED
                                    → PAUSED (manual)
                                    → DELIVERY_EXTENDED (if pacing behind)
   ```
   A line item stuck in `NEEDS_CREATIVES` means a creative is missing or size doesn't match.

**Output:** Deployment confirmed, delivery metrics, any alerts.

## Abort Conditions (Global)

- **STOP** if bootstrap not complete (no network context)
- **STOP** if tenant configuration could not be loaded and user hasn't acknowledged using defaults
- **STOP** if forecast shows < 50% availability and user hasn't acknowledged the risk
- **STOP** before any write without explicit user confirmation
- **STOP** if QA dry-run returns blocking errors
- **STOP** if creative sizes don't match line item placeholders
- **STOP** if order names would create duplicates

## Sub-Skills Reference

| Phase | MCP Skill | CLI Skill |
|-------|-----------|-----------|
| 0 | `/orbiads:bootstrap` | `/orbiads:cli-bootstrap` |
| 1 | `/orbiads:inventory-ad-units` + `/orbiads:placements-targeting` | `/orbiads:cli-inventory` + `/orbiads:cli-targeting` |
| 2 | `/orbiads:availability-forecast` | `/orbiads:cli-forecast` |
| 3-4 | `/orbiads:advertiser-order-line-items` | `/orbiads:cli-orders` |
| 5 | `/orbiads:native-image` | `/orbiads:cli-creatives` |
| 6 | `/orbiads:qa-preview` | `/orbiads:cli-qa` |
| 7 | `/orbiads:deploy-reporting` | `/orbiads:cli-deploy` |
