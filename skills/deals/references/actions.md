---
name: orbiads-deals-actions
description: Full action catalogue for the orbiads-deals skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Programmatic Deals, Products & Companies: Action Catalogue

Full per-tool action reference for the [`orbiads-deals`](../SKILL.md) skill. 75 actions across 6 parent tool(s); CLI coverage 31/75 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:companies`

_Companies dispatcher — single entry point for advertisers, agencies, contacts, and rich media partners._

- **Mode:** mixed · **Actions:** 15 (7 writes, 8 reads)
- **Surfaces:** MCP ✅ · CLI 12/15 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 12 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `advertisers.archive_advertiser` | 0.5 | yes | required | MCP-only |
| `advertisers.create` | 0 | yes | — | `orbiads advertisers create` |
| `advertisers.update` | 0 | yes | — | `orbiads advertisers update` |
| `agencies.create` | 0 | yes | — | `orbiads advertisers agencies create` |
| `agencies.update` | 0 | yes | — | `orbiads advertisers agencies update` |
| `contacts.create` | 0 | yes | — | `orbiads contacts create` |
| `contacts.update` | 0 | yes | — | `orbiads contacts update` |
| `advertisers.find` | 0 | — | — | `orbiads advertisers find` |
| `advertisers.find_or_create` | 0 | — | — | `orbiads advertisers find-or-create` |
| `advertisers.get` | 0 | — | — | `orbiads advertisers get` |
| `advertisers.list` | 0 | — | — | `orbiads advertisers list` |
| `agencies.list` | 0 | — | — | `orbiads advertisers agencies list` |
| `contacts.list` | 0 | — | — | `orbiads contacts list` |
| `rich_media.get` | 0 | — | — | MCP-only |
| `rich_media.list` | 0 | — | — | MCP-only |

### `orbiads:dai_skill` (Epic 98)

_DAI (Dynamic Ad Insertion) and broadcasting operations._

- **Mode:** mixed · **Actions:** 14 (10 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 0/14 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create_cdn_configuration` | 0 | yes | — | MCP-only |
| `create_dai_auth_key` | 0 | yes | — | MCP-only |
| `create_dai_encoding_profile` | 0 | yes | — | MCP-only |
| `delete_cdn_configuration` | 0 | yes | — | MCP-only |
| `delete_dai_encoding_profile` | 0 | yes | — | MCP-only |
| `perform_dai_auth_key_action` | 0 | yes | — | MCP-only |
| `register_sessions` | 0 | yes | — | MCP-only |
| `update_cdn_configuration` | 0 | yes | — | MCP-only |
| `update_dai_auth_key` | 0 | yes | — | MCP-only |
| `update_dai_encoding_profile` | 0 | yes | — | MCP-only |
| `get_stream_activity` | 0 | — | — | MCP-only |
| `list_cdn_configurations` | 0 | — | — | MCP-only |
| `list_dai_auth_keys` | 0 | — | — | MCP-only |
| `list_dai_encoding_profiles` | 0 | — | — | MCP-only |

### `orbiads:deals` (Epic 64)

_Parent MCP tool for PMP, PG/PD proposal authoring, and ADCP deal flows._

- **Mode:** mixed · **Actions:** 28 (15 writes, 13 reads)
- **Surfaces:** MCP ✅ · CLI 10/28 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 29 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `archive_proposal` | 0 | yes | — | MCP-only |
| `archive_proposal_line_items` | 0 | yes | — | MCP-only |
| `create_auction` | 0 | yes | — | `orbiads programmatic auctions create` |
| `create_deal` | 0 | yes | — | `orbiads programmatic deals create` |
| `create_makegoods` | 3 | yes | required | MCP-only |
| `create_proposal` | 5 | yes | required | MCP-only |
| `create_proposal_line_items` | 3 | yes | required | MCP-only |
| `edit_proposal_for_negotiation` | 0 | yes | — | MCP-only |
| `request_buyer_acceptance` | 0 | yes | — | MCP-only |
| `reserve_proposal` | 0 | yes | — | MCP-only |
| `terminate_proposal_negotiations` | 0 | yes | — | MCP-only |
| `update_auction` | 0 | yes | — | `orbiads programmatic auctions update` |
| `update_deal` | 0 | yes | — | `orbiads programmatic deals update` |
| `update_proposal` | 2 | yes | required | MCP-only |
| `update_proposal_line_items` | 1 | yes | required | MCP-only |
| `adcp_create` | 0 | — | — | MCP-only |
| `adcp_preview` | 0 | — | — | MCP-only |
| `adcp_validate` | 0 | — | — | MCP-only |
| `estimate_deal_cost` | 0 | — | — | MCP-only |
| `get_auction` | 0 | — | — | `orbiads programmatic auctions get` |
| `get_buyer` | 0 | — | — | `orbiads programmatic buyers get` |
| `get_deal` | 0 | — | — | `orbiads programmatic deals get` |
| `get_marketplace_comments` | 0 | — | — | MCP-only |
| `get_proposal` | 0 | — | — | MCP-only |
| `list_auctions` | 0 | — | — | `orbiads programmatic auctions list` |
| `list_buyers` | 0 | — | — | `orbiads programmatic buyers list` |
| `list_deals` | 0 | — | — | `orbiads programmatic deals list` |
| `list_proposal_line_items` | 0 | — | — | MCP-only |

### `orbiads:prebid_skill` (Epic 70)

_Dispatch Prebid.js / Header Bidding sub-actions through one MCP tool._

- **Mode:** mixed · **Actions:** 6 (1 writes, 5 reads)
- **Surfaces:** MCP ✅ · CLI 4/6 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `update_line_items` | 0 | yes | — | MCP-only |
| `cleanup` | 0 | — | — | `orbiads prebid cleanup` |
| `generate_line_items` | 0 | — | — | `orbiads prebid generate-line-items` |
| `generate_targeting_keys` | 0 | — | — | `orbiads prebid generate-targeting-keys` |
| `inspect_existing_setup` | 0 | — | — | MCP-only |
| `preview_batch` | 0 | — | — | `orbiads prebid preview` |

### `orbiads:products` (Epic 68.8)

_Parent products tool for the Epic 68.8 catalogue refactor batch._

- **Mode:** mixed · **Actions:** 7 (3 writes, 4 reads)
- **Surfaces:** MCP ✅ · CLI 5/7 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 9 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `archive` | 0 | yes | — | `orbiads products archive` |
| `create` | 0 | yes | — | `orbiads products create` |
| `update` | 0 | yes | — | `orbiads products update` |
| `get` | 0 | — | — | `orbiads products get` |
| `get_adcp` | 0 | — | — | MCP-only |
| `list` | 0 | — | — | `orbiads products list` |
| `pricing_suggestion` | 0 | — | — | MCP-only |

### `orbiads:yield_skill` (Epic 98)

_Yield optimization group management and forecast governance._

- **Mode:** mixed · **Actions:** 5 (2 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 0/5 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create_yield_group` | 0 | yes | — | MCP-only |
| `update_yield_group` | 0 | yes | — | MCP-only |
| `list_forecast_adjustments` | 0 | — | — | MCP-only |
| `list_forecast_segments` | 0 | — | — | MCP-only |
| `list_yield_groups` | 0 | — | — | MCP-only |

