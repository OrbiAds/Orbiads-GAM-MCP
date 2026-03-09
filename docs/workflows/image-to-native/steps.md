# Steps

1. Reuse `bootstrap` and confirm the active network.
2. Use `inventory-ad-units` and `placements-targeting` to freeze the target inventory scope and validate `validate_fluid` when required.
3. Run `availability-forecast` if the supply risk is not already known.
4. Use `advertiser-order-line-items` to resolve or create the advertiser, order, and target line items.
5. Use `native-image` to ensure the Classic Native template, create the Native creative, and associate it to the approved line items.
6. Run `qa-preview` for compliance, SSL, preview URLs, and creative coverage.
7. Stop before activation if QA or previews fail.
8. Hand off the approved creative IDs, preview packet, and residual risks to `deploy-reporting`.