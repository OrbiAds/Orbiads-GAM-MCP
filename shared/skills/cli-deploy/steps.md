# Steps

1. [start] Confirm QA has passed. Run `orbiads campaigns get <id> --json` to verify campaign is ready for deployment.
2. [depends: step 1] Run `orbiads campaigns deploy <id> --yes --json` after explicit user confirmation (costs 5 credits). Capture the returned `jobId`.
3. [depends: step 2] Poll deployment status by running `orbiads campaigns get <id> --json` every 5-10 seconds until `status` changes from `deploying` to `deployed` or `failed`.
4. [depends: step 3] If `deployed`: run `orbiads reporting run --type delivery --campaign <id> --json` to verify initial delivery data.
5. [depends: step 3] If `failed`: report the error details from the status response and recommend corrective actions.

## Polling Pattern

```bash
# Deploy
$ orbiads campaigns deploy campaign_123 --yes --json
{"status": "deploying", "jobId": "job_456"}

# Poll until done (repeat every 5-10 seconds)
$ orbiads campaigns get campaign_123 --json | jq .status
"deploying"
# ... wait ...
$ orbiads campaigns get campaign_123 --json | jq .status
"deployed"
```

## Abort Conditions

- Stop if QA has not been run — route to `cli-qa`.
- Stop if the user does not confirm deployment.
- Stop if credit balance is insufficient (5 credits required).
- Stop polling after 5 minutes — report timeout and suggest manual check.
