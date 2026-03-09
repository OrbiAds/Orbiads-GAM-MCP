---
description: Resolve advertiser, create or update orders, and manage line-item lifecycle with explicit confirmation gates.
---

# OrbiAds — advertiser-order-line-items

Resolve the advertiser and order scope before trafficking. Create, update, verify, and control line items with explicit guardrails.

## When to Use

- Advertiser resolution, order setup, line-item creation, or lifecycle review.
- A workflow is ready to move from inventory/targeting into trafficking.

**Do not use** if advertiser, order, and line-item IDs are already confirmed — pass them to `native-image` or `qa-preview` directly.

## Steps

1. Verify bootstrap complete, reuse inventory/targeting packet if available.
2. Resolve advertiser: `list_advertisers` → `get_advertiser` → `find_or_create_advertiser`. `[free]`
3. Read current order: `list_orders` + `get_order`. `[free]`
4. Create / update / verify / approve order as needed.
5. Choose line-item path: job-backed batch / single-item maintenance / deal-based variant.
6. `verify_order_setup` + `verify_line_item_setup` before activation. `[free]`
7. Activate / pause / archive only after explicit human approval.
8. Hand off advertiser, order, line-item IDs and open risks.

## Key Tools

- `list_advertisers`, `get_advertiser`, `list_orders`, `get_order`, `list_line_items_by_order`, `verify_order_setup`, `verify_line_item_setup` — `[free]`
- `find_or_create_advertiser`, `create_order`, `update_order`, `approve_order` — writes, recap before execution
- `create_line_items`, `activate_line_items`, `pause_line_items` — job-backed, require confirmation
- `create_open_bidding_line_item` — returns `NOT_IMPLEMENTED`, capability boundary only

## Abort Conditions

- Stop before any activation if `verify_line_item_setup` has not run.
- Stop if advertiser duplication risk is unresolved.
- Never document `find_or_create_order` — not a supported path.

## Output

Render order + line-item verification as an artifact table before any activation request.

```
<handoff>
advertiserId: ...
orderId: ...
lineItemIds: [...]
requiredApprovals: [...]
nextRecommendedSkill: native-image | qa-preview
</handoff>
```

Apply extended thinking before choosing between job-backed batch and single line-item maintenance.
