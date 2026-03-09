# Allowed Tools

## Targeting Reference Data

- `get_available_countries` `[free]` — retrieve the country IDs available for geo-targeting.
- `get_available_languages` `[free]` — retrieve the available language IDs.
- `get_device_categories` `[free]` — retrieve the available device categories.

## Primary Forecast Tools

- `get_standalone_forecast` `[variable]` — recommended path for a scenario without an existing line item.
- `get_delivery_forecast_by_line_item` `[variable]` — forecast from a real line item.
- `get_inventory_forecast` `[variable]` — lower-level variant for direct inventory targeting.

## Usage Rule

- these tools do not write into GAM, but some can consume credits;
- always document the assumptions used in the skill output.