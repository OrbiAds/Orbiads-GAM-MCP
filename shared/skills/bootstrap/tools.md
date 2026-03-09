# Allowed Tools

## Read-First Tools

- `get_my_tenant_id` `[free]` — mandatory first call to retrieve `tenantId`.
- `check_credentials` `[free]` — verify whether the tenant already has valid GAM credentials.
- `get_network_info` `[free]` — re-read the already initialized network context.
- `list_accessible_networks` `[free]` — list accessible networks when the user must choose.
- `get_credit_balance` `[free]` — optional, to confirm the tenant can continue with cost-sensitive tools.
- `get_tenant_settings` / `get_delivery_defaults` `[free]` — optional, to enrich tenant context.

## Authentication and Network Selection

- `initiate_gam_auth` `[free]` — start GAM OAuth if `check_credentials` shows missing credentials.
- `poll_auth_status` `[free]` — follow browser auth state until `completed` or `select_network`.
- `select_gam_network` `[free]` — allowed only after an explicit user choice.
- `switch_network` `[free]` — initialize or refresh the cached network context if `get_network_info` is empty or stale.

## Sensitive Tool

- `disconnect_gam` `[free]` — exceptional; only on explicit request, with confirmation.