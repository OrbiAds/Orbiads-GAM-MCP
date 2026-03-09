# Claude Wrapper

## Role

- package the Claude-facing plugin assets;
- reference the shared skills;
- document Claude-specific MCP setup and activation flow.

## Included Assets

- `plugin/manifest.json` — wrapper packaging manifest for this scaffold;
- `plugin/system-prompt.md` — thin Claude system layer;
- `plugin/activation.md` — fast routing and activation hints;
- `router.md` — skill and workflow dispatch map;
- `agents/orchestrator.md` — Claude-facing entrypoint to `../shared/agents/orchestrator/`;
- `skills/*.md` — thin wrapper aliases over `../../shared/skills/`;
- `examples/*.md` — Claude-ready prompts and response shapes.

## Boundary

- no duplication of business content;
- packaging, discovery, and Claude-oriented examples only.