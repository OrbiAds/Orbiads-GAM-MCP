# Shared Schemas

## Purpose

- describe the portable contracts used by skills, workflows, and wrappers;
- formalize the required inputs, outputs, and handoff packets.

## Schema Families

- skill input / output contracts;
- workflow manifest contracts for `workflow.yaml`;
- reusable response packet shapes for preview, coverage, forecast, and reporting.

## Included Portable Schemas

- `workflow.schema.yaml` — canonical contract for every workflow manifest;
- `session-packet.schema.yaml` — reusable orchestrator memory packet;
- `skill-handoff.schema.yaml` — compact handoff contract between skill-agents;
- `trigger-hints.schema.yaml` — optional wrapper-facing trigger metadata.

## Workflow Manifest Contract

- `workflow.schema.yaml` is the canonical schema for every `orbiads/docs/workflows/*/workflow.yaml` file;
- it is written as JSON Schema Draft 2020-12 in YAML syntax so editors and CI checks can reuse one source of truth;
- it validates required metadata, approved `status` values, the shared `steps` union (`skill` xor `toolBundle`), and the approved execution `mode` values;
- it also enforces that `lowLevelTools` is present when a workflow contains a `toolBundle` step.

## Rules Kept Outside the Schema

- verify that every referenced skill exists under `../skills/`;
- verify that every `toolBundle` is documented and backed by the listed `lowLevelTools`;
- keep workflow-specific human approvals and business guardrails aligned with the companion `README.md`, `steps.md`, and `tasks.md` files.

## Maintenance Rule

- update `workflow.schema.yaml` first when the workflow manifest contract evolves;
- keep the reusable packet schemas aligned with `shared/examples/` and `shared/agents/`;
- revalidate every workflow manifest after each schema change;
- keep schema wording aligned with the shared skills and real MCP tool names.