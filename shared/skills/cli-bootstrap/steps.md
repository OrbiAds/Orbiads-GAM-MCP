# Steps

1. [start] Run `orbiads --version` to confirm the CLI is installed and reachable.
2. [depends: step 1] Run `orbiads auth status --json` to verify authentication. If not authenticated, instruct the user to run `orbiads auth login` in their browser.
3. [depends: step 2] Run `orbiads network info --json` to check the active network context.
4. [depends: step 3] If no network is active or the user wants a different one, run `orbiads network list --json` to show available networks, then `orbiads network switch --network-code <code> --json` after user confirmation.

## Abort Conditions

- Stop if CLI is not installed — instruct user to install with `pip install orbiads-cli`.
- Stop if authentication is missing — instruct user to run `orbiads auth login`.
- Stop if multiple networks and user has not chosen one.
