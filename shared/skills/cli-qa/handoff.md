# Handoff

## The Skill Must Return

- campaign configuration summary;
- creative coverage and SSL status;
- dry-run results: errors, warnings, or clean pass;
- go/no-go recommendation.

## Open Risks to Surface

- creatives may lack SSL compliance;
- targeting may be incomplete;
- dry-run may miss runtime issues only visible during actual deployment.

## Next Logical Step

```
<handoff>
campaignId: ...
dryRunStatus: pass | warnings | errors
blockingIssues: [...]
warnings: [...]
nextRecommendedSkill: cli-deploy
</handoff>
```
