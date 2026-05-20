# Available CLI Commands

## Creative discovery

- `orbiads creatives list --advertiser-id <id> [--limit N]` `[free]` — list creatives for an advertiser (the only working list scope; backend exposes no network-wide collection at this path).
- `orbiads creatives list-by-network [--query <q>] [--limit N] [--offset N]` `[free]` — search the entire network by name (paginated).
- `orbiads creatives list-by-line-item <line_item_id>` `[free]` — creatives attached to a line item.
- `orbiads creatives get <creative_id>` `[free]` — full creative details.

## Creative upload (one verb per asset type)

- `orbiads creatives upload <file>` `[free]` — generic single-file upload (≤5MB, allow-listed extensions).
- `orbiads creatives upload-third-party <file>` `[free]` — third-party tag asset.
- `orbiads creatives upload-html5 <file>` `[free]` — HTML5 .zip bundle (covers 3 MCP variants).
- `orbiads creatives upload-video <file>` `[free]` — video asset.
- `orbiads creatives upload-audio <file>` `[free]` — audio asset.
- `orbiads creatives upload-images <file>...` `[free]` — bulk image upload (multiple files).
- `orbiads creatives upload-native-classic --main-image <file> [--logo <file>]` `[free]` — classic native creative.
- `orbiads creatives upload-vast-redirect <file>` `[free]` — VAST redirect creative.
- `orbiads creatives upload-companion <file>` `[free]` — companion creative.
- `orbiads creatives compress-image <file>` `[free]` — compress an image creative.

## Creative lifecycle

- `orbiads creatives update <creative_id> --file <patch.json>` `[free]` — PATCH a creative.
- `orbiads creatives duplicate <creative_id> [--yes]` `[free]` — duplicate.
- `orbiads creatives archive <creative_id> [--yes]` `[free]` — archive (reversible via GAM UI).
- `orbiads creatives preview-url <creative_id>` `[free]` — preview URL.
- `orbiads creatives native-style-previews <creative_id>` `[free]` — native-style preview URLs.

## LICAs (creative ↔ line-item association)

- `orbiads licas list-by-line-item <line_item_id>` `[free]` — raw LICA rows for a line item.
- `orbiads licas batch --file <ids.json>` `[free]` — fetch LICAs for multiple line items in one call.
- `orbiads licas update <line_item_id> <creative_id> --file <patch.json>` `[free]` — rotation weight, schedule, sizes, status.
- `orbiads licas deactivate <line_item_id> <creative_id> [--yes]` `[free]` — deactivate a single LICA.
- `orbiads licas delete --file <payload.json> [--yes]` `[free]` — detach multiple creatives (sets INACTIVE — GAM has no hard-delete).

## NativeStyles

- `orbiads native-styles list [--name-filter <q>] [--limit N]` `[free]` — list active NativeStyles.
- `orbiads native-styles get <style_id>` `[free]` — details.
- `orbiads native-styles update <style_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads native-styles duplicate <style_id> [--yes]` `[free]` — duplicate.
- `orbiads native-styles archive <style_id> [--yes]` `[free]` — archive.

## CreativeTemplates

- `orbiads creative-templates list [--name-filter <q>] [--limit N] [--offset N]` `[free]` — USER_DEFINED templates with variable metadata.
- `orbiads creative-templates get <template_id>` `[free]` — single template.
- `orbiads creative-templates ensure-classic-native --file <body.json>` `[free]` — look up or register the Classic Native template.
