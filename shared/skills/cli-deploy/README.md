# CLI Deploy & Reporting

## Purpose

- Deploy GAM campaigns via the CLI with non-interactive confirmation.
- Poll deployment status until completion.
- Run post-deployment delivery reports to verify campaign health.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.
- Campaign QA passed (run `cli-qa` first).

## Expected Output

- Deployment confirmation with job ID.
- Final campaign status after polling.
- Post-deploy delivery report data.

## Guardrails

- Always run `--dry-run` first via `cli-qa` before real deployment.
- Use `--yes` flag for non-interactive deployment (skips confirmation prompt).
- Always use `--json` flag for structured output.
- Deployment costs 5 credits — confirm with user before proceeding.
- Poll with reasonable intervals (5-10 seconds) to avoid excessive API calls.
