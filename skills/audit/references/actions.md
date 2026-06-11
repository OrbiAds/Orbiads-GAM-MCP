---
name: orbiads-audit-actions
description: Full action catalogue for the orbiads-audit skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Account Audits & Billing: Action Catalogue

Full per-tool action reference for the [`orbiads-audit`](../SKILL.md) skill. 11 actions across 3 parent tool(s); CLI coverage 3/11 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:audit` (Epic 68.5)

_Parent audit tool for the Epic 68.5 catalogue refactor batch._

- **Mode:** read-only · **Actions:** 1 (0 writes, 1 reads)
- **Surfaces:** MCP ✅ · CLI 1/1 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 1 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `query_audit_log` | 0 | — | — | `orbiads audit log` |

### `orbiads:audit_skill` (Epic 65.0a)

_OrbiAds audit suite — single entry point for audit sub-actions._

- **Mode:** read-only · **Actions:** 8 (0 writes, 8 reads)
- **Surfaces:** MCP ✅ · CLI 0/8 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 2 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `estimate_cost` | 0 | — | — | MCP-only |
| `export_authoring` | 0 | — | — | MCP-only |
| `export_xlsx` | 0 | — | — | MCP-only |
| `hygiene_check` | 0 | — | — | MCP-only |
| `inventory_extended` | 0 | — | — | MCP-only |
| `ops_diagnostic` | 0 | — | — | MCP-only |
| `standards_baseline` | 0 | — | — | MCP-only |
| `wrapper_coverage` | 0 | — | — | MCP-only |

### `orbiads:billing` (Epic 68.5)

_Parent billing tool for the Epic 68.5 catalogue refactor batch._

- **Mode:** read-only · **Actions:** 2 (0 writes, 2 reads)
- **Surfaces:** MCP ✅ · CLI 2/2 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 2 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `get_credit_balance` | 0 | — | — | `orbiads billing balance` |
| `list_transactions` | 0 | — | — | `orbiads billing transactions` |

