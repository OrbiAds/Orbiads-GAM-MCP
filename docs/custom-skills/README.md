# Authoring Custom OrbiAds Skills

This guide shows a tenant or agency developer how to write their **own** agent
skill on top of the OrbiAds surface — the hosted MCP server
(`https://orbiads.com/mcp`) and the `orbiads-cli`.

Two motivating examples used throughout:

- a **"homepage takeover pack"** skill that encodes your house campaign template
  (the standard line items, priorities, and creative slots you ship every time);
- a **"weekly delivery digest"** skill that runs the same reporting query every
  Monday and renders it in a fixed shape.

A custom skill is **procedural knowledge layered on top** of the OrbiAds tools.
It does not replace the [`orbiads`](../../skills/orbiads/SKILL.md) orchestrator
skill or its safety contract — it defers to them. Read
[`AGENTS.md`](../../AGENTS.md) (the cross-LLM hard rules) and the orchestrator
[`SKILL.md`](../../skills/orbiads/SKILL.md) before you start.

---

## 1. What a custom skill is — and when to build one

A skill is a **folder with a `SKILL.md` file** (Agent Skills open standard,
[agentskills.io](https://agentskills.io); supported by Claude Code and other
clients). The `SKILL.md` frontmatter needs at minimum a `name` and a
`description`. The body is procedural instructions the model loads on demand.

**Build a custom skill when you have:**

- **Durable procedural knowledge** — a multi-step ad-ops workflow you run
  repeatedly the same way (homepage takeover, end-of-month reporting, a
  standard new-advertiser onboarding).
- **House conventions** — your agency's naming scheme, default line item
  priorities, the creative formats you always ship, your approval etiquette.
- **Repeatable multi-entity flows** — anything where the model would otherwise
  re-derive the same plan from a long prompt every time.

**Do NOT build a skill for:**

- Things the model already knows (what a line item is, how CPM works).
- Volatile information (current balance, today's delivery numbers, live IDs) —
  these come from **reads at runtime**, never baked into the skill text.
- A single ad-hoc task — just prompt the orchestrator directly.

If you're tempted to paste live data into `SKILL.md`, stop: fetch it with a read
tool instead. The skill encodes *how*, the tools supply *what*.

---

## 2. Anatomy of a skill

### Folder layout

```
my-homepage-takeover/
├── SKILL.md              # required — frontmatter + thin procedure
├── references/           # optional — heavy reference material, loaded on demand
│   ├── naming.md         #   your house naming table
│   └── line-item-plan.md #   the standard LI/priority/format matrix
└── scripts/              # optional — deterministic helpers (validators, etc.)
```

> **Discovery is not recursive.** The client only finds
> `<skills-root>/<name>/SKILL.md` exactly one level deep. A `SKILL.md` nested
> deeper (e.g. `references/extra/SKILL.md`) is **not** discovered. Keep one
> `SKILL.md` per skill folder; put everything else under `references/`.

Keep `SKILL.md` under **~500 lines**. Move action catalogues, naming tables, and
long examples into `references/*.md` and link to them from the body. The model
loads referenced files only when the task needs them (progressive disclosure),
which keeps the routing context cheap.

### Frontmatter template

```yaml
---
name: homepage-takeover-pack
description: >-
  Use when an ad ops user wants to launch our standard homepage takeover /
  roadblock package in Google Ad Manager. Builds the house line item set
  (high-priority roadblock + companion) at fixed priorities and attaches the
  standard creative slots. Examples: "ship the homepage takeover for Acme",
  "launch our roadblock pack", "set up a homepage roadblock for next week".
user-invocable: false
---
```

> **⚠️ Spelling trap: `user-invocable`, with a `c`.**
> The frontmatter key is `user-invocable` (in-voc-able). The common misspelling
> `user-invokable` (with a **k**) is **silently ignored** — your setting does
> nothing and the default applies. Double-check the `c` every time.

Frontmatter semantics (Claude Code, verified 2026-06-11):

| Key | Effect |
| --- | --- |
| `user-invocable: false` | Hidden from the user's `/` menu, **but the model can still auto-invoke it** based on the description. Use this for skills that should fire by routing, not by the user typing a command. |
| `disable-model-invocation: true` | Hidden from the **model**; only manual `/name` invocation works. Use for skills a human must trigger deliberately. |

> **Command name comes from the directory.** For a skill placed in a plugin's
> `skills/` directory or in `.claude/skills/`, the slash-command name is the
> **directory name** (`/my-homepage-takeover`), not the frontmatter `name`. The
> `name` field is a human-readable display label. (The OrbiAds consolidated
> skills follow this: directory `campaigns/` with `name: orbiads-campaigns`.)

---

## 3. Writing the description (the routing trigger)

The `description` is **not documentation** — it is the trigger the model matches
against the user's request to decide whether to activate the skill. Rules:

- Start with **"Use when…"**.
- Keep it to **~50–60 words**.
- Include **the words real users actually type** — the description must speak
  the agent's matching vocabulary, not a marketing term. Anchor it in the domain
  with whichever synonym reads naturally (Google Ad Manager, GAM, ad ops), and
  add the nouns specific to YOUR skill (roadblock, line item, takeover, PMP,
  delivery digest…).
- **2–3 concrete user-query examples** beat an abstract summary.
- A real query should match **exactly one** skill: too broad and you steal
  traffic from sibling skills (routing interference); too narrow and the skill
  never fires.

**Bad** (abstract, no triggers, reads like a title):

```yaml
description: A skill for homepage takeover campaigns.
```

**Good** (trigger-first, vocabulary, concrete examples):

```yaml
description: >-
  Use when an ad ops user wants to launch our standard homepage takeover /
  roadblock package in Google Ad Manager — high-priority roadblock line item
  plus companion, fixed priorities, standard creative slots. Examples: "ship
  the homepage takeover for Acme", "launch our roadblock pack", "set up a
  homepage roadblock for next week".
```

---

## 4. Writing the body

The body is **thin procedure**, not a tool reference. Principles:

- **Gotchas first.** Lead with the constraints and the easy-to-get-wrong steps
  (e.g. "homepage roadblock must be priority 4, not the default"), then the
  happy path.
- **Defer routing and safety to the orchestrator.** Don't re-implement the
  preview→confirm→execute state machine — state that your skill follows the
  [`orbiads`](../../skills/orbiads/SKILL.md) orchestrator's contract and the
  [Safety Contract](#5-safety-contract-copy-paste-this) below.
- **Reference parent tools by `tool(action=…)` name.** Use the real names from
  the [tool matrix](../tool-matrix/README.md). Example: `campaign(action=…)`,
  `line_items(action=…)`, `creatives(action=…)`, `creative_qa(action=…)`,
  `reporting(action=…)`, `inventory(action=…)`, `targeting(action=…)`,
  `deals(action=…)`, `gam_admin(action=…)`, `billing(action=…)`,
  `auth check_credentials`. **Do not invent tools or actions** — if you're
  unsure an action exists, check the matrix; if still unsure, omit it.
- **Move catalogues out.** A 40-row naming table or line-item plan goes in
  `references/`, linked from the body.

### Dual-surface pattern

Every operation may exist on the **MCP surface** (parent tools) and/or the
**CLI** (`pip install orbiads-cli`). **CLI coverage is partial.** When you give
an MCP call, also give the CLI equivalent — and if the CLI lacks it, mark it
**MCP-only**. The authority for what the CLI actually supports is
[`cli/PARITY.md`](../../cli/PARITY.md) and
[`cli/parity-matrix.json`](../../cli/parity-matrix.json). **Never invent a CLI
command.**

Write each step like this:

> **Step: confirm the network.**
> Reads are free — always start by establishing the tenant/network.
>
> - MCP: `auth check_credentials` (or `get_my_tenant_id`)
> - CLI: `orbiads auth status --json`

> **Step: build the roadblock line item.**
>
> - MCP: `line_items(action="create", params={…, dry_run: true})`
> - CLI: `orbiads line-items create … --json` *(verify against `PARITY.md`
>   before relying on it; if absent, this step is **MCP-only**)*

For the CLI, **always pass `--json`** so the agent gets machine-parseable
output, and run `orbiads auth status --json` first to confirm authentication.

---

## 5. Safety Contract (copy-paste this)

Any skill that can reach a write **must** embed this contract verbatim. Paste it
into the skill body under a `## Safety Contract` heading:

```markdown
## Safety Contract (non-negotiable)

- Derive the tenant/network from the auth tools — `auth check_credentials`,
  `get_my_tenant_id`, or `orbiads auth status`. NEVER invent a `tenantId` or
  `networkCode`. If the user is not authenticated, stop and tell them to log in.
- Reads are FREE (cost = 0). Use them liberally to ground every recommendation
  in real network state.
- Every WRITE follows preview → confirm → execute:
    1. Call the tool with `dry_run: true` (or `preview`) to get an ExecutionPlan.
    2. Render the diff + the credit cost to the user.
    3. Wait for explicit confirmation.
    4. Execute with the `confirmation_token` from the preview (token TTL ≤ 5 min).
- NEVER bypass `billing_guard`. Reads free, writes cost credits — period.
- NEVER retry a failed write more than 2 times. GAM SOAP writes are NOT
  idempotent; a blind retry can double-create. Surface the error instead.
- Surface error codes as-is: CONFIRMATION_REQUIRED, IDEMPOTENCY_KEY_MISMATCH,
  BILLING_OVERDUE, SERVICE_UNAVAILABLE, DEPRECATED_TOOL — they are meaningful.
- These rules are IDENTICAL on the MCP and CLI surfaces.
```

This mirrors the orchestrator's hard rules and `AGENTS.md`. A custom skill that
omits it is not safe to distribute.

---

## 6. Fixed orchestrations (`workflow.yaml`)

A free-form skill (prose the model interprets) is right for most house
procedures. Prefer a **deterministic workflow** instead when you have a
**repeatable multi-entity flow with approval gates** — e.g. a homepage takeover
that always reserves an order, creates N line items, attaches creatives, QAs,
and reports, in that exact order, with a human gate before every real write
(BMAD-style fixed orchestration). A workflow makes the sequence and the gates
explicit and portable rather than leaving them to model judgment.

Workflows live one folder per workflow (see
[`../workflows/README.md`](../workflows/README.md)). Each folder contains
`README.md` (scope/outcomes), `steps.md` (the optimized sequence), `tasks.md`
(operator checklist), and `workflow.yaml` (portable metadata). The
`workflow.yaml` contract:

| Key | Meaning |
| --- | --- |
| `id` | Stable slug (e.g. `homepage-takeover`). |
| `name` | Human-readable name. |
| `version` | Integer, bumped on contract changes. |
| `status` | `ready` / draft / etc. |
| `objective` | One sentence — what the flow accomplishes. |
| `inputs` | Named inputs the operator supplies (e.g. `tenantId`, `orderName`, `creativeIds`). |
| `skills` | The skills this flow composes (see warning below). |
| `outputs` | Named result artifacts (e.g. `previewPacket`, `deliverySummary`). |
| `steps` | Ordered list of `{ id, skill, mode }` — plus an optional `notes` block per step spelling out the exact `tool(action=…)` calls and gates (recommended for fixed orchestrations). |
| `validationGates` | Human approval checkpoints, in plain language. |

Step **modes**:

| Mode | Use for |
| --- | --- |
| `read` | Free, state-gathering steps (bootstrap, QA preview, forecast). |
| `preview_then_write` | A write that goes through the full preview → confirm → execute gate. |
| `optional_write` | A remediation/cleanup write that may be skipped. |

> **⚠️ `skills:` must reference the ACTIVE consolidated skills**, not legacy
> micro-skills. The current set is:
> `orbiads`, `campaigns`, `inventory`, `reporting`, `deals`, `audit`, `admin`.
> Older workflows in this repo still list pre-consolidation micro-skills
> (`bootstrap`, `qa-preview`, `deploy-reporting`, `advertiser-order-line-items`);
> **do not copy those names into a new workflow.**

Sketch for the homepage takeover:

```yaml
id: homepage-takeover
name: Homepage Takeover Pack
version: 1
status: ready
objective: Deploy the house homepage roadblock package with approval gates.
inputs:
  - tenantId
  - orderName
  - flightStart
  - flightEnd
  - creativeIds
skills:
  - orbiads
  - campaigns
  - reporting
outputs:
  - previewPacket
  - deploymentSummary
  - deliverySummary
steps:
  - id: bootstrap-context
    skill: orbiads
    mode: read
  - id: build-and-preview-pack
    skill: campaigns
    mode: preview_then_write
  - id: post-deploy-delivery
    skill: reporting
    mode: read
validationGates:
  - approve the preview diff and credit cost before any write
  - review first-hour delivery before declaring the pack live
```

A worked example lives at
[`examples/homepage-takeover/`](examples/homepage-takeover/) — it pairs
[`SKILL.md`](examples/homepage-takeover/SKILL.md) (the free-form house skill)
with [`workflow.yaml`](examples/homepage-takeover/workflow.yaml) (the
deterministic flow). Use it as the canonical reference.

---

## 7. Installing & testing

### Where to put it

| Goal | Location |
| --- | --- |
| Personal / single-machine use | `.claude/skills/<name>/SKILL.md` |
| Distribute to a team / publish | a plugin's `skills/<name>/SKILL.md` |

Remember: the slash-command name is the **directory name**, and discovery is one
level deep only.

### Smoke-test the routing

1. **Positive:** ask the agent something that matches your `description`
   ("ship the homepage takeover for Acme"). Confirm the skill **activates**.
2. **Negative:** ask an adjacent-but-different request ("just pull last week's
   delivery report"). Confirm the skill does **not** wrongly activate — if it
   does, your description is too broad; tighten the triggers.
3. **Safety:** drive it to a write and confirm it presents a preview + credit
   cost and waits for confirmation before executing.

### Validation checklist

- [ ] Frontmatter is valid YAML with `name` + `description`.
- [ ] `user-invocable` is spelled with a **c** (if used).
- [ ] `SKILL.md` is under ~500 lines; heavy material is in `references/`.
- [ ] All relative links resolve.
- [ ] Every tool/action referenced exists in the
      [tool matrix](../tool-matrix/README.md) — no invented tools or actions.
- [ ] Every CLI command exists in [`cli/PARITY.md`](../../cli/PARITY.md);
      MCP-only steps are marked as such — no invented CLI commands.
- [ ] The [Safety Contract](#5-safety-contract-copy-paste-this) is present in any
      skill that can reach a write.
- [ ] If you ship a `workflow.yaml`, its `skills:` reference only the active
      consolidated skills.

---

## See also

- [`skills/orbiads/SKILL.md`](../../skills/orbiads/SKILL.md) — the orchestrator your skill defers to
- [`AGENTS.md`](../../AGENTS.md) — cross-LLM hard rules
- [`docs/tool-matrix/README.md`](../tool-matrix/README.md) — parent tool + action catalogue (source of truth)
- [`cli/PARITY.md`](../../cli/PARITY.md) — MCP ↔ CLI coverage
- [`docs/workflows/README.md`](../workflows/README.md) — the fixed-orchestration contract
