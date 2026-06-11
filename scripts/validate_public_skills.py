#!/usr/bin/env python3
"""
validate_public_skills.py — OrbiAds public skills hygiene validator.

Run from anywhere:
    python orbiads/scripts/validate_public_skills.py [--quiet]

Exit code 0 = all PASS/WARN; exit code 1 = at least one FAIL.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Configuration / constants
# ---------------------------------------------------------------------------

# Parent directory of this script = orbiads/
SCRIPT_DIR = Path(__file__).resolve().parent
ORBIADS_DIR = SCRIPT_DIR.parent

SKILLS_DIR = ORBIADS_DIR / "skills"
PARITY_MATRIX = ORBIADS_DIR / "cli" / "parity-matrix.json"
AGENTS_MD = ORBIADS_DIR / "AGENTS.md"
CLAUDE_MD = ORBIADS_DIR / "CLAUDE.md"
ORBIADS_SKILL_MD = SKILLS_DIR / "orbiads" / "SKILL.md"
WORKFLOWS_DIR = ORBIADS_DIR / "docs" / "workflows"

# Domain anchors that must appear in every skill description (at least one).
DOMAIN_ANCHORS: list[str] = [
    "GAM",
    "Google Ad Manager",
    "ad ops",
    "OrbiAds",
]

# The exact set of skill directories expected on disk.
EXPECTED_SKILLS: set[str] = {
    "orbiads",
    "admin",
    "audit",
    "campaigns",
    "deals",
    "inventory",
    "reporting",
}

# The 6 domain skills (not the orchestrator) that need references/actions.md.
DOMAIN_SKILLS: set[str] = EXPECTED_SKILLS - {"orbiads"}

# Legacy skill names referenced in workflow.yaml files that are now deleted.
LEGACY_WORKFLOW_SKILLS: set[str] = {
    "bootstrap",
    "qa-preview",
    "deploy-reporting",
    "advertiser-order-line-items",
}

# Stale claims to hunt for in doc files.
STALE_CLAIMS: list[str] = [
    "27 sub-skills",
    "27 parent",
    "28 parent",
    "6 sub-skills",
]

MAX_SKILL_LINES = 500
MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024


# ---------------------------------------------------------------------------
# Result accumulation
# ---------------------------------------------------------------------------

class Finding(NamedTuple):
    level: str   # "PASS" | "WARN" | "FAIL"
    check: str
    detail: str


_findings: list[Finding] = []


def record(level: str, check: str, detail: str) -> None:
    _findings.append(Finding(level, check, detail))


def fail(check: str, detail: str) -> None:
    record("FAIL", check, detail)


def warn(check: str, detail: str) -> None:
    record("WARN", check, detail)


def ok(check: str, detail: str) -> None:
    record("PASS", check, detail)


# ---------------------------------------------------------------------------
# Frontmatter parser (stdlib only — no PyYAML)
# ---------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict, int] | tuple[None, int]:
    """
    Parse YAML-ish frontmatter delimited by ``---\\n`` at byte 0 and ``\\n---\\n``.

    Returns (dict_of_top_level_keys, end_line_number) or (None, 0) on failure.
    Only top-level scalar key-value pairs are parsed exactly; nested structures
    are treated leniently (the raw string is stored).
    """
    if not text.startswith("---\n"):
        return None, 0
    end = text.find("\n---\n", 4)
    if end == -1:
        # Also accept trailing ``---`` at EOF without trailing newline.
        end_alt = text.find("\n---", 4)
        if end_alt != -1 and text[end_alt:].rstrip() == "\n---":
            end = end_alt
        else:
            return None, 0
    fm_text = text[4:end]  # content between the two delimiters
    close_line = text[:end].count("\n") + 1  # 1-based line of the closing ---

    result: dict = {}
    current_key: str | None = None
    current_indent: int = 0

    for line in fm_text.splitlines():
        # Skip blank lines
        if not line.strip():
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0:
            # Top-level key
            if ":" in stripped:
                key, _, val = stripped.partition(":")
                key = key.strip()
                val = val.strip()
                result[key] = val if val else {}
                current_key = key
                current_indent = indent
            # else: continuation or weird line — skip
        else:
            # Nested: just collect raw text under the current key
            if current_key and isinstance(result.get(current_key), dict):
                nested = result[current_key]
                if ":" in stripped:
                    k, _, v = stripped.partition(":")
                    nested[k.strip()] = v.strip()

    return result, close_line


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def skill_dirs() -> list[Path]:
    """Return all direct subdirectories of SKILLS_DIR."""
    if not SKILLS_DIR.is_dir():
        return []
    return [d for d in sorted(SKILLS_DIR.iterdir()) if d.is_dir()]


def read_text(path: Path) -> str | None:
    """Read a file to string; return None if unreadable."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def find_md_links(text: str) -> list[str]:
    """Extract all relative markdown link targets from text (not http:// ones)."""
    raw = re.findall(r"\[(?:[^\]]*)\]\(([^)]+)\)", text)
    result = []
    for href in raw:
        href = href.split(" ")[0].strip()  # strip optional title
        if not href.startswith("http"):
            result.append(href)
    return result


