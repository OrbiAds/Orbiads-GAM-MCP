# Available CLI Commands

## Ad unit discovery

- `orbiads inventory ad-units [--search <name>] [--limit N]` `[free]` — list active ad units.
- `orbiads inventory search-ad-units --query <q> [--limit N] [--offset N]` `[free]` — search by name/code.
- `orbiads inventory ad-units-by-ids --file <ids.json>` `[free]` — bulk fetch by ID.
- `orbiads inventory sizes` `[free]` — distinct ad-unit sizes in the network.

## Ad unit mutations

- `orbiads inventory create-ad-units --file <selection.json>` `[free]` — batch create/import.
- `orbiads inventory update-ad-unit <ad_unit_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads inventory archive-ad-unit <ad_unit_id>` `[free]` — soft-delete.
- `orbiads inventory list-inactive [--days N]` `[free]` — zero-impression ad units in last N days (default 90).
- `orbiads inventory archive-inactive --file <ids.json>` `[free]` — bulk archive inactive.
- `orbiads inventory validate-fluid --file <req.json>` `[free]` — verify Fluid-sizing support.
- `orbiads inventory audit [--file <body.json>]` `[free]` — run an inventory audit.

## Placement discovery & lifecycle

- `orbiads inventory placements [--limit N]` `[free]` — list placements.
- `orbiads inventory placement-create --file <body.json>` `[free]` — create.
- `orbiads inventory placement-update <placement_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads inventory placement-archive <placement_id>` `[free]` — archive.

## Custom-targeting keys

- `orbiads inventory keys [--limit N]` `[free]` — list keys.
- `orbiads inventory search-custom-targeting --query <q>` `[free]` — search keys + values.
- `orbiads inventory create-key --file <body.json>` `[free]` — create a key.
- `orbiads inventory update-key <key_id> --file <patch.json>` `[free]` — PATCH.
- `orbiads inventory delete-key <key_id>` `[free]` — delete.

## Custom-targeting values (separate noun)

- `orbiads custom-targeting-values list [--key-id <id>] [--search <q>] [--limit N]` `[free]` — list values (optionally filtered by key).
- `orbiads custom-targeting-values create <key_id> --file <vals.json>` `[free]` — create values for a key.
- `orbiads custom-targeting-values update <value_id> --file <patch.json>` `[free]` — PATCH a single value.
- `orbiads custom-targeting-values action --file <body.json>` `[free]` — bulk activate/deactivate/delete.

## Reference data

- `orbiads inventory countries` `[free]` — geo-target catalogue.
- `orbiads inventory device-categories` `[free]` — device categories.
- `orbiads inventory languages [--query <q>] [--limit N]` `[free]` — targeting languages.

## Blueprints

- `orbiads inventory blueprint-generate --file <bp.json>` `[free]` — dry-run blueprint.
- `orbiads inventory blueprint-push --file <bp.json>` `[free]` — push blueprint to GAM.
- `orbiads inventory ads-json` `[free]` — ads.json manifest.
