# OrbiAds — Google Ad Manager MCP

[English](README.md) · [Français](README.fr.md)

![OrbiAds Terminal Mockup](./logo/terminal_mockup.png)

[![MCP Protocol](https://img.shields.io/badge/MCP-2025--03--26-blue)](https://modelcontextprotocol.io)
[![GAM API](https://img.shields.io/badge/GAM_API-v202605-orange)](https://developers.google.com/ad-manager/api/rel_notes)
[![Version](https://img.shields.io/badge/version-1.7.0-green)](./version.json)
[![CLI](https://img.shields.io/badge/CLI-pip_install_orbiads--cli-brightgreen)](./docs/install/cli.md)
[![Works with Claude](https://img.shields.io/badge/Claude-✓-purple)](./docs/install/claude.md)
[![Works with ChatGPT](https://img.shields.io/badge/ChatGPT-✓-teal)](./docs/install/chatgpt.md)
[![Works with Gemini](https://img.shields.io/badge/Gemini-✓-blue)](./docs/install/gemini.md)
[![GLAMA Registry](https://img.shields.io/badge/GLAMA-Registry-blue)](https://glama.ai/mcp/servers/OrbiAds/Orbiads-GAM-MCP)

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

> [!IMPORTANT]
> **Windows/macOS/Linux PATH Warning**: If you install the CLI via `pip` (especially with `--user`), ensure the Python scripts directory is added to your user `PATH`. Without this, your terminal and local AI agents (like Claude Code, Cursor, or Gemini) will fail to find or execute the `orbiads` command. See the [Troubleshooting section in the CLI Guide](docs/install/cli.md#troubleshooting) for quick setup commands.

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

## Installation Guide

OrbiAds offers three integration pathways depending on your environment.

### 1. Zero-Install MCP Server (ChatGPT, Gemini, Claude Desktop)
Connect your AI assistant to our hosted server using the Model Context Protocol:
- **Claude Desktop**: Add this to your `claude_desktop_config.json`:
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
- **Gemini / AI Studio**: Go to Tools → MCP configuration → Add `https://orbiads.com/mcp`
- **ChatGPT**: Go to Settings → Connectors → Add connector → MCP URL: `https://orbiads.com/mcp`
- **GLAMA / MCP Registry**: Access, test, and connect the server directly in your browser via [glama.ai/mcp/servers/OrbiAds/Orbiads-GAM-MCP](https://glama.ai/mcp/servers/OrbiAds/Orbiads-GAM-MCP)
- **Other environments (Cursor, Codex, Warp)**: Add the `https://orbiads.com/mcp` endpoint to your configuration and copy [`AGENTS.md`](./AGENTS.md) to your project root.

### 2. Claude Code Plugin (Slash Commands)
Add the `/adops` command set directly into your Claude Code CLI terminal:
```bash
claude plugin install orbiads
```

### 3. Agent Skills (Structured Workflows)
Install our markdown-based guidelines permanently into Claude Code's memory:
1. Clone this repository locally.
2. Run the skill installer:
   ```bash
   ./install.sh skills --copy
   ```
This copies our 6 consolidated skill files to your `~/.claude/skills/` directory. Claude Code will automatically leverage them to prevent hallucinations and strictly apply the plan-before-mutate workflow.

→ Installation guides: [Claude](./docs/install/claude.md) · [ChatGPT](./docs/install/chatgpt.md) · [Gemini](./docs/install/gemini.md) · [OpenAI Codex](./docs/install/openai-codex.md)

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
| **GLAMA** (MCP registry) | [glama.ai/mcp/servers/OrbiAds/Orbiads-GAM-MCP](https://glama.ai/mcp/servers/OrbiAds/Orbiads-GAM-MCP) | MCP registry |
| **Cursor / Codex / Warp / other** | [AGENTS.md](./AGENTS.md) | AGENTS.md + MCP wiring |

All platforms connect to the same hosted MCP endpoint at `https://orbiads.com/mcp`.

---

## 5 Slash Commands

After installing the plugin, these `/adops` commands are available directly in Claude Code.

| Command | What it does |
| --- | --- |
| `/adops campaign` | Read live state, plan deployment, dry-run (`ExecutionPlan`), deploy, pause, rollback — with mandatory plan→confirm→execute gate |
| `/adops audit` | Multi-dimensional account audit: delivery, inventory, security, creatives, billing |
| `/adops report` | Custom reports, delivery queries, CSV export, billing summaries, forecasts |
| `/adops deal` | PMP deals, private auctions, Marketplace PG/PD proposals |
| `/adops creative` | Upload creatives, QA compliance, SSL validation, preview URLs, line item association |

## What's Inside (MCP Tools & Skills)

The OrbiAds surface maps the Google Ad Manager API into **28 parent tools** and **270+ actions**, consolidated into **6 core Agent Skills** to keep context usage clean.

Click on any domain below to see which tools and capabilities are included:

<details>
<summary><b>1. Campaigns & Creative QA (orbiads-campaigns)</b></summary>

*   `campaign` — Read live campaign state, plan deployment, dry-run, deploy, pause, and rollback campaigns.
*   `orders` — Create and list orders, contacts, and roles.
*   `line_items` — Define line item delivery rules, CPMs, and targeting logic.
*   `creatives` — Upload creatives (images, HTML5, video/audio) and configure native styles.
*   `creative_assets` — Manage associated image and file assets.
*   `creative_qa` — Audit click-trackers, perform compliance scans, and validate SSL certificates.
*   `creative_wrapper_skill` — Manage third-party wrappers and delivery presets.
*   `formats` — Discover and configure ad creative formats.
*   `jobs` & `gam_jobs` — Monitor async campaign compilation and deployment workflows.
</details>

<details>
<summary><b>2. Inventory & Targeting (orbiads-inventory)</b></summary>

*   `inventory` — Retrieve ad unit trees, sizes, and generate ads.json manifests.
*   `placements` — Create, update, and list ad placement groups.
*   `targeting` — Manage custom targeting keys/values, countries, and categories.
*   `audiences` — Retrieve and modify first-party audience segments.
*   `blueprint` — Generate and push structured network inventory blueprints.
</details>

<details>
<summary><b>3. Reporting & Forecasting (orbiads-reporting)</b></summary>

*   `reporting` — Run custom reports from templates, check line item delivery, and integrate GA4.
*   `preview` — Verify inventory coverage and export preview URLs.
*   `pql` — Run raw PQL database queries.
</details>

<details>
<summary><b>4. Programmatic Deals (orbiads-deals)</b></summary>

*   `deals` — Manage PMP deals, private auctions, and marketplace buyers.
*   `companies` — Manage agency and advertiser company profiles.
</details>

<details>
<summary><b>5. Network Admin (orbiads-admin)</b></summary>

*   `gam_admin` — Access advanced fields, network labels, teams, and site records.
*   `gam_features` — Query active Google Ad Manager beta and system features.
*   `network` — List accessible networks and switch active network context.
*   `settings` — Configure default CPMs, pacing, and brand naming templates.
*   `tenant_catalog` — Access tenant-specific catalogs.
</details>

<details>
<summary><b>6. Audits & Billing (orbiads-audit)</b></summary>

*   `audit_skill` — Run automated security, hygiene, and wrapper coverage audits.
*   `billing` — Fetch credit balances and transaction histories.
*   `audit` — Search network audit logs.
</details>

> See [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md) for the complete parity matrix detailing exact costs, writes, and parameters for all 270+ actions.

---

## Safety by Design

Every write action requires an explicit `ExecutionPlan` preview and confirmation token. No campaign goes live by accident.

- **Plan-before-mutate** on campaign, deal, and product writes — preview the signed `ExecutionPlan` before you push
- **Dry-run mode** on all deployment actions — `confirmationToken` TTL 300 seconds
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
| GAM API version | `v202605` |
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

<p align="center">
  <br/>
  <img src="./logo/orbiads-logo-brand.png" alt="OrbiAds Brand Logo" width="220"/>
</p>
