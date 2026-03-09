# Steps

1. [start] Call `get_my_tenant_id` and confirm the active `tenantId`.
2. [depends: step 1] Call `check_credentials` and `get_network_info` in parallel when the session has no trusted bootstrap packet.
3. [depends: step 2] If credentials are missing, run `initiate_gam_auth`, open the browser URL, then follow progress with `poll_auth_status`.
4. [depends: step 3] If auth returns multiple networks, call `list_accessible_networks`, ask the user which `networkCode` to keep, then call `select_gam_network`.
5. [depends: step 2 or 4] If the network context is empty, stale, or explicitly challenged, call `switch_network`.
6. [depends: step 5] Optionally enrich the packet with `get_credit_balance`, `get_tenant_settings`, or `get_delivery_defaults` when downstream billed work is about to start.
7. [depends: steps 1-6] Return a compact packet with `tenantId`, `networkCode`, auth status, network initialization state, and the next recommended skill.

## Abort Conditions

- stop if browser authentication is still pending;
- stop if multiple networks are available and the user has not chosen one;
- stop if credentials remain invalid after a completed auth round.