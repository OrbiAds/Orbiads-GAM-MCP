# Install on ChatGPT

OrbiAds is a **skill for ChatGPT** — it connects ChatGPT to your Google Ad Manager account via an MCP connector.

## Prerequisites

- An OrbiAds account — [sign up free at orbiads.com](https://orbiads.com) (5 credits, no card required)
- Your GAM account connected in the OrbiAds dashboard
- **ChatGPT Pro** subscription
- Developer Mode enabled

---

## Step 1 — Enable Developer Mode

Go to **ChatGPT → Settings → Beta features** and enable **Developer Mode**.

---

## Step 2 — Create the connector

1. Go to **Settings → Connectors → Create connector**
2. Fill in:

| Field | Value |
| --- | --- |
| Name | `OrbiAds` |
| Description | `Google Ad Manager AdOps skill — inventory, trafficking, forecast, reporting` |
| MCP URL | `https://orbiads.com/mcp` |

3. Click **Save**

---

## Step 3 — Authenticate

ChatGPT redirects you to the OrbiAds OAuth flow. Sign in with the Google account that has access to your GAM network.

---

## Step 4 — Test

> *"Connect to my GAM account"*

ChatGPT should return your tenant and network information.

---

## Smoke checks

| Prompt | Expected result |
| --- | --- |
| *"What is my tenant ID?"* | Your OrbiAds tenant |
| *"List my GAM networks"* | Your GAM networks |
| *"Check inventory on the homepage 300x250 next week"* | An availability forecast |
