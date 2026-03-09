# Gemini Installation

## Scope

- package the installable Gemini extension;
- document the direct MCP fallback mode;
- explain the operational limits of each mode.

## Asset Map

- `../../gemini-extension/extension/manifest.json` — extension descriptor;
- `../../gemini-extension/extension/function-declarations.yaml` — callable routing surface;
- `../../gemini-extension/extension/system-instruction.md` — thin Gemini platform layer;
- `../../gemini-extension/router.md` — skill dispatch;
- `../../gemini-extension/skills/*.md` and `../../gemini-extension/examples/*.md` — thin skill aliases and examples.

## Installation Topics to Cover

- exact extension packaging format;
- local installation steps;
- extension vs direct MCP comparison matrix;
- how shared skills are exposed without duplicating business content.

## Recommended Modes

- use the extension wrapper when Gemini can load the manifest, system instruction, and function declarations together;
- use direct MCP fallback when the runtime cannot preserve the wrapper packaging cleanly or needs faster local iteration;
- in both modes, keep `../../shared/agents/` and `../../shared/skills/` as the only business source of truth.

## Recommended Steps

1. start the MCP server in `streamable-http` mode for the normal path;
2. load the extension assets from `../../gemini-extension/extension/`;
3. validate that Gemini routes through `../../gemini-extension/router.md` before calling a skill wrapper;
4. fall back to direct MCP mode only when packaging constraints block the normal extension flow.

## Smoke Check

- ask Gemini to classify a request into the correct skill without executing writes;
- verify that the answer references the expected thin wrapper and shared skill;
- confirm that preview, QA, and confirmation remain required after routing.

## Rollback

- revert the extension manifest and function declarations together if Gemini stops routing cleanly;
- switch temporarily to direct MCP fallback rather than duplicating skill logic in the extension layer;
- keep the fallback documented and aligned with the same guardrails as the extension path.

## Guardrails

- keep the extension wrapper thin and shared-skill driven;
- document when users should fall back to direct MCP mode;
- preserve the same preview, QA, and confirmation rules as the other wrappers.