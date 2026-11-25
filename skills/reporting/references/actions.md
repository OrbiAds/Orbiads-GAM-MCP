---
name: orbiads-reporting-actions
description: Full action catalogue for the orbiads-reporting skill — per-action cost, write flags, confirmation tokens, and CLI equivalents.
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Reporting, Forecasting & Delivery Analytics: Action Catalogue

Full per-tool action reference for the [`orbiads-reporting`](../SKILL.md) skill. 47 actions across 4 parent tool(s); CLI coverage 44/47 actions.

**CLI column:** `orbiads <command>` = available on the CLI surface (joined from `cli/parity-matrix.json`); `MCP-only` = no CLI command — call the MCP action (or web app) instead. The two surfaces share the same billing guard and preview → confirm → execute contract.

### `orbiads:mcm` (Epic 88.1)

_Multi-Customer Management: earnings, child publishers and their agreements._

- **Mode:** mixed · **Actions:** 8 (5 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 8/8 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `invite_child_publisher` | 0.5 | yes | required | `orbiads mcm child-publishers invite` |
| `renegotiate_child_publisher` | 0 | yes | required | `orbiads mcm child-publishers renegotiate` |
| `resend_child_publisher_invitation` | 0 | yes | required | `orbiads mcm child-publishers resend-invitation` |
| `update_child_publisher` | 0 | yes | required | `orbiads mcm child-publishers update` |
| `withdraw_child_publisher` | 0 | yes | required | `orbiads mcm child-publishers withdraw` |
| `earnings_fetch` | 0 | — | — | `orbiads mcm earnings` |
| `get_child_publisher` | 0 | — | — | `orbiads mcm child-publishers get` |
| `list_child_publishers` | 0 | — | — | `orbiads mcm child-publishers list` |

### `orbiads:pql` (Epic 68.2)

_Parent pql tool for the Epic 68.2 catalogue refactor batch._

- **Mode:** read-only · **Actions:** 3 (0 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 1/3 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 1 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `list_tables` | 0 | — | — | MCP-only |
| `run_query` | 0 | — | — | `orbiads pql query` |
| `validate_query` | 0 | — | — | MCP-only |

### `orbiads:preview` (Epic 68.2)

_Parent preview tool for the Epic 68.2 catalogue refactor batch._

- **Mode:** read-only · **Actions:** 3 (0 writes, 3 reads)
- **Surfaces:** MCP ✅ · CLI 3/3 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 3 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `check_creative_coverage` | 0 | — | — | `orbiads preview coverage` |
| `get_campaign_preview_urls` | 0.25 per preview (manual free; +1 Google blank in soap) | — | — | `orbiads preview campaign` |
| `get_preview_urls` | 0.25 per preview (manual free; +1 Google blank in soap) | — | — | `orbiads preview share` |

### `orbiads:reporting` (Epic 68.7b)

_Parent reporting tool for the Epic 68.7b catalogue refactor batch._

- **Mode:** mixed · **Actions:** 33 (7 writes, 26 reads)
- **Surfaces:** MCP ✅ · CLI 32/33 actions
- **Reference:** see the public [tool matrix](../../../docs/tool-matrix/README.md) for parameter schemas.

> **Legacy wrappers:** 31 pre-refactor child tool(s) still route to this parent. See [`legacy-tool-mapping.md`](../../../_docs/legacy-tool-mapping.md).

| Action | Cost | Write? | Confirmation token | CLI |
|---|---|---|---|---|
| `create_gam_report` | 0 | yes | required | `orbiads reporting gam-reports create-from-template` |
| `delete_gam_report` | 0 | yes | required | `orbiads reporting gam-reports delete` |
| `delete_report_template` | 0 | yes | — | `orbiads reporting templates delete` |
| `duplicate_report_template` | 0 | yes | — | `orbiads reporting templates duplicate` |
| `save_report_template` | 0 | yes | — | `orbiads reporting templates save` |
| `update_gam_report` | 0 | yes | required | `orbiads reporting gam-reports update-from-template` |
| `update_report_template` | 0 | yes | — | `orbiads reporting templates update` |
| `check_budget_alerts` | 0.25 | — | — | `orbiads reporting alerts-budget` |
| `check_delivery_status` | 0 | — | — | `orbiads reporting delivery-status` |
| `check_underdelivery_alerts` | 0.25 | — | — | `orbiads reporting alerts-underdelivery` |
| `export_report_csv` | 0.5 | — | — | `orbiads reporting export-csv` |
| `fetch_delivery_report` | 0 | — | — | `orbiads reporting delivery-report` |
| `fetch_inventory_report` | 0.5 | — | — | `orbiads reporting inventory` |
| `generate_billing_report` | 0.5 | — | — | `orbiads reporting billing-report` |
| `get_availability_forecast_by_line_item` | 0 | — | — | `orbiads reporting forecast-availability` |
| `get_delivery_forecast_by_line_item` | 0 | — | — | `orbiads reporting forecast-line-item` |
| `get_ga_dimensions` | 0 | — | — | `orbiads reporting ga4 dimensions` |
| `get_ga_metrics` | 0 | — | — | `orbiads reporting ga4 metrics` |
| `get_gam_report` | 0 | — | — | `orbiads reporting gam-reports get` |
| `get_prospective_delivery_forecast` | 0 | — | — | `orbiads reporting forecast prospective` |
| `get_report_date_ranges` | 0 | — | — | `orbiads reporting date-ranges` |
| `get_report_dimensions` | 0 | — | — | `orbiads reporting dimensions` |
| `get_report_download_link` | 0.5 (free with resultId) | — | — | MCP-only |
| `get_report_metrics` | 0 | — | — | `orbiads reporting metrics` |
| `get_report_result` | 0 | — | — | `orbiads reporting executions` |
| `get_standalone_forecast` | 0 | — | — | `orbiads reporting forecast standalone` |
| `get_traffic_data` | 0 | — | — | `orbiads reporting forecast traffic` |
| `list_gam_reports` | 0 | — | — | `orbiads reporting gam-reports list` |
| `list_report_templates` | 0 | — | — | `orbiads reporting templates list` |
| `run_custom_report` | 0.5 | — | — | `orbiads reporting run` |
| `run_ga_report` | 0.5 | — | — | `orbiads reporting ga4 run` |
| `run_gam_report` | 0.5 | — | — | `orbiads reporting export` |
| `run_report_from_template` | 0.5 | — | — | `orbiads reporting templates run` |
