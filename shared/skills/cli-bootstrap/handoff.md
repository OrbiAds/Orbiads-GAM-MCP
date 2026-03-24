# Handoff

## The Skill Must Return

- confirmed CLI version;
- active tenant and authentication status;
- active `networkCode`;
- `networkInitialized` indicator.

## Open Risks to Surface

- CLI not installed or outdated;
- authentication expired or missing;
- network context not initialized;
- multiple networks available and none selected.

## Next Logical Step

```
<handoff>
cliVersion: ...
authStatus: authenticated | unauthenticated
networkCode: ...
networkInitialized: true | false
nextRecommendedSkill: cli-inventory
</handoff>
```
