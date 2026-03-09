# Claude Skill Wrapper — qa-preview

- load `../../shared/agents/qa-preview/`;
- execute `../../shared/skills/qa-preview/`;
- use this skill for compliance, SSL, preview, and go/no-go review.

## Claude-Specific Hints

- render the go/no-go verdict as a prominent artifact with a clear `✅ GO` or `❌ BLOCKED` header;
- list every blocker as a numbered item — unresolved blockers must appear before any deployment suggestion;
- use `<handoff>` tags to pass preview URLs, compliance summary, and coverage status to `deploy-reporting`;
- never suggest deployment in the same turn as a blocking finding — force a separate user confirmation.

## Example

- see `../examples/native-go-live.md`.
