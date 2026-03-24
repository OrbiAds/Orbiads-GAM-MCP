# Steps

1. [start] Run `orbiads inventory ad-units --json` to discover the full ad-unit catalog, or use `--search` to filter.
2. [depends: step 1] Identify the relevant ad units for the user's workflow. Note their IDs and sizes.
3. [depends: step 1] Run `orbiads inventory placements --json` if the user needs placement information.
4. [depends: step 1] Run `orbiads inventory keys --json` to list available targeting keys and values.
5. [depends: steps 1-4] Return the selected `adUnitIds`, sizes, and targeting keys to the user.

## Abort Conditions

- Stop if no ad units match the search criteria — suggest broadening the search.
- Stop if the network context is not initialized — route to `cli-bootstrap`.
