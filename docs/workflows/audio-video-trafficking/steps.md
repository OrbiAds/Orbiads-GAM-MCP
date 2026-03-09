# Steps

1. Reuse `bootstrap` and confirm the active network.
2. Validate the inventory, placement, and targeting scope before rich media creation.
3. Run `availability-forecast` when the audio or video scope is highly constrained.
4. Resolve advertiser, order, and line-item context through `advertiser-order-line-items`.
5. Create the approved creative with `create_audio_creative` or `create_video_creative` and associate it to the correct line items.
6. Run `qa-preview` for preview URLs, coverage, and the checks that remain relevant to the rich media format.
7. Stop before activation if preview, coverage, or manual companion handling is still unresolved.
8. Hand off the trafficking packet to `deploy-reporting` for activation and monitoring.