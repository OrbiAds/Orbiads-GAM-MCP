# Business Queries

## Purpose

- Group ready-to-use prompts by AdOps job to accelerate adoption.
- Complement the skills and workflows with realistic user inputs.

## Prompt Packet

- include the known `tenantId`, `networkCode`, IDs already in hand, and the desired stopping point;
- say explicitly whether the request is read-only, `dry_run`, or ready for a confirmation gate;
- for multi-stage work, ask for the smallest next decision rather than the whole end-to-end flow in one sentence.

## Query Families

- `bootstrap`
  - "Confirm the active tenant, check credentials, list reachable networks if needed, and stop before any write."
- `inventory-ad-units`
  - "Audit the ad-unit tree, flag inactive branches, and prepare a blueprint only if the naming issues are clear."
- `placements-targeting`
  - "List the placements tied to this inventory packet, validate fluid support, and summarize the targeting dimensions we still need."
- `availability-forecast`
  - "Given this inventory and traffic goal, tell me whether supply is sufficient before we create or activate anything."
- `advertiser-order-line-items`
  - "Reuse the existing advertiser if it matches, verify the order setup, draft line items, and stop before activation."
- `native-image`
  - "Turn this approved image asset into a Classic Native creative and keep the output ready for QA only."
- `qa-preview`
  - "Run compliance, SSL, preview, and creative coverage checks, then give me a go/no-go summary."
- `deploy-reporting`
  - "Prepare a deployment dry run, list the rollback path, and show the lightest delivery read I should use after launch."

## Routing Rule

- when a prompt spans more than one family, route through `../../shared/agents/orchestrator/` first;
- once the next skill is clear, keep the request narrow so the wrapper stays thin and predictable.