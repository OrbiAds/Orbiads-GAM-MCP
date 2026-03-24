# Steps

1. [start] Run `orbiads inventory keys --json` to list available targeting keys and values.
2. [depends: step 1] Select the targeting keys and values relevant to the campaign scope.
3. [depends: step 2] Run `orbiads inventory ad-units --id <id> --json` for each target ad unit to validate compatibility with the selected targeting.
4. [depends: step 3] Summarize the targeting configuration and confirm with the user.

## Abort Conditions

- Stop if no targeting keys exist — the network may need key creation via the web UI or MCP.
- Stop if ad units are incompatible with the selected targeting scope.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
