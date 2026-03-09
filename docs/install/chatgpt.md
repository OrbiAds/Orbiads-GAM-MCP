# ChatGPT Installation

## Scope

- connect ChatGPT and GPT-5.4-style chat sessions to the OrbiAds MCP server through a remote connector;
- explain the execution environment ChatGPT uses for MCP discovery and tool calling;
- document when a connector is enough and when Apps SDK should be added.

## Asset Map

- `backend/main.py` — mounts the MCP endpoint at `/mcp` for `streamable-http` mode;
- `backend/src/mcp/server.py` — real MCP server and tool registry;
- `../../shared/skills/` and `../../shared/agents/` — canonical business behavior that tool descriptions and approvals must stay aligned with;
- `../safety/README.md` — confirmation, preview, QA, and reporting guardrails.

## ChatGPT Execution Environment

- ChatGPT connects to a public HTTPS MCP endpoint;
- tool discovery comes from the connector metadata plus the MCP-advertised tool surface;
- ChatGPT does not rely on local `AGENTS.md`, local router files, or `stdio` startup scripts;
- if the real goal is local file-based skill steering, prefer the `openai-codex/` workspace wrapper instead of ChatGPT;
- use Apps SDK only when ChatGPT also needs a packaged UI or richer app presentation.

## Recommended Steps

1. deploy or expose the backend so ChatGPT can reach `https://<public-host>/mcp` over HTTPS;
2. keep the server on `streamable-http` for the primary path and use a tunnel only for local development;
3. enable ChatGPT developer mode if your workspace requires it, then open `Settings -> Connectors -> Create`;
4. enter a connector name and description that clearly explain when OrbiAds should be used;
5. verify the advertised tool list before any real workflow, then start with bootstrap-only prompts;
6. add Apps SDK later only if the connector needs UI, rich components, or app-specific packaging.

## Connector Metadata Guidelines

- choose a connector name that sounds like a business capability, not a generic model helper;
- write the description around user intent such as tenant bootstrap, inventory audit, forecast checks, QA, and reporting;
- say when the connector should not be used, especially for unconfirmed writes or out-of-scope requests;
- keep the exposed tool surface narrow enough that ChatGPT can route reliably.

## Smoke Check

- create the connector and confirm ChatGPT lists the tools exposed by the public `/mcp` endpoint;
- ask ChatGPT to confirm only `tenantId` and `networkCode`, and expect a bootstrap-style path first;
- run one read-only inventory or forecast preparation request before any write candidate;
- confirm that activation-style requests still require preview, QA, and explicit approval.

## Rollback

- disable or remove the ChatGPT connector first if routing becomes unstable;
- revert the public MCP endpoint or connector metadata before touching shared business docs;
- keep Codex/OpenAI workspace docs separate instead of mixing ChatGPT fixes into `AGENTS.md`.

## Guardrails

- never point production ChatGPT usage at `stdio` or a local-only endpoint;
- keep connector name, description, and tool descriptions concise because they drive model discovery;
- preserve read/write boundaries and require explicit confirmation before real writes;
- keep auth and tenant scoping server-side because ChatGPT does not inherit local workspace context.