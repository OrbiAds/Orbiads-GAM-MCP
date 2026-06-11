# Steps

1. Use the `orbiads` skill to confirm the active tenant and network.
2. Confirm the target sizes and delivery scope with the `inventory` skill (`targeting(action="list_ad_units")`, `inventory(action="list_ad_unit_sizes")`); run the `reporting` skill (`reporting(action="get_standalone_forecast")`) for supply validation when needed.
3. Resolve advertiser, order, and line-item context through the `campaigns` skill: `companies(action="advertisers.find_or_create")`, `orders(action="find_or_create")`, `line_items(action="create_batch")`.
4. Build the approved bundle and upload it with `creative_assets(action="create_html5_from_files")` or `creative_assets(action="upload_html5_zip")`.
5. Associate the creative to the correct line items via `creatives(action="associate_creative")`.
6. Run `creative_qa(action="scan_creative_compliance")` and `creative_qa(action="validate_creative_ssl")` for compliance, SSL, preview URLs, and creative coverage.
7. Stop before activation if the uploaded bundle, preview, or coverage is not acceptable.
8. Use the `campaigns` skill for the deploy gate: `campaign(action="dry_run")` → confirm → `campaign(action="deploy")`; then verify with `reporting(action="check_delivery_status")`.