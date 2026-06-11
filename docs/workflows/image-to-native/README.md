# Image to Native

## Goal

- Turn approved image assets and copy into a Native delivery package.
- Validate that the target inventory supports Native or Fluid constraints.
- End with a reviewed Native creative associated to the correct line items and ready for QA and preview.

## Skill Composition

- `orbiads` (orchestrator — auth context and tenant confirmation)
- `inventory` (ad unit validation, fluid compatibility check)
- `reporting` (availability forecast when supply risk is unknown)
- `campaigns` (advertiser/order/line-item resolution, Native creative creation, creative association, QA)
- `campaigns` → reporting steps (deploy gate and post-deploy delivery check)

## Entry Conditions

- the target advertiser, order, and line items are known or can be created;
- image assets, destination URLs, and business copy are approved;
- the intended ad units are known and can be checked for Native or Fluid compatibility.

## Exit States

- Native template and creative created;
- creative associated to the intended line items;
- QA and preview packet ready for the deploy gate (`campaign` deploy via the `campaigns` skill) and post-deploy delivery monitoring via `reporting`.