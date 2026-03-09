# Steps

1. Reuse `bootstrap` and confirm the active network.
2. Confirm the target sizes and delivery scope with `inventory-ad-units` and `availability-forecast` when needed.
3. Resolve advertiser, order, and line-item context through `advertiser-order-line-items`.
4. Build the approved bundle and upload it with `create_html5_creative_from_files`.
5. Associate the creative to the correct line items.
6. Run `qa-preview` for compliance, SSL, preview URLs, and creative coverage.
7. Stop before activation if the uploaded bundle, preview, or coverage is not acceptable.
8. Hand off the creative packet to `deploy-reporting` for the final push gate.