# ---------------------------------------------------------------------------
# Check 1: Frontmatter present and closed
# ---------------------------------------------------------------------------

def check_frontmatter_present() -> None:
    check = "1-frontmatter"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            fail(check, f"{d.name}/SKILL.md missing or unreadable")
            continue
        fm, _ = parse_frontmatter(text)
        if fm is None:
            fail(check, f"{d.name}/SKILL.md: no valid frontmatter (must start with --- and have closing ---)")
        else:
            ok(check, f"{d.name}/SKILL.md: frontmatter present and closed")


# ---------------------------------------------------------------------------
# Check 2: Required fields name + description
# ---------------------------------------------------------------------------

_NAME_RE = re.compile(r"^[a-z][a-z0-9-]*$")


def check_required_fields() -> None:
    check = "2-required-fields"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        fm, _ = parse_frontmatter(text)
        if fm is None:
            continue

        # name
        name = fm.get("name", "")
        if not name:
            fail(check, f"{d.name}/SKILL.md: missing 'name' field")
        else:
            if not _NAME_RE.match(name):
                fail(check, f"{d.name}/SKILL.md: name '{name}' is not lowercase-hyphenated")
            if len(name) > MAX_NAME_LEN:
                fail(check, f"{d.name}/SKILL.md: name '{name}' exceeds {MAX_NAME_LEN} chars")

        # description
        desc = fm.get("description", "").strip().strip('"').strip("'")
        if not desc:
            fail(check, f"{d.name}/SKILL.md: missing 'description' field")
        else:
            if len(desc) > MAX_DESC_LEN:
                fail(check, f"{d.name}/SKILL.md: description exceeds {MAX_DESC_LEN} chars ({len(desc)})")
            anchors_found = [a for a in DOMAIN_ANCHORS if a.lower() in desc.lower()]
            if not anchors_found:
                fail(check, (
                    f"{d.name}/SKILL.md: description contains none of the domain anchors "
                    f"{DOMAIN_ANCHORS!r}"
                ))
            else:
                ok(check, f"{d.name}/SKILL.md: description OK (anchor: {anchors_found[0]!r})")


# ---------------------------------------------------------------------------
# Check 3: Dir/name mismatch is a WARN
# ---------------------------------------------------------------------------

def check_name_dir_match() -> None:
    check = "3-name-dir-match"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        fm, _ = parse_frontmatter(text)
        if fm is None:
            continue
        name = fm.get("name", "")
        if not name:
            continue
        expected_alt = f"orbiads-{d.name}"
        if name != d.name and name != expected_alt:
            warn(check, (
                f"{d.name}/SKILL.md: frontmatter name='{name}' matches neither "
                f"'{d.name}' nor '{expected_alt}' (harmless for Claude Code; "
                f"agentskills.io purists may prefer alignment)"
            ))
        else:
            ok(check, f"{d.name}/SKILL.md: name matches dir (name='{name}')")


