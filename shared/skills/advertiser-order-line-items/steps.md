# Steps

1. [start] Verify that `bootstrap` is complete and reuse any inventory or targeting packet already available.
2. [depends: step 1] Resolve the advertiser with `list_advertisers`, `get_advertiser`, or `find_or_create_advertiser`.
3. [depends: step 2] Read the current order scope with `list_orders` and `get_order`; if an order already exists, `list_line_items_by_order` is `[parallel-safe]` with the order read.
4. [depends: step 3] Create, update, verify, and if needed approve the order.
5. [depends: step 4] Choose the line-item path: standard job-backed batch, targeted single-line-item maintenance, or a deal-based variant.
6. [depends: step 5] Verify line-item setup and targeting before activation.
7. [depends: step 6] Activate, pause, or archive only after explicit human approval.
8. [depends: steps 2-7] Hand off the advertiser, order, line-item IDs, verification state, and open risks to the next workflow.

## Abort Conditions

- stop if advertiser matching remains ambiguous;
- stop before approval, activation, pause, or archive without explicit confirmation;
- stop if preferred-deal or Ad Exchange inputs are incomplete.