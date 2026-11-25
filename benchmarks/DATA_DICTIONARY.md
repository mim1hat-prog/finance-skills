# Public benchmark data dictionary

This dataset is the **public-benchmark** stream. Approved internal figures and internal workflow status belong in their approved systems and separate contracts. A public observation does not establish an internal driver, an approved assumption, a booked rate, a complete reporting input or a submission status.

## Catalogue

`catalog.json` is the authoritative series inventory. Each series has a stable project `id`, exact `provider_series_id` when verified, `source_id` in the research registry, original provider/source URL, geography, frequency, unit, currency or index base, seasonal adjustment, access mode, adapter and actual validation status. A null provider series ID means configuration is incomplete; the collector must not invent one.

`rights` records the terms URL, license, attribution, check date, selected-series limitations and whether redistribution is permitted. This repository's software license does not license provider data. BOJ values are not mirrored because its time-series notice requires advance permission for commercial copying. MHLW candidates do not become usable merely because an e-Stat application ID exists.

`freshness_days` is an explicit public-dataset age policy measured from the last observation period end. It is not a company close deadline or materiality threshold. The configured daily and monthly defaults can be reviewed separately; `within-policy` means only that the recorded age is within that limit.

## Immutable snapshots

Each `snapshots/<id>/` directory contains:

- `snapshot.json`: frozen series metadata, observations, coverage, retrieval time and capture method.
- `observations.csv`: a deterministic tabular representation of the same observations; structured input references and transformations are JSON cells.
- `manifest.json`: exact file sizes and SHA-256 checksums for both representations.

A new retrieval creates a new snapshot. An existing ID cannot be replaced with changed bytes. The API validates the schemas, inventory, checksums and JSON/CSV agreement before serving it. These checks establish consistency, not a digital signature or independent provider certification.

`data_class` distinguishes actual verified public observations from independently invented synthetic fixtures. They cannot be mixed in one snapshot. Public queries never fall back to synthetic data.

`retrieved_at` records completion of source-byte acquisition by this collector/import operation, including a timezone. The request start is not treated as availability evidence. `knowledge_basis` is `retrieval-time`. `capture_method` identifies the adapter or verified retrieval and the source-content SHA-256 where available. No raw provider workbook, unrelated tab or PDF is included in this dataset.

## Observation fields

| Field | Meaning |
| --- | --- |
| `series_id`, `provider`, `provider_series_id` | Stable project ID, publishing provider and exact upstream series/column identifier |
| `source_id`, `source_url` | Research-registry source and credential-free public locator |
| `observation_period` | Provider period: `YYYY-MM-DD` for daily or `YYYY-MM` for monthly data |
| `period_start`, `period_end` | Calendar bounds for complete periods; a partial record ends at its explicit observed-through date. Monthly values are never silently prorated |
| `value` | Finite decimal string preserving source precision; missing values are not replaced with zero |
| `unit`, `currency`, `index_base` | Exact interpretation; an index base is distinct from a price currency |
| `geography`, `frequency`, `seasonal_adjustment` | Coverage and series convention; original and seasonally adjusted data remain separate |
| `release_date` | Provider's publication/update date when explicitly available; otherwise null |
| `release_at` | Exact publication timestamp only when supplied and verified; no midnight time is invented from a date |
| `retrieved_at`, `snapshot_id` | Retrieval evidence and immutable retained vintage |
| `origin` | `original`, separately labeled project `derived`, or `synthetic` |
| `period_completeness` | `complete`, `partial` or `unknown`; partial/unknown periods cannot pass the complete-period change calculation |
| `observation_status` | Published, provisional, revised or synthetic; this does not assert that history will never be revised |
| `inputs`, `transformation` | Derived input series/period/snapshot references plus formula and transformation version |

ECB original quotes are currency units **per EUR**. The separate project JPY crosses divide JPY per EUR by USD/CNY/THB per EUR for the same complete date and snapshot. They are not ECB published cross quotes. The calculation uses 40-digit Decimal precision and retains its two original inputs.

Pink Sheet observations remain nominal **USD** prices in their published units. No automatic JPY conversion is stored. A future conversion must record its chosen FX period, quote and aggregation basis separately so commodity movement and FX are not counted twice.

## Cutoff, revision and freshness semantics

`snapshot_id` selects exact retained bytes. `as_of` selects a matching retained snapshot whose retrieval timestamp is no later than the requested cutoff. A release date or observation period does not establish that today's revised values were known at an earlier cutoff. If no such retained snapshot exists, the API returns **`as_of_unavailable`**. It never substitutes the latest history.

Refresh receipts use `attempted_at` for the time the completed outcome was recorded. An `as_of` query includes only a receipt recorded by that cutoff, or null when none was retained. A later success or outage cannot become historical evidence. Freshness remains a present-time age assessment and does not alter the frozen observations or their availability timestamp.

Without either selector, the result is labeled **`latest-available`**. The response contains the selected frozen definition, retrieval time, freshness age and last refresh status. An old snapshot remains old even if the server is running today.

`coverage` describes actual retained observations, not completeness of every business day or month. A successful source response with missing selected series is rejected. An empty selected result is distinct from a failed fetch. A failed refresh leaves every good snapshot unchanged and records a sanitized failure receipt separately under `refresh-status/`; it cannot silently switch to another source or series.

## Validation scope

The project uses a documented subset of JSON Schema for its own schemas and checks that unsupported validation keywords fail closed. It does not claim general JSON Schema, full OpenAPI tooling or DCAT conformance. The OpenAPI document is JSON syntax in `api/openapi.yaml`, which is valid YAML. Both dispatcher responses and stored snapshots are checked against the same on-disk schema definitions.
