# Handoff

## The Skill Must Return

- list of matching ad units with IDs and sizes;
- available targeting keys if explored;
- placement details if explored.

## Open Risks to Surface

- no ad units found matching criteria;
- network context not initialized;
- ad units may be inactive or archived.

## Next Logical Step

```
<handoff>
selectedAdUnitIds: [...]
availableSizes: [...]
targetingKeys: [...]
nextRecommendedSkill: cli-orders | cli-targeting
</handoff>
```
