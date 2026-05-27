---
name: adops-audit
description: Multi-dimensional GAM audit: delivery health, inventory hygiene, security baseline, creative compliance, billing alignment. Read-only and free.
argument-hint: "[delivery|inventory|security|creative|billing|all] [--framework=iso27001|nist|iab|orbiads_baseline]"
allowed-tools: Task,mcp__orbiads__audit_skill,mcp__orbiads__reporting,mcp__orbiads__inventory,mcp__orbiads__creative_qa,mcp__orbiads__billing,Read,Write
model: sonnet
---

# GAM Account Audit

Always start by confirming the tenant: call `get_my_tenant_id`. All audit operations are read-only and cost 0 credits unless noted.

## Dimensions

Parse `$ARGUMENTS` to decide which dimensions to run.

| Dimension | Condition | Primary tool |
| --- | --- | --- |
| `delivery` | Always | `reporting(action="check_delivery_status")` + `reporting(action="check_underdelivery_alerts")` (0.25 cr) |
| `inventory` | Always | `inventory(action="audit_inventory")` + `audit_skill(action="hygiene_check")` |
| `security` | If `security` or `all` | `audit_skill(action="standards_baseline", params={framework})` |
| `creative` | If `creative` or `all` and line items > 0 | `creative_qa(action="scan_creative_compliance")` + `creative_qa(action="audit_order_tracking")` (0.5 cr) |
| `billing` | If `billing` or `all` | `reporting(action="generate_billing_report")` (0.5 cr) + `reporting(action="check_budget_alerts")` (0.25 cr) |

Default (no argument): run all dimensions.

For `--framework`, pass to `audit_skill(action="standards_baseline", params={framework})`. Supported values: `iso27001`, `nist`, `iab`, `orbiads_baseline` (default).

## Running the audit

Probe line item count first via `reporting(action="check_delivery_status")`. Then spawn each applicable subagent in parallel via the `Task` tool with `context: fork`. Each subagent writes to its own output file — never share a file between subagents.

Output file naming: `audit-<dimension>-<network_code>.md`

**Subagent routing:**

| Dimension | Subagent file |
| --- | --- |
| `delivery` | `agents/audit-delivery.md` |
| `inventory` | `agents/audit-inventory.md` |
| `security` | `agents/audit-security-baseline.md` |
| `creative` | `agents/audit-creative.md` |
| `billing` | `agents/audit-billing.md` |

Wait for all tasks to complete before aggregating.

## Per-dimension tool calls

**Delivery** — `reporting(action="check_delivery_status", params={job_id})` for each active campaign. Then `reporting(action="check_underdelivery_alerts")` (0.25 cr) for network-wide anomalies. `reporting(action="get_prospective_delivery_forecast", params={line_item_id})` for any line item showing < 80% pacing.

**Inventory** — `inventory(action="audit_inventory")` for ad unit health. `inventory(action="find_inactive_ad_units")` (0.25 cr) to surface orphaned units. `audit_skill(action="hygiene_check")` for naming and structural issues. `audit_skill(action="ops_diagnostic")` for operational gaps.

**Security** — `audit_skill(action="standards_baseline", params={framework})` runs the full standards-based audit for the selected framework and returns a markdown report. `audit_skill(action="wrapper_coverage")` checks MCP surface coverage.

**Creative** — `creative_qa(action="scan_creative_compliance", params={creative_id})` per active creative. `creative_qa(action="validate_creative_ssl", params={creative_id})` for SSL hygiene. `creative_qa(action="audit_order_tracking", params={order_id})` (0.5 cr) for tracking coverage across an order.

**Billing** — `reporting(action="generate_billing_report", params={month})` (0.5 cr) for the current or previous month. `reporting(action="check_budget_alerts")` (0.25 cr) for budget overruns.

## Aggregation

After all subagents finish, read their output files and produce three documents:

**`AUDIT-REPORT-<network_code>.md`** — Full findings, one section per dimension. Score each dimension out of 10. Flag findings as 🔴 CRITICAL, 🟡 WARNING, or 🟢 OK.

**`AUDIT-QUICK-WINS-<network_code>.md`** — Top 5 findings by impact-to-effort ratio. One action per finding with the exact MCP call needed to fix it.

**`AUDIT-ACTION-PLAN-<network_code>.md`** — Sequenced remediation: P0 blockers first, then P1, then P2. Include credit cost estimate per step.

Present the Quick Wins inline to the user. Offer to run the highest-priority fix immediately.
