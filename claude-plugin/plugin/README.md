# Claude Plugin

## Purpose

- store the Claude-facing packaging assets only;
- keep manifests, plugin metadata, and any platform-specific discovery files here;
- point every business instruction back to `../../shared/skills/`.

## Expected Contents

- `manifest.json` for wrapper packaging metadata;
- `system-prompt.md` for the Claude platform layer;
- `activation.md` for lightweight discovery and startup hints;
- lightweight assets required for installation or updates;
- no duplicated workflow logic, no duplicated tool descriptions.

## Rule

- if a document starts describing AdOps business steps, move that content back to `../../shared/skills/` or `../../docs/workflows/`.