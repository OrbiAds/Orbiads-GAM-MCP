# Claude Skill Index

## Purpose

- list the shared skills exposed through the Claude wrapper;
- keep the exported names aligned with `../../shared/skills/`.

## Current Skill Set

- `bootstrap`
- `inventory-ad-units`
- `availability-forecast`
- `deploy-reporting`
- `advertiser-order-line-items`
- `placements-targeting`
- `native-image`
- `qa-preview`

## Wrapper Rule

- expose the shared folders as-is whenever possible;
- keep one thin wrapper file per skill in this folder;
- add Claude-specific activation hints here only if they do not duplicate the business instructions.