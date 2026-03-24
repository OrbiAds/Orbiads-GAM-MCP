# Handoff

## The Skill Must Return

- selected targeting keys and values;
- validated ad unit IDs;
- compatibility status.

## Open Risks to Surface

- targeting keys may have no values yet;
- ad units may not support the selected sizes;
- geo, language, or device targeting may need MCP or web UI.

## Next Logical Step

```
<handoff>
targetingKeys: [{key: "...", values: [...]}]
validatedAdUnitIds: [...]
compatibilityStatus: ok | warnings
nextRecommendedSkill: cli-creatives | cli-deploy
</handoff>
```
