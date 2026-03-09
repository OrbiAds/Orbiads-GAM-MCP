# Examples

## Example User Inputs

- “Tell me whether these 3 ad units can support 2 million impressions from April 1 to April 30 in 300x250.”
- “Check the forecast for line item 123456 before activation.”
- “Give me the useful country and language IDs, then run a forecast for France on smartphones.”

## Example Response Plan

- confirm the delivery window and creative sizes;
- resolve the useful targeting IDs;
- run the right forecast;
- explain the numbers and risk level;
- recommend the next step.

## Example Structured Output

- `scenarioType`;
- `targetingAssumptions`;
- `availableUnits`;
- `pressureLevel`;
- `recommendation`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not use this skill to create or activate line items directly;
- do not run a forecast before the user confirms dates, sizes, and core targeting assumptions.