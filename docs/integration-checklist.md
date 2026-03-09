# Integration Checklist

## Purpose

- List every task that should be finished before extracting the scaffold into its own repository.
- Keep the rollout order simple so architecture, skills, wrappers, and validation do not get mixed together.

## Phase 0 — Lock the Scope

- confirm the first skill batch: `bootstrap`, `inventory-ad-units`, `availability-forecast`, `deploy-reporting`;
- confirm the exact MCP tools exposed by each skill;
- confirm the expected outputs and handoffs between skills;
- isolate what stays outside batch 1: source-image flows, advanced HTML5, audio, video, and demo UX.

## Phase 1 — Fill the Shared Foundation

- create one real folder per skill in `shared/skills/`;
- write `README.md`, `tools.md`, `steps.md`, `examples.md`, and `handoff.md` for each skill;
- define the guardrails: read-only when possible, `dry_run`, human confirmation, preview, and QA;
- align business wording across skills, workflows, and wrappers;
- document portable input/output contracts in `shared/schemas/`.

## Phase 2 — Write the Composed Workflows

- create one folder per workflow in `docs/workflows/`;
- include `README.md`, `steps.md`, `tasks.md`, and `workflow.yaml` for each workflow;
- write `inventory-to-placement/` as a complete and optimized workflow;
- write `deploy-to-reporting/` as a complete and optimized workflow;
- prepare `image-to-native/`, `image-to-html5/`, and `audio-video-trafficking/` with the same contract;
- link each workflow to the shared skills and intermediate deliverables;
- cover, for every workflow, prerequisites, nominal path, variants, restart points, human validations, handoffs, and risk signals;
- document expected optimizations: fewer unnecessary calls, reuse of prior skill outputs, and the safest execution order.

## Phase 3 — Integrate the Platform Wrappers

- reference the shared skills from `claude-plugin/`;
- reference the shared skills from `openai-codex/`;
- reference the shared skills from `gemini-extension/`;
- complete `docs/install/claude.md`, `openai-codex.md`, and `gemini.md`;
- keep Gemini documentation aligned across extension packaging and direct MCP mode.

## Phase 4 — Add Business Queries and Examples

- expand `docs/queries/` with ready-to-use business prompts;
- add workflow examples in `shared/examples/`;
- add platform-specific examples in each wrapper;
- verify that every critical batch-1 skill has at least one example.

## Phase 5 — Check Consistency and Safety

- verify that every documented skill maps to real MCP tools;
- verify that names stay aligned across `shared/`, wrappers, and workflows;
- verify that sensitive steps require preview, QA, and confirmation;
- verify that the docs clearly distinguish read-only, `dry_run=True`, and real writes;
- run `git diff --check` before extraction.

## Phase 6 — Extract the Standalone Repository

- create the new external repository;
- copy the `orbiads/` folder;
- adjust relative paths and internal links;
- verify that each wrapper contains packaging only;
- prepare the first PR batch by functional block.

## Recommended Order

1. lock batch 1;
2. fill `shared/skills/`;
3. write the complete and optimized workflows;
4. wire Claude, Codex, and Gemini to the shared foundation;
5. complete queries and examples;
6. run consistency checks;
7. extract to the standalone repository.