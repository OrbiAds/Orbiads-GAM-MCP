# OrbiAds CLI — Installation Guide

## Prerequisites

- **Python 3.10+** (check with `python3 --version` or `python --version`)
- **pip** or **pipx** (pipx recommended — auto-manages PATH and isolation)
- An **OrbiAds account** ([sign up free](https://orbiads.com) — 5 credits, no card)
- A **Google Ad Manager** account connected to OrbiAds

---

## Installation

### Method 1: pipx (recommended)

[pipx](https://pipx.pypa.io/) installs Python CLI tools in isolated environments and automatically adds them to PATH. No PATH headaches.

```bash
# Install pipx if you don't have it
pip install pipx
pipx ensurepath    # restart your terminal after this

# Install OrbiAds CLI
pipx install orbiads-cli
```

### Method 2: pip

```bash
pip install orbiads-cli
```

> If `orbiads` is not found after install, your Python scripts directory is not in PATH. See [Troubleshooting](#troubleshooting).

### Method 3: From the repository

```bash
git clone https://github.com/OrbiAds/Orbiads-GAM-MCP.git
cd Orbiads-GAM-MCP
./install.sh cli
```

The `install.sh` script detects your environment, prefers pipx if available, and guides you through PATH configuration if needed.

### Verify installation

```bash
orbiads --version
```

Expected: `orbiads 1.0.1`

If you get `command not found`, try:
```bash
python -m orbiads_cli --version
```

---

## Authentication

OrbiAds CLI uses **Google OAuth 2.0 Device Flow** — no passwords are stored locally.

### Step 1: Log in

```bash
orbiads auth login
```

The CLI displays:

```
Open this URL in your browser:
  https://orbiads.com/auth/device?code=ABCD-1234

Waiting for authorization...
```

1. Open the URL
2. Enter the code shown
3. Authorize with your Google account
4. The CLI confirms: `Authenticated as user@gmail.com`

### Step 2: Verify

```bash
orbiads auth status
```

Expected: `Authenticated as user@gmail.com (network: 12345678)`

### Token storage

Tokens are stored in `~/.orbiads/config.json` with restricted file permissions (0600 on Unix). To remove them:

```bash
orbiads auth logout
```

---

## First Commands

```bash
# Show your GAM network details
orbiads network info

# List all accessible networks
orbiads network list

# List active campaigns
orbiads campaigns list

# Get JSON output (for scripts and piping)
orbiads campaigns list --json | jq '.data[] | .name'

# Check your credit balance
orbiads billing balance
```

---

## Configuration

The CLI stores settings in `~/.orbiads/config.json`:

```bash
orbiads config list                  # show all settings
orbiads config set network_id 12345  # set default GAM network
orbiads config set output json       # default output format (table, json, csv)
```

---

## CLI + Skills + MCP — Complete Integration

OrbiAds provides three complementary layers. Here's when to use each:

### The 3 layers

| Layer | Interface | Best for |
|-------|-----------|----------|
| **CLI** | Terminal, scripts | Quick lookups, CI/CD, automation, piped workflows |
| **MCP** | AI agents (Claude, ChatGPT, Gemini) | Interactive exploration, conversational workflows |
| **Skills** | Claude Code slash commands | Guided multi-step workflows with guardrails |

All three share the **same backend, same credits, same safety guardrails**.

### Install all three together

```bash
# 1. CLI — for terminal and scripts
./install.sh cli

# 2. MCP — for AI agents
./install.sh claude            # Claude Code (current project)
./install.sh claude --global   # Claude Code (all projects)

# 3. Skills — for guided workflows
./install.sh skills --copy     # install permanently
```

Or install everything at once:

```bash
./install.sh all
```

### Using CLI inside Claude Code

Claude Code can execute CLI commands directly. This is powerful for combining AI reasoning with structured data:

```
You: Run `orbiads campaigns list --json` and tell me which campaigns
     have less than 50% delivery after 7 days

Claude: [executes CLI] Here are the underperforming campaigns...
```

### Using Skills with CLI data

Skills provide guided workflows. You can feed CLI output into Skills:

```
You: /orbiads:qa-preview
     Here's the campaign data: [paste orbiads campaigns get 123 --json]

Claude: [runs QA checks using the skill's guardrails]
```

### Automation with CLI + jq

```bash
# Export all campaigns as CSV
orbiads campaigns list --output csv > campaigns.csv

# Get the first underperforming campaign ID
orbiads reporting run --template delivery --json | \
  jq -r '.data[] | select(.deliveryRate < 50) | .id' | head -1

# Pipe into another command
CAMPAIGN_ID=$(orbiads campaigns list --json | jq -r '.data[0].id')
orbiads campaigns get "$CAMPAIGN_ID" --json
```

---

## Available Skills (Claude Code)

When Skills are installed, these slash commands become available:

| Skill | What it does |
|-------|-------------|
| `/orbiads:bootstrap` | Connect GAM, verify credentials, select network |
| `/orbiads:inventory-ad-units` | Browse ad units, placements, targeting keys |
| `/orbiads:availability-forecast` | Check inventory before trafficking (read-only) |
| `/orbiads:advertiser-order-line-items` | Create advertisers, orders, line items |
| `/orbiads:placements-targeting` | Build targeting configurations |
| `/orbiads:native-image` | Traffic native/image creatives with upload |
| `/orbiads:qa-preview` | Preview and coverage check before live push |
| `/orbiads:deploy-reporting` | Deploy with dry-run + post-push delivery reports |

---

## Troubleshooting

### `command not found: orbiads`

Your Python scripts directory is not in PATH. Three solutions:

**1. Use pipx (recommended — fixes PATH permanently):**
```bash
pip install pipx
pipx ensurepath
pipx install orbiads-cli
# restart your terminal
```

**2. Add Python scripts to PATH manually:**

| OS | Command |
|----|---------|
| macOS | `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc` |
| Linux | `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc` |
| Windows (PowerShell admin) | `$p = python -c "import sysconfig; print(sysconfig.get_path('scripts'))"; [Environment]::SetEnvironmentVariable('PATH', $env:PATH + ";$p", 'User')` |

**3. Use the module directly (no PATH change):**
```bash
python -m orbiads_cli --version
python -m orbiads_cli auth login
python -m orbiads_cli campaigns list
```

### `Authentication failed`

```bash
orbiads auth logout
orbiads auth login   # re-authenticate from scratch
```

Verify your Google account has access to OrbiAds and GAM.

### `Network not found`

```bash
orbiads network list              # list all available networks
orbiads config set network_id ID  # set the correct one
```

### Proxy / corporate firewall

```bash
export HTTPS_PROXY=http://proxy.corp.com:8080
orbiads auth login
```

---

## Next Steps

- [Command Reference](https://orbiads.com/docs/cli/commands) — detailed docs for every command
- [MCP vs CLI](https://orbiads.com/docs/cli/compare) — choose the right tool for the job
- [Skills Guide](https://orbiads.com/docs/cli/skills) — guided workflows in Claude Code
- [OrbiAds Dashboard](https://orbiads.com) — manage credits and GAM connections
