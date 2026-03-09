# Agent Trigger — qa-preview

## Enter when

- activation or deployment is about to happen — QA gate is mandatory;
- a creative bundle, Native creative, or order needs compliance proof and preview links.

## Do not enter when

- creatives are not yet associated to line items — associate first, then run QA;
- the user only wants to list preview URLs without a go/no-go decision — use `get_preview_urls` directly;
- the request is post-launch monitoring — route to `deploy-reporting` instead.

## Disambiguation

- "scan this HTML5 bundle for compliance" → `scan_creative_compliance` only, not a full QA run;
- "validate SSL for these creatives" → `validate_creative_ssl_batch` only if IDs are known;
- "show me preview URLs" → `get_preview_urls` or `get_campaign_preview_urls`, full QA still recommended before activation;
- "is coverage complete?" → `check_creative_coverage` only, fast check before a broader QA pass.
