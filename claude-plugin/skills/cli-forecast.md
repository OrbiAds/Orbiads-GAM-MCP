# OrbiAds CLI — Forecast

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- load `../../shared/agents/cli-forecast/` for routing and memory;
- execute `../../shared/skills/cli-forecast/` as the business source of truth;
- use this skill to check supply availability before deployment.

## Claude-Specific Hints

- present forecast results as an artifact table with available vs requested impressions;
- apply extended thinking before recommending whether supply is sufficient.
