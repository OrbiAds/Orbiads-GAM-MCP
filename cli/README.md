# OrbiAds CLI

Google Ad Manager from the command line. Deploy campaigns, check inventory, run reports — without opening a browser.

---

## Install (30 seconds)

```bash
# Option 1 — pipx (recommended, auto-handles PATH)
pipx install orbiads-cli

# Option 2 — pip
pip install orbiads-cli

# Option 3 — from this repo
./install.sh cli
```

Verify:

```bash
orbiads --version
# orbiads 1.0.1
```

> **`command not found`?** See [Troubleshooting](#troubleshooting) below.

---

## Authenticate (one time)

```bash
orbiads auth login
```

A code and URL are displayed. Open the URL, enter the code, authorize with Google. Done.

```bash
orbiads auth status
# Authenticated as user@gmail.com (network: 12345678)
```

---

## Quick Start

```bash
# See your GAM network
orbiads network info

# List campaigns
orbiads campaigns list

# Get JSON output (for scripts)
orbiads campaigns list --json

# Run a delivery report
orbiads reporting run --template 12345 --json

# Check inventory before trafficking
orbiads inventory ad-units

# Check credit balance
orbiads billing balance
```

---

## All Commands

| Group | Commands | Description |
|-------|----------|-------------|
| `auth` | `login`, `logout`, `status` | Google OAuth Device Flow |
| `network` | `info`, `list`, `switch` | GAM network context |
| `campaigns` | `list`, `get`, `deploy`, `pause`, `archive` | Campaign management |
| `orders` | `list`, `get`, `create` | Order management |
| `creatives` | `list`, `get`, `upload` | Creative management |
| `advertisers` | `list`, `get`, `create` | Advertiser management |
| `inventory` | `ad-units`, `placements`, `targeting-keys` | Inventory browsing |
| `reporting` | `run`, `templates` | Reports and exports |
| `billing` | `balance`, `usage` | Credit balance and history |
| `config` | `list`, `set`, `get` | CLI configuration |

### Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Raw JSON output (for piping to `jq`, scripts) |
| `--output table\|json\|csv` | Output format |
| `--yes`, `-y` | Skip confirmation prompts |
| `--version` | Show CLI version |

---

## CLI + MCP + Skills — How They Work Together

OrbiAds has 3 integration layers that complement each other:

```
┌─────────────────────────────────────────────────┐
│  Skills (8 guided workflows)                    │
│  /orbiads:bootstrap  /orbiads:qa-preview  ...   │
│  → Load in Claude Code, ChatGPT, Gemini         │
├─────────────────────────────────────────────────┤
│  MCP Server (168 tools)                         │
│  https://orbiads.com/mcp                        │
│  → AI agents call tools via MCP protocol        │
├─────────────────────────────────────────────────┤
│  CLI (10 command groups)                        │
│  orbiads campaigns list --json                  │
│  → Terminal, scripts, CI/CD, automation          │
└─────────────────────────────────────────────────┘
         ↓           ↓           ↓
      Same API · Same credits · Same guardrails
```

| Use case | Best tool |
|----------|-----------|
| Explore GAM interactively with AI | **MCP** (via Claude/ChatGPT) |
| Guided campaign deployment | **Skills** (`/orbiads:deploy-reporting`) |
| Scripted automation, CI/CD | **CLI** (`orbiads deploy --json`) |
| Quick checks from terminal | **CLI** (`orbiads network info`) |
| Complex multi-step workflows | **Skills** + MCP combined |

### Use CLI inside Claude Code

Claude Code can call the CLI directly:

```
> Run `orbiads campaigns list --json` and summarize the active campaigns
```

Or use it as a data source for Skills:

```
> /orbiads:qa-preview
> Use `orbiads reporting run --template 789` to check delivery
```

---

## Configuration

Settings are stored in `~/.orbiads/config.json`:

```bash
orbiads config set output json       # default output format
orbiads config set network_id 12345  # default GAM network
orbiads config list                  # show all settings
```

---

## Troubleshooting

### `command not found: orbiads`

The Python scripts directory is not in your PATH.

**Quick fix (any OS):**
```bash
python -m orbiads_cli --version
```

**Permanent fix — use pipx (recommended):**
```bash
pip install pipx
pipx ensurepath   # adds ~/.local/bin to PATH automatically
pipx install orbiads-cli
# restart your terminal
```

**Manual fix by OS:**

| OS | Command |
|----|---------|
| **macOS** | `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc` |
| **Linux** | `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc` |
| **Windows** | In PowerShell (admin): `[Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';' + (python -c "import sysconfig; print(sysconfig.get_path('scripts'))"), 'User')` |

### `Authentication failed`

```bash
orbiads auth logout
orbiads auth login   # re-authenticate
```

### `Network not found`

```bash
orbiads network list              # see available networks
orbiads config set network_id ID  # set the correct one
```

---

## Links

- [Full documentation](https://orbiads.com/docs/cli)
- [Command reference](https://orbiads.com/docs/cli/commands)
- [MCP vs CLI comparison](https://orbiads.com/docs/cli/compare)
- [OrbiAds Dashboard](https://orbiads.com)
- [GitHub](https://github.com/OrbiAds/Orbiads-GAM-MCP)
