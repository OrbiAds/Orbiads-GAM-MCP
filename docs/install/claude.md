# Install on Claude

OrbiAds is a **skill for Claude** — it gives Claude Desktop and claude.ai direct access to your Google Ad Manager account via MCP.

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- Claude Desktop (macOS or Windows) **or** claude.ai Pro / Team

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

If you already have other MCP servers, just add the `orbiads` block inside the existing `mcpServers` object.

### Step 3 — Restart Claude Desktop

Quit and reopen. The OrbiAds tools load automatically.

### Step 4 — Authenticate

On first use, Claude opens a browser to complete the OAuth flow with your OrbiAds account.

### Step 5 — Test

Start a new conversation:

> *"Connect to my GAM account"*

Claude should confirm your OrbiAds tenant and list your GAM networks.

---

## claude.ai (web)

1. Go to **Settings → Integrations**
2. Click **Add MCP server**
3. Enter: `https://orbiads.com/mcp`
4. Complete the OAuth flow
5. Test: *"Connect to my GAM account"*

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Networks linked to your account |
| *"Check my GAM credentials"* | Auth confirmed |