# ---------------------------------------------------------------------------
# Check 4: Recommended fields version / author / license
# ---------------------------------------------------------------------------

def check_recommended_fields() -> None:
    check = "4-recommended-fields"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        fm, _ = parse_frontmatter(text)
        if fm is None:
            continue
        for field in ("version", "author", "license"):
            if not fm.get(field):
                warn(check, f"{d.name}/SKILL.md: recommended field '{field}' missing")
            else:
                ok(check, f"{d.name}/SKILL.md: '{field}' present")


# ---------------------------------------------------------------------------
# Check 5: user-invokable (misspelled) is FAIL; invocability rules
# ---------------------------------------------------------------------------

def check_invocability() -> None:
    check = "5-invocability"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        fm, _ = parse_frontmatter(text)
        if fm is None:
            continue

        if "user-invokable" in fm:
            fail(check, (
                f"{d.name}/SKILL.md: found misspelled key 'user-invokable' "
                f"(must be 'user-invocable'); the misspelled key is inert"
            ))

        if d.name == "orbiads":
            # Orchestrator must have NO invocability flag
            if "user-invocable" in fm:
                fail(check, (
                    f"{d.name}/SKILL.md: orchestrator must NOT carry a 'user-invocable' flag "
                    f"(got '{fm['user-invocable']}')"
                ))
            else:
                ok(check, f"{d.name}/SKILL.md: orchestrator has no invocability flag (correct)")
        else:
            # Sub-skills must have user-invocable: false
            if "user-invocable" not in fm:
                # Only WARN if 'user-invokable' not also present (already FAILed above)
                if "user-invokable" not in fm:
                    warn(check, (
                        f"{d.name}/SKILL.md: sub-skill missing 'user-invocable: false' "
                        f"(will appear in slash menu)"
                    ))
            else:
                val = fm.get("user-invocable", "")
                if str(val).lower() != "false":
                    fail(check, (
                        f"{d.name}/SKILL.md: sub-skill 'user-invocable' should be 'false', "
                        f"got '{val}'"
                    ))
                else:
                    ok(check, f"{d.name}/SKILL.md: user-invocable: false (correct)")


# ---------------------------------------------------------------------------
# Check 6: SKILL.md <= 500 lines
# ---------------------------------------------------------------------------

def check_line_count() -> None:
    check = "6-line-count"
    for d in skill_dirs():
        skill_md = d / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        lines = text.splitlines()
        n = len(lines)
        if n > MAX_SKILL_LINES:
            fail(check, (
                f"{d.name}/SKILL.md: {n} lines > {MAX_SKILL_LINES} limit; "
                f"move heavy catalogues to references/"
            ))
        else:
            ok(check, f"{d.name}/SKILL.md: {n} lines (within {MAX_SKILL_LINES})")


# ---------------------------------------------------------------------------
# Check 7: Domain skills have references/actions.md and link to it
# ---------------------------------------------------------------------------

def check_references_actions() -> None:
    check = "7-references-actions"
    for domain in sorted(DOMAIN_SKILLS):
        skill_dir = SKILLS_DIR / domain
        if not skill_dir.is_dir():
            # Missing dir — handled by check 9
            continue
        ref_path = skill_dir / "references" / "actions.md"
        if not ref_path.exists():
            fail(check, f"{domain}/references/actions.md: does not exist")
            continue
        ok(check, f"{domain}/references/actions.md: exists")

        # Must be linked from SKILL.md
        skill_md = skill_dir / "SKILL.md"
        text = read_text(skill_md)
        if text is None:
            continue
        links = find_md_links(text)
        normalized = [l.replace("\\", "/") for l in links]
        linked = any("references/actions.md" in l for l in normalized)
        if not linked:
            fail(check, f"{domain}/SKILL.md: does not link to references/actions.md")
        else:
            ok(check, f"{domain}/SKILL.md: links to references/actions.md")


