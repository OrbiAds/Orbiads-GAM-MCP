---
description: "Deploy GAM campaigns and monitor delivery via CLI. Use when deploying ads or checking delivery status."
---

# OrbiAds CLI — Deploy

Deploy a GAM campaign to production and monitor its delivery status.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Commands

- `orbiads campaigns deploy <id> --yes --json` `[5 credits]` — deploy campaign (requires explicit confirmation)
- `orbiads campaigns get <id> --json` `[free]` — check campaign status
- `orbiads reporting run --type delivery --campaign <id> --json` `[free]` — get delivery report

## Steps

1. [start] Confirm QA has passed. Run `orbiads campaigns get <id> --json` to verify readiness.
2. [depends: step 1] **Pre-deploy check:** Verify delivery defaults are configured appropriately for this campaign. Inspect the campaign JSON to confirm that CPM rate, pacing (deliveryRateType), frequency caps, and line item type match the campaign brief. If the user has tenant-level delivery defaults, these should already be applied. Flag any mismatches before deploying.
3. [depends: step 2] Run `orbiads campaigns deploy <id> --yes --json` after explicit user confirmation (costs 5 credits). Capture the jobId from the response.
4. [depends: step 3] Poll status: run `orbiads campaigns get <id> --json` every 5-10 seconds until status is `deployed` or `failed`. Stop after 5 minutes maximum.
5. [depends: step 4] If deployed: run `orbiads reporting run --type delivery --campaign <id> --json` to get initial delivery data.
6. [depends: step 4] If failed: report the errors and recommend fixes.

## Abort Conditions

- QA has not been run: route to cli-qa skill first.
- User does not explicitly confirm deployment.
- Insufficient credits (deployment costs 5 credits).
- Polling timeout after 5 minutes with no terminal status.
- Delivery defaults mismatch detected in pre-deploy check: stop and confirm with user.

## Output

Deployment result with campaign status and delivery metrics. Polling pattern example:

```bash
# Deploy
orbiads campaigns deploy 12345 --yes --json

# Poll until terminal state (max 5 min)
for i in $(seq 1 30); do
  sleep 10
  STATUS=$(orbiads campaigns get 12345 --json | jq -r '.data.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "deployed" ] || [ "$STATUS" = "failed" ]; then break; fi
done

# Check delivery
orbiads reporting run --type delivery --campaign 12345 --json
```
