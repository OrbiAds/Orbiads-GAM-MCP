# Claude Skill Wrapper — availability-forecast

- load `../../shared/agents/availability-forecast/`;
- execute `../../shared/skills/availability-forecast/`;
- use this skill for supply checks and forecast decisions before activation.

## Claude-Specific Hints

- render the forecast result as a structured artifact with `availableUnits`, `pressureLevel`, and `recommendation`;
- use `<handoff>` tags to pass forecast assumptions and key numbers to the next skill;
- apply extended thinking when comparing multiple targeting scenarios before choosing which forecast to run;
- always state the credit cost implication before running a `[variable]` forecast tool.
