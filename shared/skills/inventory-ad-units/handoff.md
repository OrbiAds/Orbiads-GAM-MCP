# Handoff

## The Skill Must Return

- the `selectedAdUnitIds` or `createdAdUnitIds` list;
- the chosen parent/child structure;
- the inventory audit summary;
- optionally a pending `confirmationToken` if the write has not been confirmed yet.

## Open Risks to Surface

- naming conflicts or missing parent;
- sizes inconsistent with the target formats;
- inactive ad units not cleaned up;
- Native/Fluid compatibility not yet verified.

## Next Logical Step

- continue to `availability-forecast` to validate supply;
- or move to placement/targeting skills if the inventory is already stable.