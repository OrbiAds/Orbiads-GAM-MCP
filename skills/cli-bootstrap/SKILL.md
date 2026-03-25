---
description: "Verify OrbiAds CLI is installed, authenticated, and connected to a GAM network. Use when setup or connection check is needed."
---

# OrbiAds CLI — Bootstrap

Verify the OrbiAds CLI is installed, authenticated, and connected to the correct GAM network before running any other CLI skill.

Requires `orbiads` CLI (`pip install orbiads-cli`). All commands use `--json` for structured output. Use the Bash tool to execute.

## Commands

- `orbiads --version` `[free]` — print the installed CLI version
- `orbiads auth status --json` `[free]` — check authentication state and active tenant
- `orbiads network info --json` `[free]` — show the currently active GAM network context and tenant configuration
- `orbiads network list --json` `[free]` — list all accessible GAM networks for this tenant
- `orbiads network switch --network-code <code> --json` `[free]` — switch to a different GAM network

## Steps

1. [start] Run `orbiads --version` to confirm the CLI is installed.
2. [depends: step 1] Run `orbiads auth status --json`. If not authenticated, tell user to run `orbiads auth login`.
3. [depends: step 2] Run `orbiads network info --json` to check active network.
4. [depends: step 3] If no network or user wants a different one, run `orbiads network list --json` then `orbiads network switch --network-code <code> --json` after user choice.
5. [depends: step 3] Optionally read `orbiads network info --json` output to confirm tenant configuration is active (naming conventions, delivery defaults, campaign presets). This confirms the backend will apply the user's settings when creating entities in subsequent skills.

## Abort Conditions

- CLI not installed: tell user to run `pip install orbiads-cli`.
- Auth missing or expired: tell user to run `orbiads auth login`.
- Multiple networks available and user hasn't chosen: stop and ask user which network to use.

## Output

Active network code, tenant ID, authentication status, and tenant configuration summary. Ready for any subsequent CLI skill.
