# Examples

## Example User Inputs

- “Connect my GAM tenant and tell me whether the network is ready to create ad units.”
- “Check my GAM auth and refresh the network context if needed.”
- “I want to know which network is active before launching a forecast.”

## Example Response Plan

- retrieve `tenantId`;
- check credentials;
- start browser auth only if needed;
- confirm the active `networkCode`;
- state the next recommended skill.

## Example Structured Output

- `tenantId`;
- `authStatus`;
- `networkCode`;
- `networkInitialized`;
- `nextRecommendedSkill`.

## Counter-Examples

- do not use this skill to create inventory, placements, or creatives;
- do not auto-select a network when the user still needs to choose one.