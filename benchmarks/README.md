# Public benchmarks for finance commentary

The initial public snapshots retain the recorded completion times and hashes of their saved public source bytes. The bundled success receipts use `offline-seed-validation-complete` and the later time at which those snapshots were validated locally. They do not claim another provider fetch. Historical queries can select an acquired snapshot before that validation receipt existed; their `refresh_status` remains null until a recorded receipt is eligible for the cutoff.

Use this dataset after the approved result and verified internal explanation. Cite **provider, series, observation period, unit and snapshot ID**. A public benchmark supplies context for a question or scenario; it cannot reconstruct a missing internal forecast, mapping, exposure or granular personnel-cost split.

## Included data and access status

The actual snapshot files contain a bounded verified ECB daily reference-rate extract and selected World Bank Pink Sheet monthly prices. Original data and project-derived FX crosses are separately identified. See each snapshot's exact coverage, retrieval timestamp, source hash, frozen rights record and attribution; see [the dictionary](DATA_DICTIONARY.md) for interpretation.

- **ECB FX:** JPY, USD, CNY and THB per EUR, plus separate project-calculated JPY per USD/CNY/THB crosses. The direct public CSV endpoint and strict parser were exercised.
- **World Bank Pink Sheet:** aluminum, copper, Brent and Japan LNG in their published nominal USD units. The current official workbook and selected columns/units were inspected; only permitted normalized observations are included.
- **BOJ price indices:** exact domestic producer/import-price series metadata and a parser are present. Commercial reproduction permission is unresolved for this use, so the collector blocks mirroring and no BOJ values are bundled.
- **METI transport equipment:** original and seasonally adjusted candidates are distinct. The official landing page was inaccessible and exact workbook URL/row codes remain unverified. A configured-workbook parser is tested with invented data; it is not labeled a verified live adapter. Transport equipment is broader than vehicle production.
- **MHLW wages/hours through e-Stat:** configuration candidates and a strict classification parser are present. The exact statistics table/series have not been selected and an application ID is required. No wage/hour values or credentials are bundled.

Source review and rights are recorded per series in `catalog.json` and linked to the canonical research registry. No raw provider XLSX/PDF is distributed. This software's MIT license does not replace provider licenses.

## Query offline

The checked-in snapshots work without a network request, subscription or API key:

```powershell
py -3 scripts\benchmark_api.py --check
py -3 scripts\benchmark_api.py
```

The second command starts a manual foreground server bound to `127.0.0.1:8765`. Stop it with **Ctrl+C**. It is not a deployment, a work-PC daemon or an automatic Copilot/Gemini connector.

```text
GET /v1/datasets
GET /v1/series/ecb-jpy-per-eur
GET /v1/series/ecb-jpy-per-eur/observations?start=2026-11-01&end=2026-11-24&limit=10
GET /v1/series/worldbank-copper/observations?start=2025-11-01&end=2026-10-31&limit=12
GET /v1/snapshots/{snapshot_id}
```

Use `snapshot_id` to reproduce exact retained values, or `as_of` with a timezone to select a snapshot actually retained by that cutoff. They are mutually exclusive. A query for an earlier unretained cutoff returns `as_of_unavailable`, even when the observations themselves concern that earlier period.

Retrieval timestamps follow completion of the fetch or file read. Historical queries exclude refresh receipts recorded after the cutoff; missing historical receipts remain null. Original and derived public rows must match their frozen series definition, so derived values cannot bypass input/formula checks by being relabeled original.

Observation requests require both dates, at most 3,660 days apart. Only complete observation periods inside those bounds are selected. `limit` is 1–500; `offset` is 0–100,000, and `next_offset` indicates a following page. There are no write routes. Errors use RFC 9457 `application/problem+json`. [OpenAPI contract](../api/openapi.yaml)

## Explicit refresh

These commands make public provider requests only when deliberately run. The ordinary skill packages and API queries never start them:

```powershell
py -3 scripts\benchmark_collect.py --adapter ecb --start 2026-11-01 --end 2026-11-24
py -3 scripts\benchmark_collect.py --adapter worldbank --start 2025-11-01 --end 2026-10-31
```

Choose the dates you need. Review the public rights/source configuration before collection. An updated provider workbook URL, column definition, index base or license is a reviewable metadata change; it is not silently inferred. To import a provider file obtained through an approved route, supply `--input` with the same adapter and date range. This does not bypass source or rights checks.

Future approved e-Stat setup must select an exact table, classifications, units and rights first. Keep `ESTAT_APP_ID` in the local environment. Do not put it in the catalogue, configuration JSON, source URLs saved to disk or logs. The implemented request path sanitizes failures and never copies a credentialed URL into a snapshot.

Failed adapters retain the last good snapshot and record failure separately. They do not report a failed request as “no observations,” overwrite a good snapshot, borrow another series or fill a missing value with zero.

## Offline fixtures and limits

`fixtures/` contains a separately labeled, independently invented dataset for offline regression checks. It is never a fallback for public observations. Request its `synthetic` data class explicitly when using that separate store.

The local API does not grant an assistant access to your PC or company systems. Import the public snapshot through a supported approved host route, or have an approved local client query the API. Public network deployment, authentication, company integrations and native work-account acceptance remain separate work.
