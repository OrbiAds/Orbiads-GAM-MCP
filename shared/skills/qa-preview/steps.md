# Steps

1. [start] Verify that `bootstrap` is complete and confirm the relevant creative, line-item, or order scope.
2. [depends: step 1] Run `scan_creative_compliance` when the source payload or uploaded bundle still needs a compliance scan.
3. [depends: step 1] Run `validate_creative_ssl` or `validate_creative_ssl_batch`; this check is `[parallel-safe]` with step 2 when the scope is stable.
4. [depends: steps 2-3] Generate preview URLs with `get_preview_urls` or `get_campaign_preview_urls`.
5. [depends: steps 3-4] Run `check_creative_coverage` before any activation request.
6. [depends: step 5] Summarize blockers, warnings, and the go / no-go recommendation.
7. [depends: step 6] Hand off the decision packet to `deploy-reporting` only if the QA gate is acceptable.

## Abort Conditions

- stop if creative scope is incomplete or still changing;
- stop if compliance or SSL blockers remain unresolved;
- stop if preview generation does not cover the requested decision scope.