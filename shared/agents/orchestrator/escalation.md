# Escalation

## Require Human Confirmation

- selecting a network when multiple choices exist;
- any real write after a `dry_run` or preview;
- activation, pause, archive, rollback, disconnect, or destructive cleanup;
- actions that may spend credits without a clear business goal.

## Hand Off to a Specialist

- send budget-sensitive operations through `../credit-guard/` policy;
- send stale or oversized context through `../context-manager/` policy;
- send failures, retries, or degraded paths through `../error-recovery/` policy.