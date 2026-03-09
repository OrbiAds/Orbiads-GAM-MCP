# Image to HTML5

## Goal

- Turn approved image assets into a packaged HTML5 creative flow that remains reviewable and safe.
- Keep the creative build step explicit until a dedicated shared HTML5 skill is added.
- End with an HTML5 creative uploaded, associated, and validated through the same QA and preview gate as other creative flows.

## Skill Composition

- `bootstrap`
- `inventory-ad-units`
- `availability-forecast`
- `advertiser-order-line-items`
- low-level creative packaging via `create_html5_creative_from_files`
- `qa-preview`
- `deploy-reporting`

## Entry Conditions

- the destination advertiser, order, and line items are known or can be created;
- the HTML, CSS, JS, and asset bundle is approved;
- the inventory scope and target sizes are already known.

## Exit States

- HTML5 creative uploaded and associated to line items;
- compliance, preview, and coverage packet accepted;
- deployment packet ready for the push phase.