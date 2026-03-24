# CLI Creatives — Upload & Management

## Purpose

- List existing creatives in the GAM network.
- Upload new creative assets (images, HTML5 bundles).
- Verify that creatives are properly created and associated.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.
- Creative asset files accessible from the local filesystem.

## Expected Output

- List of creatives with IDs, names, and statuses.
- Confirmation of newly uploaded creatives.

## Guardrails

- Always use `--json` flag for structured output.
- Creative upload costs 5 credits — confirm with user before proceeding.
- Verify file paths exist before attempting upload.
