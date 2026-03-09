# Journey Examples

End-to-end session examples grouped by business goal.
Platform-specific examples live in each wrapper: `../claude-plugin/examples/`, `../openai-codex/examples/`, `../gemini-extension/examples/`.

## Available Examples

- `../claude-plugin/examples/bootstrap-session.md` — connect tenant, select network, hand off to inventory
- `../claude-plugin/examples/native-go-live.md` — image-to-native full flow with QA gate
- `../claude-plugin/examples/reporting-follow-up.md` — post-deploy delivery monitoring and report
- `../openai-codex/examples/bootstrap-and-network.md` — bootstrap in Codex message format
- `../openai-codex/examples/order-to-preview.md` — trafficking to QA in Codex format
- `../openai-codex/examples/reporting-rollback.md` — delivery monitoring and rollback plan
- `../gemini-extension/examples/forecast-check.md` — supply check before activation
- `../gemini-extension/examples/inventory-cleanup-boundary.md` — audit with cleanup boundary
- `../gemini-extension/examples/qa-to-deploy.md` — QA gate to deployment

## Portable JSON Examples (shared)

- `../shared/examples/session-packet.json` — canonical session packet shape
- `../shared/examples/forecast-summary.json` — forecast result packet
- `../shared/examples/qa-decision.json` — QA go/no-go decision packet
- `../shared/examples/deployment-summary.json` — post-deploy summary packet

## Rule

- one example = one clear business goal plus the matching guardrails;
- do not duplicate business logic — reference `../shared/skills/` for the canonical steps.
