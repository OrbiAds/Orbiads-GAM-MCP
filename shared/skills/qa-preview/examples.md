# Examples

## Example User Inputs

- “Before activation, scan this HTML5 bundle, validate SSL, and show me the preview URLs.”
- “Give me the campaign-level preview pack for this order and tell me whether coverage is complete.”
- “Check these creatives for SSL and summarize whether deployment can proceed.”

## Example Response Plan

- run the relevant compliance and SSL checks;
- generate the smallest useful preview pack;
- verify coverage;
- return a clear go / no-go packet with the remaining blockers.

## Example Structured Output

- `complianceFindings`;
- `sslStatus`;
- `previewUrls`;
- `coverageStatus`;
- `goNoGoRecommendation`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not move to deployment while blockers are still unresolved;
- do not request a campaign-wide preview pack when one line-item preview is enough for the decision.