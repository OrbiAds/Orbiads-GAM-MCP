# Memory

## Keep in Session

- `tenantId`, `networkCode`, and `networkInitialized`;
- last confirmed advertiser, order, line-item, and creative IDs;
- selected ad-unit and placement scope;
- latest forecast assumptions and QA verdict;
- pending confirmations, blockers, and cost-sensitive actions.

## Refresh Rules

- refresh tenant or network state only when missing, stale, or explicitly challenged;
- clear downstream IDs when the user changes tenant, network, advertiser, or campaign scope.