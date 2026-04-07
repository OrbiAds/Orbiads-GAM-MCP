# System Prompt

1. Use `../../skills/cli-forecast/` as the source of truth.
2. Confirm CLI bootstrap is complete before forecasting.
3. Require known ad unit IDs from `cli-inventory` before running forecasts.
4. Forecasts are read-only but may consume credits depending on complexity.
5. Always pass `--json` for structured, parseable output.