# ---------------------------------------------------------------------------
# Check 8: Relative markdown links resolve; no backend/src links
# ---------------------------------------------------------------------------

def check_md_links() -> None:
    check = "8-md-links"
    for skill_file in sorted(SKILLS_DIR.rglob("*.md")):
        text = read_text(skill_file)
        if text is None:
            continue
        links = find_md_links(text)
        for href in links:
            href_clean = href.split("#")[0]  # strip fragment
            if not href_clean:
                continue

            # Check for forbidden backend/src references
            if "backend/src" in href_clean.replace("\\", "/"):
                fail(check, f"{skill_file.relative_to(ORBIADS_DIR)}: link contains 'backend/src' → {href!r}")
                continue

            # Resolve relative to the file's directory
            resolved = (skill_file.parent / href_clean).resolve()
            # Must be within the repo
            try:
                resolved.relative_to(ORBIADS_DIR.parent)  # repo root = gam-native
            except ValueError:
                fail(check, f"{skill_file.relative_to(ORBIADS_DIR)}: link escapes repo → {href!r}")
                continue

            if not resolved.exists():
                fail(check, f"{skill_file.relative_to(ORBIADS_DIR)}: broken link → {href!r} (resolved: {resolved})")
            else:
                ok(check, f"{skill_file.relative_to(ORBIADS_DIR)}: link OK → {href!r}")


# ---------------------------------------------------------------------------
# Check 9: Expected skill set exactly matches disk
# ---------------------------------------------------------------------------

def check_skill_set() -> None:
    check = "9-skill-set"
    disk = {d.name for d in skill_dirs()}
    extra = disk - EXPECTED_SKILLS
    missing = EXPECTED_SKILLS - disk
    for name in sorted(missing):
        fail(check, f"Expected skill directory 'skills/{name}' is MISSING from disk")
    for name in sorted(extra):
        fail(check, f"Unexpected skill directory 'skills/{name}' found on disk (not in expected set)")
    if not missing and not extra:
        ok(check, f"Skill set matches expected: {sorted(EXPECTED_SKILLS)}")


# ---------------------------------------------------------------------------
# Check 10: CLI-cell integrity in references/actions.md
# ---------------------------------------------------------------------------

def check_cli_cells() -> None:
    check = "10-cli-cells"
    parity_text = read_text(PARITY_MATRIX)
    if parity_text is None:
        warn(check, f"cli/parity-matrix.json not found at {PARITY_MATRIX}; skipping CLI cell check")
        return

    for domain in sorted(DOMAIN_SKILLS):
        actions_md = SKILLS_DIR / domain / "references" / "actions.md"
        if not actions_md.exists():
            # Already flagged in check 7
            continue
        text = read_text(actions_md)
        if text is None:
            continue

        # Find all table cells that look like CLI commands (start with 'orbiads ').
        # Cells are typically wrapped in backticks: `orbiads pql query` — strip them
        # first, otherwise the startswith() test never matches and the check is vacuous.
        cells: list[str] = re.findall(r"\|([^|\n]+)\|", text)
        for raw_cell in cells:
            cell = raw_cell.strip().strip("`").strip()
            if not cell:
                continue
            # Only check cells that look like orbiads commands
            if cell.startswith("orbiads "):
                # The matrix stores commands WITHOUT the 'orbiads ' prefix.
                bare = cell[len("orbiads "):].strip()
                if bare not in parity_text and cell not in parity_text:
                    fail(check, (
                        f"{domain}/references/actions.md: CLI cell '{cell}' not found in "
                        f"cli/parity-matrix.json (invented command or needs matrix update)"
                    ))
                else:
                    ok(check, f"{domain}/references/actions.md: CLI cell '{cell}' found in matrix")
            elif cell.lower() == "mcp-only":
                ok(check, f"{domain}/references/actions.md: 'MCP-only' cell — OK")
            # Other cells (headers, cost values, etc.) are not validated here


