# CLI Workflow Reference

Durable CLI-specific procedures and gotchas for OrbiAds operations. Load this file when
working on the CLI surface. Not needed for MCP-only sessions.

---

## Bootstrap sequence

Always run this before any CLI operation in a session:

```bash
orbiads --version                          # confirm CLI is installed
orbiads auth status --json                 # check auth + active tenant
orbiads network info --json                # confirm active network context
```

- If not authenticated: tell the user to run `orbiads auth login` (browser OAuth flow).
- If multiple networks: run `orbiads network list --json`, ask the user to choose, then
  `orbiads network switch --network-code <code> --json`.
- If credentials expired: same as not authenticated.
- Auth missing / CLI not installed: `pip install orbiads-cli`.

**`orbiads network info --json` is the tenant-settings oracle for CLI sessions.**
It includes naming conventions, delivery defaults, campaign presets, preview pages, and
auto-archival config — the same data `get_naming_conventions` + `get_delivery_defaults` +
`list_presets` + `get_tenant_settings` return via MCP. Read it once at Phase 0; store the
result for use throughout the session.

---

## `--json` discipline

**Always pass `--json`** to every CLI call. Without it, output is human-readable and
unparseable by the model. Structured output is required to extract IDs and status fields.

---

## Fallback naming conventions

When `orbiads network info --json` shows null templates (user has not configured naming),
apply these defaults:

| Entity      | Pattern                                    | Example                              |
|-------------|-------------------------------------------|--------------------------------------|
| Advertiser  | `{BrandName}`                              | `Renault`                            |
| Order       | `{Brand} — {Campaign} — {Month YYYY}`     | `Renault — Spring Launch — Apr 2026` |
| Line Item   | `{Brand} — {Size} — {Targeting} — {Type}` | `Renault — MPU 300x250 — FR Desktop — Standard` |
| Creative    | `{Brand} — {Size} — {Version}`            | `Renault — MPU 300x250 — v1`         |

Rules:
- Use `—` (em dash) as separator, **not** `-` (hyphen).
- Keep names unique across the network (GAM enforces this for Orders).
- Include size in Line Item and Creative names.
- Add version numbers to creatives when A/B testing.

When templates ARE configured, the `--name` values you pass are used as **macro values**
(e.g. `{advertiser}`, `{campaign}`) that the backend expands into the final name.

---

## Per-phase CLI command sequences

### Phase 0 — Bootstrap & configuration
```bash
orbiads --version
orbiads auth status --json
orbiads network info --json
# If network not active:
orbiads network list --json
orbiads network switch --network-code <code> --json
```

### Phase 1 — Inventory discovery
```bash
# Check presets first (already in network info output)
orbiads inventory ad-units --json
orbiads inventory ad-units --search "<name>" --json
orbiads inventory placements --json
orbiads inventory keys --json
orbiads inventory keys --key "<name>" --json
```

### Phase 2 — Forecast (free)
```bash
orbiads reporting run --type forecast \
  --ad-units <id1>,<id2> \
  --start <YYYY-MM-DD> --end <YYYY-MM-DD> \
  --json
```

### Phase 3 — Advertiser & order
```bash
# Search before creating (avoid duplicates)
orbiads advertisers list --search "<brand>" --json
orbiads advertisers create --name "<brand>" --json        # 1 credit
orbiads orders list --advertiser <id> --json
orbiads orders create --advertiser <id> --name "<name>" --json  # 1 credit
```

### Phase 4 — Line items
Line items with complex targeting are created via MCP or GAM UI. CLI supports read:
```bash
orbiads orders get --id <orderId> --json
```

### Phase 5 — Creatives
```bash
orbiads creatives upload --file <path> --name "<name>" --advertiser <id> --json  # 5 credits
orbiads creatives get --id <id> --json                   # verify creation
orbiads creatives list --search "<name>" --json
```

### Phase 6 — QA
```bash
orbiads campaigns get <id> --json                        # inspect full config
orbiads creatives get --id <id> --json                   # check compliance + SSL fields
orbiads campaigns deploy <id> --dry-run --json           # simulate (free)
```

