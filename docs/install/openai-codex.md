# Install on OpenAI Codex

OrbiAds gives Codex (CLI, IDE extension and the Codex app) access to your Google Ad
Manager account through **Agent Skills** (the working method) + a **remote MCP server**
(the tools). Both use Codex-native mechanisms — no `.mcp.json`, no repo clone.

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- Codex with MCP support

---

## Step 1 — Add the Skills

Codex discovers skills from `.agents/skills/` (current folder / repo root) and
`~/.agents/skills/` (user-wide). Download the Skills from the release and unzip them there:

```bash
mkdir -p ~/.agents/skills
# Download the .zip files from:
# https://github.com/OrbiAds/Orbiads-GAM-MCP/releases/tag/skills-latest
unzip orbiads.zip            -d ~/.agents/skills/   # router — required
unzip orbiads-reporting.zip  -d ~/.agents/skills/   # add the domains you want
```

Each `.zip` extracts to `<skill-name>/SKILL.md`. No restart needed — Codex picks them up.
Official reference: <https://developers.openai.com/codex/skills>

> Optional: drop the repo-root `AGENTS.md` into your workspace for the cross-LLM
> operating contract.

---

## Step 2 — Add the MCP server (the tools)

Codex stores MCP servers in `~/.codex/config.toml` (or `.codex/config.toml` per project),
in **TOML** — not a `.mcp.json`:

```toml
[mcp_servers.orbiads]
url = "https://orbiads.com/mcp"
```

Then authenticate (Codex supports OAuth for remote MCP servers):

```bash
codex mcp login orbiads
```

> Note: on some Codex versions, remote streamable-HTTP MCP requires enabling
> `experimental_use_rmcp_client`. See <https://developers.openai.com/codex/mcp>.

---

## Step 3 — Test

Open a Codex session in your workspace:

> *"Connect to my GAM account"*

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Your GAM networks |
| *"Check inventory on the homepage 300x250 next week"* | An availability forecast |
