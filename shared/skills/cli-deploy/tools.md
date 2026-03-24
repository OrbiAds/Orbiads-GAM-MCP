# Available CLI Commands

## Deployment

- `orbiads campaigns deploy <id> --yes --json` `[5 credits]` — deploy the campaign non-interactively. Returns a job ID for status polling.

## Status Polling

- `orbiads campaigns get <id> --json` `[free]` — get campaign status. Poll until `status` is `deployed` or `failed`.

## Post-Deploy Reporting

- `orbiads reporting run --type delivery --campaign <id> --json` `[free]` — run a delivery report for the deployed campaign.
