# Steps

1. [start] Run `orbiads creatives list --json` to see existing creatives, or `--search` to filter.
2. [depends: step 1] If a new creative is needed, confirm the file path, name, and advertiser ID with the user.
3. [depends: step 2] Run `orbiads creatives upload --file <path> --name "<name>" --advertiser <id> --json` after user confirmation (costs 5 credits).
4. [depends: step 3] Run `orbiads creatives get --id <id> --json` to verify the creative was created successfully.

## Abort Conditions

- Stop if the file path does not exist.
- Stop if credit balance is insufficient for upload (5 credits).
- Stop if the user declines the upload.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
