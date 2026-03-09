# Claude Installation

## Scope

- package the Claude-facing plugin assets;
- wire Claude to the OrbiAds MCP server;
- expose the shared skills without duplicating business content.

## Asset Map

- `../../claude-plugin/plugin/manifest.json` — wrapper descriptor;
- `../../claude-plugin/plugin/system-prompt.md` — thin Claude platform layer;
- `../../claude-plugin/plugin/activation.md` — entry routing hints;
- `../../claude-plugin/router.md` — skill dispatch;
- `../../claude-plugin/agents/orchestrator.md` and `../../claude-plugin/skills/*.md` — bridges to the shared layer.

## Recommended Wrapper Model

- keep the Claude wrapper thin;
- keep the canonical business instructions in `../../shared/skills/`;
- use filesystem-based skills for discovery and on-demand loading;
- keep examples and optional resources small and platform-specific;
- avoid copying workflow logic into the plugin package.

## Installation Topics to Cover

- Claude-side plugin packaging format;
- expected MCP server configuration (`streamable-http` first, `stdio` only for local fallback);
- skill discovery and activation rules;
- update and rollback procedure for packaged assets.

## Recommended Steps

1. start the MCP server with `scripts/run-mcp.sh http` or `cd backend && python -m src.mcp.server`;
2. load the wrapper files from `../../claude-plugin/` and keep `../../shared/` mounted as the source of truth;
3. route the first user turn through `../../claude-plugin/router.md` and `../../shared/agents/orchestrator/`;
4. confirm bootstrap state before any workflow that can write or spend credits.

## Smoke Check

- ask Claude to confirm the active tenant and GAM network only;
- expect the route to land in `bootstrap` without touching write paths;
- verify that follow-up turns can move to another thin skill wrapper while keeping the same session packet.

## Rollback

- revert only the wrapper assets in `../../claude-plugin/`;
- keep `../../shared/` unchanged unless the business contract itself is wrong;
- if routing regresses, fall back to the previous manifest plus router pair and retest bootstrap.

## Guardrails

- route users to shared skills first, then to low-level tools only when needed;
- require preview, QA, and confirmation before real writes;
- keep safety rules aligned with `../safety/README.md`.