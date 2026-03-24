# OrbiAds CLI — Bootstrap

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- execute `../../shared/skills/cli-bootstrap/` as the business source of truth;
- use this skill when `tenantId` or `networkCode` is still unconfirmed.

## Claude-Specific Hints

- run `orbiads --version` first to confirm CLI is available;
- use `orbiads auth status --json` and parse the JSON to check auth state;
- show network selection as a table artifact when multiple networks are available.
