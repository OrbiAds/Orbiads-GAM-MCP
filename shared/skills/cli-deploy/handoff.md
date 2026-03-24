# Handoff

## The Skill Must Return

- deployment status: deploying, deployed, or failed;
- job ID for tracking;
- delivery report summary if deployment succeeded;
- error details if deployment failed.

## Open Risks to Surface

- deployment may take longer than expected;
- delivery data may not be available immediately after deployment;
- failed deployments may leave partial resources that need cleanup.

## Next Logical Step

```
<handoff>
campaignId: ...
jobId: ...
deploymentStatus: deployed | failed
deliveryImpressions: ...
deliveryStatus: delivering | not_started
nextRecommendedSkill: null
</handoff>
```
