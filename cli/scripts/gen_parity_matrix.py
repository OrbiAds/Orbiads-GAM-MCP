#!/usr/bin/env python3
"""Story 61.1 — CLI <-> MCP parity matrix generator (source of truth).

Mechanically derives the authoritative parity classification between the MCP
server, the backend REST API and the OrbiAds CLI. Counts are DERIVED here and
nowhere else — no audit/memory hand-tally is authoritative.

Inputs (all static-parsed, no backend import required):
  - backend/src/mcp/tools/*.py     -> every @mcp.tool (AST)            [authoritative tool set]
  - orbiads/cli/src/orbiads_cli/   -> Typer command tree (AST)         [present CLI commands]
  - orbiads/cli/MCP_TO_REST.yaml   -> curated tool -> {area,rest,cli,exempt}

Outputs:
  - orbiads/cli/parity-matrix.json  (machine-readable, the guard's data source)
  - orbiads/cli/PARITY.md           (human-readable, grouped by GAM area)

Status:
  FULL       REST endpoint exists AND a CLI command maps to it
  REST-ONLY  REST endpoint exists, no CLI command  (cheap: pure CLI wrapper)
  MCP-ONLY   no REST route                          (blocked: needs a route first)
  EXEMPT     intentionally out of parity scope (documented reason)
  UNMAPPED   @mcp.tool with no MCP_TO_REST.yaml entry (curation gap — must fix)

Exit codes:
  0  matrix generated, no UNMAPPED tools
  1  one or more @mcp.tool is UNMAPPED (curation incomplete)
  2  --check mode: a non-EXEMPT tool is not FULL (parity regression) — used by Story 63.2 guard
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - yaml is a hard dep of the CLI
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    raise SystemExit(1)

REPO_ROOT = Path(__file__).resolve().parents[3]
MCP_TOOLS_DIR = REPO_ROOT / "backend" / "src" / "mcp" / "tools"
CLI_SRC = REPO_ROOT / "orbiads" / "cli" / "src" / "orbiads_cli"
MAP_FILE = REPO_ROOT / "orbiads" / "cli" / "MCP_TO_REST.yaml"
OUT_JSON = REPO_ROOT / "orbiads" / "cli" / "parity-matrix.json"
OUT_MD = REPO_ROOT / "orbiads" / "cli" / "PARITY.md"


def _is_mcp_tool_decorator(dec: ast.expr) -> bool:
    """True for `@mcp.tool(...)` (Call) or bare `@mcp.tool` (Attribute)."""
    node = dec.func if isinstance(dec, ast.Call) else dec
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "tool"
        and isinstance(node.value, ast.Name)
        and node.value.id == "mcp"
    )


def extract_mcp_tools(tools_dir: Path) -> dict[str, str]:
    """Return {tool_name: module} for every @mcp.tool function. Authoritative."""
    tools: dict[str, str] = {}
    for path in sorted(tools_dir.glob("*.py")):
        if path.name == "__init__.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for fn in ast.walk(tree):
            if isinstance(fn, ast.FunctionDef | ast.AsyncFunctionDef) and any(
                _is_mcp_tool_decorator(d) for d in fn.decorator_list
            ):
                if fn.name in tools:
                    sys.stderr.write(
                        f"WARN duplicate @mcp.tool name {fn.name!r} "
                        f"({tools[fn.name]} & {path.stem})\n"
                    )
                tools[fn.name] = path.stem
    return tools


def _typer_command_name(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    """Resolve a Typer command verb from an @app.command(...) decorated fn."""
    for dec in fn.decorator_list:
        target = dec.func if isinstance(dec, ast.Call) else dec
        if not (isinstance(target, ast.Attribute) and target.attr == "command"):
            continue
        if isinstance(dec, ast.Call) and dec.args and isinstance(dec.args[0], ast.Constant):
            return str(dec.args[0].value)
        # Typer derives the command name from the function name; it keeps the
        # raw identifier (FastAPI/Typer do not auto-kebab unless configured).
        return fn.name
    return None


def extract_cli_commands(cli_src: Path) -> set[str]:
    """Return a set of full "<noun> [<subnoun> ...] <verb>" command paths.

    Resolves both the top-level Typer mounts (main.py `app.add_typer(mod.app, name=...)`)
    AND in-module sub-Typer mounts (e.g. `app.add_typer(templates_app, name="templates")`
    inside ``reporting.py``), so nested groups like
    ``reporting templates list`` are properly detected.
    """
    main_py = cli_src / "main.py"
    module_to_noun: dict[str, str] = {}
    main_tree = ast.parse(main_py.read_text(encoding="utf-8"), filename=str(main_py))
    for call in ast.walk(main_tree):
        if (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "add_typer"
            and call.args
        ):
            arg = call.args[0]
            mod = arg.value.id if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name) else None
            noun = next(
                (kw.value.value for kw in call.keywords if kw.arg == "name" and isinstance(kw.value, ast.Constant)),
                None,
            )
            if mod and noun:
                module_to_noun[mod] = noun

    commands: set[str] = set()
    for mod, noun in module_to_noun.items():
        path = cli_src / "commands" / f"{mod}.py"
        if not path.exists():
            path = cli_src / f"{mod}.py"  # auth.py lives at package root
        if not path.exists():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

        # Inside this module, every Typer-var name maps to its full command-path
        # (relative to the CLI root). The module's main Typer instance is named
        # ``app`` by convention (verified across the existing commands/*.py).
        typer_paths: dict[str, str] = {"app": noun}

        # Walk add_typer calls in this module to attach sub-Typer vars.
        for call in ast.walk(tree):
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "add_typer"
                and call.args
                and isinstance(call.func.value, ast.Name)
            ):
                parent = call.func.value.id
                if parent not in typer_paths:
                    continue
                child_arg = call.args[0]
                child_var = child_arg.id if isinstance(child_arg, ast.Name) else None
                sub_name = next(
                    (kw.value.value for kw in call.keywords
                     if kw.arg == "name" and isinstance(kw.value, ast.Constant)),
                    None,
                )
                if child_var and sub_name:
                    typer_paths[child_var] = f"{typer_paths[parent]} {sub_name}"

        for fn in ast.walk(tree):
            if not isinstance(fn, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            for dec in fn.decorator_list:
                target = dec.func if isinstance(dec, ast.Call) else dec
                if not (isinstance(target, ast.Attribute) and target.attr == "command"):
                    continue
                if not isinstance(target.value, ast.Name):
                    break
                var_name = target.value.id
                if var_name not in typer_paths:
                    break
                if isinstance(dec, ast.Call) and dec.args and isinstance(dec.args[0], ast.Constant):
                    verb = str(dec.args[0].value)
                else:
                    verb = fn.name
                commands.add(f"{typer_paths[var_name]} {verb}")
                break
    return commands


def classify(entry: dict, cli_present: set[str]) -> str:
    if entry.get("exempt"):
        return "EXEMPT"
    rest = entry.get("rest")
    cli = entry.get("cli")
    has_rest = bool(rest) and rest != "NO-REST"
    if not has_rest:
        return "MCP-ONLY"
    if cli:
        return "FULL"
    return "REST-ONLY"


def build_matrix() -> dict:
    tools = extract_mcp_tools(MCP_TOOLS_DIR)
    cli_present = extract_cli_commands(CLI_SRC)
    curated: dict = yaml.safe_load(MAP_FILE.read_text(encoding="utf-8")) or {}
    mapping: dict = curated.get("tools", {})

    rows: list[dict] = []
    for name, module in sorted(tools.items(), key=lambda kv: (kv[1], kv[0])):
        entry = mapping.get(name)
        if entry is None:
            rows.append(
                {"tool": name, "module": module, "area": module,
                 "rest": None, "cli": None, "exempt": None, "status": "UNMAPPED"}
            )
            continue
        status = classify(entry, cli_present)
        cli_cmd = entry.get("cli")
        rows.append(
            {
                "tool": name,
                "module": module,
                "area": entry.get("area", module),
                "rest": entry.get("rest"),
                "cli": cli_cmd,
                "exempt": entry.get("exempt"),
                "status": status,
                "cli_present": (cli_cmd in cli_present) if cli_cmd else None,
            }
        )

    counts: dict[str, int] = {}
    per_area: dict[str, dict[str, int]] = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
        a = per_area.setdefault(r["area"], {})
        a[r["status"]] = a.get(r["status"], 0) + 1

    return {
        "total_tools": len(rows),
        "counts": counts,
        "per_area": per_area,
        "cli_commands_detected": sorted(cli_present),
        "rows": rows,
    }


def write_outputs(m: dict, out_json: Path = OUT_JSON, out_md: Path = OUT_MD) -> None:
    out_json.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    c = m["counts"]
    order = ["FULL", "REST-ONLY", "MCP-ONLY", "EXEMPT", "UNMAPPED"]
    lines: list[str] = [
        "# OrbiAds CLI <-> MCP Parity Matrix",
        "",
        "> Generated by `orbiads/cli/scripts/gen_parity_matrix.py` (Story 61.1).",
        "> **Single source of truth.** Do not hand-edit; do not hardcode these counts elsewhere.",
        "",
        f"**Total @mcp.tool:** {m['total_tools']}  |  "
        + "  ".join(f"**{k}:** {c.get(k, 0)}" for k in order if c.get(k)),
        "",
        "## Summary by GAM area",
        "",
        "| Area | " + " | ".join(order) + " | Total |",
        "|------|" + "|".join(["---"] * len(order)) + "|-------|",
    ]
    for area in sorted(m["per_area"]):
        pa = m["per_area"][area]
        tot = sum(pa.values())
        lines.append(
            f"| {area} | " + " | ".join(str(pa.get(k, 0)) for k in order) + f" | {tot} |"
        )
    lines += ["", "## Full matrix", ""]
    cur_area = None
    for r in sorted(m["rows"], key=lambda r: (r["area"], r["status"], r["tool"])):
        if r["area"] != cur_area:
            cur_area = r["area"]
            lines += [
                "",
                f"### {cur_area}",
                "",
                "| Tool | Status | REST | CLI |",
                "|------|--------|------|-----|",
            ]
        lines.append(
            f"| `{r['tool']}` | {r['status']} | {r.get('rest') or '—'} | "
            f"{('`' + r['cli'] + '`') if r.get('cli') else '—'} |"
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate the CLI<->MCP parity matrix")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Story 63.2 guard mode: exit 2 if any non-EXEMPT tool is not FULL",
    )
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Override write destination for parity-matrix.json and PARITY.md. "
            "When omitted, writes to the canonical orbiads/cli paths."
        ),
    )
    args = ap.parse_args()

    m = build_matrix()
    out_json = OUT_JSON
    out_md = OUT_MD
    if args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        out_json = args.output_dir / "parity-matrix.json"
        out_md = args.output_dir / "PARITY.md"
    write_outputs(m, out_json=out_json, out_md=out_md)

    c = m["counts"]
    if not args.quiet:
        print(f"parity-matrix.json + PARITY.md written ({m['total_tools']} tools)")
        print("  " + "  ".join(f"{k}={v}" for k, v in sorted(c.items())))

    unmapped = [r["tool"] for r in m["rows"] if r["status"] == "UNMAPPED"]
    if unmapped:
        sys.stderr.write(
            f"\n{len(unmapped)} UNMAPPED tool(s) — add them to MCP_TO_REST.yaml:\n"
            + "\n".join(f"  - {t}" for t in unmapped)
            + "\n"
        )
        return 1

    if args.check:
        offenders = [
            r["tool"] for r in m["rows"] if r["status"] not in ("FULL", "EXEMPT")
        ]
        if offenders:
            sys.stderr.write(
                f"\nPARITY GUARD FAIL — {len(offenders)} tool(s) not FULL/EXEMPT:\n"
                + "\n".join(f"  - {t}" for t in offenders)
                + "\n"
            )
            return 2
        if not args.quiet:
            print("PARITY GUARD OK — every @mcp.tool is FULL or EXEMPT")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
