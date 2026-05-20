# Available CLI Commands

## Targeting discovery

- `orbiads inventory keys [--limit N]` `[free]` — list custom targeting keys.
- `orbiads inventory search-custom-targeting --query <q>` `[free]` — search keys + values by name.
- `orbiads custom-targeting-values list [--key-id <id>] [--search <q>] [--limit N]` `[free]` — list values (optionally filtered by key).

## Targeting key + value mutations

- `orbiads inventory create-key --file <body.json>` `[free]` — create a custom-targeting key.
- `orbiads inventory update-key <key_id> --file <patch.json>` `[free]` — PATCH a key.
- `orbiads inventory delete-key <key_id>` `[free]` — delete a key.
- `orbiads custom-targeting-values create <key_id> --file <vals.json>` `[free]` — create values for a key.
- `orbiads custom-targeting-values update <value_id> --file <patch.json>` `[free]` — PATCH a value.
- `orbiads custom-targeting-values action --file <body.json>` `[free]` — bulk activate/deactivate/delete.

## Audience segments

- `orbiads audiences list` `[free]` — list audience segments.
- `orbiads audiences get <segment_id>` `[free]` — details.
- `orbiads audiences create --file <seg.json>` `[free]` — create.
- `orbiads audiences update <segment_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads audiences action --file <body.json>` `[free]` — bulk activate/deactivate/delete.

## Reference data for targeting

- `orbiads inventory countries` `[free]` — geo-target catalogue.
- `orbiads inventory device-categories` `[free]` — device categories.
- `orbiads inventory languages [--query <q>] [--limit N]` `[free]` — targeting languages.

## Ad unit qualification

- `orbiads inventory ad-units [--search <name>] [--limit N]` `[free]` — list ad units.
- `orbiads inventory search-ad-units --query <q>` `[free]` — name/code search.
- `orbiads inventory ad-units-by-ids --file <ids.json>` `[free]` — bulk fetch.
- `orbiads inventory sizes` `[free]` — distinct sizes.

## Apply targeting to line items

- `orbiads line-items update-targeting <campaign_id> <line_item_id> --file <tgt.json>` `[free]` — patch the targeting of a line item under a campaign.
