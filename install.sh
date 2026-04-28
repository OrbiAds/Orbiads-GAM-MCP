#!/usr/bin/env bash
# install.sh — OrbiAds Plugin Installer
#
# Usage:
#   ./install.sh claude          — register MCP in Claude Code (current project)
#   ./install.sh claude --global — register MCP globally in Claude Code
#   ./install.sh openai          — print OpenAI MCP config to copy
#   ./install.sh gemini          — print Gemini extension install steps
#   ./install.sh cli             — install orbiads-cli from local cli/ directory
#   ./install.sh all             — run all commands

set -euo pipefail
# Audit 2026-04-27 phase 4 — aligned with other critical scripts (release.sh,
# us-done.sh, setup-budget-alert.sh) : -u catches unset vars, -o pipefail
# catches failures in piped commands.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_URL="https://orbiads.com/mcp"
PLUGIN_NAME="orbiads"

# ── colours ──────────────────────────────────────────────────────────────────
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

ok()   { echo -e "${GREEN}✅ $*${RESET}"; }
warn() { echo -e "${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "${RED}❌ $*${RESET}"; exit 1; }

# ── claude ───────────────────────────────────────────────────────────────────
install_claude() {
  local scope=""
  [[ "${2:-}" == "--global" ]] && scope="--scope global"

  echo ""
  echo "Installing OrbiAds MCP for Claude Code..."

  if ! command -v claude &>/dev/null; then
    fail "Claude Code CLI not found. Install it first: https://claude.ai/download"
  fi

  # Remove stale entry if it exists, ignore error if not present
  claude mcp remove "$PLUGIN_NAME" $scope 2>/dev/null || true

  # Register the MCP server
  # shellcheck disable=SC2086
  claude mcp add "$PLUGIN_NAME" \
    --transport http \
    --url "$MCP_URL" \
    $scope

  ok "Claude Code: OrbiAds MCP registered at $MCP_URL"

  # Smoke check hint
  echo ""
  echo "  Smoke check (run inside a Claude Code session):"
  echo "    > Confirm my active GAM tenant and network — read-only, no writes."
  echo ""
  echo "  Skills source: $SCRIPT_DIR/claude-plugin/skills/"
  echo "  Agents source: $SCRIPT_DIR/shared/agents/"
  echo "  System prompt: $SCRIPT_DIR/claude-plugin/plugin/system-prompt.md"
}

# ── openai ───────────────────────────────────────────────────────────────────
install_openai() {
  local config="$SCRIPT_DIR/openai-codex/mcp/config.remote.json"
  local agents="$SCRIPT_DIR/openai-codex/AGENTS.md"

  echo ""
  echo "Installing OrbiAds MCP for OpenAI / Codex..."
  echo ""
  echo "  1. Add the following to your OpenAI client MCP configuration:"
  echo ""
  cat "$config"
  echo ""
  echo "  2. Copy AGENTS.md to your workspace root:"
  echo "     cp \"$agents\" ./AGENTS.md"
  echo ""
  ok "OpenAI: config printed above — add to your client settings manually."
  echo ""
  echo "  Smoke check:"
  echo "    > Confirm my active GAM tenant and network — read-only, no writes."
}

# ── gemini ───────────────────────────────────────────────────────────────────
install_gemini() {
  local manifest="$SCRIPT_DIR/gemini-extension/extension/manifest.json"
  local functions="$SCRIPT_DIR/gemini-extension/extension/function-declarations.yaml"
  local instruction="$SCRIPT_DIR/gemini-extension/extension/system-instruction.md"

  echo ""
  echo "Installing OrbiAds Extension for Gemini..."
  echo ""
  echo "  Extension assets:"
  echo "    Manifest    : $manifest"
  echo "    Functions   : $functions"
  echo "    Instruction : $instruction"
  echo ""
  echo "  Load these files into Gemini via:"
  echo "    - Google AI Studio: Extensions > Upload local extension > select extension/"
  echo "    - Vertex AI Agent Builder: attach manifest.json as a tool set"
  echo "    - Direct MCP fallback: point your Gemini client to $MCP_URL"
  echo ""
  ok "Gemini: assets ready at $SCRIPT_DIR/gemini-extension/extension/"
  echo ""
  echo "  Smoke check:"
  echo "    > Classify this request without executing: 'Check my GAM network status.'"
  echo "    > Expected: routes to bootstrap skill, no write path."
}

# ── skills ───────────────────────────────────────────────────────────────────
# Two modes:
#   (default)   print the claude --plugin-dir command for this session
#   --copy      copy SKILL.md files permanently into ~/.claude/skills/
install_skills() {
  local mode="${2:-}"

  echo ""
  echo "Installing OrbiAds skills for Claude Code..."

  if ! command -v claude &>/dev/null; then
    fail "Claude Code CLI not found. Install it first: https://claude.ai/download"
  fi

  if [[ "$mode" == "--copy" ]]; then
    local skills_dir
    skills_dir="$(eval echo "~/.claude/skills")"
    mkdir -p "$skills_dir"

    for skill_dir in "$SCRIPT_DIR/skills"/*/; do
      local skill_name="orbiads-$(basename "$skill_dir")"
      local target="$skills_dir/$skill_name"
      mkdir -p "$target"
      cp "$skill_dir/SKILL.md" "$target/SKILL.md"
      ok "Installed: /orbiads:$(basename "$skill_dir")  →  $target"
    done

    echo ""
    echo "  Skills are now permanently available in all Claude Code sessions."
    echo "  Invoke with:  /orbiads:bootstrap  /orbiads:qa-preview  etc."
  else
    echo ""
    echo "  Start Claude Code with the OrbiAds plugin for this session:"
    echo ""
    echo "    claude --plugin-dir \"$SCRIPT_DIR\""
    echo ""
    echo "  Skills available once loaded:"
    for skill_dir in "$SCRIPT_DIR/skills"/*/; do
      echo "    /orbiads:$(basename "$skill_dir")"
    done
    echo ""
    ok "To install permanently: ./install.sh skills --copy"
  fi

  echo ""
  echo "  Smoke check:  /orbiads:bootstrap"
}

# ── cli (pip/pipx install only) ──────────────────────────────────────────────
_install_cli_binary() {
  local cli_dir="$SCRIPT_DIR/cli"

  echo ""
  echo "Installing OrbiAds CLI..."

  # ── Prefer pipx (auto-handles PATH isolation) ──
  if command -v pipx &>/dev/null; then
    echo "  Using pipx (recommended)..."
    pipx install "$cli_dir" --force
    ok "OrbiAds CLI installed via pipx"
  else
    if ! command -v pip &>/dev/null && ! command -v pip3 &>/dev/null; then
      fail "pip not found. Install Python 3.10+ first: https://python.org"
    fi

    if [[ ! -d "$cli_dir" ]]; then
      fail "CLI directory not found at $cli_dir. Ensure the repo is complete."
    fi

    local pip_cmd="pip"
    command -v pip3 &>/dev/null && pip_cmd="pip3"

    $pip_cmd install -e "$cli_dir"
    ok "OrbiAds CLI installed via pip"
  fi

  # ── Verify orbiads is on PATH ──
  echo ""
  if command -v orbiads &>/dev/null; then
    ok "orbiads is on PATH — $(orbiads --version 2>/dev/null || echo 'ready')"
  else
    warn "orbiads is not on PATH. Fix it with one of these:"
    echo ""
    case "$(uname -s)" in
      MINGW*|MSYS*|CYGWIN*|Windows*)
        local win_path
        win_path="$(python -c 'import sysconfig; print(sysconfig.get_path("scripts"))' 2>/dev/null || echo '%APPDATA%\Python\Python3xx\Scripts')"
        echo "  Windows — add to PATH (run in PowerShell as admin):"
        echo "    [Environment]::SetEnvironmentVariable('PATH', \$env:PATH + ';$win_path', 'User')"
        echo ""
        echo "  Or install with pipx (handles PATH automatically):"
        echo "    pip install pipx && pipx ensurepath && pipx install $cli_dir"
        ;;
      Darwin*)
        echo "  macOS — add to your shell profile:"
        echo "    echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.zshrc && source ~/.zshrc"
        echo ""
        echo "  Or use pipx:  brew install pipx && pipx ensurepath && pipx install $cli_dir"
        ;;
      *)
        echo "  Linux — add to your shell profile:"
        echo "    echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
        echo ""
        echo "  Or use pipx:  pip install pipx && pipx ensurepath && pipx install $cli_dir"
        ;;
    esac
    echo ""
    echo "  Workaround (no PATH change):"
    echo "    python -m orbiads_cli --version"
    echo ""
  fi
}

