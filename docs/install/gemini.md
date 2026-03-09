# Install on Gemini

OrbiAds is a **skill for Gemini** — it connects Gemini to your Google Ad Manager account via MCP.

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- Gemini Advanced **or** Google AI Studio with MCP tool support

---

## Option A — Google AI Studio

1. In your AI Studio project, open **Tools → MCP configuration**
2. Add:

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

3. Save and reload the project
4. Complete the OAuth flow
5. Test: *"Connect to my GAM account"*

---

## Option B — Gemini extension

Load the ready-to-use extension files from this repository:

| File | Purpose |
| --- | --- |
| `gemini-extension/extension/manifest.json` | Extension descriptor |
| `gemini-extension/extension/function-declarations.yaml` | Callable tool surface |
| `gemini-extension/extension/system-instruction.md` | AdOps operating rules |

Follow the standard Gemini extension install process for your environment.

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Your GAM networks |

> **Note:** Gemini MCP support is evolving. If your version doesn't yet support remote MCP, use Claude or ChatGPT in the meantime.
