# Claude Skill Wrapper — placements-targeting

- load `../../shared/agents/placements-targeting/`;
- execute `../../shared/skills/placements-targeting/`;
- use this skill for placements, taxonomy work, fluid checks, and targeting packets.

## Claude-Specific Hints

- render the placement coverage gap as an artifact table (existing vs. missing vs. proposed);
- use `<handoff>` tags to pass `placementIds`, targeting key/value IDs, and Fluid compatibility result;
- surface destructive operations (key deletion, ad-unit archive) as a separate confirmation block — never bundle them with safe writes;
- use extended thinking when the targeting taxonomy change has downstream impact on existing line items.
