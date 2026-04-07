# OrbiAds CLI — QA

Use the Bash tool to run `orbiads` commands. Always use `--json` flag for structured output.

- load `../../shared/agents/cli-qa/` for routing and memory;
- execute `../../shared/skills/cli-qa/` as the business source of truth;
- use this skill for compliance checks and dry-run validation before deployment.

## Claude-Specific Hints

- present dry-run results as a checklist artifact with pass/fail per check;
- apply extended thinking to evaluate whether blockers are real or warnings only.
