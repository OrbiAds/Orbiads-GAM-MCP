---
name: adops-deal
description: Manage programmatic deal lifecycle — PMP, private auctions, Marketplace proposals. Guards writes with preview→confirm→execute.
argument-hint: "<list|get|create|update|reserve|validate> [deal-id]"
allowed-tools: mcp__orbiads__deals,mcp__orbiads__companies,mcp__orbiads__billing,mcp__orbiads__settings
model: sonnet
---

# GAM Programmatic Deals

Always confirm the tenant first: `get_my_tenant_id`. Write operations require a `confirmation_token` from a prior preview call.

## Naming conventions (always fetch before creating)

Before naming any proposal or deal, call `settings(action="get_naming_conventions")` and apply the returned pattern. Convention violations cause ambiguity in billing reports. If no pattern is configured, ask the user to confirm the name explicitly.

## Estimating cost before writes

For any proposal, run `deals(action="estimate_deal_cost", params={deal_type, targeting, impressions_goal, cpm_floor})` first — it returns a credit breakdown at zero cost. Surface the estimate to the user before proceeding.

## list

Calls `deals(action="list_deals")` and `deals(action="list_auctions")` in parallel. Render a table: type | name | buyer | status | CPM floor.

## get `<deal-id>`

Call `deals(action="get_deal", params={deal_id})` for PMP deals or `deals(action="get_proposal", params={proposal_id})` for Marketplace proposals. Show full targeting, floor price, buyers, and associated line items.

For auction details: `deals(action="get_auction", params={auction_id})`.

## create

Ask the user for deal type, then follow the corresponding path:

**PMP deal or private auction:**

1. Fetch available buyers: `deals(action="list_buyers")`.
2. Fetch naming conventions: `settings(action="get_naming_conventions")`.
3. Estimate cost: `deals(action="estimate_deal_cost", params={...})`.
4. Call `deals(action="create_deal", params={name, buyer_id, cpm_floor, targeting, ...})` — preview step (0 cr, no token required).
5. For private auctions: `deals(action="create_auction", params={name, floor_price, targeting, ...})`.

**Marketplace PG/PD proposal (costs 5 cr, token required):**

1. Validate feasibility first: `deals(action="adcp_validate", params={targeting, goal, cpm})` — free.
2. Preview the proposal: `deals(action="adcp_preview", params={...})` — returns estimated delivery. Free.
3. Fetch buyers: `deals(action="list_buyers")`.
4. Fetch naming conventions: `settings(action="get_naming_conventions")`.
5. Estimate credit cost: `deals(action="estimate_deal_cost", params={...})`.
6. Preview ADCP: `deals(action="adcp_create", params={..., dry_run: true})` — returns a signed `ExecutionPlan` with `dealSpecs[]`, `packageCount`, `partialFailureRisk`, `estimatedCost`, and `confirmationToken`. Show the full plan to the user. If `partialFailureRisk` is present or high, call out that package 0..N-1 may remain in GAM if package N fails.
7. Execute ADCP: `deals(action="adcp_create", params={..., confirmation_token: "<token>"})` — creates through `DealPipeline` (PMP REST / PG SOAP / PD SOAP).
8. Add line items when needed: `deals(action="create_proposal_line_items", params={proposal_id, ...})`. Costs 3 cr, requires a fresh `confirmation_token`.

### ADCP token contract

- `CONFIRMATION_REQUIRED`: token absent; re-run `deals(action="adcp_create", params={..., dry_run: true})`.
- `PAYLOAD_MISMATCH`: payload changed between preview and execute; re-run the dry-run.
- High `partialFailureRisk`: warn the user explicitly that if package N fails after packages 0..N-1, earlier deals remain in GAM because there is no global rollback. Require explicit confirmation before execute.

## update `<deal-id>`

Fetch current state with `deals(action="get_deal")` or `deals(action="get_proposal")`, ask what to change, then:

- PMP deal: `deals(action="update_deal", params={deal_id, ...})`.
- Auction: `deals(action="update_auction", params={auction_id, ...})`.
- Marketplace proposal in negotiation: `deals(action="edit_proposal_for_negotiation", params={proposal_id, ...})`.
- Proposal (general update, 2 cr, token required): `deals(action="update_proposal", params={proposal_id, ...})` — preview first.
- Proposal line items (1 cr, token required): `deals(action="update_proposal_line_items", params={proposal_id, ...})` — preview first.

For Marketplace proposals requiring buyer sign-off: `deals(action="request_buyer_acceptance", params={proposal_id})` after update.

## reserve `<proposal-id>`

Locks inventory and commits budget. Call `deals(action="reserve_proposal", params={proposal_id})`. This is irreversible — confirm with the user before executing.

To end an ongoing negotiation: `deals(action="terminate_proposal_negotiations", params={proposal_id})`.

## validate `<deal-id>`

`deals(action="adcp_validate", params={deal_id})` — free, no confirmation needed. Shows feasibility score and blocking issues. Always run this before creating a Marketplace proposal.

For Marketplace commentary: `deals(action="get_marketplace_comments", params={proposal_id})`.

## Hard rules

- Never call `deals(action="adcp_create")` without a dry-run preview first.
- Never bypass the `confirmation_token` — `inspect.unwrap` of legacy wrappers is forbidden.
- Always run `adcp_validate` before any Marketplace proposal creation.
- Always estimate cost with `estimate_deal_cost` before proposing a write to the user.
- Never surface raw buyer IDs in public-facing output.
