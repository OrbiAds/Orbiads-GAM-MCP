# Native image

## Purpose

- Turn approved copy and image assets into a controlled Native creative flow.
- Ensure the Classic Native template exists before creative creation.
- Return associated creative IDs ready for QA, preview, and deployment.

## Prerequisites

- `bootstrap` has been completed;
- advertiser, order, and line-item context is already known or reusable;
- image assets, copy, and destination URLs were approved by humans;
- Native / Fluid compatibility was checked upstream when required.

## Inputs

- `tenantId`;
- `advertiserId` and target `lineItemIds`;
- approved image asset or image upload intent;
- Native copy fields such as headline, body, CTA, and landing URL;
- optional naming and labeling rules for the created creative.

## Expected Output

- uploaded image asset summary when applicable;
- ensured Native template status;
- created Native creative IDs;
- association packet ready for QA and preview.

## Guardrails

- resolve the delivery context before creative creation;
- ensure the Classic Native template before creating the Native creative;
- validate image selection, copy, and destination URL with humans;
- associate creatives only after the creative payload is approved;
- route immediately to `qa-preview` before any deployment action.

## Handoff

- pass `creativeIds`, `lineItemIds`, template status, and association summary;
- pass any unresolved compliance or preview concerns;
- route next to `qa-preview`.