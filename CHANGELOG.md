# Changelog

## v1.0.0 — 2026-03-09

### Initial scaffold release

- 8 shared skills (Batch 1: bootstrap, inventory-ad-units, availability-forecast, deploy-reporting; Batch 2: advertiser-order-line-items, placements-targeting, native-image, qa-preview)
- 12 shared agents (orchestrator, 8 skill agents, credit-guard, context-manager, error-recovery)
- 5 composed workflows (inventory-to-placement, image-to-native, image-to-html5, audio-video-trafficking, deploy-to-reporting)
- Platform wrappers for Claude, OpenAI/Codex, and Gemini
- JSON Schema 2020-12 contracts for skill handoffs, session packets, trigger hints, and workflow manifests

### Known API boundaries (current support: GAM v202602)

- `CreativeAssetService` removed — use inline bytes via `createCreatives`
- `RateCardService` and `PremiumRateService` unavailable — pricing tools return `SERVICE_UNAVAILABLE`
- `create_open_bidding_line_item` not yet implemented — documented as capability boundary only
- REST Interactive Reports API does not work on test networks — production networks only

### Upgrade notes

- bump `compatibleWith.gamApi` in `version.json` when targeting a new GAM API version;
- review `shared/skills/*/tools.md` after each GAM API release for removed or renamed tools;
- update `gemini-extension/extension/function-declarations.yaml` if MCP tool signatures change.
