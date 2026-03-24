# CLI Forecast — Availability

## Purpose

- Run availability forecasts to check whether supply is sufficient for a planned delivery scope.
- Analyze forecast results to guide campaign sizing decisions.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.
- Known ad unit IDs (from `cli-inventory`).

## Expected Output

- Forecast data: available impressions, matched, possible, contending line items.
- Actionable recommendation on whether to proceed with the planned scope.

## Guardrails

- Always use `--json` flag for structured output.
- Forecasts are read-only but may consume credits depending on complexity.
- Document assumptions (date range, targeting, ad units) in the output.
