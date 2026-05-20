# Available CLI Commands

## Inventory forecast (GAM ForecastService)

- `orbiads inventory forecast --file <req.json>` `[free]` — line-item probabilistic delivery forecast.
- `orbiads reporting forecast standalone --file <req.json>` `[free]` — standalone inventory forecast (no draft LI needed).
- `orbiads reporting forecast prospective --file <req.json>` `[free]` — prospective delivery forecast.
- `orbiads reporting forecast traffic --file <req.json>` `[free]` — historical traffic data.
- `orbiads reporting forecast-line-item <job_id>` `[free]` — delivery forecast for the line items of a job.

## GA4 (cross-source verification)

- `orbiads reporting ga4 run --file <req.json>` `[free]` — run a GA4 report.
- `orbiads reporting ga4 dimensions` `[free]` — list GA4 dimensions.
- `orbiads reporting ga4 metrics` `[free]` — list GA4 metrics.

## Custom reporting (for after-the-fact verification)

- `orbiads reporting run --dimensions <list> --metrics <list> --start <YYYY-MM-DD> --end <YYYY-MM-DD>` `[free]` — run a custom report.
- `orbiads reporting dimensions` `[free]` — REST-valid dimension catalogue.
- `orbiads reporting metrics` `[free]` — REST-valid metric catalogue.
- `orbiads reporting date-ranges` `[free]` — relative date-range presets.

## Supporting inventory reads

- `orbiads inventory ad-units [--search <name>] [--limit N]` `[free]` — list ad units to target.
- `orbiads inventory ad-units-by-ids --file <ids.json>` `[free]` — bulk fetch ad units.
- `orbiads inventory search-ad-units --query <q> [--limit N] [--offset N]` `[free]` — name/code search.
- `orbiads inventory sizes` `[free]` — distinct sizes in the network.
- `orbiads inventory countries|device-categories|languages` `[free]` — reference data for targeting.
