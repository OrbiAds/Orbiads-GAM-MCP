# Shared Prompts

## Purpose

- centralize reusable snippets across wrappers and agents;
- keep business prompting portable and thin-wrapper friendly.

## Available Snippets

- `confirmation-request.md` — ask for explicit approval before a real write;
- `credit-warning.md` — announce a cost-sensitive path;
- `guardrail-reminder.md` — restate read/preview/QA safety rules;
- `handoff-formatter.md` — normalize compact packets between skills;
- `recovery-plan.md` — summarize a safe retry or fallback path.

## Rule

- wrappers may adapt the tone, but must preserve the same guardrails and field names.