# OrbiAds — AI Agent Instructions

> **For Cursor · Codex CLI · Gemini CLI · GitHub Copilot · Aider · Windsurf · Jules · Factory · Warp · RooCode · Zed · any AGENTS.md-aware tool.**
> Claude Code users: see [`CLAUDE.md`](./CLAUDE.md) for Claude-specific guidance (this file is the cross-LLM contract; CLAUDE.md adds project-internal context).

OrbiAds is a **Google Ad Manager (GAM) copilot for AI agents**. It exposes the entire GAM operations surface (campaigns, inventory, creatives, reporting, audits, deals, billing) through two equivalent transports — a hosted MCP server (`https://orbiads.com/mcp`) and a Python CLI (`pip install orbiads-cli`) — both protected by the same per-tenant billing guard, confirmation tokens, and audit log.

The catalogue is organized **parent>child** (28 parent tools dispatching ~270 operations via an `action` discriminator). New integrations should call the parent tools; the 219 pre-refactor child names remain available as soft-deprecated wrappers.

---

## Quick Reference

| Slash command (future) | What it does | Parent MCP tools involved |
| --- | --- | --- |
| `/adops campaign` | Read live state, plan deployment, dry-run (ExecutionPlan), deploy, pause, status, rollback — plan→confirm→execute gate | `campaign`, `line_items`, `creatives`, `creative_qa`, `orders`, `reporting` |
| `/adops audit` | Multi-dimensional GAM account audit via parallel subagents | `audit_skill`, `inventory`, `reporting`, `creative_qa`, `billing` |
| `/adops report` | Reporting queries — delivery, custom reports, CSV export, templates, billing, forecast | `reporting` |
| `/adops deal` | Programmatic deal lifecycle — PMP, private auction, Marketplace PG/PD | `deals`, `companies`, `settings` |
| `/adops creative` | Creative upload, QA, SSL validation, preview URLs, association | `creatives`, `creative_qa`, `creative_assets`, `creative_wrapper_skill`, `settings` |
| `/adops inventory` | Ad units + placements + targeting + blueprint | `inventory`, `placements`, `targeting`, `blueprint` |
| `/adops admin` | Multi-user / team / label / site (Epic 65) | `gam_admin` |

Slash commands are defined in `commands/adops-*.md` (shipped in Story 81.3, Epic 81). Claude Code discovers them automatically after `claude plugin install orbiads`.

> **plan-before-mutate**: all write operations (campaign deploy, deal ADCP create, product publish) require an explicit `ExecutionPlan` preview step (`dry_run: true`) before execution. The plan is signed with a `confirmationToken` (TTL 300 s). Executing without a valid token returns `CONFIRMATION_REQUIRED`.

---

## Connect

### MCP server (recommended for chat agents)

```
MCP endpoint:    https://orbiads.com/mcp
MCP protocol:    2025-03-26 (streamable-http)
Authentication:  OAuth 2.0 (per-tenant Google login)
```

Connect from Claude Code:
```bash
claude /plugin install orbiads
```

Connect from Cursor / Codex / Gemini CLI: add to your MCP server config:
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

### CLI (recommended for scripts / CI / headless)

```bash
pip install orbiads-cli
orbiads auth login                 # OAuth Device Flow
orbiads network info               # Smoke test
orbiads campaign preview --help    # Drill into commands
```

Same billing model, same credits, same confirmation tokens as the MCP server.

---

## How to upload a creative

MCP does not support hydration-free binary transport between servers (see `_docs/research/mcp-binary-transport-2026-05.md`). Choose the path based on asset size:

| Asset | Path | Why |
|-------|------|-----|
| Image (< ~100 KB) | MCP `creative_assets` tool — pass base64 inline | ~25K tokens max, tolerable |
| Any asset with a public/local URL | `creative_assets(action="upload_from_url", url=...)` | 0 LLM tokens — server fetches directly |
| HTML5 ZIP, video, audio (> 100 KB) | CLI: `orbiads creatives upload <file>` | 0 LLM tokens — local process uploads over HTTPS |
| Local heavy file, no shell access | Host the file at an HTTP URL, then use `upload_from_url` | Only viable MCP path for large local files |

