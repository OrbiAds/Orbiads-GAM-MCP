# Allowed Tools

## Read and Qualification

- `list_advertisers` `[free]` — list the advertiser catalog.
- `get_advertiser` `[free]` — re-read a single advertiser.
- `list_orders` `[free]` — search or list current orders.
- `get_order` `[free]` — re-read one order precisely.
- `list_line_items_by_order` `[free]` — inspect the current line-item scope of an order.
- `get_line_item` `[free]` — re-read one line item precisely.
- `verify_order_setup` `[free]` — verify order readiness before downstream steps.
- `verify_line_item_setup` `[free]` — verify targeting, pacing, and delivery readiness.
- `list_private_deals` `[free]` — inspect available deals before deal-based line items.

## Advertiser Resolution and Order Writes

- `find_advertiser` `[free]` — resolve an advertiser when only partial identity is known.
- `create_advertiser` `[free]` — create a new advertiser when no safe match exists.
- `find_or_create_advertiser` `[free]` — resolve the advertiser when the ID is not already known.
- `update_order` `[free]` — revise an existing order.
- `approve_order` `[free]` — move an order to the approved state.
- `archive_order` `[free]` — exceptional order deactivation.

## Line-Item Writes and Lifecycle

- `create_line_items` `[free]` — create a standard job-backed batch of line items.
- `update_line_item` `[free]` — revise one existing line item.
- `duplicate_line_item` `[free]` — clone a line item before targeted changes.
- `update_line_item_targeting` `[free]` — adjust targeting after review.
- `activate_line_items` `[free]` — activate the job-backed line-item batch.
- `pause_line_items` `[free]` — pause a job-backed line-item batch.
- `archive_line_item` `[free]` — exceptional archive path for one line item.

## Deal Variants and Capability Boundary

- programmatic guaranteed and preferred-deal variants stay inside the standard order and line-item preparation flow until dedicated exposed tools are available.
- `create_open_bidding_line_item` `[free]` — currently returns `NOT_IMPLEMENTED`; keep it as a documented boundary, not the default path.