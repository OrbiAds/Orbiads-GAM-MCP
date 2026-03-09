# OpenAI / Codex Wrapper

## Role

- package the Codex/OpenAI workspace-specific instruction and MCP config layer;
- provide the simplest local skill-like steering model for OpenAI-compatible workspaces;
- expose the shared skills and shared agents without duplicating AdOps logic;
- keep prompt examples small, portable, and tool-accurate.

## Boundary

- use this wrapper when the host can read local `AGENTS.md` and router files;
- use this wrapper when you want a local `AGENTS.md` + `router.md` + `skills/*.md` flow similar to Claude skill discovery;
- use `../docs/install/chatgpt.md` for ChatGPT connector installation instead of this workspace wrapper.

## Included Assets

- `AGENTS.md`
- `mcp/config.json`
- `mcp/config.stdio.json`
- `router.md`
- `skills/*.md`
- `examples/*.md`