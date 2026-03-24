# Steps

1. [start] Run `orbiads campaigns get <id> --json` to inspect the full campaign configuration.
2. [depends: step 1] Verify that creatives are associated. Run `orbiads creatives get --id <id> --json` for each creative to check compliance and SSL status.
3. [depends: step 2] Run `orbiads campaigns deploy <id> --dry-run --json` to simulate deployment and surface any warnings or errors.
4. [depends: step 3] Summarize findings: list any blocking issues, warnings, and the overall go/no-go recommendation.

## Abort Conditions

- Stop if the campaign does not exist or has no line items.
- Stop if dry-run returns blocking errors — list them for the user.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
