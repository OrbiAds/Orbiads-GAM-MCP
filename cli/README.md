# OrbiAds CLI

Google Ad Manager from the command line. Deploy campaigns, check inventory, run reports — without opening a browser.

---

## Version Status

- PyPI stable: `orbiads-cli 1.0.1`
- Source tree: `orbiads-cli 1.1.0` (unreleased)

`1.1.0` is a real CLI change, not just a version bump: the local client no
longer ships a baked-in Firebase API key and requires `ORBIADS_FIREBASE_KEY`
for refresh-token exchange. Do not publish `1.1.0` to PyPI until the CLI release
gate is green.

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
# PyPI install: orbiads 1.0.1
# Local source install: orbiads 1.1.0
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

For source builds at `1.1.0` and later, token refresh also requires:

```bash
export ORBIADS_FIREBASE_KEY="<firebase-web-api-key>"
```

Windows PowerShell:

```powershell
$env:ORBIADS_FIREBASE_KEY="<firebase-web-api-key>"
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

## PyPI Release Policy

Publish a new `orbiads-cli` package only when the CLI package itself changes:
CLI source code, commands, local auth/config behavior, runtime or dev
dependencies, packaging metadata, or documentation rendered on PyPI.

Do not publish PyPI for backend-only, hosted MCP-only, or remote server behavior
changes that remain compatible with the existing CLI client.

Before publishing:

1. Verify the latest PyPI version.
2. Ensure `pyproject.toml`, `src/orbiads_cli/__init__.py`, and this README agree.
3. Run the CLI tests: `uv run pytest -q`.
4. Build the package: `uv build`.
5. Check the distributions: `twine check dist/*`.
6. Upload, then verify from a clean environment with `pip install orbiads-cli==<version>`.

If the source version is ahead of PyPI but the release gate is not green, keep
the source version marked as unreleased instead of publishing or pretending the
version exists on PyPI.

Current release gate for `1.1.0`: not green. On 2026-06-10, `uv run pytest -q`
passes collection after adding `PyYAML` to the dev extra, but the suite still
fails on public CLI catalogue drift and MCP parity drift (`server_info`
unmapped). PyPI therefore remains at `1.0.1`.

---

## Links

- [Full documentation](https://orbiads.com/docs/cli)
- [Command reference](https://orbiads.com/docs/cli/commands)
- [MCP vs CLI comparison](https://orbiads.com/docs/cli/compare)
- [OrbiAds Dashboard](https://orbiads.com)
- [GitHub](https://github.com/OrbiAds/Orbiads-GAM-MCP)
