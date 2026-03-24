# CLI Targeting — Keys, Values & Ad Unit Qualification

## Purpose

- Explore and select targeting keys and values for campaign line items.
- Validate ad unit compatibility with the planned targeting scope.

## Prerequisites

- `orbiads` CLI installed and authenticated (run `cli-bootstrap` first).
- Active GAM network context.
- Known ad unit IDs (from `cli-inventory`).

## Expected Output

- Selected targeting keys and values.
- Validated ad unit compatibility.
- Targeting packet ready for line-item creation.

## Guardrails

- Always use `--json` flag for structured output.
- This skill is read-only; no targeting keys are created.
- Validate ad unit compatibility before handing off to deployment.
