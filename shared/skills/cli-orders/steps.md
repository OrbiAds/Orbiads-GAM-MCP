# Steps

1. [start] Run `orbiads advertisers list --search "<name>" --json` to find the advertiser. If not found, ask the user whether to create one.
2. [depends: step 1] If creating: run `orbiads advertisers create --name "<name>" --json` after user confirmation (costs 1 credit).
3. [depends: step 1 or 2] Run `orbiads orders list --advertiser <id> --json` to check for existing orders.
4. [depends: step 3] If no suitable order exists, run `orbiads orders create --advertiser <id> --name "<name>" --json` after user confirmation (costs 1 credit).
5. [depends: step 4] Return the confirmed advertiser ID and order ID.

## Abort Conditions

- Stop if the user declines advertiser or order creation.
- Stop if credit balance is insufficient for billed operations.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
