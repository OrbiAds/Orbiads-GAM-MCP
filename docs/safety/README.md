# Guardrails

## Baseline Rules

- default to read-only whenever possible;
- require `dry_run` before any batch write;
- require human confirmation before real pushes;
- require preview and QA before activation;
- review billing and audit signals after deployment.

## Session and Auth Gates

- bootstrap must confirm `tenantId`, credentials, and `networkCode` before downstream skills run;
- stop early when auth is incomplete, network selection is ambiguous, or the active tenant is unclear;
- retain session memory so later skills do not silently switch tenant or network context.

## Credit and Latency Control

- warn before forecast, preview, compliance, or reporting paths that can consume credits or add latency;
- prefer the lightest read that answers the user question before escalating to heavier report or preview bundles;
- batch only when the shared skill marks a step as safe to parallelize.

## Write Gates

- inventory writes must start from audit, blueprint, or candidate review before batch creation or archival;
- advertiser, order, line-item, placement, and campaign writes require a clear recap before confirmation;
- deployment actions must separate `dry_run`, approval, execution, and post-action monitoring.

## Creative and Launch Gates

- Native and HTML5 creative work requires approved assets plus naming context before creation;
- compliance scan, SSL validation, preview, and coverage checks must complete before live activation;
- never treat preview URLs as approval by themselves: a human go/no-go is still required.

## Recovery and Escalation

- route multi-stage or blocked flows back through `shared/agents/orchestrator/`;
- use rollback only after summarizing the blast radius and obtaining explicit approval;
- consult audit and delivery signals after any sensitive action.

## Documented Boundaries

- do not document `find_or_create_order` in wrapper or skill guidance;
- treat `create_open_bidding_line_item` as a capability boundary only until its backend implementation is complete.

## Next Safety Expansions

- skill-family specific rules;
- volume limits;
- error and rollback strategy.