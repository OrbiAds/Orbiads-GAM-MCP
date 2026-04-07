# Agent Trigger — cli-forecast

## Enter when

- the user asks to check supply availability or run a forecast via CLI;
- a workflow needs to verify impression capacity before deployment.

## Do not enter when

- ad unit IDs are not yet known — route to `cli-inventory` first;
- the request is about deployment — route to `cli-deploy`;
- the request is about targeting configuration — route to `cli-targeting`.

## Disambiguation

- "check availability" or "forecast" → run forecast with known ad units;
- "is there enough supply?" → forecast path;
- "how many impressions?" → forecast read, not inventory read.