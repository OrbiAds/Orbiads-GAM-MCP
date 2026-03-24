# Handoff

## The Skill Must Return

- confirmed advertiser ID and name;
- confirmed order ID and name;
- order status (draft, approved, etc.).

## Open Risks to Surface

- advertiser may already exist under a different name;
- order creation consumes credits;
- order may need approval before line items can be activated.

## Next Logical Step

```
<handoff>
advertiserId: ...
advertiserName: ...
orderId: ...
orderName: ...
orderStatus: DRAFT | APPROVED
nextRecommendedSkill: cli-targeting
</handoff>
```
