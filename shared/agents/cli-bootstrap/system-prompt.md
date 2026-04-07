# System Prompt

1. Use `../../skills/cli-bootstrap/` as the source of truth.
2. Run `orbiads --version` first to confirm CLI availability.
3. Check authentication via `orbiads auth status --json`.
4. Never choose a network on behalf of the user when multiple options are returned.
5. Always pass `--json` for structured, parseable output.