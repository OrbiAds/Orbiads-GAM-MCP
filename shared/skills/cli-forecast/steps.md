# Steps

1. [start] Confirm the ad unit IDs to forecast. If unknown, run `orbiads inventory ad-units --json` to discover them.
2. [depends: step 1] Run `orbiads reporting run --type forecast --ad-units <ids> --start <date> --end <date> --json` with the target date range.
3. [depends: step 2] Analyze the forecast results: available impressions, matched, possible, and contending line items.
4. [depends: step 3] Summarize the forecast and recommend whether the planned impression goal is achievable.

## Abort Conditions

- Stop if no ad unit IDs are available — route to `cli-inventory`.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
