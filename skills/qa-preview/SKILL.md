---
description: Last quality gate before activation — compliance scan, SSL validation, previews, coverage check, and explicit go/no-go verdict.
---

# OrbiAds — qa-preview

Centralize the last quality gate before any real campaign action. Validate compliance, SSL, previews, and creative coverage. Return an explicit go/no-go decision packet.

## When to Use

- Activation or deployment is about to happen — this gate is mandatory.
- A creative bundle, Native creative, or order needs compliance proof and preview links.

**Do not use** if creatives are not yet associated to line items — associate first, then run QA.
**Do not use** for post-launch monitoring — that belongs in `deploy-reporting`.

## Steps

1. Verify bootstrap complete and confirm creative / line-item / order scope.
2. `scan_creative_compliance` if source payload or uploaded bundle needs a compliance scan.
3. `validate_creative_ssl` (single) or `validate_creative_ssl_batch` (multiple).
4. `get_preview_urls` (line-item scope) or `get_campaign_preview_urls` (order scope).
5. `check_creative_coverage` before any activation request.
6. Summarize blockers, warnings, and the go/no-go recommendation.
7. Hand off to `deploy-reporting` only if QA gate is acceptable.

## Key Tools

- `scan_creative_compliance` — compliance scan
- `validate_creative_ssl` / `validate_creative_ssl_batch` — SSL check
- `get_preview_urls` / `get_campaign_preview_urls` — preview generation
- `check_creative_coverage` — coverage gap detection

## Abort Conditions

- Stop on any blocking compliance finding — do not suggest deployment in the same turn.
- Stop if creative coverage is incomplete — list missing associations before continuing.
- Never hide unresolved QA issues behind a deployment request.

## Output

Render go/no-go verdict as a prominent artifact:

```
✅ GO — all checks passed
  or
❌ BLOCKED — [list numbered blockers]
```

```
<handoff>
complianceFindings: [...]
sslStatus: passed | failed | partial
previewUrls: [...]
coverageStatus: complete | incomplete
goNoGo: go | blocked
nextRecommendedSkill: deploy-reporting
</handoff>
```

Never suggest deployment in the same turn as a blocking finding — force a separate user confirmation.
