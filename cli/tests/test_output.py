"""Tests for output formatters — Story 55.9 Task 1.

Covers: render() in table/JSON/CSV mode, auto-JSON detection for non-TTY,
confirm() with --yes, JSON→stdout-only, errors→stderr-only.
"""

import csv
import io
import json
import sys
from unittest.mock import patch

import pytest

from orbiads_cli.output import OutputContext, confirm, error, render, render_detail


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

_ROWS = [
    {"id": "c1", "name": "Campaign A", "status": "draft"},
    {"id": "c2", "name": "Campaign B", "status": "deployed"},
]
_COLUMNS = ["id", "name", "status"]


# ===========================================================================
# render() — table format
# ===========================================================================


class TestRenderTable:

    def test_table_output_contains_column_headers(self, capsys):
        ctx = OutputContext(format="table")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        assert "id" in out
        assert "name" in out
        assert "status" in out

    def test_table_output_contains_data(self, capsys):
        ctx = OutputContext(format="table")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        assert "Campaign A" in out
        assert "c2" in out

    def test_table_output_no_json(self, capsys):
        """Table output should not be valid JSON."""
        ctx = OutputContext(format="table")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        with pytest.raises(json.JSONDecodeError):
            json.loads(out)


# ===========================================================================
# render() — JSON format
# ===========================================================================


class TestRenderJSON:

    def test_json_output_is_valid(self, capsys):
        ctx = OutputContext(format="json")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) == 2

    def test_json_preserves_data(self, capsys):
        ctx = OutputContext(format="json")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data[0]["name"] == "Campaign A"
        assert data[1]["status"] == "deployed"

    def test_json_empty_list(self, capsys):
        ctx = OutputContext(format="json")
        render([], _COLUMNS, ctx)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data == []

    def test_json_output_has_no_stderr(self, capsys):
        """JSON data goes to stdout only — stderr must be empty."""
        ctx = OutputContext(format="json")
        render(_ROWS, _COLUMNS, ctx)
        captured = capsys.readouterr()
        assert captured.err == ""
        # stdout should contain the JSON
        data = json.loads(captured.out)
        assert len(data) == 2


# ===========================================================================
# render() — CSV format
# ===========================================================================


class TestRenderCSV:

    def test_csv_has_headers(self, capsys):
        ctx = OutputContext(format="csv")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        reader = csv.reader(io.StringIO(out))
        header = next(reader)
        assert header == ["id", "name", "status"]

    def test_csv_has_correct_rows(self, capsys):
        ctx = OutputContext(format="csv")
        render(_ROWS, _COLUMNS, ctx)
        out = capsys.readouterr().out
        reader = csv.DictReader(io.StringIO(out))
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["name"] == "Campaign A"
        assert rows[1]["id"] == "c2"

    def test_csv_empty_data(self, capsys):
        ctx = OutputContext(format="csv")
        render([], _COLUMNS, ctx)
        out = capsys.readouterr().out
        reader = csv.reader(io.StringIO(out))
        header = next(reader)
        assert header == ["id", "name", "status"]
        remaining = list(reader)
        assert remaining == []


# ===========================================================================
# render_detail() — JSON / table
# ===========================================================================


class TestRenderDetail:

    def test_detail_json(self, capsys):
        ctx = OutputContext(format="json")
        render_detail({"plan": "starter", "credits": 42}, ctx)
        out = capsys.readouterr().out
        data = json.loads(out)
        assert data["plan"] == "starter"
        assert data["credits"] == 42

    def test_detail_table(self, capsys):
        ctx = OutputContext(format="table")
        render_detail({"plan": "starter", "credits": 42}, ctx)
        out = capsys.readouterr().out
        assert "plan" in out
        assert "starter" in out

    def test_detail_csv(self, capsys):
        ctx = OutputContext(format="csv")
        render_detail({"plan": "starter", "credits": 42}, ctx)
        out = capsys.readouterr().out
        reader = csv.DictReader(io.StringIO(out))
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["plan"] == "starter"


# ===========================================================================
# Auto-JSON when stdout is not a TTY
# ===========================================================================


class TestAutoJSON:

    def test_auto_json_when_not_tty(self):
        """When stdout.isatty() returns False and no format specified, use JSON."""
        with patch.object(sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            ctx = OutputContext.from_flags(json_flag=False, output=None, yes=False)
        assert ctx.format == "json"

    def test_table_when_tty(self):
        """When stdout.isatty() returns True and no format specified, use table."""
        with patch.object(sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = True
            ctx = OutputContext.from_flags(json_flag=False, output=None, yes=False)
        assert ctx.format == "table"

    def test_explicit_csv_overrides_auto(self):
        """Explicit --output csv should win even if not a TTY."""
        with patch.object(sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = False
            ctx = OutputContext.from_flags(json_flag=False, output="csv", yes=False)
        assert ctx.format == "csv"

    def test_json_flag_overrides_all(self):
        """--json flag always produces JSON regardless of TTY."""
        with patch.object(sys, "stdout") as mock_stdout:
            mock_stdout.isatty.return_value = True
            ctx = OutputContext.from_flags(json_flag=True, output=None, yes=False)
        assert ctx.format == "json"


# ===========================================================================
# confirm() with --yes
# ===========================================================================


class TestConfirm:

    def test_confirm_yes_returns_true(self):
        """When yes=True, confirm() returns True without prompting."""
        ctx = OutputContext(yes=True)
        assert confirm("Delete everything?", ctx) is True

    def test_confirm_non_tty_returns_true(self):
        """When stderr is not a TTY, confirm() auto-accepts."""
        ctx = OutputContext(yes=False)
        with patch.object(sys, "stderr") as mock_stderr:
            mock_stderr.isatty.return_value = False
            result = confirm("Continue?", ctx)
        assert result is True


# ===========================================================================
# error() goes to stderr only — no stdout content
# ===========================================================================


class TestErrorSeparation:

    def test_error_output_no_stdout(self, capsys):
        """error() writes to stderr only — stdout must be empty."""
        error("Something went wrong")
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Something went wrong" in captured.err
