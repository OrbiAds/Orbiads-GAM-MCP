---
name: adops-campaign
description: Read, plan, deploy, preview, pause or check a GAM campaign — live recap, ExecutionPlan preview, creative association, preview→confirm→execute gate.
argument-hint: "<read|dry-run|plan-deployment|deploy-media|deploy|preview|pause|status|rollback> [campaign-id]"
allowed-tools: mcp__orbiads__campaign,mcp__orbiads__companies,mcp__orbiads__orders,mcp__orbiads__line_items,mcp__orbiads__creatives,mcp__orbiads__creative_qa,mcp__orbiads__reporting,mcp__orbiads__targeting,mcp__orbiads__billing
model: sonnet
---

# GAM Campaign Lifecycle

Always start by confirming the tenant: call `get_my_tenant_id`. If unauthenticated, stop and ask the user to run `orbiads auth login`.

## read

Call `campaign(action="read", params={campaign_id})`.

This returns a live `CampaignRecap`: order, groups, line items, LICAs, creatives, and targeting assembled from GAM. It is free and performs zero GAM writes.

Use this recap as the source of truth before edit-intents, diagnostics, or resume work. It reflects **GAM live state**, not a Firestore mirror or previous LLM context that may have drifted.

## dry-run

Call `campaign(action="dry_run", params={campaign_id})` or `campaign(action="dry_run", params={job_id})`.

The server returns a signed `ExecutionPlan`:

```text
{
  operation,
  resourceType: "campaign",
  preview,
  mutations[],
  risks[],
  warnings[],
  estimatedCost,
  confirmationToken,
  expiresIn: 300
}
```

This step is free and performs zero GAM or Firestore writes. The `confirmationToken` produced here is consumed by `campaign(action="deploy")`.

Error handling:

- `CONFIRMATION_REQUIRED`: no token was supplied for execute; re-run `dry_run`.
- `PAYLOAD_MISMATCH`: the payload drifted between dry-run and deploy; re-run `dry_run`.
- `TOKEN_EXPIRED`: the token is older than 300 seconds; re-run `dry_run`.

## plan-deployment

Call `campaign(action="plan_deployment", params={preset, ...})`.

Available presets: `display_banner`, `video_vast`, `video_hosted`, `audio_vast`, `audio_hosted`, `custom_spec`. Pass `product_id` when an ADCP Product should prefill placements, pricing, and formats.

The server returns a signed `ExecutionPlan` with `dry_run=true` implied. It is free, and the resulting token is consumed by `campaign(action="deploy_media")`.

## deploy-media

Call `campaign(action="deploy_media", params={confirmation_token})`.

This executes through the unified `CampaignPipeline.deploy` saga. It costs credits using the same grid as `deploy`, and it requires a `confirmation_token` from `plan_deployment` or `dry_run`.

Non-regression: `campaign(action="deploy")` remains the entry point for campaigns coming from a Firestore `CampaignDocument` or a legacy job.

## Full deploy flow (new campaign)

### 1 — Advertiser and order setup (free)

Resolve the advertiser with `companies(action="advertisers.find_or_create", params={name, type: "ADVERTISER"})`. Then resolve or create the order with `orders(action="find_or_create", params={name, advertiser_id, traffic_amount, start_date, end_date})`.

If the order already exists, fetch it with `orders(action="get")` and verify it is in `DRAFT` or `APPROVED` status before continuing.

### 2 — Inventory forecast (free, mandatory before any write)

Before creating a single line item, verify the campaign can actually deliver. Call:

```text
reporting(action="get_standalone_forecast", params={
  targeting: { ad_unit_ids, geo_targets, device_categories },
  line_item_type,
  start_date_time,
  end_date_time,
  units_bought,
  cost_type,
  cost_per_unit
})
```

If `available_units` < `units_bought`, warn the user with the exact numbers and ask how to proceed (reduce goal, change targeting, or accept overbooking). Never silently continue with an impossible goal.

For an existing line item being updated, use `reporting(action="get_delivery_forecast_by_line_item", params={line_item_id})` instead.

### 3 — Line item creation (free)

Create line items with `line_items(action="create_batch", params={order_id, line_items: [...]})`. Each line item needs `targeting`, `start_date_time`, `end_date_time`, `cost_per_unit`, `units_bought`, and `line_item_type`.

Verify creation with `line_items(action="verify", params={line_item_id})`.

### 4 — Creative association (free)

Associate creatives with `campaign(action="create_licas", params={line_item_id, creative_ids: [...]})`. Run a quick compliance check first with `creative_qa(action="scan_creative_compliance", params={creative_id})` — do not associate a non-SSL creative without warning the user.

### 5 — Forecast recheck before deploy (free)

After line items and creatives are in place, recheck deliverability: `reporting(action="get_prospective_delivery_forecast", params={line_item_id})`. This catches targeting conflicts that only appear after full setup. If the forecast degrades significantly from step 2, surface the delta to the user.

### 6 — Preview and deploy (costs credits)

Call `campaign(action="dry_run", params={campaign_id})` to get the signed `ExecutionPlan`. Show the user:

- Mutations: orders, line items, creatives, and LICAs to be written
- Risks and warnings
- Estimated credit cost
- `confirmationToken`
- Token expiry (300 seconds)

Then wait for explicit confirmation. Call `campaign(action="deploy", params={campaign_id, confirmation_token: "<token>"})` to execute.

On `CONFIRMATION_REQUIRED`: token missing, re-run `dry_run`. On `PAYLOAD_MISMATCH`: payload changed, re-run `dry_run`. On `TOKEN_EXPIRED`: token expired, re-run `dry_run`.

### 7 — Order approval (free)

After deploy, approve the order: `orders(action="approve", params={order_id})`. Then verify delivery has started: `reporting(action="check_delivery_status", params={job_id: campaign_id})`.

---

## status

`campaign(action="read", params={campaign_id})` + `orders(action="get")` + `reporting(action="check_delivery_status")`. Show name, GAM status, pacing %, impressions vs. goal, and any active alerts from `reporting(action="check_underdelivery_alerts")`.

## pause

`campaign(action="pause", params={campaign_id})` — pauses all line items. Requires confirmation token. Provide a resume path: `line_items(action="activate_batch", params={line_item_ids})`.

## rollback

`campaign(action="rollback", params={campaign_id})` — deletes all GAM resources created by the deployment. Requires confirmation token. Surface any SOAP fault verbatim. Do not retry more than twice.

---

## Hard rules

- Never skip the inventory forecast (step 2). An unforecasted deploy is a blind deploy.
- Never call `campaign(action="deploy")` without a `confirmation_token` from `dry_run` or `plan_deployment` less than 5 minutes old.
- For media campaigns (video/audio), prefer `plan_deployment` -> `deploy_media` over the raw deploy path.
- Never call a write action without a `confirmation_token` less than 5 minutes old.
- Never retry a failed write more than twice. GAM SOAP is not idempotent.
- Never invent a `tenantId` or `networkCode`.
