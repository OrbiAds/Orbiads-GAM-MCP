# Available CLI Commands

## Advertiser Management

- `orbiads advertisers list --json` `[free]` — list all advertisers in the network.
- `orbiads advertisers list --search "<name>" --json` `[free]` — search advertisers by name.
- `orbiads advertisers create --name "<name>" --json` `[1 credit]` — create a new advertiser.

## Order Management

- `orbiads orders list --json` `[free]` — list all orders in the network.
- `orbiads orders list --advertiser <id> --json` `[free]` — list orders for a specific advertiser.
- `orbiads orders create --advertiser <id> --name "<name>" --json` `[1 credit]` — create a new order.
- `orbiads orders get --id <id> --json` `[free]` — get details for a specific order.
