# Bootstrap & Network

## Purpose

- Connect the right OrbiAds tenant to the right Google Ad Manager account.
- Verify that GAM authentication is ready before any business workflow starts.
- Initialize or re-read the active network context for the next steps.

## Prerequisites

- be connected to the MCP server with the user Google account;
- have GAM access on behalf of the user;
- have a browser available if GAM authentication must be started.

## Inputs

- `tenantId` retrieved through `get_my_tenant_id`;
- optionally a `networkCode` if multiple networks are accessible;
- optionally an explicit request to refresh the network context.

## Expected Output

- validated tenant;
- confirmed or cleanly re-started GAM auth;
- identified active network;
- network context ready for `inventory-ad-units`, forecast, or trafficking.

## Guardrails

- call `get_my_tenant_id` before any other tool;
- prefer `check_credentials` before re-running auth;
- run `select_gam_network` only after an explicit user choice;
- use `switch_network` only when `get_network_info` is empty or a refresh is requested;
- do not use `disconnect_gam` unless explicitly requested or required by a credential incident.

## Handoff

- pass `tenantId`, the active `networkCode`, and the network initialization state to the next workflow;
- move next to `inventory-ad-units`, `availability-forecast`, or advertiser / order flows.