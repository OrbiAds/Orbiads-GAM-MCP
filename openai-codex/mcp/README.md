# MCP Configuration

## Purpose

- document how Codex/OpenAI workspace clients connect to the OrbiAds MCP server;
- keep local, remote, and fallback connection modes explicit.

## Topics to Cover

- local stdio configuration for development only;
- remote MCP configuration for shared environments;
- why ChatGPT connector mode uses the public `/mcp` endpoint directly instead of these workspace files;
- authentication and environment variables;
- smoke checks and rollback steps when a config changes.

## Included Files

- `config.json` — default remote `streamable-http` example;
- `config.stdio.json` — local dev-only stdio example.

## Boundary

- configuration only;
- no business workflow duplication here;
- ChatGPT connector setup lives in `../../docs/install/chatgpt.md`.