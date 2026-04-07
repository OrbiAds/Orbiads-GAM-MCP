# OrbiAds CLI — Inventory

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- load `../../shared/agents/cli-inventory/` for routing and memory;
- execute `../../shared/skills/cli-inventory/` as the business source of truth;
- use this skill for inventory discovery, ad-unit audit, or targeting key lookup.

## Claude-Specific Hints

- use an artifact table to display ad units and sizes for user review;
- pipe JSON output through `jq` for filtering when result sets are large.
