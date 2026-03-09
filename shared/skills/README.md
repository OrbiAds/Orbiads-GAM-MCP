# Shared Skills

## Purpose

- Host the canonical version of the business skills.
- Serve as the source of truth for Claude, OpenAI/Codex, and Gemini.

## Contract

- one folder per skill;
- each skill must contain `README.md`, `tools.md`, `steps.md`, `trigger.md`, `examples.md`, and `handoff.md`;
- wrappers must reference these folders instead of duplicating the business instructions.

## Available Skills

- Batch 1 foundation:
  - `bootstrap`
  - `inventory-ad-units`
  - `availability-forecast`
  - `deploy-reporting`
- Batch 2 trafficking and QA:
  - `advertiser-order-line-items`
  - `placements-targeting`
  - `native-image`
  - `qa-preview`

## Conventions

- use `_template/` to create the next real skills.
- keep names stable across `shared/skills/`, workflows, and wrappers.
- keep `trigger.md` concise so wrappers can route quickly without copying the full skill steps.
- route users to shared skills first, then to low-level tools only when needed.