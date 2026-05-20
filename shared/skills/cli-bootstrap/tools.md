# Available CLI Commands

## Version & local config

- `orbiads --version` `[free]` — print the installed CLI version.
- `orbiads config show` `[free]` — display local config (tokens masked).
- `orbiads config set --network-code <code> [--api-url <url>] [--default-output table|json|csv]` `[free]` — update `~/.orbiads/config.json`.

## Authentication (Device Flow)

- `orbiads auth login` `[free]` — start Google OAuth Device Flow, store token.
- `orbiads auth logout` `[free]` — clear local credentials (does not revoke server-side).
- `orbiads auth status --json` `[free]` — check auth state, tenant, network, credits.

## Network selection

- `orbiads network info --json` `[free]` — current GAM network details.
- `orbiads network list --json` `[free]` — accessible GAM networks for this tenant.
- `orbiads network switch --network-code <code>` `[free]` — change active GAM network.
- `orbiads network update --file <patch.json>` `[free]` — PATCH network settings (e.g. displayName).

## Tenant settings (server-side — distinct from `config`)

- `orbiads settings general get|set --file <body.json>` `[free]` — tenant general settings (PUT replaces).
- `orbiads settings naming get|set --file <body.json>` `[free]` — naming conventions.
- `orbiads settings delivery-defaults get|set --file <body.json>` `[free]` — delivery defaults.
- `orbiads settings presets list|create --file <body.json>|delete <preset_id>` `[free]` — delivery presets.

## Audit trail

- `orbiads audit log [--limit N]` `[free]` — query the tenant audit log (timestamp, actor, action, target).

## PQL passthrough (advanced)

- `orbiads pql query "<SELECT ... FROM ...>"` `[free]` — run a PQL SELECT against GAM.
