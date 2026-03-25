---
description: "Full campaign setup via OrbiAds CLI — from advertiser to live delivery. Orchestrates CLI commands in the correct GAM entity order with naming conventions and QA checks. Use when the user wants to create a complete campaign from the terminal."
---

# OrbiAds CLI — Campaign Workflow (Master)

Orchestrate a complete GAM campaign using CLI commands. Same workflow as the MCP skill, executed via bash. Each phase uses `orbiads` commands with `--json` for structured output.

Requires `orbiads` CLI (`pip install orbiads-cli`). Use the Bash tool to execute all commands.

## GAM Entity Hierarchy

```
Advertiser → Order → Line Item → Creative → Assignment (LICA) → Deploy
```

Each entity depends on its parent. You cannot skip levels.

## User Configuration

The user may have configured naming conventions, delivery defaults, and campaign presets via the OrbiAds web app (orbiads.com/settings). The backend applies these settings automatically when creating entities through the API.

**Key points for CLI usage:**
- **Naming conventions** are applied automatically by the backend when configured. The `--name` flag values you provide are used as macro values (e.g., advertiser name, campaign name) that get expanded by the configured templates. Check the user's settings at orbiads.com/settings if entity names look unexpected.
- **Delivery defaults** (line item type, CPM, pacing, frequency caps, etc.) are applied automatically by the backend. Override with explicit CLI flags only when the campaign brief requires different values.
- **Campaign presets** (Pack Homepage, Pack ROS, Pack Interstitiel, plus custom presets) pre-configure ad units and targeting. If a preset matches the campaign goal, it saves manual inventory discovery.
- **Tenant settings** include preview pages, auto-archival, and GA4 property configuration.

To inspect current configuration via CLI, run `orbiads network info --json` which includes tenant-level settings.

### Fallback Naming Conventions

If the user has not configured naming templates, the backend uses these defaults:

| Entity | Pattern | Example |
|--------|---------|---------|
| Advertiser | `{BrandName}` | `Renault` |
| Order | `{Brand} — {Campaign} — {Month YYYY}` | `Renault — Spring Launch — Apr 2026` |
| Line Item | `{Brand} — {Size} — {Targeting} — {Type}` | `Renault — MPU 300x250 — FR Desktop — Standard` |
| Creative | `{Brand} — {Size} — {Version}` | `Renault — MPU 300x250 — v1` |

Use `—` (em dash) as separator. Keep names unique.

## Phase 0 — Bootstrap & Configuration

```bash
orbiads --version
orbiads auth status --json
orbiads network info --json
```

**If not authenticated:** tell user to run `orbiads auth login`.
**If no network:** `orbiads network list --json` then `orbiads network switch --network-code <code> --json`.

Review the `network info` output to understand the tenant's current configuration (naming conventions, delivery defaults, presets). This determines how entities will be named and configured in subsequent phases.

## Phase 1 — Inventory & Targeting

**Check presets first.** If the user's tenant has campaign presets (visible in `network info` output or at orbiads.com/settings), and a preset matches the campaign brief (e.g., homepage takeover matches `Pack Homepage`), the ad units and targeting are already selected. Skip manual discovery.

If no preset matches, proceed with manual discovery:

```bash
# Discover ad units
orbiads inventory ad-units --json
orbiads inventory ad-units --search "homepage" --json

# Check placements
orbiads inventory placements --json

# List targeting keys
orbiads inventory keys --json
```

**Output:** Note the `adUnitIds` and available sizes for the campaign.

## Phase 2 — Forecast

```bash
orbiads reporting run --type forecast \
  --ad-units <id1>,<id2> \
  --start 2026-04-01 --end 2026-04-30 \
  --json
```

**Interpret:** `availableUnits` > goal = safe. < 50% of goal = stop and adjust targeting.

**GAM rule:** Always forecast before creating line items. Forecasts are free.

## Phase 3 — Advertiser & Order

```bash
# Find advertiser
orbiads advertisers list --search "Renault" --json

# Create if not found (1 credit)
orbiads advertisers create --name "Renault" --json

# Create order (1 credit)
# The --name value provides macro values for the configured orderTemplate.
# If no template is configured, use the fallback pattern: {Brand} — {Campaign} — {Month YYYY}
orbiads orders create \
  --advertiser <advertiserId> \
  --name "Renault — Spring Launch — Apr 2026" \
  --json
```

