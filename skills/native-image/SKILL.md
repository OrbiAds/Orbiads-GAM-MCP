---
description: Turn approved image assets and copy into a Classic Native creative, associated to line items and ready for QA.
---

# OrbiAds — native-image

Turn approved copy and image assets into a controlled Native creative flow. Ensure the Classic Native template exists before creative creation.

## When to Use

- An approved image, copy set, and destination URL must become a Classic Native creative.
- Line items are ready and the next step is creative production before QA.

**Do not use** if assets or copy have not been approved by a human — block and request approval first.
**Do not use** for HTML5, audio, or video creatives — those use different tools outside this skill.

## Steps

1. Verify bootstrap complete and advertiser + line-item context stable.
2. Reconfirm approved copy (headline, body, CTA), image asset, and destination URL with user.
3. `create_image_creative` if asset is not already in GAM.
4. `ensure_classic_native_template` — required before creative creation.
5. `create_classic_native_creative` from approved payload.
6. `associate_creative` to the approved line items.
7. Hand off creative IDs and template details to `qa-preview`.

## Key Tools

- `ensure_classic_native_template` — idempotent, always run first
- `create_image_creative` — write, requires approved asset
- `create_classic_native_creative` — write, requires approved payload + template
- `associate_creative` — write, run after creative ID confirmed

## Abort Conditions

- Stop if image, copy, or destination URL is not explicitly confirmed in the conversation.
- Flag template recreation risk inline if `ensure_classic_native_template` returns a mismatch.
- Never create the creative and skip straight to association in the same step.

## Output

Show the creative payload as an artifact before creation — one human approval required.

```
<handoff>
creativeIds: [...]
templateStatus: ensured | recreated | mismatch
lineItemIds: [...]
nextRecommendedSkill: qa-preview
</handoff>
```
