# Claude Activation

- first, determine whether the request is bootstrap, inventory, targeting, forecast, trafficking, creative, QA, or reporting;
- second, load the matching thin skill file from `../skills/`;
- third, follow the canonical skill from `../../shared/skills/` and the matching agent from `../../shared/agents/`;
- if the user spans multiple stages, route through `../agents/orchestrator.md` before acting.