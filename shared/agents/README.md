# Shared Agents

## Purpose

- host the canonical orchestration layer above `../skills/`;
- define routing, memory, escalation, and recovery rules once for every wrapper;
- keep Claude, OpenAI/Codex, and Gemini wrappers thin.

## Folder Contract

- `orchestrator/` owns intent routing and session-wide decisions;
- one folder per business skill-agent mirrors `../skills/`;
- transversal agents centralize credit, context, and recovery behavior.

## Skill-Agent Contract

- `persona.md` — operating role and success criteria;
- `system-prompt.md` — execution rules and delegation behavior;
- `trigger.md` — when to enter the skill;
- `abort.md` — when to stop or escalate;
- `memory.md` — session fields worth retaining.

## Rule

- wrappers may rephrase activation hints, but must not duplicate business steps already documented in `../skills/`.