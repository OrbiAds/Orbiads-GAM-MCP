# Claude Skill Wrapper — advertiser-order-line-items

- load `../../shared/agents/advertiser-order-line-items/`;
- execute `../../shared/skills/advertiser-order-line-items/`;
- use this skill for advertiser lookup, order setup, and line-item trafficking.

## Claude-Specific Hints

- render the order and line-item verification summary as an artifact table before any activation request;
- use `<handoff>` tags to pass `advertiserId`, `orderId`, and `lineItemIds` to `native-image` or `qa-preview`;
- apply extended thinking before choosing between job-backed batch creation and single line-item maintenance;
- format the confirmation gate as a clear question with the exact IDs and action listed — one approval per write.
