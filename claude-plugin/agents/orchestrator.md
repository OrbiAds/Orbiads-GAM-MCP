# Claude Orchestrator Bridge

- primary source: `../../shared/agents/orchestrator/`;
- use `routing.md`, `memory.md`, and `escalation.md` before crossing skill boundaries;
- keep Claude-specific wording thin and never restate the business steps from shared skills;
- emit a compact session packet compatible with `../../shared/schemas/session-packet.schema.yaml`.