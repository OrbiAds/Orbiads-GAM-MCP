# Image to HTML5

## Goal

- Turn approved image assets into a packaged HTML5 creative flow that remains reviewable and safe.
- Keep the creative build step explicit until a dedicated shared HTML5 skill is added.
- End with an HTML5 creative uploaded, associated, and validated through the same QA and preview gate as other creative flows.

## Skill Composition

- `orbiads` (orchestrator — auth context and tenant confirmation)
- `inventory` (delivery scope confirmation and size validation)
- `reporting` (availability forecast when needed)
- `campaigns` (advertiser/order/line-item resolution, HTML5 creative upload, association, QA, and deploy gate)

## Entry Conditions

- the destination advertiser, order, and line items are known or can be created;
- the HTML, CSS, JS, and asset bundle is approved;
- the inventory scope and target sizes are already known.

## Exit States

- HTML5 creative uploaded and associated to line items;
- compliance, preview, and coverage packet accepted;
- deployment packet ready for the push phase.