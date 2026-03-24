# CLI Bootstrap & Network

## Purpose

- Verify that the OrbiAds CLI is installed, authenticated, and connected to a GAM network.
- Confirm the active network context before any downstream CLI workflow.

## Prerequisites

- `orbiads` CLI installed (`pip install orbiads-cli`).
- A terminal with Bash tool access.
- GAM credentials already configured via `orbiads auth login` (browser-based).

## Inputs

- None required; the CLI reads stored credentials automatically.
- Optionally a `--network-code` if multiple networks are accessible.

## Expected Output

- CLI version confirmed.
- Authentication status verified.
- Active GAM network identified and ready.

## Guardrails

- Run `orbiads --version` before any other command.
- Do not switch networks without explicit user confirmation.
- Always use `--json` flag for structured, parseable output.