# ── cli (full: binary + skills) ──────────────────────────────────────────────
install_cli() {
  _install_cli_binary

  # Auto-install CLI skills permanently
  echo ""
  echo "Installing CLI skills..."
  local skills_dir
  skills_dir="$(eval echo "~/.claude/skills")"
  mkdir -p "$skills_dir"

  local count=0
  for skill_dir in "$SCRIPT_DIR/skills"/cli-*/; do
    [[ ! -d "$skill_dir" ]] && continue
    local skill_base
    skill_base="$(basename "$skill_dir")"
    local skill_name="orbiads-${skill_base}"
    local target="$skills_dir/$skill_name"
    mkdir -p "$target"
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    count=$((count + 1))
  done
  ok "$count CLI skills installed in $skills_dir"
  echo ""

  echo "  Ready to go:"
  echo "    1. orbiads auth login       — authenticate with Google"
  echo "    2. orbiads network info     — verify your GAM connection"
  echo "    3. orbiads --help           — see all commands"
  echo ""
  echo "  CLI skills available in Claude Code:"
  for skill_dir in "$SCRIPT_DIR/skills"/cli-*/; do
    [[ ! -d "$skill_dir" ]] && continue
    echo "    /orbiads:$(basename "$skill_dir")"
  done
  echo ""
}

