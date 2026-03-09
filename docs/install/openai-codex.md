# Install on OpenAI Codex

OrbiAds is a **skill for OpenAI Codex** — it gives Codex access to your Google Ad Manager account via `AGENTS.md` and a remote MCP config.

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- OpenAI Codex with MCP support

---

## Step 1 — Copy files to your workspace root

From this repository, copy two files into the **root of your Codex workspace**:

```
openai-codex/AGENTS.md                →  AGENTS.md    (workspace root)
openai-codex/mcp/config.remote.json   →  .mcp.json    (workspace root)
```

`AGENTS.md` tells Codex what OrbiAds can do and how to use the skills.
`.mcp.json` points Codex to the hosted OrbiAds MCP server.

---

## Step 2 — Verify .mcp.json

```json
{
  "mcpServers": {
    "orbiads": {
      "type": "http",
      "url": "https://orbiads.com/mcp"
    }
  }
}
```

No changes needed. Codex handles OAuth on first use.

---

## Step 3 — Test

Open a Codex session in your workspace:

> *"Connect to my GAM account"*

Codex reads `AGENTS.md`, connects to `https://orbiads.com/mcp`, and runs the bootstrap skill.

---

## Optional — Per-skill files

Copy `openai-codex/skills/` to your workspace root for richer per-skill instructions.

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Your GAM networks |
| *"Check inventory on the homepage 300x250 next week"* | An availability forecast |
