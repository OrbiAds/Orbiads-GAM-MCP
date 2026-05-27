# OrbiAds — Claude Code Project Guidance

> This file is read by **Claude Code** when working IN this repo.
> For agents working THROUGH this repo (calling the OrbiAds MCP server or CLI from another project), see [`AGENTS.md`](./AGENTS.md) — it covers cross-LLM boundaries (Cursor, Codex, Gemini, etc.) and the OrbiAds surface contract.

---

## What this repo is

The **public mirror** of the `orbiads/` subtree of the private monorepo `gam-native`. Published as a Claude Code plugin (`@orbiads`) + Python CLI (`orbiads-cli`) + MCP server (`https://orbiads.com/mcp`).

Source of truth = `gam-native` (private). This repo is **read-mostly** — most of its files are **generated** from the backend code by `scripts/generate_skills/generate.py` and protected by a CI drift gate. Hand-edit a generated file → CI fails. Edits go to the backend source instead, then re-run the generator.

---

## Generated vs hand-authored — IMPORTANT for Claude Code

| File / directory | Generated? | Source of truth | Edit policy |
| --- | --- | --- | --- |
| `version.json` | ✅ generated | `scripts/generate_skills/lib/generators/version_bump.py` + catalogue state | DO NOT EDIT — re-run generator |
| `CHANGELOG.md` | ✅ generated (idempotent prepend) | same | DO NOT EDIT existing entries; new entries are prepended by the generator |
| `docs/tool-matrix/README.md` | ✅ generated | `backend/src/mcp/tools/*.py` via AST | DO NOT EDIT |
| `_docs/legacy-tool-mapping.md` | ✅ generated | `@deprecated_tool` decorators in `backend/src/mcp/tools/*.py` | DO NOT EDIT |
| `skills/<parent>/SKILL.md` | ✅ generated (Story 81.2+) | parent metadata from catalogue | DO NOT EDIT |
| `skills/orbiads/SKILL.md` | ❌ hand-authored | this file | EDIT — it's the orchestrator narrative |
| `AGENTS.md` | ❌ hand-authored | this file | EDIT — cross-LLM contract, careful with breaking changes |
| `CLAUDE.md` | ❌ hand-authored | this file | EDIT — Claude-internal guidance |
| `README.md` | ❌ hand-authored | this file | EDIT — GitHub human-facing |
| `.claude-plugin/plugin.json` | ❌ hand-authored (version field bumped manually for now) | this file | EDIT — manifest evolves with packaging changes |
| `.claude-plugin/marketplace.json` | ❌ hand-authored | this file | EDIT |
| `cli/parity-matrix.json` | semi-generated | external `scripts/coverage-audit/` pipeline | EDIT via that pipeline — DO NOT hand-edit |

**The CI gate** (`.github/workflows/generated-files-check.yml` in the parent monorepo) runs `generate.py --check` and fails if any generated file diverges. Run it locally before pushing:

```bash
python ../scripts/generate_skills/generate.py --check
```

---

## Project structure

See [`AGENTS.md`](./AGENTS.md) section "Project structure" for the full tree. Highlights:

- `skills/` — Agent Skills (orchestrator + 27 sub-skills, one per MCP parent tool)
- `cli/` — Python CLI source (`orbiads-cli` publishable to PyPI)
- `docs/` — install guides, tool matrix, safety
- `_docs/` — internal docs (legacy mapping, anti-collision rules)
- `shared/` — transitional folder (pre-Epic 81 layout, will be sunset in Story 81.4)
- `extensions/` — gemini-extension + openai-codex helpers (transition)

---

## Claude Code-specific patterns

### Extended thinking
Use it generously when planning a write to GAM. The MCP tool calls cost real credits — a few seconds of thinking saves a credit refund cycle.

### Sub-agents via the `Task` tool
For multi-dimensional audits (`/adops audit`), the recommended pattern is parallel-spawn with `context: fork` and dedicated output files. See claude-ads / claude-seo plugins for reference implementations. Story 81.4 introduces this pattern in OrbiAds (`agents/audit-delivery.md`, etc.).

### Plugin install
```bash
claude plugin install orbiads
```
After install, this directory is **copied** to `~/.claude/plugins/marketplaces/<marketplace>/orbiads/` — Claude Code does NOT symlink. That's why we don't use symlinks for cross-file references (they'd break post-install).

### Slash commands (Story 81.3)
Will live in `commands/adops-*.md` with frontmatter `description`, `argument-hint`, `allowed-tools`, `model`. The frontmatter `allowed-tools` is the security boundary — it mechanically prevents the LLM from calling tools outside the command's scope.

---

## Tech stack

| Layer | Detail |
| --- | --- |
| **Backend** (gam-native private monorepo) | Python 3.11+, FastAPI, Pydantic V2, FastMCP, Firestore, Cloud Run |
| **Frontend** (gam-native private) | SvelteKit 5, TypeScript, Tailwind 4 |
| **Public repo (this)** | Markdown + JSON + Python CLI |
| **GAM API target** | `v202605` |
| **MCP protocol** | `2025-03-26` (streamable-http) |
| **Architecture** | Clean: `domain` ← `adapters` ← `services` ← `api` (private repo); spec-driven generation (public repo) |
| **API format** | JSend-inspired: `{ data, error }`. JSON camelCase on the wire. |

---

## Workflow for changing this repo

If you (Claude) are editing this repo to add/change a feature:

1. **Is the change a fix to a generated file?** ❌ — fix the backend source instead, then re-run the generator. Verify with `--check`.

2. **Is the change to a hand-authored file?** ✅ proceed.
   - Markdown content (AGENTS.md, CLAUDE.md, README.md, skills/orbiads/SKILL.md): just edit.
   - Plugin manifest (`plugin.json`, `marketplace.json`): bump `version` if shipping a new release.
   - CLI source (`cli/src/...`): standard Python changes + tests.

3. **Branch / commit / PR**
   - Branch: `story/81.X` (or `feature/<name>`) from `master`.
   - Commit: Conventional Commits, `Co-Authored-By` trailer.
   - PR: target `master`. 1 story = 1 PR (cross-story mixing is discouraged).

4. **Run the local drift check** before pushing if you touched anything generator-adjacent:
   ```bash
   python ../scripts/generate_skills/generate.py --check
   python -m pytest ../scripts/generate_skills/tests/
   ```

---

## Safety boundaries (mirror of AGENTS.md but emphasized for Claude)

- ✅ Reads are free, call them liberally for state discovery.
- ✅ Use `extended_thinking` before any write.
- ❌ Never bypass `billing_guard` in the backend or the CLI.
- ❌ Never call `action="deploy"` on `campaign` without a fresh `confirmation_token`.
- ❌ Never hand-edit a generated file.
- ❌ Never push directly to `master` — always PR.
- ❌ Never invent a `tenantId` / `networkCode` — call `get_my_tenant_id` first.

---

## Where to look

- **What can the MCP do?** → [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md) (27 parents + actions)
- **Legacy → parent migration** → [`_docs/legacy-tool-mapping.md`](./_docs/legacy-tool-mapping.md)
- **CLI commands** → [`cli/PARITY.md`](./cli/PARITY.md)
- **Cross-LLM contract** → [`AGENTS.md`](./AGENTS.md)
- **Examples** → [`examples/`](./examples/)
- **GitHub README** → [`README.md`](./README.md)
