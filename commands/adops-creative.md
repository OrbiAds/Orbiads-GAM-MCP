---
name: adops-creative
description: Creative lifecycle — upload assets, naming conventions, QA scans, SSL validation, preview URLs, associate creatives to line items.
argument-hint: "<upload|qa|ssl|preview|associate|list|duplicate> [creative-id]"
allowed-tools: mcp__orbiads__creatives,mcp__orbiads__creative_assets,mcp__orbiads__creative_qa,mcp__orbiads__creative_wrapper_skill,mcp__orbiads__settings,mcp__orbiads__billing
model: sonnet
---

# GAM Creative Lifecycle

Always confirm the tenant first: `get_my_tenant_id`. Reads are free. Writes require a confirmation token.

## Naming conventions (always fetch before creating)

Before naming any creative, call `settings(action="get_naming_conventions")` and apply the returned pattern. Typical patterns enforce advertiser code, format type, size, and date. A creative named outside the convention will be rejected at QA or cause reporting ambiguity. If no convention is configured, ask the user to confirm the name explicitly.

## upload

Identify the creative type from the asset the user provides, then call the matching `creative_assets` action:

| Type | Action | Key params |
| --- | --- | --- |
| Image (JPG/PNG/GIF/WebP) | `creative_assets(action="create_image")` | `advertiser_id`, `name`, `image_url` or `image_bytes` |
| HTML5 ZIP | `creative_assets(action="upload_html5_zip")` | `advertiser_id`, `name`, `zip_url` |
| HTML5 from files | `creative_assets(action="create_html5_from_files")` | `advertiser_id`, `name`, `files[]` |
| VAST redirect (video) | `creative_assets(action="create_vast_redirect")` | `advertiser_id`, `name`, `vast_url`, `duration` |
| Video (direct) | `creative_assets(action="create_video")` | `advertiser_id`, `name`, `video_url` — poll `get_video_transcode_status` until `COMPLETE` |
| Third-party tag | `creative_assets(action="create_third_party")` | `advertiser_id`, `name`, `snippet`, `size` |
| Native classic | `creative_assets(action="create_classic_native")` | `advertiser_id`, `name`, `headline`, `body`, `call_to_action`, `image_url` |
| Audio | `creative_assets(action="create_audio")` | `advertiser_id`, `name`, `audio_url`, `duration` |

If the user provides a URL to an existing hosted asset, use `creative_assets(action="upload_from_url")` regardless of type — the server auto-detects the format.

For multiple files in one shot: `creative_assets(action="bulk_upload", params={advertiser_id, assets: [...]})`.

If the image exceeds GAM size limits, compress first: `creative_assets(action="compress_image", params={image_url, max_size_kb})`.

After creation, run `qa` automatically on the new creative ID before returning results.

## qa `<creative-id>`

Run all three checks in order — all free:

1. `creative_qa(action="scan_creative_compliance", params={creative_id})` — format validation, size compliance, click tag detection.
2. `creative_qa(action="validate_creative_ssl", params={creative_id})` — all asset URLs must be HTTPS.
3. `creative_qa(action="audit_creative_tracking", params={creative_id})` — verifies impression and click trackers are present and reachable. Costs 0.5 cr.

Show ✅ PASS or ❌ FAIL per check. For each failure, include the error code and the exact URL or field that caused it. A creative with any SSL failure must not be associated to a live line item without the user's explicit acknowledgement.

To scan an entire order at once: `creative_qa(action="audit_order_tracking", params={order_id})`. Costs 0.5 cr.

For third-party tags, also run `creative_qa(action="validate_tag_snippet", params={tag_snippet})` — validates the raw HTML/JS without requiring a GAM creative ID.

## ssl `<creative-id>`

`creative_qa(action="validate_creative_ssl", params={creative_id})`. Lists every insecure URL found (asset src, tracker, click tag). For third-party tags use `validate_tag_snippet`. Show the recommended HTTPS equivalent for each HTTP URL where possible.

## preview `<creative-id>`

`creatives(action="get_creative_preview_url", params={creative_id})` for a single creative. For all creatives on a campaign: `creatives(action="get_campaign_preview_links", params={campaign_id})`. For native styles: `creatives(action="get_native_style_preview_urls", params={native_style_id})`.

## associate `<creative-id> <line-item-id>`

Before associating:

1. Check existing coverage: `creatives(action="get_licas_by_line_item", params={line_item_id})`.
2. Run `pre_archive_check` if the creative is older than 90 days: `creative_qa(action="pre_archive_check", params={creative_id})`. Costs 0.5 cr.

Then: `creatives(action="associate_creative", params={creative_id, line_item_id, sizes: [...]})`.

For bulk association across multiple line items: `creatives(action="bulk_associate_creatives", params={creative_id, line_item_ids: [...]})`.

## list `[advertiser-id]`

`creatives(action="list_creatives_by_advertiser", params={advertiser_id})` — returns ID, name, type, size, SSL status, last modified. Use `list_creatives_by_network` for a network-wide view (slow on large networks). Use `list_creatives_by_line_item` to audit coverage for a specific line item.

## duplicate `<creative-id>`

`creatives(action="duplicate_creative", params={creative_id})`. Costs 0.5 cr and requires a confirmation token. The duplicate gets a `_COPY` suffix by default — check naming conventions and rename if needed via `creatives(action="update_creative", params={creative_id, name})`.
