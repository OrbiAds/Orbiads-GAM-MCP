# Available CLI Commands

## Advertiser management

- `orbiads advertisers list` `[free]` — list advertisers.
- `orbiads advertisers find --name <name>` `[free]` — exact name lookup (read-only).
- `orbiads advertisers find-or-create --name <name> [--type ADVERTISER|AGENCY]` `[free]` — upsert.
- `orbiads advertisers get <advertiser_id>` `[free]` — details.
- `orbiads advertisers create --name <name>` `[1 credit]` — create a new advertiser.
- `orbiads advertisers update <advertiser_id> --file <patch.json>` `[free]` — PATCH.

## Agencies (sub-noun)

- `orbiads advertisers agencies list` `[free]` — list agencies.
- `orbiads advertisers agencies create --name <name>` `[free]` — create.
- `orbiads advertisers agencies update <agency_id> --file <patch.json>` `[free]` — PATCH.

## Contacts (advertiser/agency people)

- `orbiads contacts list [--company-id <id>]` `[free]` — list (optionally filtered by company).
- `orbiads contacts create --file <body.json>` `[free]` — create (body: name, email, companyId).
- `orbiads contacts update <contact_id> --file <patch.json>` `[free]` — PATCH.

## Order management

- `orbiads orders list [--advertiser-id <id>] [--query <q>] [--limit N] [--offset N]` `[free]` — list orders.
- `orbiads orders list-delivering [--limit N]` `[free]` — filter shorthand.
- `orbiads orders get <order_id>` `[free]` — details.
- `orbiads orders create --name <name> --advertiser-id <id>` `[1 credit]` — create.
- `orbiads orders approve <order_id> [--yes]` `[free]` — Draft → Approved.
- `orbiads orders archive <order_id> [--yes]` `[free]` — archive.
- `orbiads orders update <order_id> --file <patch.json>` `[free]` — PATCH. Read-only fields (start/end dates, totals, currency) rejected with 422.

## Users & roles (read-only)

- `orbiads users list [--search <q>] [--limit N] [--offset N]` `[free]` — list GAM users.
- `orbiads roles list` `[free]` — list GAM roles.
