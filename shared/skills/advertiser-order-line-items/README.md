# Advertiser, orders & line items

## Purpose

- Resolve the advertiser and order scope before trafficking.
- Create, update, verify, and control line items with explicit guardrails.
- Return a delivery-ready packet for creative work, QA, preview, or deployment.

## Prerequisites

- `bootstrap` has been completed;
- the business brief is known: advertiser, dates, budget, pricing, and sales context;
- the inventory and targeting scope is known or can be reused from upstream skills.

## Inputs

- `tenantId`;
- advertiser identifiers or advertiser creation intent;
- order identifiers or order creation / update payload;
- `jobId`, `orderId`, `lineItemIds`, or direct line-item specifications depending on the path;
- optionally a private deal context for deal-based line items.

## Expected Output

- resolved `advertiserId` and `orderId`;
- created, updated, or qualified `lineItemIds`;
- verification summary for orders and line items;
- lifecycle status or pending approval packet for the next workflow.

## Guardrails

- read the existing advertiser, order, and line-item state before creating new resources;
- use `find_or_create_advertiser` when advertiser resolution is uncertain;
- remember that `create_line_items`, `activate_line_items`, and `pause_line_items` are job-backed paths;
- verify order and line-item setup before activation;
- keep archive operations and deal-specific variants behind explicit human approval.

## Handoff

- pass `advertiserId`, `orderId`, `lineItemIds`, and any `jobId` still in use;
- pass unresolved targeting, QA, preview, or approval requirements;
- route next to `native-image`, `qa-preview`, or `deploy-reporting`.