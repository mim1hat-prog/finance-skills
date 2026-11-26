# Use the correct information vintage without inventing an internal forecast

This entire case is independently invented. The public benchmark is an
Exampleland production index with base 2020 = 100, for observation period
February 2024. Two immutable snapshots are available:

| Snapshot | Provider release time, UTC | Retrieval time, UTC | Value |
| --- | --- | --- | ---: |
| s-20240315 | 2024-03-14T09:00:00Z | 2024-03-15T09:00:00Z | 101 |
| s-20240410 | 2024-04-09T09:00:00Z | 2024-04-10T09:00:00Z | 104 |

The forecast cutoff is **2024-03-31T23:59:59Z**. The internal approved production
forecast for the requested entity is missing, and no other approved internal
source is available in this case. The benchmark may provide context but cannot
replace that forecast or prove a business driver.

Return only a JSON object with `benchmark_at_cutoff`, `latest_benchmark`,
`snapshot_at_cutoff`, `observation_period`, `unit`, `internal_forecast`,
`internal_forecast_status`, `public_backfill`, `benchmark_role`, and
`driver_causality`.

Use JSON numbers for available values and JSON null for an unavailable forecast.
Use `2024-02` for the observation period, `index, 2020=100` for the unit,
`unavailable` for missing internal status, a JSON boolean for public backfill,
`context` for the benchmark role and `unconfirmed` when causality is unsupported.
