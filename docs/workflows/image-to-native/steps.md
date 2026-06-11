# Steps

1. Use the `orbiads` skill to confirm the active tenant and network.
2. Use the `inventory` skill to freeze the target inventory scope via `targeting(action="list_ad_units")` and `placements(action="list_placements")`; validate fluid compatibility with `targeting(action="validate_fluid")` when required.
3. Run the `reporting` skill (`reporting(action="get_standalone_forecast")`) if the supply risk is not already known.
4. Use the `campaigns` skill to resolve or create the advertiser via `companies(action="advertisers.find_or_create")`, the order via `orders(action="find_or_create")`, and target line items via `line_items(action="create_batch")`.
5. Use the `campaigns` skill to ensure the Classic Native template exists, create the Native creative via `creative_assets(action="create_classic_native")`, and associate it to the approved line items via `creatives(action="associate_creative")`.
6. Run `creative_qa(action="scan_creative_compliance")` and `creative_qa(action="validate_creative_ssl")` for compliance, SSL, preview URLs, and creative coverage.
7. Stop before activation if QA or previews fail.
8. Use the `reporting` skill for the deploy gate: `campaign(action="dry_run")` → confirm → `campaign(action="deploy")`; then verify with `reporting(action="check_delivery_status")`.