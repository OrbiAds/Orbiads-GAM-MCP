# OpenAI / Codex Installation

## Scope

- use `AGENTS.md` as the persistent instruction layer;
- orient the model locally with a simple skill-like file layout similar to Claude-style skill loading;
- reference the shared business skills separately from platform glue;
- support local or remote MCP connections.

## Boundary

- use this guide for Codex/OpenAI workspaces that can load `AGENTS.md`, router files, and local wrapper assets;
- use this path when you want local file-based guidance instead of a remote ChatGPT connector flow;
- use `chatgpt.md` when the host is ChatGPT or GPT-5.4 running through a connector;
- do not treat `mcp/config.stdio.json` as a ChatGPT deployment path.

## Asset Map

- `../../openai-codex/AGENTS.md` — persistent operating rules;
- `../../openai-codex/router.md` — intent to skill routing;
- `../../openai-codex/mcp/config.json` — remote `streamable-http` example;
- `../../openai-codex/mcp/config.stdio.json` — local dev-only stdio example;
- `../../openai-codex/skills/*.md` and `../../openai-codex/examples/*.md` — thin skill aliases and prompt examples.

## Recommended Local Skill Model

- keep `AGENTS.md` as the persistent local steering layer;
- use `router.md` to map user intent to the smallest useful skill wrapper;
- keep one thin file in `skills/` per shared business skill;
- keep the real business behavior in `../../shared/agents/` and `../../shared/skills/`.

## Installation Topics to Cover

- MCP configuration examples per environment;
- mapping between common user prompts, shared skills, and expected outputs;
- explicit confirmation rules before any sensitive write;
- fallback behavior when direct skill guidance is insufficient.

## Recommended Steps

1. choose `mcp/config.json` for remote OAuth-backed usage or `mcp/config.stdio.json` for local dev only;
2. keep `AGENTS.md` and `router.md` in the active Codex/OpenAI workspace so the model sees the routing layer first;
3. load the matching file from `skills/` instead of embedding business logic directly in `AGENTS.md`;
4. keep `../shared/agents/` and `../shared/skills/` available as the canonical execution source;
5. validate bootstrap before any forecast, preview, deploy, or reporting request.

## Smoke Check

- run a bootstrap-only prompt that asks for tenant, credentials, and network confirmation;
- verify that the workspace can route from `router.md` to `skills/bootstrap.md` before any downstream skill;
- verify that the client hits `/mcp` in remote mode or starts `python -m src.mcp.server` in stdio mode;
- verify that the next prompt can reuse the same session fields without repeating bootstrap.

## Rollback

- revert the selected MCP config file first if connection behavior changes unexpectedly;
- keep `AGENTS.md` thin and restore the previous router if a skill misroutes;
- never patch around a routing bug by duplicating shared skill logic inside `AGENTS.md`.

## Guardrails

- prefer shared skills before low-level tool calls;
- keep `AGENTS.md` thin and use it to steer, not to duplicate business workflows;
- explain the plan before important actions;
- require availability checks, QA, and preview before activation;
- keep confirmation rules consistent with `../safety/README.md`;
- keep ChatGPT connector metadata and public-host guidance in `chatgpt.md`, not in this workspace-only guide.