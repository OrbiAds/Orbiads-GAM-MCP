# Agent Trigger — cli-qa

## Enter when

- the user asks to validate or check a campaign before deployment via CLI;
- a workflow needs dry-run validation before proceeding to `cli-deploy`.

## Do not enter when

- the campaign has already passed QA — proceed to `cli-deploy`;
- the request is about creative upload — route to `cli-creatives`;
- the request is about targeting — route to `cli-targeting`.

## Disambiguation

- "validate campaign" or "dry-run" → full QA check;
- "is the campaign ready?" → dry-run validation;
- "check creative coverage" → QA sub-check, still this skill.