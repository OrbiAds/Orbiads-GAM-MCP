"""Tests for the CLI<->MCP parity matrix generator — Story 61.1.

Locks the keystone deliverable: a code-derived, authoritative classification
of every @mcp.tool. Also exercises the --check guard hook consumed by Story 63.2.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

CLI_ROOT = Path(__file__).resolve().parents[1]
GEN = CLI_ROOT / "scripts" / "gen_parity_matrix.py"

_spec = importlib.util.spec_from_file_location("gen_parity_matrix", GEN)
gpm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gpm)

VALID_STATUSES = {"FULL", "REST-ONLY", "MCP-ONLY", "EXEMPT", "UNMAPPED"}


@pytest.fixture(scope="module")
def matrix():
    return gpm.build_matrix()


def test_all_mcp_tools_extracted():
    """AST extraction must find every @mcp.tool.

    Story 68.6: +4 EXEMPT parents (creative_qa, inventory, placements,
    targeting) folding 39 legacy tools behind the parent>child pattern.
    Story 68.5: +4 EXEMPT parents (audit, billing, gam_features, network).
    Story 76.1: +1 FULL parent creative_wrapper_skill.
    Total 257 -> 258."""
    tools = gpm.extract_mcp_tools(gpm.MCP_TOOLS_DIR)
    assert len(tools) == 258, f"expected 258 @mcp.tool, found {len(tools)}"
    # spot-check a few known tools land in the right module
    assert tools["deploy_campaign"] == "campaign_ops"
    assert tools["run_pql_query"] == "pql"
    assert tools["list_advertisers"] == "advertisers"


def test_every_tool_classified_no_unmapped(matrix):
    """The curated map must cover 100% of tools — zero UNMAPPED."""
    assert matrix["total_tools"] == 258
    statuses = {r["status"] for r in matrix["rows"]}
    assert statuses <= VALID_STATUSES
    unmapped = [r["tool"] for r in matrix["rows"] if r["status"] == "UNMAPPED"]
    assert unmapped == [], f"UNMAPPED tools (add to MCP_TO_REST.yaml): {unmapped}"


def test_counts_reconcile(matrix):
    """The split must sum to the total — fixes the audit's non-reconciling tally."""
    assert sum(matrix["counts"].values()) == matrix["total_tools"] == 258


def test_pricing_is_exempt(matrix):
    """GAM removed RateCardService/PremiumRateService v202502+ — permanently EXEMPT."""
    pricing = [r for r in matrix["rows"] if r["area"] == "pricing"]
    assert len(pricing) == 5
    assert all(r["status"] == "EXEMPT" for r in pricing)
    assert all(r["exempt"] for r in pricing)


def test_full_tools_have_a_real_cli_command(matrix):
    """Any FULL tool must map to a CLI command that actually exists in the
    Typer tree — catches mapping drift in MCP_TO_REST.yaml."""
    detected = set(matrix["cli_commands_detected"])
    drift = [
        (r["tool"], r["cli"])
        for r in matrix["rows"]
        if r["status"] == "FULL" and r["cli"] not in detected
    ]
    assert drift == [], f"FULL tools mapped to non-existent CLI command: {drift}"


def test_creative_wrapper_skill_documents_every_sub_action(matrix):
    row = next(r for r in matrix["rows"] if r["tool"] == "creative_wrapper_skill")

    assert set(row["sub_actions"]) == {
        "list",
        "get",
        "create",
        "update",
        "activate",
        "deactivate",
        "archive",
        "set_data_declaration",
        "list_rich_media_ads_companies",
        "find_third_party_company",
        "create_preset",
        "list_wrapper_presets",
    }
    assert row["sub_actions"]["list"]["rest"] == "GET /api/gam/creative-wrappers"
    assert row["sub_actions"]["deactivate"]["cli"] == "creative-wrappers deactivate"
    assert row["sub_actions"]["archive"]["rest"] == "NO-REST"
    assert (
        row["sub_actions"]["set_data_declaration"]["rest"]
        == "PATCH /api/gam/creative-wrappers/{wrapper_id}/data-declaration"
    )
    assert row["sub_actions"]["create_preset"]["rest"] == "NO-REST"
    assert "Story 76.2" in row["sub_actions"]["list_wrapper_presets"]["exempt"]


def test_mcp_only_tools_have_no_rest(matrix):
    for r in matrix["rows"]:
        if r["status"] == "MCP-ONLY":
            assert r["rest"] in (None, "NO-REST"), r


def test_outputs_written_and_valid(tmp_path, monkeypatch):
    """gen writes a valid JSON matrix + a Markdown report; plain run exits 0."""
    rc = subprocess.run(
        [sys.executable, str(GEN), "--quiet"], cwd=str(CLI_ROOT), capture_output=True, text=True
    )
    assert rc.returncode == 0, rc.stderr
    data = json.loads((CLI_ROOT / "parity-matrix.json").read_text(encoding="utf-8"))
    assert data["total_tools"] == 258
    md = (CLI_ROOT / "PARITY.md").read_text(encoding="utf-8")
    assert "OrbiAds CLI <-> MCP Parity Matrix" in md
    assert "single source of truth" in md.lower()


def test_check_mode_is_the_story_63_2_guard():
    """--check exits 0 once every tool is FULL or EXEMPT.

    Updated 2026-05-21 (Story 66.1) : with Epic 63 landed and Story 66.1
    adding `reporting_skill` as FULL, every tool is now classified — guard
    flips to exit 0. If a future @mcp.tool lands without a CLI/REST mapping
    or an explicit `exempt:` entry, this guard fails again (its intended
    long-term role)."""
    rc = subprocess.run(
        [sys.executable, str(GEN), "--check", "--quiet"],
        cwd=str(CLI_ROOT),
        capture_output=True,
        text=True,
    )
    assert rc.returncode == 0, f"parity should be complete; stderr={rc.stderr}"
