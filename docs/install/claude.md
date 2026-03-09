# Install on Claude

OrbiAds is a **skill for Claude** — it gives Claude direct access to your Google Ad Manager account via MCP.

Three installation modes depending on which Claude product you use:

| Product | Mode |
| --- | --- |
| **Claude Desktop** (macOS / Windows) | MCP server in config file |
| **claude.ai** (web, Pro / Team) | MCP server in Integrations settings |
| **Claude Code** (CLI) | `install.sh` script or one-line command |

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

### Option A — install.sh (recommended)

Clone this repo, then run:

```bash
./install.sh claude          # register OrbiAds for the current project
./install.sh claude --global # register globally across all projects
./install.sh skills          # load all 8 skills for this session
./install.sh skills --copy   # install skills permanently in ~/.claude/skills/
```

The script runs `claude mcp add orbiads --transport http --url https://orbiads.com/mcp` and prints a smoke-check hint.

### Option B — no clone required

Without cloning, run this in any Claude Code session:

```text
/install-github OrbiAds/Orbiads-GAM-MCP
```

### Test

> *"Connect to my GAM account"*

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Networks linked to your account |
| *"Check my GAM credentials"* | Auth confirmed |
