# Examples

## Example User Inputs

- “Resolve or create the advertiser for this brand, then create the order for April.”
- “Review this order, update the pacing notes, and verify the existing line items before activation.”
- “List the private deals available for this tenant and tell me whether a preferred deal line item is the right path.”

## Example Response Plan

- resolve the advertiser and current order state;
- create or update the order if required;
- inspect or create the relevant line items;
- verify readiness and summarize which approvals are still needed.

## Example Structured Output

- `advertiserId`;
- `orderId`;
- `lineItemIds`;
- `orderVerification` and `lineItemVerification`;
- `requiredApprovals`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not document `find_or_create_order`; it is not an exposed tool;
- do not present open bidding as a supported default creation path while `create_open_bidding_line_item` returns `NOT_IMPLEMENTED`.