# ── claude (MCP + MCP skills + CLI + CLI skills) ─────────────────────────────
install_claude_full() {
  local scope=""
  [[ "${2:-}" == "--global" ]] && scope="--global"

  # 1. Register MCP server
  install_claude "$@"

  # 2. Install MCP skills permanently
  echo ""
  echo "Installing MCP skills..."
  local skills_dir
  skills_dir="$(eval echo "~/.claude/skills")"
  mkdir -p "$skills_dir"

  local count=0
  for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    [[ ! -d "$skill_dir" ]] && continue
    [[ "$(basename "$skill_dir")" == cli-* ]] && continue  # skip CLI skills
    local skill_name="orbiads-$(basename "$skill_dir")"
    local target="$skills_dir/$skill_name"
    mkdir -p "$target"
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    count=$((count + 1))
  done
  ok "$count MCP skills installed in $skills_dir"

  # 3. Install CLI binary + CLI skills
  _install_cli_binary

  echo ""
  echo "Installing CLI skills..."
  local cli_count=0
  for skill_dir in "$SCRIPT_DIR/skills"/cli-*/; do
    [[ ! -d "$skill_dir" ]] && continue
    local skill_name="orbiads-$(basename "$skill_dir")"
    local target="$skills_dir/$skill_name"
    mkdir -p "$target"
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    cli_count=$((cli_count + 1))
  done
  ok "$cli_count CLI skills installed in $skills_dir"

  echo ""
  echo "  ━━━ Installation complete ━━━"
  echo "  MCP server : registered at $MCP_URL"
  echo "  MCP skills : $count skills (guided AI workflows)"
  echo "  CLI binary : orbiads $(orbiads --version 2>/dev/null || echo '1.0.x')"
  echo "  CLI skills : $cli_count skills (lightweight bash commands)"
  echo ""
  echo "  All skills available in Claude Code:"
  for skill_dir in "$SCRIPT_DIR/skills"/*/; do
    [[ ! -d "$skill_dir" ]] && continue
    echo "    /orbiads:$(basename "$skill_dir")"
  done
  echo ""
  echo "  Smoke check:"
  echo "    > Confirm my active GAM tenant and network — read-only, no writes."
  echo ""
}

# ── all ───────────────────────────────────────────────────────────────────────
install_all() {
  install_claude_full "$@"
  echo ""
  install_openai
  install_gemini
}

# ── dispatch ──────────────────────────────────────────────────────────────────
case "${1:-}" in
  skills) install_skills "$@" ;;
  claude) install_claude_full "$@" ;;
  openai) install_openai ;;
  gemini) install_gemini ;;
  cli)    install_cli ;;
  all)    install_all "$@" ;;
  *)
    echo ""
    echo "Usage: ./install.sh <command> [options]"
    echo ""
    echo "  Commands:"
    echo "    claude              full setup: MCP + skills + CLI (recommended)"
    echo "    claude --global     same, registered globally across all projects"
    echo "    cli                 install CLI binary + CLI skills"
    echo "    openai              print OpenAI MCP config"
    echo "    gemini              print Gemini extension install steps"
    echo "    skills              print the claude --plugin-dir command (session)"
    echo "    skills --copy       copy skills permanently into ~/.claude/skills/"
    echo "    all                 claude + openai + gemini"
    echo ""
    echo "  Quick start (plugin for this session):"
    echo "    claude --plugin-dir \"$SCRIPT_DIR\""
    echo ""
    echo "  MCP endpoint: $MCP_URL"
    echo "  Version:      $(cat "$SCRIPT_DIR/version.json" | grep '"version"' | head -1 | cut -d'"' -f4)"
    echo ""
    exit 1
    ;;
esac
