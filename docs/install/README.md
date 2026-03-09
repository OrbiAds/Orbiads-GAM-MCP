# Installation by Platform

## Shared Prerequisites

- the real MCP server lives in `backend/src/mcp/server.py` and is mounted at `/mcp` in `backend/main.py` for `streamable-http` mode;
- supported transports are `streamable-http` (default), `sse`, and `stdio` (local development only);
- ChatGPT connector mode requires a public HTTPS `/mcp` endpoint and does not use `stdio`;
- remote mode expects Google OAuth environment variables such as `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `MCP_BASE_URL`;
- wrappers stay thin and must point back to `../../shared/agents/`, `../../shared/skills/`, `../../shared/prompts/`, `../../shared/examples/`, and `../../shared/schemas/`.

## Host Boundary

- filesystem wrappers apply when the host can load local packaging files such as `AGENTS.md`, manifests, routers, or extension descriptors;
- use `openai-codex/` when the goal is a simple local skill-like setup driven by `AGENTS.md`, `router.md`, and `skills/*.md`;
- ChatGPT connector mode relies on the remote MCP server plus connector metadata rather than local wrapper files;
- use Apps SDK only when ChatGPT also needs a packaged UI, not for the basic connector path.

## Recommended Startup

1. start the MCP server with `scripts/run-mcp.sh http` for the default remote path;
2. use `scripts/run-mcp.sh sse` only for SSE-capable clients;
3. use `scripts/run-mcp.sh stdio` only for local dev or smoke testing;
4. confirm that the wrapper routes through `shared/agents/orchestrator/` before entering a skill.

## Platform Guides

- `claude.md` — Claude plugin packaging, shared skill exposure, activation flow, and MCP configuration.
- `chatgpt.md` — ChatGPT / GPT-5.4 connector setup, execution environment, and MCP discovery guidance.
- `openai-codex.md` — `AGENTS.md`, router, skill wrappers, and separate MCP wiring for Codex/OpenAI flows.
- `gemini.md` — Gemini extension packaging, function declarations, and direct MCP fallback mode.

## Common Smoke Checks

- bootstrap first and confirm `tenantId` plus `networkCode`;
- validate that the client reaches `http://localhost:8080/mcp` in remote mode;
- for ChatGPT, confirm connector creation exposes the advertised tool list from the public `/mcp` endpoint;
- stop before writes unless the shared skill explicitly reaches a confirmed execution step;
- require preview, QA, and reporting guardrails from `../safety/README.md` before live actions.

## Rule

- Each guide must cover authentication, MCP transport, guardrails, and operational troubleshooting.