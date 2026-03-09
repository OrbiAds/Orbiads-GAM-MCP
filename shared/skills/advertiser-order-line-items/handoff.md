# Handoff

## The Skill Must Return

- the resolved `advertiserId` and `orderId`;
- the created or selected `lineItemIds`;
- the verification summary for the order and line items;
- any job-backed lifecycle status that still matters downstream.

## Open Risks to Surface

- advertiser duplication risk or wrong advertiser mapping;
- order not yet approved;
- targeting or pacing mismatch on line items;
- preferred-deal inputs missing or invalid;
- open bidding still outside the supported path.

## Next Logical Step

- continue to `native-image` when the delivery context is ready for creative production;
- or move to `qa-preview` / `deploy-reporting` when creatives already exist.