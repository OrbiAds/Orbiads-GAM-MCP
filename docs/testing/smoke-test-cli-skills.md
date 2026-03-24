# Smoke Test — CLI Skills with AI Agents

Manual procedure to verify CLI skills work correctly when loaded by an AI agent.

## Prerequisites

1. `orbiads` CLI installed and authenticated (`orbiads auth status` returns authenticated)
2. CLI skills installed in the agent (e.g., `./install.sh skills --copy`)
3. A GAM network accessible via the authenticated account

## Test Procedure

### Test 1: Bootstrap (cli-bootstrap)

**Prompt:** "Check my GAM network status"

**Expected behavior:**
- Agent activates `cli-bootstrap` skill
- Runs `orbiads auth status --json`
- Runs `orbiads network info --json`
- Reports tenant ID, network code, and auth status

**Pass criteria:** Agent uses `orbiads` CLI commands (not MCP tools) and returns valid JSON results.

### Test 2: Inventory Discovery (cli-inventory)

**Prompt:** "List my ad units"

**Expected behavior:**
- Agent activates `cli-inventory` skill
- Runs `orbiads inventory ad-units --json`
- Displays ad units in a structured format

**Pass criteria:** Agent runs the correct CLI command and parses JSON output.

### Test 3: Deploy Dry-Run (cli-qa + cli-deploy)

**Prompt:** "Do a dry-run deployment check for campaign X"

**Expected behavior:**
- Agent activates `cli-qa` or `cli-deploy` skill
- Runs `orbiads campaigns deploy <id> --dry-run --json`
- Reports blockers or confirms readiness

**Pass criteria:** Agent uses `--dry-run` flag and presents results clearly.

## Transport Detection Test

**Prompt:** "Help me set up a GAM campaign" (with CLI installed)

**Expected behavior:**
- Agent reads `router.md`
- Detects CLI is available via `which orbiads` or `orbiads --version`
- Routes to `cli-*` skills instead of MCP skills

**Pass criteria:** Agent uses bash-based CLI commands, not MCP tool calls.

## Verification Checklist

- [ ] Agent detects CLI availability before choosing skill set
- [ ] Agent uses `--json` flag on all `orbiads` commands
- [ ] Agent parses JSON output correctly
- [ ] Agent does not mix MCP tool calls with CLI commands
- [ ] Handoff between CLI skills preserves session context
- [ ] Agent asks for confirmation before write operations (create, deploy)

## Platform-Specific Notes

### Claude Code
- Skills loaded from `~/.claude/skills/orbiads-cli-*/SKILL.md`
- Uses Bash tool to run CLI commands
- Verify with: `/skills` command in Claude Code

### OpenAI Codex
- Skills referenced via `AGENTS.md` → `router.md` → `skills/cli-*.md`
- Uses shell execution for CLI commands

### Gemini CLI
- Skills referenced via `router.md` → `skills/cli-*.md`
- Uses shell execution for CLI commands
