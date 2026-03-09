# Examples

## Example User Inputs

- “Audit my inventory and tell me which ad units are problematic.”
- “Generate a web + app blueprint for the brand `leparisien` with home/article and native/mpu formats.”
- “Prepare a dry run to create these 8 ad units and summarize what still needs confirmation.”

## Example Response Plan

- read the real inventory;
- qualify the units that already exist;
- propose a blueprint or a batch;
- provide the creation preview;
- summarize the expected human validations.

## Example Structured Output

- `selectedAdUnitIds`;
- `auditFindings`;
- `creationPreview` or `blueprintSummary`;
- `confirmationNeeded`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not use this skill to create placements or targeting keys directly;
- do not promise destructive cleanup just because inactive candidates were found.