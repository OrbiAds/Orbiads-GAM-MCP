# Steps

1. [start] Verify that `bootstrap` is complete and that the active network is initialized.
2. [depends: step 1] Explore the current state with `list_ad_units`, `search_ad_units`, `get_ad_unit_tree`, and `audit_inventory`; run the read tools in parallel when the scope is already clear.
3. [depends: step 2] If cleanup is in scope, call `find_inactive_ad_units` and summarize the candidates without taking destructive action.
4. [depends: step 2] Choose the path: read-only review, direct creation through `create_ad_units_batch`, or blueprint generation through `generate_inventory_blueprint`.
5. [depends: step 4] Always produce a preview with `dry_run=True` for any write batch or with a generated blueprint before a push.
6. [depends: step 5] Ask for human validation of names, parents, sizes, and expected volume.
7. [depends: step 6] Execute `create_ad_units_batch` or `push_inventory_blueprint` only after explicit confirmation.
8. [depends: steps 2-7] Hand off the useful `adUnitIds`, preview summary, and residual risks to the next workflow.

## Abort Conditions

- stop if the parent hierarchy is still unclear;
- stop before any destructive cleanup without explicit human approval;
- stop if naming conventions or placement goals remain ambiguous.