**Rule for agents:** if the user mentions a local file > 100 KB (ZIP, video, audio), redirect immediately to the CLI or ask for a hosted URL. Do **not** attempt to read the file via `resources/read` or receive it as base64 — this saturates the context window without benefit.

```bash
# Local file — always use the CLI
orbiads creatives upload ~/Downloads/banner_300x250.zip --advertiser-id 123 --name "Banner 300x250"

# Already hosted — use MCP directly
creative_assets(action="upload_from_url", url="https://cdn.example.com/banner.zip", advertiser_id="123", name="Banner 300x250")
```

---

## Boundaries — hard rules every agent MUST follow

1. **Never invent a `tenantId` or `networkCode`.** Always call `get_my_tenant_id` (or `auth check_credentials`) first. If the user has not authenticated, refuse to continue and instruct them to run `orbiads auth login` or open the MCP OAuth flow.

2. **Never bypass `billing_guard`.** Every write operation (cost > 0) requires a fresh `confirmation_token` produced by a preview call. The SHA-256 over the payload locks the preview→execute boundary; any drift fails the token check. Token TTL is 5 minutes.

3. **Reads are always free** (cost = 0 credits) and may be called without confirmation. Use them liberally to surface state before proposing writes.

4. **Never retry a failed write more than 2 times.** GAM does not guarantee idempotency on its SOAP `Service.performXxxAction` operations. If a second retry fails, surface the error to the user — do not loop.

5. **Never call `action="deploy"` on `campaign` without a `confirmation_token` < 5 min old.** Same for any operation in the orders/line_items/deals chains touching production inventory.

6. **OrbiAds is NOT a reseller.** Each tenant owns their own GAM network and inventory. Do not propose "OrbiAds will buy inventory" or "OrbiAds owns this campaign" — OrbiAds is technical infrastructure, the tenant remains the contractual owner.

7. **Buy-side agents (ADCP) NEVER auth directly to OrbiAds.** ADCP buy agents send briefs by email to the tenant; the tenant processes those briefs via their own MCP session. Do not attempt M2M auth flows.

---

## Personas — the 5 dominant use cases

### A. Campaign deployment (revenue-critical)

Plan a multi-line campaign, validate inventory availability, deploy to GAM, monitor, rollback if needed. **State machine: build_draft → validate → preview (cost + diff) → confirm_gate → reserve_order → attach_creatives → activate → emit_audit_log**. Cost: typically 5-15 credits.

### B. Account audit (governance / compliance)

Multi-dimensional audit (delivery health, security baseline, inventory hygiene, creative compliance, billing alignment). Recommended pattern in Story 81.4: parallel subagents (one per dimension) that each write to their own output file, aggregated by an orchestrator. Read-only, free.

### C. Reporting (analytics)

REST Interactive Reports API (`POST /networks/{nc}/reports`). Build query → run → poll → fetch CSV. Free (reads).

### D. Deal management (programmatic)

Marketplace deals + ADCP validation pipeline. Same preview→confirm→execute pattern as campaigns.

### E. Inventory administration (governance)

Ad units, placements, custom targeting, blueprint preferences, multi-site network sharing (Epic 78.15). Mix of free reads and 0.5-credit writes.

---

## Tech stack — what the surface guarantees

| Layer | Detail |
| --- | --- |
| GAM API target | `v202605` (locked — see `compatibleWith.gamApi` in `version.json`) |
| MCP protocol | `2025-03-26` (streamable-http transport) |
| Auth | Google OAuth 2.0 (Authorization Code Flow); per-tenant refresh tokens encrypted at rest via Cloud KMS |
| Server runtime | FastAPI + FastMCP, Cloud Run europe-west1, scale-to-zero (cold start ~3 s) |
| Storage | Firestore Native Mode (`projects/orbiads`) |
| CLI runtime | Python 3.10+, `httpx` for HTTP, `typer` for CLI |
| Catalogue | 28 parent tools, 219 deprecated wrappers (still functional), 24 standalones — **271 tools total**. See [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md). |

---

## Setup