# ---------------------------------------------------------------------------
# Check 11: Doc-claim sweep + workflow legacy skill names
# ---------------------------------------------------------------------------

def check_doc_claims() -> None:
    check = "11-doc-claims"

    # Files to check for stale claims
    sweep_files = [AGENTS_MD, CLAUDE_MD, ORBIADS_SKILL_MD]

    for path in sweep_files:
        if not path.exists():
            warn(check, f"{path.relative_to(ORBIADS_DIR)}: file not found, skipping stale-claim sweep")
            continue
        text = read_text(path)
        if text is None:
            continue
        for claim in STALE_CLAIMS:
            for lineno, line in enumerate(text.splitlines(), 1):
                if claim.lower() in line.lower():
                    fail(check, (
                        f"{path.relative_to(ORBIADS_DIR)}:{lineno}: "
                        f"stale claim '{claim}' — {line.strip()!r}"
                    ))

    # Workflow yamls: look for legacy skill names in skills: lists
    if WORKFLOWS_DIR.is_dir():
        for wf_yaml in sorted(WORKFLOWS_DIR.rglob("workflow.yaml")):
            text = read_text(wf_yaml)
            if text is None:
                continue
            for legacy in sorted(LEGACY_WORKFLOW_SKILLS):
                for lineno, line in enumerate(text.splitlines(), 1):
                    stripped = line.strip()
                    # Only flag if it's a list item value matching the legacy skill name
                    if re.fullmatch(r"[-\s]*" + re.escape(legacy), stripped) or \
                            re.search(r"skill:\s+" + re.escape(legacy), stripped):
                        fail(check, (
                            f"{wf_yaml.relative_to(ORBIADS_DIR)}:{lineno}: "
                            f"legacy skill name '{legacy}' — {stripped!r}"
                        ))

    ok(check, "doc-claim sweep complete")


# ---------------------------------------------------------------------------
# Check 12: tool(action="…") references in commands/ and workflows/ are real
# ---------------------------------------------------------------------------

COMMANDS_DIR = ORBIADS_DIR / "commands"

_ACTION_REF_RE = re.compile(r'\b([a-z_][a-z0-9_]*)\(action="([a-zA-Z0-9_.]+)"')
_CATALOG_TOOL_RE = re.compile(r"^### `orbiads:([a-z_][a-z0-9_]*)`", re.MULTILINE)
_CATALOG_ACTION_RE = re.compile(r"^\| `([a-zA-Z0-9_.]+)` \|", re.MULTILINE)


def _load_action_catalog() -> dict[str, set[str]]:
    """Build {parent_tool: {actions}} from all skills/*/references/actions.md."""
    catalog: dict[str, set[str]] = {}
    for domain in sorted(DOMAIN_SKILLS):
        text = read_text(SKILLS_DIR / domain / "references" / "actions.md")
        if text is None:
            continue
        # Split by tool headers, attribute action rows to the preceding header.
        current_tool: str | None = None
        for line in text.splitlines():
            m_tool = _CATALOG_TOOL_RE.match(line)
            if m_tool:
                current_tool = m_tool.group(1)
                catalog.setdefault(current_tool, set())
                continue
            m_action = _CATALOG_ACTION_RE.match(line)
            if m_action and current_tool:
                catalog[current_tool].add(m_action.group(1))
    return catalog