**GAM rules:**
- Advertiser must have `type=ADVERTISER` (not agency)
- Order names must be unique across the network

## Phase 4 — Line Items

**The backend applies tenant delivery defaults automatically** (line item type, CPM rate, pacing, frequency caps, priority, etc.). Only override with explicit flags when the campaign brief requires different values.

Line item type selection (use the user's configured default if the brief doesn't specify):

| Goal | Type | Priority |
|------|------|----------|
| Guaranteed impressions | `STANDARD` | 6-10 |
| Share of voice | `SPONSORSHIP` | 4 |
| Remnant / backfill | `PRICE_PRIORITY` | 12 |
| Self-promo | `HOUSE` | 16 |

**GAM rules:**
- `costType=CPM` requires `unitType=IMPRESSIONS`
- Creative placeholder sizes must match creative sizes exactly
- Inventory targeting (ad units) is mandatory
- Start with broad targeting, narrow later

Line items are created through the MCP or GAM UI for complex configurations. CLI supports listing and status:

```bash
# List line items for the order
orbiads orders get --id <orderId> --json
```

## Phase 5 — Creatives

```bash
# Upload creative (5 credits)
# The --name value provides macro values for the configured creativeTemplate.
# If no template is configured, use the fallback: {Brand} — {Size} — {Version}
orbiads creatives upload \
  --file ./banner-300x250.png \
  --name "Renault — MPU 300x250 — v1" \
  --advertiser <advertiserId> \
  --json

# Verify creation
orbiads creatives get --id <creativeId> --json
```

**GAM rules:**
- Creative size must exactly match a line item's `creativePlaceholder` — size mismatch is the #1 API error
- `CreativeAssetService` removed in v202502 — image bytes are inlined in `createCreatives`
- A line item stuck in `NEEDS_CREATIVES` means a creative size is missing

## Phase 6 — QA

```bash
# Inspect campaign configuration
orbiads campaigns get <id> --json

# Check creative SSL and compliance
orbiads creatives get --id <creativeId> --json

# Dry-run deployment (free — no actual push)
orbiads campaigns deploy <id> --dry-run --json
```

**Pre-check:** Verify delivery defaults are configured appropriately for this campaign. If the campaign requires non-standard CPM, pacing, or frequency caps, confirm they were set correctly (either via defaults or explicit overrides).

**QA Checklist (verify in the JSON output):**
- [ ] Order name matches brief (and follows the configured naming template if set)
- [ ] Correct advertiser
- [ ] Line item dates, rates, goals match brief
- [ ] Delivery defaults applied correctly (CPM, pacing, frequency caps)
- [ ] All creatives assigned with matching sizes
- [ ] Targeting matches brief (geo, device, ad units)
- [ ] Frequency caps set if required
- [ ] Dry-run returns no blocking errors
- [ ] Line item status is `READY` (not `NEEDS_CREATIVES`)

**Decision:** All checks pass → proceed. Blocking errors → STOP and fix.

## Phase 7 — Deploy & Monitor

```bash
# Deploy (5 credits — requires explicit user confirmation)
orbiads campaigns deploy <id> --yes --json

# Poll status (every 10s, max 5 min)
for i in $(seq 1 30); do
  sleep 10
  STATUS=$(orbiads campaigns get <id> --json | jq -r '.data.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "deployed" ] || [ "$STATUS" = "failed" ]; then break; fi
done

# Check delivery (after 1h or 24h)
orbiads reporting run --type delivery --campaign <id> --json
```

**Line item lifecycle:** `DRAFT → NEEDS_CREATIVES → READY → DELIVERING → COMPLETED`

## Abort Conditions

- **STOP** if bootstrap not complete
- **STOP** if forecast < 50% availability without user acknowledgment
- **STOP** before any write without explicit user confirmation
- **STOP** if QA dry-run returns blocking errors
- **STOP** if creative sizes don't match line item placeholders

## Sub-Skills

| Phase | CLI Skill |
|-------|-----------|
| 0 | `/orbiads:cli-bootstrap` |
| 1 | `/orbiads:cli-inventory` + `/orbiads:cli-targeting` |
| 2 | `/orbiads:cli-forecast` |
| 3 | `/orbiads:cli-orders` |
| 5 | `/orbiads:cli-creatives` |
| 6 | `/orbiads:cli-qa` |
| 7 | `/orbiads:cli-deploy` |
