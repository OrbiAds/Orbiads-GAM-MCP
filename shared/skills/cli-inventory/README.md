# CLI Inventory — Ad Units

## Purpose

- Explore the GAM inventory: ad units, placements, sizes, and targeting keys.
- Qualify ad units needed for downstream workflows (targeting, forecasting, orders).

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.

## Expected Output

- List of ad units matching the user's criteria.
- Available sizes and targeting keys for selected ad units.
- Confirmed `adUnitIds` ready for downstream skills.

## Guardrails

- Always use `--json` flag for structured output.
- Use `--search` to filter results rather than listing everything.
- This skill is read-only; no ad units are created or modified.
