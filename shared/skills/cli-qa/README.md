# CLI QA — Pre-Deploy Validation

## Purpose

- Validate campaign configuration before deployment.
- Check creative coverage, targeting, and overall readiness.
- Run dry-run deployment to catch issues before going live.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.
- Campaign ID with creatives and targeting already configured.

## Expected Output

- Campaign configuration summary.
- Creative coverage validation results.
- Dry-run deployment output with any warnings or errors.

## Guardrails

- Always use `--json` flag for structured output.
- Dry-run mode (`--dry-run`) is free and safe — always run it before real deployment.
- Do not proceed to deployment if dry-run shows errors.
