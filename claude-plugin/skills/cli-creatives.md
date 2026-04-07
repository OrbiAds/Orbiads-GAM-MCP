# OrbiAds CLI — Creatives

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- load `../../shared/agents/cli-creatives/` for routing and memory;
- execute `../../shared/skills/cli-creatives/` as the business source of truth;
- use this skill for creative listing, upload, and management.

## Claude-Specific Hints

- show creative payload as an artifact before upload — one human approval required;
- never upload without explicit user confirmation of asset and destination URL.
