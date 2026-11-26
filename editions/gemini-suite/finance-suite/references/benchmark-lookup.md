# Public benchmark lookup

Use one shared dataset across finance workflows. Keep approved internal figures, internal workflow status and public benchmarks separate. Answer in this order: approved result, evidenced internal driver, relevant public benchmark, then unresolved gap and next approved source. Public observations must never fill an internal actual, forecast, exposure, mapping, job-rank cost or missing owner confirmation.

## Choose the appropriate observation

Identify the decision, geography, required frequency/horizon, period or cutoff, currency/unit or index base, and seasonal adjustment. Use a documented dataset series or immutable snapshot when supplied. If the current host can access the approved local API, use its read-only lookup; otherwise inspect an authorized JSON/CSV snapshot. A Copilot/Gemini cloud session cannot be assumed to reach the user's loopback API or Windows files.

Read provider and exact series ID, observation period, unit, geography, adjustment/base, retrieval time, release date when known, rights and freshness status. Keep actual public observations distinct from synthetic test examples. A series' metadata or successful HTTP response is not proof of usable current observations.

## Preserve information vintage

For a historical forecast cutoff, request an available `as_of` or explicit immutable `snapshot_id`. Use only observations actually evidenced as available by that cutoff. A date attached to an observation or a current revised history does not prove what was known then. If the dataset returns `as_of_unavailable`, state that limit; do not substitute the latest revised series.

Keep revisions and prior snapshots. Distinguish a partial period, a rebased index, a changed series definition, stale data, a provider failure and a valid empty observation result. A failed refresh does not mean zero movement or no events. Use a last-good snapshot only with its age and failure/stale status visible.

## Interpret without inventing internal drivers

Use production indices to challenge volume assumptions, commodity indices to test material/energy sensitivity, wage/hours measures to benchmark assumptions and public FX to describe market direction. They do not reconstruct product-level orders/costs/inventory, supplier prices, utility tariffs, job-rank payroll, booked rates or approved planning exposures.

Keep original observations separate from derived crosses, conversions and percentage changes. Retain input series/observations, formula and transformation version. Preserve USD commodity values when also presenting a JPY conversion; do not count FX twice. Do not compare indices across base revisions without a supported link.

Before treating an external indicator as a forecasting driver, compare with a simple baseline at rolling forecast origins using only data available at each origin. Keep horizon and metric fixed for comparison. Published forecasting research does not prove improvement for the user's dataset.

## Deliver

Give the relevant benchmark concisely, citing provider, series, period, unit, snapshot and freshness. Explain its limited relevance to the internal question and preserve any unresolved input gap. Do not emit an automatic bibliography, audit table or extra worksheet.

Use only rights-cleared values from the shared dataset. Permission-required or unresolved sources remain metadata/retrieval recipes until permission is established. The repository software license does not cover upstream observations or papers. Never send private prompts, workbook values, company identifiers or credentials to public providers.
