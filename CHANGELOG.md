# Changelog


## v1.7.0 — 2026-05-28

### Catalogue refactor — parent>child consolidation

Replaces the flat catalogue (8 shared skills + ~270 child tools at v1.0.0) with **28 parent tools** that dispatch all operations via an `action` discriminator. The 219 pre-refactor child tools remain available as soft-deprecated wrappers that route to their parent (emit `deprecated_tool_called` analytics).

### New parent tools by Epic batch

- **Epic 20**: `campaign`
- **Epic 64**: `deals`
- **Epic 65**: `audit_skill`, `gam_admin`
- **Epic 68**: `audiences`, `audit`, `billing`, `creative_assets`, `creative_qa`, `creatives`, `gam_features`, `inventory`, `jobs`, `line_items`, `network`, `orders`, `placements`, `pql`, `preview`, `reporting`, `settings`, `targeting`
- **Epic 76**: `creative_wrapper_skill`
- **Epic 70**: `prebid_skill` REST/CLI parity for generated line items, targeting keys, preview, and cleanup
- **Epic 78**: `blueprint`, `formats`, `tenant_catalog`
- **Epic 82**: `gam_jobs`

### Largest parent tools (by action count)

| Parent | Actions | Mode |
|---|---|---|
| `gam_admin` | 48 | mixed (read + write) |
| `reporting` | 31 | mixed (read + write) |
| `deals` | 28 | mixed (read + write) |
| `creatives` | 27 | mixed (read + write) |
| `targeting` | 18 | mixed (read + write) |
| `creative_assets` | 15 | mixed (read + write) |
| `line_items` | 15 | mixed (read + write) |
| `blueprint` | 13 | mixed (read + write) |

### Migration guide

- New consumers: call parent tools with `action: <child_name>` (or `(area, action)` for `companies` / `gam_admin`). See [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md).
- Existing integrations using legacy tool names: no action required — wrappers still work but emit deprecation telemetry. Plan migration per [`_docs/legacy-tool-mapping.md`](./_docs/legacy-tool-mapping.md).
- GAM API target: `v202602` (unchanged). MCP protocol: `2025-03-26` (unchanged).

## v1.6.0 — 2026-05-27

### Catalogue refactor — parent>child consolidation

Replaces the flat catalogue (8 shared skills + ~270 child tools at v1.0.0) with **27 parent tools** that dispatch all operations via an `action` discriminator. The 219 pre-refactor child tools remain available as soft-deprecated wrappers that route to their parent (emit `deprecated_tool_called` analytics).

### New parent tools by Epic batch

- **Epic 20**: `campaign`
- **Epic 64**: `deals`
- **Epic 65**: `audit_skill`, `gam_admin`
- **Epic 68**: `audiences`, `audit`, `billing`, `creative_assets`, `creative_qa`, `creatives`, `gam_features`, `inventory`, `jobs`, `line_items`, `network`, `orders`, `placements`, `pql`, `preview`, `reporting`, `settings`, `targeting`
- **Epic 76**: `creative_wrapper_skill`
- **Epic 78**: `blueprint`, `formats`, `tenant_catalog`

### Largest parent tools (by action count)

| Parent | Actions | Mode |
|---|---|---|
| `gam_admin` | 48 | mixed (read + write) |
| `reporting` | 31 | mixed (read + write) |
| `deals` | 28 | mixed (read + write) |
| `creatives` | 27 | mixed (read + write) |
| `targeting` | 18 | mixed (read + write) |
| `creative_assets` | 15 | mixed (read + write) |
| `line_items` | 15 | mixed (read + write) |
| `blueprint` | 13 | mixed (read + write) |

### Migration guide

- New consumers: call parent tools with `action: <child_name>` (or `(area, action)` for `companies` / `gam_admin`). See [`docs/tool-matrix/README.md`](./docs/tool-matrix/README.md).
- Existing integrations using legacy tool names: no action required — wrappers still work but emit deprecation telemetry. Plan migration per [`_docs/legacy-tool-mapping.md`](./_docs/legacy-tool-mapping.md).
- GAM API target: `v202602` (unchanged). MCP protocol: `2025-03-26` (unchanged).
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
