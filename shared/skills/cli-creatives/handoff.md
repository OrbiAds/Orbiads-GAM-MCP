# Handoff

## The Skill Must Return

- list of creative IDs with names and statuses;
- confirmation of any newly uploaded creatives;
- creative-to-advertiser association.

## Open Risks to Surface

- upload may fail if file format is unsupported;
- creative may need SSL validation before deployment;
- credit cost (5 per upload) — confirm balance.

## Next Logical Step

```
<handoff>
creativeIds: [...]
uploadedCount: ...
creditsUsed: ...
nextRecommendedSkill: cli-qa | cli-deploy
</handoff>
```
