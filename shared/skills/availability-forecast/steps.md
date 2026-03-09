# Steps

1. [start] Verify that the active network and the reference ad units or line items are known.
2. [depends: step 1] Resolve the required targeting IDs with `get_available_countries`, `get_available_languages`, and `get_device_categories`; these reads are `[parallel-safe]`.
3. [depends: steps 1-2] Choose the correct path: `get_standalone_forecast`, `get_delivery_forecast_by_line_item`, or `get_inventory_forecast`.
4. [depends: step 3] Run the selected forecast with dates, creative sizes, and targeting assumptions described as explicitly as possible.
5. [depends: step 4] Interpret `availableUnits`, `forecastUnits`, `possibleUnits`, and the competitive pressure level.
6. [depends: step 5] Produce a clear recommendation: continue, adjust targeting, reduce the goal, or stop.
7. [depends: step 6] Hand off the assumptions, cost-sensitive notes, and risks to the next workflow.

## Abort Conditions

- stop if dates, sizes, delivery goal, or targeted scope are still missing;
- stop if the user requests many speculative reruns without approving the cost-sensitive path;
- stop if the forecast inputs contradict the known line-item or inventory setup.