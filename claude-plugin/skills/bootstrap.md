# Claude Skill Wrapper — bootstrap

- load `../../shared/agents/bootstrap/` for routing and memory;
- execute `../../shared/skills/bootstrap/` as the business source of truth;
- use this skill when `tenantId` or `networkCode` is still unconfirmed.

## Claude-Specific Hints

- wrap the output packet in `<handoff>` tags so downstream skills can parse it without re-reading;
- use an artifact (table) for network selection when `list_accessible_networks` returns more than one result;
- apply extended thinking before deciding whether to run full bootstrap or call `switch_network` only;
- keep the confirmation message short — one sentence per confirmed field is enough.

## Example

- see `../examples/bootstrap-session.md`.
