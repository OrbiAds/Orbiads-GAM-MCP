# OrbiAds CLI — Installation Guide

## Prerequisites

- **Python 3.10+** (check with `python3 --version`)
- **pip** (usually included with Python)
- An **OrbiAds account** ([sign up free](https://orbiads.com))
- A **Google Ad Manager** account connected to OrbiAds

---

## Installation

### From PyPI (recommended)

```bash
pip install orbiads-cli
```

### From the repository

```bash
git clone https://github.com/OrbiAds/Orbiads-GAM-MCP.git
cd Orbiads-GAM-MCP
./install.sh cli
```

This runs `pip install -e cli/` from the local directory.

### Verify installation

```bash
orbiads --version
```

Expected output: `orbiads-cli 1.0.0`

---

## Authentication

OrbiAds CLI uses **Google OAuth 2.0 Device Flow** — no passwords are stored.

### Step 1: Log in

```bash
orbiads auth login
```

The CLI displays a code and a URL. Open the URL in your browser, enter the code, and authorize with your Google account.

### Step 2: Verify

```bash
orbiads auth status
```

Expected output: `Authenticated as user@gmail.com (network: 12345678)`

### Token storage

Tokens are stored in `~/.orbiads/credentials.json`, encrypted at rest. To remove them:

```bash
orbiads auth logout
```

---

## First Command

```bash
orbiads network info
```

This fetches your GAM network details (name, ID, timezone, currency) and confirms the CLI is working.

---

## Configuration

The CLI stores settings in `~/.orbiads/config.toml`:

```toml
[default]
network_id = "12345678"
output = "table"        # or "json"
locale = "en"           # fr, en, es, it
```

Manage via CLI:

```bash
orbiads config set network_id 12345678
orbiads config set output json
orbiads config list
```

---

## Troubleshooting

### `command not found: orbiads`

Your Python scripts directory is not in PATH. Try:

```bash
python3 -m orbiads_cli --version
```

Or add the pip scripts directory to your PATH:

- **macOS/Linux**: `export PATH="$HOME/.local/bin:$PATH"` (add to `~/.bashrc` or `~/.zshrc`)
- **Windows**: `pip install` usually adds to PATH automatically; restart your terminal

### `Authentication failed`

1. Run `orbiads auth logout` then `orbiads auth login` to re-authenticate
2. Ensure your Google account has access to OrbiAds and GAM
3. Check your internet connection

### `Network not found`

1. Run `orbiads network list` to see available networks
2. Set the correct network: `orbiads config set network_id <ID>`
3. Ensure GAM is connected in your OrbiAds dashboard

### Proxy / corporate firewall

```bash
export HTTPS_PROXY=http://proxy.corp.com:8080
orbiads auth login
```

---

## Next Steps

- [Command Reference](https://orbiads.com/docs/cli/commands) — full list of commands
- [MCP vs CLI](https://orbiads.com/docs/cli/compare) — choose the right method
- [OrbiAds Dashboard](https://orbiads.com) — manage credits and settings
