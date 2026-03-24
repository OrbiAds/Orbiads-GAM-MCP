# Examples

## Run a forecast for specific ad units

```bash
$ orbiads reporting run --type forecast --ad-units 12345,12346 --start 2026-04-01 --end 2026-04-30 --json
{"available": 1250000, "matched": 980000, "possible": 1500000, "contending": [{"lineItemId": "99001", "name": "Competing Campaign", "impressions": 200000}]}
```

## Discover ad units first, then forecast

```bash
$ orbiads inventory ad-units --search "leaderboard" --json
[{"id": "12345", "name": "Homepage_Leaderboard", "sizes": ["728x90"]}]

$ orbiads reporting run --type forecast --ad-units 12345 --start 2026-04-01 --end 2026-04-15 --json
{"available": 625000, "matched": 490000, "possible": 750000, "contending": []}
```

## Counter-Examples

- Do not use this skill to create orders or line items.
- Do not use this skill for delivery reporting on live campaigns.
