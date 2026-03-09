# Examples

## Example User Inputs

- “Review the placements covering these ad units and tell me which ones should be created or updated.”
- “Show me the current custom targeting taxonomy for this tenant and prepare the new values we need for this campaign.”
- “Before we promise Native delivery, validate Fluid support and estimate supply for this constrained inventory.”

## Example Response Plan

- read the current placement and targeting state;
- qualify the relevant ad units and compatibility checks;
- prepare the write plan only for the approved scope;
- summarize what can move directly to trafficking and what still needs approval.

## Example Structured Output

- `selectedAdUnitIds`;
- `placementSummary`;
- `targetingSummary`;
- `compatibilityChecks`;
- `forecastSummary`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not create targeting keys or archive placements before the user approves the exact scope;
- do not run supply-sensitive targeting changes without clarifying whether a forecast check is needed.