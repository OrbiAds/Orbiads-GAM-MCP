---
description: Connect the right GAM tenant, verify auth, and initialize network context before any downstream skill.
---

# OrbiAds — bootstrap

Connect the right OrbiAds tenant to the right Google Ad Manager account, verify credentials, and return a confirmed session packet.

## When to Use

- No confirmed `tenantId` or `networkCode` in the current session.
- User mentions auth, tenant setup, network selection, or readiness checks.
- Before any skill that writes into GAM or consumes credits.

**Do not use** if `tenantId` and `networkCode` are already confirmed — reuse the session packet instead.

## Steps

1. `get_my_tenant_id` — mandatory first call. `[free]`
2. `check_credentials` + `get_network_info` in parallel if no trusted session packet. `[free]`
3. If credentials missing → `initiate_gam_auth`, open browser URL, poll with `poll_auth_status`. `[free]`
4. If multiple networks → `list_accessible_networks`, ask user to choose, then `select_gam_network`. `[free]`
5. If network context empty or stale → `switch_network`. `[free]`
6. Optional: `get_credit_balance` before billed downstream work. `[free]`
7. Return compact session packet.

## Abort Conditions

- Stop if browser auth is still pending — wait for the user.
- Stop if multiple networks available and user has not chosen one.
- Escalate if credentials remain invalid after a completed auth round.

## Output

Wrap the result in `<handoff>` tags:

```
<handoff>
tenantId: ...
networkCode: ...
authStatus: completed | pending | select_network | expired
networkInitialized: true | false
nextRecommendedSkill: inventory-ad-units
</handoff>
```

Use an artifact table when `list_accessible_networks` returns more than one result.
Apply extended thinking before deciding between full bootstrap and `switch_network` only.
