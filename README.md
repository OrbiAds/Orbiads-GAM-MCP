# OrbiAds — Google Ad Manager MCP

[![MCP Protocol](https://img.shields.io/badge/MCP-2025--03--26-blue)](https://modelcontextprotocol.io)
[![GAM API](https://img.shields.io/badge/GAM_API-v202602-orange)](https://developers.google.com/ad-manager/api/rel_notes)
[![Version](https://img.shields.io/badge/version-1.1.0-green)](./version.json)
[![CLI](https://img.shields.io/badge/CLI-pip_install_orbiads--cli-brightgreen)](./docs/install/cli.md)
[![Works with Claude](https://img.shields.io/badge/Claude-✓-purple)](./docs/install/claude.md)
[![Works with ChatGPT](https://img.shields.io/badge/ChatGPT-✓-teal)](./docs/install/chatgpt.md)
[![Works with Gemini](https://img.shields.io/badge/Gemini-✓-blue)](./docs/install/gemini.md)

**A skill for Claude, ChatGPT, Gemini, and OpenAI Codex that gives your AI assistant direct access to Google Ad Manager.**

[**→ Get started free at orbiads.com**](https://orbiads.com) · [**★ Star this repo**](https://github.com/OrbiAds/Orbiads-GAM-MCP)

---

## Two Ways to Connect

OrbiAds offers two integration methods — choose the one that fits your workflow.

### Option A: MCP Server (AI agents)

Connect your AI assistant (Claude, ChatGPT, Gemini) to GAM via the hosted MCP endpoint. Conversational, guided, zero-install.

```
MCP endpoint: https://orbiads.com/mcp
```

### Option B: CLI (terminal & scripts)

A lightweight Python CLI for developers, CI/CD pipelines, and headless automation. Same API, same credits, same guardrails.

```bash
pip install orbiads-cli
orbiads auth login
orbiads network info
```

### Comparison

| Criteria | MCP Server | CLI |
| --- | --- | --- |
| Interface | AI agent (Claude, ChatGPT, Gemini) | Terminal / command line |
| Installation | URL to paste into agent settings | `pip install orbiads-cli` |
| Authentication | OAuth via browser (automatic) | OAuth Device Flow (code displayed) |
| Best for | Exploration, conversations, guided workflows | Scripts, CI/CD, headless automation |
| Output format | Natural language via the agent | JSON or structured table |
| Credits | Same consumption grid | Same consumption grid |
| Offline | No — requires internet | No — requires internet |
| Python required | No | Yes (3.10+) |

> Both methods share the same backend, credits, and safety guardrails.

### CLI Quick Reference

| Command | Description |
| --- | --- |
| `orbiads auth login` | Authenticate via Google OAuth Device Flow |
| `orbiads auth status` | Check authentication status |
| `orbiads network info` | Show current GAM network details |
| `orbiads network list` | List accessible GAM networks |
| `orbiads orders list` | List orders in the network |
| `orbiads line-items list --order ID` | List line items for an order |
| `orbiads creatives list` | List creatives |
| `orbiads inventory ad-units` | List ad units |
| `orbiads forecast check --ad-unit ID` | Check inventory availability |
| `orbiads report run --template ID` | Run a delivery report |

> Full command reference: [orbiads.com/docs/cli/commands](https://orbiads.com/docs/cli/commands)

---

## Install the skill

**Claude Code (CLI)** — one command:

```bash
claude plugin install orbiads
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

**Other tools (Codex, Cursor, Gemini CLI)** — copy [`AGENTS.md`](./AGENTS.md) to your workspace root and add the MCP endpoint to your config

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
| **Claude** (Desktop / claude.ai / Claude Code) | [docs/install/claude.md](./docs/install/claude.md) | Plugin + MCP remote |
| **ChatGPT** (Pro connector) | [docs/install/chatgpt.md](./docs/install/chatgpt.md) | MCP remote (HTTP) |
| **Gemini** | [docs/install/gemini.md](./docs/install/gemini.md) | MCP remote |
| **Cursor / Codex / Warp / other** | [AGENTS.md](./AGENTS.md) | AGENTS.md + MCP wiring |

All platforms connect to the same hosted MCP endpoint at `https://orbiads.com/mcp`.

---

## 5 Slash Commands

After installing the plugin, these `/adops` commands are available directly in Claude Code.

| Command | What it does |
| --- | --- |
| `/adops campaign` | Deploy, preview, pause, rollback — with mandatory forecast gate before any write |
| `/adops audit` | Multi-dimensional account audit: delivery, inventory, security, creatives, billing |
| `/adops report` | Custom reports, delivery queries, CSV export, billing summaries, forecasts |
| `/adops deal` | PMP deals, private auctions, Marketplace PG/PD proposals |
| `/adops creative` | Upload creatives, QA compliance, SSL validation, preview URLs, line item association |

## 27 Parent MCP Tools

The full GAM surface is organized into 27 parent tools, each dispatching multiple operations via an `action` discriminator. See [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md) for the complete matrix with 270 actions, costs, and write-status.

Key parents: `campaign`, `line_items`, `orders`, `creatives`, `creative_qa`, `creative_assets`, `reporting`, `inventory`, `deals`, `audit_skill`, `targeting`, `placements`, `companies`, `billing`, `settings`, `gam_admin`.

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
- [Other tools (Cursor, Codex, Warp) →](./AGENTS.md)

Then start with:

> *"Connect to my GAM account and show me my active networks"*

---

## MCP Server Details

| Property | Value |
| --- | --- |
| Endpoint | `https://orbiads.com/mcp` |
| Transport | `streamable-http` (default) · `sse` |
| Auth | OAuth 2.0 — Google account via OrbiAds |
| GAM API version | `v202602` |
| MCP Protocol | `2025-03-26` |

---

## Repository Structure

```text
skills/           ← 27 parent-tool sub-skills + orchestrator (generated from backend)
commands/         ← 5 /adops slash commands for Claude Code
agents/           ← Parallel audit subagents (audit-delivery, audit-inventory, …)
hooks/            ← Claude Code hooks (hooks.json)
cli/              ← OrbiAds CLI package (pip install orbiads-cli)
docs/             ← Installation guides, tool matrix, query library
_docs/            ← Internal: legacy tool mapping, anti-collision rules
.claude-plugin/   ← Claude plugin manifest (plugin.json, marketplace.json)
AGENTS.md         ← Cross-LLM contract for Cursor, Codex, Gemini, Warp, etc.
CLAUDE.md         ← Claude Code project guidance
```

> Skills and the tool matrix are **generated** from the backend catalogue — do not hand-edit them. See `CLAUDE.md` for the generated vs. hand-authored breakdown.

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

The contents of this repository — distribution scaffold, skills, agents, workflows, JSON schemas, CLI client, platform integration manifests, documentation, and examples — are released under the [MIT License](./LICENSE).

The OrbiAds MCP server backend and Cloud Run services that the hosted endpoint at `https://orbiads.com/mcp` connects to are NOT in this repository and are governed by separate proprietary terms — [see terms at orbiads.com](https://orbiads.com).
