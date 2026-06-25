# Install on Gemini CLI

OrbiAds gives the Gemini CLI access to your Google Ad Manager account through
**Agent Skills** (the working method) + a **remote MCP server** (the tools).

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- Gemini CLI with MCP support

---

## Step 1 — Add the Skills

Gemini CLI discovers skills from `~/.gemini/skills/` or `~/.agents/skills/` (user) and
`.gemini/skills/` or `.agents/skills/` (workspace). Download from the release and install:

```bash
mkdir -p ~/.agents/skills
# Download the .zip files from:
# https://github.com/OrbiAds/Orbiads-GAM-MCP/releases/tag/skills-latest
unzip orbiads.zip           -d ~/.agents/skills/    # router — required
unzip orbiads-reporting.zip -d ~/.agents/skills/    # add the domains you want
```

Or install a skill folder directly:

```bash
gemini skills install ./orbiads --consent
```

Official reference: <https://geminicli.com/docs>

---

## Step 2 — Add the MCP server (the tools)

Add OrbiAds to `~/.gemini/settings.json` (user) or `.gemini/settings.json` (project),
using the **`httpUrl`** key for a remote HTTP server (⚠ `url` means SSE in Gemini CLI):

```json
{
  "mcpServers": {
    "orbiads": {
      "httpUrl": "https://orbiads.com/mcp"
    }
  }
}
```

Or via the command:

```bash
gemini mcp add --transport http orbiads https://orbiads.com/mcp
```

Gemini CLI supports OAuth 2.0 for remote MCP; authenticate with `/mcp auth orbiads`.

---

## Step 3 — Test

> *"Connect to my GAM account"*

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Your GAM networks |

> Google AI Studio is a separate product; its MCP/tool support differs from the
> Gemini CLI and is not covered here.
