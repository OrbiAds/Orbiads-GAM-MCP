# OrbiAds CLI — Deploy

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- load `../../shared/agents/cli-deploy/` for routing and memory;
- execute `../../shared/skills/cli-deploy/` as the business source of truth;
- use this skill for campaign deployment, monitoring, and reporting.

## Claude-Specific Hints

- always run `--dry-run` before real deployment and show results as an artifact;
- after deploy, poll with `orbiads campaigns get <id> --json` until status is final;
- use `<handoff>` tags to pass deployment status and jobId to the user.
