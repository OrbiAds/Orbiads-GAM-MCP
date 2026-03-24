# OrbiAds CLI — Orders

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- execute `../../shared/skills/cli-orders/` as the business source of truth;
- use this skill for advertiser, order, and line-item management.

## Claude-Specific Hints

- confirm advertiser and order details with user before any create command;
- use `<handoff>` tags to pass orderId and advertiserId to downstream skills.
