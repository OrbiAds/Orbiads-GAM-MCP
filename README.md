# OrbiAds — Google Ad Manager MCP

[![MCP Protocol](https://img.shields.io/badge/MCP-2025--03--26-blue)](https://modelcontextprotocol.io)
[![GAM API](https://img.shields.io/badge/GAM_API-v202602-orange)](https://developers.google.com/ad-manager/api/rel_notes)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](./version.json)
[![Works with Claude](https://img.shields.io/badge/Claude-✓-purple)](./docs/install/claude.md)
[![Works with ChatGPT](https://img.shields.io/badge/ChatGPT-✓-teal)](./docs/install/chatgpt.md)
[![Works with Gemini](https://img.shields.io/badge/Gemini-✓-blue)](./docs/install/gemini.md)

**A skill for Claude, ChatGPT, Gemini, and OpenAI Codex that gives your AI assistant direct access to Google Ad Manager.**

[**→ Get started free at orbiads.com**](https://orbiads.com)

---

## Install the skill

**Claude Code (CLI)** — run in any Claude Code session:

```text
/install-github OrbiAds/Orbiads-GAM-MCP
```

**Claude Desktop** — add to `claude_desktop_config.json`:

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

**claude.ai** — Settings → Integrations → Add MCP server → `https://orbiads.com/mcp`

**ChatGPT** — Settings → Connectors → Create connector → MCP URL: `https://orbiads.com/mcp`

**Gemini / AI Studio** — Tools → MCP configuration → `https://orbiads.com/mcp`

**OpenAI Codex** — copy [`openai-codex/AGENTS.md`](./openai-codex/AGENTS.md) and [`openai-codex/mcp/config.remote.json`](./openai-codex/mcp/config.remote.json) to your workspace root

→ Full guides: [Claude](./docs/install/claude.md) · [ChatGPT](./docs/install/chatgpt.md) · [Gemini](./docs/install/gemini.md) · [OpenAI Codex](./docs/install/openai-codex.md)

---

## What is OrbiAds?

OrbiAds is a hosted **MCP server** that connects your AI assistant directly to Google Ad Manager (GAM). Instead of clicking through the GAM interface or writing API scripts, you describe what you want in plain language — OrbiAds handles the API calls, guardrails, and audit trail.

```text
You: "Check inventory availability on the homepage banner for a 300x250 in France next week"
OrbiAds: [runs forecast] → Available: 1.2M impressions. Pressure: low. Safe to traffic.

You: "Create the line item for Renault, €15 CPM, Monday to Friday"
OrbiAds: [applies guardrails] → Preview ready. Confirm to push?
```

No scripts. No API tokens to manage. No switching tabs.

---

## Who is this for?

- **AdOps managers** who traffic campaigns daily and want to move faster without making mistakes
- **Publishers** who manage their own GAM network and want AI-assisted workflows
- **Media agencies** running multiple GAM accounts who want a consistent, auditable process
- **Developers** building AdOps automation on top of Claude, ChatGPT, or Gemini

---

## Supported AI Platforms

| Platform | Setup guide | Mode |
| --- | --- | --- |
| **Claude** (Desktop / claude.ai) | [docs/install/claude.md](./docs/install/claude.md) | Plugin + MCP remote |
| **ChatGPT** (Pro connector) | [docs/install/chatgpt.md](./docs/install/chatgpt.md) | MCP remote (HTTP) |
| **Gemini** | [docs/install/gemini.md](./docs/install/gemini.md) | Extension + MCP fallback |
| **OpenAI Codex** | [docs/install/openai-codex.md](./docs/install/openai-codex.md) | AGENTS.md + MCP wiring |

All platforms connect to the same hosted MCP endpoint at `https://orbiads.com/mcp`.

---

## 8 Built-in Skills

Each skill is a guided, guardrailed workflow. Your AI assistant loads them on demand.

| Skill | What it does |
| --- | --- |
| `bootstrap` | Connect your GAM account, verify credentials, select network |
| `inventory-ad-units` | Browse and query ad units, placements, and targeting keys |
| `availability-forecast` | Check inventory availability before trafficking — no writes |
| `advertiser-order-line-items` | Create and manage advertisers, orders, and line items |
| `placements-targeting` | Build and verify targeting configurations |
| `native-image` | Traffic native and image creatives with inline upload |
| `qa-preview` | Preview and coverage check before any live push |
| `deploy-reporting` | Deploy with dry-run protection + post-push delivery reports |

---

## 5 Composed Workflows

End-to-end workflows that chain skills automatically.

| Workflow | Description |
| --- | --- |
| `inventory-to-placement` | From ad unit discovery to targeting-ready placement |
| `image-to-native` | Upload image → create native creative → traffic line item |
| `image-to-html5` | Same flow for HTML5 display creatives |
| `audio-video-trafficking` | Audio/video line item setup with format guardrails |
| `deploy-to-reporting` | Push campaign + monitor delivery + generate report |

---

## Safety by Design

Every write action requires explicit confirmation. No campaign goes live by accident.

- **Dry-run mode** on all deployment actions — preview before you push
- **Forecast gate** before inventory commits — availability verified upfront
- **Audit trail** on every action — who did what, when, with what result
- **Credit guard** — read operations are always free, writes deduct credits transparently

---

## Quick Start (3 steps)

### 1. Create your free account

Go to [orbiads.com](https://orbiads.com) and sign up. You get **5 free credits** — no credit card required.

### 2. Connect Google Ad Manager

From the OrbiAds dashboard, click **Connect GAM** and authorize with your Google account. OrbiAds uses OAuth — your GAM credentials never leave Google's infrastructure.

### 3. Configure your AI assistant

Pick your platform and follow the guide:

- [Claude setup →](./docs/install/claude.md)
- [ChatGPT setup →](./docs/install/chatgpt.md)
- [Gemini setup →](./docs/install/gemini.md)
- [OpenAI Codex setup →](./docs/install/openai-codex.md)

Then start with:

> *"Connect to my GAM account and show me my active networks"*

---

## MCP Server Details

| Property | Value |
| --- | --- |
| Endpoint | `https://orbiads.com/mcp` |
| Transport | `streamable-http` (default) · `sse` · `stdio` (local dev only) |
| Auth | OAuth 2.0 — Google account via OrbiAds |
| GAM API version | `v202602` |
| MCP Protocol | `2025-03-26` |

---

## Repository Structure

```text
shared/           ← Canonical skills, agents, prompts, workflows, JSON schemas
docs/             ← Installation guides, safety rules, tool matrix, query library
claude-plugin/    ← Claude plugin packaging (manifest, system prompt, router)
openai-codex/     ← AGENTS.md + router for OpenAI/Codex workspaces
gemini-extension/ ← Gemini extension descriptor + function declarations
```

> Business logic lives in `shared/`. Platform wrappers are thin adapters that point back to it.

---

## Pricing

| Plan | Price | Credits |
| --- | --- | --- |
| Trial | Free | 5 credits (no card) |
| Starter | €39/month | 50 credits/month |
| Early Access | **€29/month** ← locked for life | 50 credits/month |
| Pack S | €29 one-time | +50 credits |
| Pack L | €45 one-time | +100 credits |

Reads are always free. Credits are only consumed on write and deploy operations.

[**Start free →**](https://orbiads.com)

---

## License

This repository contains the MCP distribution scaffold and platform integration guides for OrbiAds.
The OrbiAds MCP server and backend are proprietary — [see terms at orbiads.com](https://orbiads.com).
