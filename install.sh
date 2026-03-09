#!/usr/bin/env bash
# install.sh — OrbiAds Plugin Installer
#
# Usage:
#   ./install.sh claude          — register MCP in Claude Code (current project)
#   ./install.sh claude --global — register MCP globally in Claude Code
#   ./install.sh openai          — print OpenAI MCP config to copy
#   ./install.sh gemini          — print Gemini extension install instructions
#   ./install.sh all             — run all three

set -e

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

# ── all ───────────────────────────────────────────────────────────────────────
install_all() {
  install_skills "$@"
  install_claude "$@"
  install_openai
  install_gemini
}

# ── dispatch ──────────────────────────────────────────────────────────────────
case "${1:-}" in
  skills) install_skills "$@" ;;
  claude) install_claude "$@" ;;
  openai) install_openai ;;
  gemini) install_gemini ;;
  all)    install_all "$@" ;;
  *)
    echo ""
    echo "Usage: ./install.sh <command> [options]"
    echo ""
    echo "  Commands:"
    echo "    skills              print the claude --plugin-dir command (session)"
    echo "    skills --copy       copy skills permanently into ~/.claude/skills/"
    echo "    claude              register MCP in Claude Code (current project)"
    echo "    claude --global     register MCP globally in Claude Code"
    echo "    openai              print OpenAI MCP config"
    echo "    gemini              print Gemini extension install steps"
    echo "    all                 run all commands"
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
