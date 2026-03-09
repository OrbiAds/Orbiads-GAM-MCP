# Steps

1. [start] Verify that the required campaign resources (`jobId`, `orderId`, line items, creatives) are known.
2. [depends: step 1] Check coverage and generate the useful previews before any real push; these checks are `[parallel-safe]` when the scope is stable.
3. [depends: step 2] Produce an action preview with `dry_run=True` for every campaign operation.
4. [depends: step 3] Ask for explicit human validation before any real `deploy`, `update`, `pause`, `archive`, or `rollback`.
5. [depends: step 3 or 4] After execution or simulation, read `check_delivery_status` and `fetch_delivery_report` in parallel to qualify delivery state.
6. [depends: step 5] Run the appropriate reporting path: template, custom report, inventory report, GAM report, or GA report.
7. [depends: steps 5-6] Review `query_audit_log`, alerts, and summarize the recommended next actions.

## Abort Conditions

- stop if coverage or preview evidence is incomplete;
- stop before any real campaign action without explicit confirmation;
- stop if rollback is requested before the impacted resources are clearly identified.