### Prerequisites
- A Google Ad Manager account with API access enabled (or use the test network 45515589 — note: REST Reports do not work on test networks, only production).
- An `orbiads.com` account (sign up free at <https://orbiads.com>, 5 trial credits, no card required).
- For CLI: Python 3.10+ + `pip`.

### First connection (3 minutes)
1. Sign up at <https://orbiads.com>.
2. Click "Connect GAM" — completes the OAuth handshake.
3. Choose the network code (auto-detected from your GAM access).
4. Install the plugin/CLI per your tool's instructions above.
5. Smoke test: ask your agent `"check my GAM credentials and tell me my network code"`.

---

## Project structure (what lives where in this repo)

```
orbiads-gam-mcp/                       # this repo (public mirror of orbiads/ subtree)
├── .claude-plugin/
│   ├── plugin.json                    # Claude Code plugin manifest (name, version, MCP server)
│   └── marketplace.json               # marketplace catalog entry
├── AGENTS.md                          # this file — cross-LLM contract
├── CLAUDE.md                          # Claude Code project guidance
├── README.md                          # human-facing GitHub README
├── CHANGELOG.md                       # version history (generated)
├── version.json                       # semver + layer versions + GAM/MCP compatibility (generated)
├── skills/                            # Claude Code Agent Skills
│   ├── orbiads/                       # orchestrator skill (user-invokable: true)
│   │   ├── SKILL.md                   # Quick Reference + routing logic + hard rules
│   │   └── references/                # reference files loaded on demand
│   └── <group>/SKILL.md               # 6 sub-skills, grouping all parent tools (user-invokable: false)
├── docs:
│   ├── tool-matrix/README.md          # the 28 parents + their actions (generated)
│   ├── install/                       # per-tool install guides (claude.md, cursor.md, ...)
│   └── safety/                        # boundaries, error codes, rollback recipes
├── _docs/
│   └── legacy-tool-mapping.md         # the 219 deprecated wrappers → parents (generated)
├── cli/                               # Python CLI source (publishable as orbiads-cli)
│   ├── src/orbiads_cli/               # implementation
│   ├── parity-matrix.json             # MCP↔CLI coverage matrix (semi-generated)
│   └── PARITY.md                      # parity policy and exemptions
├── shared/                            # legacy shared skills/agents/schemas (transition — sunset in Story 81.4)
└── extensions/                        # gemini-extension + openai-codex helpers (transition)
```

---

## Boundary / fail-safe behaviors

- **`SERVICE_UNAVAILABLE` on pricing tools** — `RateCardService` + `PremiumRateService` were removed from GAM v202502. Pricing-related actions return `SERVICE_UNAVAILABLE` with a clear message. Don't retry.
- **`REST Reports do not work on test networks`** — explicit error from the `reporting` parent. If you see it, the user is on a test network (e.g. 45515589) and must switch to a production network for reporting.
- **`CONFIRMATION_REQUIRED`** — every write returns this on the first call. Show the preview to the user, capture their consent, then re-call with the `confirmationToken`.
- **`IDEMPOTENCY_KEY_MISMATCH`** — the payload changed between preview and execute. Re-run preview to get a fresh token.
- **`BILLING_OVERDUE`** — the tenant is past due. Direct them to <https://orbiads.com/billing>.
- **`DEPRECATED_TOOL`** — info-level, not an error. Old child names still work; agent should plan migration to the parent>child form per [`_docs/legacy-tool-mapping.md`](./_docs/legacy-tool-mapping.md).

---

## Where to look for more

- **Tool catalogue + costs** — [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md) (generated, source of truth)
- **Legacy migration** — [`_docs/legacy-tool-mapping.md`](./_docs/legacy-tool-mapping.md) (the 219 deprecated wrappers)
- **CLI commands** — [`cli/PARITY.md`](./cli/PARITY.md)
- **Install guides per tool** — [`docs/install/`](./docs/install/) (Claude, Cursor, Codex, Gemini)
- **MCP server details** — [`mcp/`](./mcp/) (config samples, auth flow)
- **Examples by use case** — [`examples/`](./examples/)

---

> 🚦 **If you, the agent reading this, are unsure: prefer reads, ask the user before writes, and never bypass the confirmation_token gate. The billing_guard exists for a reason.**