### Phase 7 — Deploy & poll
```bash
# Deploy (5 credits — requires explicit user confirmation)
orbiads campaigns deploy <id> --yes --json
```

Deploy polling loop (max 5 minutes):
```bash
for i in $(seq 1 30); do
  sleep 10
  STATUS=$(orbiads campaigns get <id> --json | jq -r '.data.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "deployed" ] || [ "$STATUS" = "failed" ]; then break; fi
done
```

Post-deploy monitoring:
```bash
orbiads reporting run --type delivery --campaign <id> --json
```

---

## Abort conditions

| Condition | Action |
|-----------|--------|
| Bootstrap not complete | Stop; run bootstrap sequence first |
| Auth missing or expired | Tell user `orbiads auth login` |
| CLI not installed | Tell user `pip install orbiads-cli` |
| Forecast < 50% of goal | Stop; report to user; require acknowledgment before proceeding |
| QA dry-run has blocking errors | Stop; fix before deploying |
| Creative size ≠ line item placeholder | Stop; size mismatch is the #1 API error |
| Order name already exists | Stop; GAM enforces network-wide uniqueness |
| User declines confirmation | Stop; never auto-proceed on writes |
| 5-minute polling timeout | Stop; report last known status to user |
| Delivery defaults mismatch detected in pre-deploy check | Stop; confirm with user |

---

## Tenant-settings interplay

`orbiads network info --json` returns the tenant's OrbiAds configuration. Key fields:

- `namingConventions.orderTemplate` / `lineItemTemplate` / `creativeTemplate` / `nativeStyleTemplate`
  — the backend expands these automatically. When set, the `--name` values you pass are macro
  inputs, not final names. When null, the backend uses `--name` as-is (apply fallback table above).
- `deliveryDefaults.*` — applied automatically on entity creation. Only pass explicit flags when
  the campaign brief overrides a default.
- `presets` — pre-configured ad-unit + targeting bundles. Check before manual inventory discovery.
- `tenantSettings.previewPages` — site page URLs for in-context creative preview.

---

## CLI coverage gaps

Not all MCP actions have CLI equivalents. When a user needs an action that is `MCP-only` in
the consolidated skill's `references/actions.md`:

1. Tell the user that action is available via MCP or the web app.
2. Do **not** improvise raw REST or SOAP calls.
3. Do **not** shell out to curl/python as a workaround.

The sub-skill action tables (each domain skill's `references/actions.md`) carry a CLI column
showing which actions are mapped and which are `MCP-only`.

---

## Misc gotchas

**Source: cli-bootstrap / cli-campaign (2026-06-11 harvest)**

- `orbiads network info --json` (not just `auth status`) confirms tenant configuration is
  active. Always run both in the bootstrap sequence.
- CLI does not have a `find_or_create_advertiser` equivalent; always search first, then create
  only if not found — prevents duplicates.
- Line item type defaults: if the brief does not specify, use the tenant's configured
  `deliveryDefaults.lineItemType`. Falling back to `STANDARD` without checking is wrong.
- `CreativeAssetService` removed in GAM v202502 — image bytes are inlined in `createCreatives`.
  Relevant for CLI creative upload: the `orbiads creatives upload` command handles this
  transparently, but raw API calls must not use the removed service.
- A line item stuck in `NEEDS_CREATIVES` means a creative size is missing or the assignment
  failed — check `creativePlaceholders` match.
- GAM rule: `advertiserId` on an Order must point to a Company with `type=ADVERTISER`. Using
  an agency ID causes an API error.
- GAM rule: Order names must be unique across the **entire network** (not just per advertiser).
- Test network 45515589: available for writes, but the REST Reporting API does not work there.
  Use `orbiads reporting run` only against production networks.
- Dry-run (`--dry-run`) is free and must be shown to the user before executing a real deploy.
  The `--yes` flag bypasses the interactive prompt but still requires explicit user confirmation
  in the conversation before the agent runs the command.
