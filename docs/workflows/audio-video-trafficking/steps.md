# Steps

1. Use the `orbiads` skill to confirm the active tenant and network.
2. Validate the inventory, placement, and targeting scope with the `inventory` skill: `targeting(action="list_ad_units")`, `placements(action="list_placements")`, `targeting(action="list_custom_targeting_keys")`.
3. Use the `reporting` skill (`reporting(action="get_standalone_forecast")`) when the audio or video scope is highly constrained.
4. Resolve advertiser, order, and line-item context through the `campaigns` skill: `companies(action="advertisers.find_or_create")`, `orders(action="find_or_create")`, `line_items(action="create_batch")`.
5. Create the approved creative with `creative_assets(action="create_audio")` or `creative_assets(action="create_video")` (poll `creatives(action="get_video_transcode_status")` until `COMPLETE` for video), then associate to the correct line items via `creatives(action="associate_creative")`.
6. Use the `campaigns` skill to run `creative_qa(action="scan_creative_compliance")` and check preview URLs; surface any manual companion or packaging dependency instead of hiding it.
7. Stop before activation if preview, coverage, or manual companion handling is still unresolved.
8. Use the `campaigns` skill for the deploy gate: `campaign(action="dry_run")` → confirm → `campaign(action="deploy")`; then monitor with `reporting(action="check_delivery_status")`.