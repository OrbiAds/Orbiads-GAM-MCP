# Install on Claude

OrbiAds is a **skill for Claude** — it gives Claude direct access to your Google Ad Manager account via MCP.

Three installation modes depending on which Claude product you use:

| Product | Mode |
| --- | --- |
| **Claude Desktop** (macOS / Windows) | MCP server in config file |
| **claude.ai** (web, Pro / Team) | MCP server in Integrations settings |
| **Claude Code** (CLI) | Plugin installed from GitHub |

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard

---

## Claude Desktop

### Step 1 — Find your config file

| OS | Path |
| --- | --- |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

Open it with any text editor.

### Step 2 — Add OrbiAds

Add the `orbiads` entry inside `mcpServers`:

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

If you already have other MCP servers, add the `orbiads` block inside the existing `mcpServers` object.

### Step 3 — Restart Claude Desktop

Quit and reopen. The OrbiAds tools load automatically.

### Step 4 — Authenticate

On first use, Claude opens a browser to complete the OAuth flow with your OrbiAds account.

### Step 5 — Test

> *"Connect to my GAM account"*

Claude should confirm your tenant and list your GAM networks.

---

## claude.ai (web)

1. Go to **Settings → Integrations**
2. Click **Add MCP server**
3. Enter: `https://orbiads.com/mcp`
4. Complete the OAuth flow when prompted
5. Test: *"Connect to my GAM account"*

---

## Claude Code (CLI)

Claude Code can load the OrbiAds skill directly from this GitHub repository.

### Option A — Install from GitHub (recommended)

In any Claude Code session, run:

```
/install-github OrbiAds/Orbiads-GAM-MCP
```

Claude Code reads `.claude-plugin/plugin.json` and `.mcp.json` from the repo root and wires everything automatically.

### Option B — Manual setup

1. Clone or download this repo
2. Copy `.mcp.json` from the root into your project folder (or your `~/.claude/` directory for global access)
3. In Claude Code, the OrbiAds tools will be available in any session started in that folder

### Step — Test

> *"Connect to my GAM account"*

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Networks linked to your account |
| *"Check my GAM credentials"* | Auth confirmed |