def check_action_references() -> None:
    """Every tool(action="X") in commands/ and docs/workflows/ must exist in the
    generated catalogues — catches fabricated tool/action names in hand-authored docs."""
    check = "12-action-refs"
    catalog = _load_action_catalog()
    if not catalog:
        warn(check, "no actions.md catalogues found; skipping action-reference check")
        return

    scan_files: list[Path] = []
    if COMMANDS_DIR.is_dir():
        scan_files += sorted(COMMANDS_DIR.glob("*.md"))
    if WORKFLOWS_DIR.is_dir():
        scan_files += sorted(WORKFLOWS_DIR.rglob("*.yaml"))
        scan_files += sorted(WORKFLOWS_DIR.rglob("*.md"))

    for path in scan_files:
        text = read_text(path)
        if text is None:
            continue
        for tool, action in _ACTION_REF_RE.findall(text):
            rel = path.relative_to(ORBIADS_DIR)
            if tool not in catalog:
                # Tool not covered by the 6 domain catalogues (e.g. auth) — can't
                # ground it here; warn so a human checks the tool-matrix.
                warn(check, f"{rel}: tool '{tool}' not in domain catalogues — verify '{tool}.{action}' against docs/tool-matrix")
            elif action not in catalog[tool]:
                fail(check, (
                    f"{rel}: action '{action}' does not exist on tool '{tool}' "
                    f"(fabricated name? closest real actions: "
                    f"{sorted(a for a in catalog[tool] if action.split('.')[-1][:4] in a)[:3]})"
                ))
            else:
                ok(check, f"{rel}: {tool}(action=\"{action}\") grounded in catalogue")


# ---------------------------------------------------------------------------
# Check 13: workflow.yaml step modes restricted to the documented vocabulary
# ---------------------------------------------------------------------------

ALLOWED_WORKFLOW_MODES = {"read", "preview_then_write", "optional_write"}


def check_workflow_modes() -> None:
    check = "13-workflow-modes"
    if not WORKFLOWS_DIR.is_dir():
        return
    for wf_yaml in sorted(WORKFLOWS_DIR.rglob("workflow.yaml")):
        text = read_text(wf_yaml)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            m = re.match(r"\s*mode:\s*(\S+)", line)
            if m and m.group(1) not in ALLOWED_WORKFLOW_MODES:
                fail(check, (
                    f"{wf_yaml.relative_to(ORBIADS_DIR)}:{lineno}: mode '{m.group(1)}' "
                    f"not in documented vocabulary {sorted(ALLOWED_WORKFLOW_MODES)}"
                ))
    ok(check, "workflow mode vocabulary check complete")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _safe_print(text: str) -> None:
    """Print text, replacing any un-encodable characters for the current stdout encoding."""
    out = sys.stdout
    enc = getattr(out, "encoding", "utf-8") or "utf-8"
    print(text.encode(enc, errors="replace").decode(enc))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate OrbiAds public skills hygiene."
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Print only FAIL/WARN lines and summary (suppress PASS lines).",
    )
    args = parser.parse_args()

    # Run all checks
    check_frontmatter_present()
    check_required_fields()
    check_name_dir_match()
    check_recommended_fields()
    check_invocability()
    check_line_count()
    check_references_actions()
    check_md_links()
    check_skill_set()
    check_cli_cells()
    check_doc_claims()
    check_action_references()
    check_workflow_modes()

    # Report
    errors = [f for f in _findings if f.level == "FAIL"]
    warnings = [f for f in _findings if f.level == "WARN"]
    passes = [f for f in _findings if f.level == "PASS"]

    for f in _findings:
        if args.quiet and f.level == "PASS":
            continue
        label = {"FAIL": "FAIL", "WARN": "WARN", "PASS": "PASS"}[f.level]
        _safe_print(f"[{label}] ({f.check}) {f.detail}")

    _safe_print("")
    if errors:
        _safe_print(f"FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        return 1
    elif warnings:
        _safe_print(f"PASS ({len(passes)} checks, {len(warnings)} warnings)")
        return 0
    else:
        _safe_print(f"PASS ({len(passes)} checks)")
        return 0


if __name__ == "__main__":
    sys.exit(main())
