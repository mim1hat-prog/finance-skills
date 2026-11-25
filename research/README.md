# Research and source registry

Generated from `research/sources.json`. Edit the registry, then run `python scripts/research_registry.py`.

Each entry identifies the exact skill, implementation decision or test it supports. A method reference is not proof of performance on a particular dataset. Normative standards, empirical research, provider documentation, software inspiration and project design choices are labeled separately.

This project uses a lightweight catalog informed by FAIR and DCAT. It does not claim full FAIR certification, DCAT conformance or registration of dataset DOIs.

## Maintenance

`python scripts/research_registry.py --check` validates IDs, exact use paths, declared test symbols, review states, rights decisions, pinned upstream consistency and this generated page without network access. Catalog `researchIds` must agree with the uses below.

`python scripts/research_registry.py --check-updates` is an optional read-only network review. It reads DOI metadata from Crossref and identifies publisher review links; failures remain unknown. No result automatically approves a source, updates a skill, refreshes an imported host or establishes that a paper has never been corrected or retracted.

The research maintainer reviews publisher notices, editions and licence terms. Record a correction, supersession, expression of concern or retraction with its affected uses. Unresolved notices and referenced retractions block release. A candidate is visible in this registry but cannot support an active skill or implementation. A reviewed link-only correction may retain the method with a written impact assessment. No upstream PDFs or full papers are included. Software licensing does not relicense upstream data.

## Source map

| ID | Evidence type | Review | Exact skills |
| --- | --- | --- | --- |
| [`agent-skills-spec`](#agent-skills-spec) | normative-standard | reviewed | Implementation / registry |
| [`alfred-realtime`](#alfred-realtime) | provider-documentation | reviewed | `benchmark-lookup`, `forecast-variance` |
| [`alfred-vintages`](#alfred-vintages) | provider-documentation | reviewed | `benchmark-lookup` |
| [`boj-cgpi`](#boj-cgpi) | provider-documentation | reviewed-with-limitations | `benchmark-lookup` |
| [`boj-terms`](#boj-terms) | data-license | reviewed-with-limitations | Implementation / registry |
| [`citation-file-format-1.2`](#citation-file-format-12) | normative-standard | reviewed | Implementation / registry |
| [`copilot-researcher`](#copilot-researcher) | provider-documentation | reviewed | `evidence-research`, `work-tool-routing` |
| [`copilot-skills`](#copilot-skills) | provider-documentation | reviewed | Implementation / registry |
| [`crossref-updates`](#crossref-updates) | metadata-guidance | reviewed | `evidence-research` |
| [`datacite-metadata`](#datacite-metadata) | metadata-guidance | reviewed | Implementation / registry |
| [`ecb-data-usage`](#ecb-data-usage) | data-license | reviewed | Implementation / registry |
| [`ecb-exr-api`](#ecb-exr-api) | provider-documentation | reviewed | `benchmark-lookup`, `fx-allocation-preflight` |
| [`estat-api`](#estat-api) | provider-documentation | reviewed-with-limitations | Implementation / registry |
| [`estat-terms`](#estat-terms) | data-license | reviewed | Implementation / registry |
| [`fair-principles`](#fair-principles) | empirical-research | reviewed | `benchmark-lookup`, `reproducible-analysis` |
| [`fpp-tscv`](#fpp-tscv) | method-guide | reviewed | `forecast-variance`, `reproducible-analysis`, `scenario-planning` |
| [`gemini-deep-research`](#gemini-deep-research) | provider-documentation | reviewed | `evidence-research`, `work-tool-routing` |
| [`gemini-skills`](#gemini-skills) | provider-documentation | reviewed | Implementation / registry |
| [`json-schema-2020-12`](#json-schema-2020-12) | normative-standard | reviewed | Implementation / registry |
| [`m4-competition`](#m4-competition) | empirical-research | needs-review | Candidate; no active use |
| [`meti-iip`](#meti-iip) | provider-documentation | reviewed-with-limitations | `benchmark-lookup`, `forecast-variance` |
| [`meti-terms`](#meti-terms) | data-license | reviewed-with-limitations | Implementation / registry |
| [`mhlw-monthly-labour`](#mhlw-monthly-labour) | provider-documentation | reviewed-with-limitations | `benchmark-lookup`, `workforce-reconciliation` |
| [`openapi-3.1`](#openapi-31) | normative-standard | reviewed | Implementation / registry |
| [`project-finance-design`](#project-finance-design) | project-design | reviewed | `close-controls`, `connected-reporting`, `evidence-research`, `excel-agent-core`, `fx-allocation-preflight`, `provision-reconciliation`, `workforce-reconciliation` |
| [`rfc9457`](#rfc9457) | normative-standard | reviewed | Implementation / registry |
| [`semantic-versioning-2.0.0`](#semantic-versioning-200) | normative-standard | reviewed | Implementation / registry |
| [`spdx-license-identifiers`](#spdx-license-identifiers) | normative-standard | reviewed | Implementation / registry |
| [`synthetic-fixtures`](#synthetic-fixtures) | project-design | reviewed | Implementation / registry |
| [`tool-fabric`](#tool-fabric) | provider-documentation | reviewed | `connected-reporting`, `power-bi-analysis` |
| [`tool-m365`](#tool-m365) | provider-documentation | reviewed | `sharepoint-evidence`, `work-tool-routing` |
| [`tool-planning-analytics`](#tool-planning-analytics) | provider-documentation | reviewed-with-limitations | `connected-reporting` |
| [`tool-planning-writeback`](#tool-planning-writeback) | provider-documentation | reviewed-with-limitations | `connected-reporting` |
| [`tool-power-bi`](#tool-power-bi) | provider-documentation | reviewed | `connected-reporting`, `power-bi-analysis` |
| [`tool-power-query`](#tool-power-query) | provider-documentation | reviewed | `excel-data-coverage`, `power-query-etl` |
| [`tool-sap-analysis`](#tool-sap-analysis) | provider-documentation | reviewed-with-limitations | `connected-reporting` |
| [`upstream-addy-agent-skills`](#upstream-addy-agent-skills) | software-reference | carried-forward | `account-mapping`, `business-document`, `project-context` |
| [`upstream-anthropic-skills`](#upstream-anthropic-skills) | software-reference | carried-forward | `business-document`, `cash-working-capital`, `excel-data-coverage`, `management-presentation`, `scenario-planning`, `spreadsheet-modeling` |
| [`upstream-claude-mem`](#upstream-claude-mem) | software-reference | carried-forward | `project-context` |
| [`upstream-d3-viz`](#upstream-d3-viz) | software-reference | carried-forward | `interactive-visualization` |
| [`upstream-diagram-design`](#upstream-diagram-design) | software-reference | carried-forward | `process-diagram` |
| [`upstream-dot-brand-kit`](#upstream-dot-brand-kit) | software-reference | carried-forward | Implementation / registry |
| [`upstream-duckdb-skills`](#upstream-duckdb-skills) | software-reference | carried-forward | `account-mapping`, `analytical-sql`, `power-query-etl` |
| [`upstream-ecc`](#upstream-ecc) | software-reference | carried-forward | `evidence-research` |
| [`upstream-hallmark`](#upstream-hallmark) | software-reference | carried-forward | `corporate-style`, `design-review` |
| [`upstream-hyperframes`](#upstream-hyperframes) | software-reference | carried-forward | `video-storyboard` |
| [`upstream-impeccable`](#upstream-impeccable) | software-reference | carried-forward | `design-review` |
| [`upstream-markitdown`](#upstream-markitdown) | software-reference | carried-forward | `document-extraction` |
| [`upstream-mattpocock-skills`](#upstream-mattpocock-skills) | software-reference | carried-forward | `project-context` |
| [`upstream-scientific-skills`](#upstream-scientific-skills) | software-reference | carried-forward | `forecast-variance`, `reproducible-analysis`, `scenario-planning`, `workforce-reconciliation` |
| [`upstream-superpowers`](#upstream-superpowers) | software-reference | carried-forward | `close-controls`, `excel-data-coverage`, `work-tool-routing` |
| [`upstream-valyu`](#upstream-valyu) | software-reference | carried-forward | `evidence-research`, `sharepoint-evidence` |
| [`w3c-dcat3`](#w3c-dcat3) | normative-standard | reviewed | `benchmark-lookup` |
| [`w3c-dwbp`](#w3c-dwbp) | normative-standard | reviewed | `benchmark-lookup`, `reproducible-analysis` |
| [`worldbank-data-terms`](#worldbank-data-terms) | data-license | reviewed | Implementation / registry |
| [`worldbank-pink-sheet`](#worldbank-pink-sheet) | provider-documentation | reviewed | `benchmark-lookup`, `scenario-planning` |

## agent-skills-spec

**[Agent Skills specification](https://agentskills.io/specification)**

Agent Skills maintainers; Agent Skills maintainers. Year: living documentation. Edition: Current format specification reviewed 25 November 2026.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Rights: [Publisher document terms; links and summaries only](https://agentskills.io/specification); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Agent Skills maintainers

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Validate SKILL.md names/descriptions and deterministic packages; keep large reference material outside the main instructions.
  **Supporting section:** Directory structure, required frontmatter, naming and progressive disclosure
  **Limits:** Format portability does not establish host availability, script execution permissions or unlimited context. This repository uses a deliberately narrow metadata profile.
  **Paths:** [`scripts/build.py`](../scripts/build.py), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md)
  **Tests:** `tests/test_build_install.py::PackagingTests.test_invalid_names_unbundled_resources_and_bom_fail`

## alfred-realtime

**[FRED API: Real-Time Periods](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html)**

Federal Reserve Bank of St. Louis; Federal Reserve Bank of St. Louis. Year: living documentation. Edition: Living API documentation accessed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Federal Reserve Bank of St. Louis

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Distinguish retrieval time and historical information availability; return as_of_unavailable without a captured vintage.
  **Supporting section:** Default current history versus a historical real-time period
  **Limits:** This is point-in-time design guidance. No FRED collector or universal reconstruction of other providers' past vintages is claimed.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/forecast-variance/SKILL.md`](../skills/forecast-variance/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_api.py`](../scripts/benchmark_api.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_after_cutoff_revision_never_uses_latest`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_as_of_response_excludes_refresh_results_after_cutoff`

## alfred-vintages

**[FRED API: fred/series/vintagedates](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html)**

Federal Reserve Bank of St. Louis; Federal Reserve Bank of St. Louis. Year: living documentation. Edition: Living API documentation accessed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://fred.stlouisfed.org/docs/api/fred/series_vintagedates.html); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Federal Reserve Bank of St. Louis

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Preserve previously captured observations instead of replacing history after a revision.
  **Supporting section:** Vintage dates and the distinction from all release dates
  **Limits:** A vintage date records a new or revised observation; no-change releases may be absent. Local snapshots do not create evidence for dates before collection.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_api.py`](../scripts/benchmark_api.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_after_cutoff_revision_never_uses_latest`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_outage_preserves_last_good_and_redacts_credentials`

## boj-cgpi

**[Bank of Japan: Corporate Goods Price Index (2020 base)](https://www.stat-search.boj.or.jp/ssi/mtshtml/pr01_m_1_en.html)**

Bank of Japan; Bank of Japan. Year: living documentation. Edition: Monthly CY2020=100 series; table reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Related primary sources: [https://www.stat-search.boj.or.jp/ssi/mtshtml/csv/pr01_m_1.csv](https://www.stat-search.boj.or.jp/ssi/mtshtml/csv/pr01_m_1.csv).

Rights: [Bank of Japan time-series website notice](https://www.stat-search.boj.or.jp/info/notice_en.html); checked 2026-11-25. Raw redistribution: `permission-required`; derived redistribution: `permission-required`.

Attribution: Source: Bank of Japan, Corporate Goods Price Index; exact series and period.

The official notice requires advance permission for commercial copying/reproduction and restricts alteration. Metadata and retrieval recipes only; no BOJ observations are bundled for work redistribution.

- **Use:** Identify PR01'PRCG20_2200000000 and PR01'PRCG20_2600000000 without confusing level indices with percentage-change columns.
  **Supporting section:** Domestic Producer Price Index and yen-basis Import Price Index, All commodities
  **Limits:** Metadata is verified; commercial redistribution permission is not established, and no BOJ numeric snapshot is shipped.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)

## boj-terms

**[Notice on the Bank of Japan Time-Series Data Search website](https://www.stat-search.boj.or.jp/info/notice_en.html)**

Bank of Japan; Bank of Japan. Year: living documentation. Edition: Current notice reviewed 25 November 2026.

Type: `data-license`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Bank of Japan time-series website notice](https://www.stat-search.boj.or.jp/info/notice_en.html); checked 2026-11-25. Raw redistribution: `permission-required`; derived redistribution: `permission-required`.

Attribution: Source: Bank of Japan, Corporate Goods Price Index; exact series and period.

The official notice requires advance permission for commercial copying/reproduction and restricts alteration. Metadata and retrieval recipes only; no BOJ observations are bundled for work redistribution.

- **Use:** Keep the BOJ adapter behind an explicit rights decision and publish metadata only by default.
  **Supporting section:** Copyright and permission for commercial use
  **Limits:** Public download access does not itself establish commercial redistribution rights.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_rights_gate_blocks_before_fetch`

## citation-file-format-1.2

**[Citation File Format: schema and guide](https://citation-file-format.github.io/)**

Citation File Format maintainers; Citation File Format maintainers. Year: living documentation. Edition: CFF 1.2.0.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

The official schema, guide and licence were retrieved through the GitHub plugin. The schema was inspected for required fields and entity authors; no invented personal author, DOI or institution is needed.

Related primary sources: [https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md](https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md); [https://github.com/citation-file-format/citation-file-format/blob/main/schema.json](https://github.com/citation-file-format/citation-file-format/blob/main/schema.json).

Rights: [CC BY 4.0 for the CFF specification](https://github.com/citation-file-format/citation-file-format/blob/main/LICENSE); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Citation File Format maintainers

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Provide machine-readable software citation metadata with the actual repository and release version.
  **Supporting section:** Required authors, cff-version, message and title; entity author, version, release date and repository metadata
  **Limits:** A CITATION.cff file does not register a DOI, create academic affiliation, certify research quality or imply peer review. The official CFF schema uses JSON Schema draft-07, distinct from the dataset contracts.
  **Paths:** [`CITATION.cff`](../CITATION.cff), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`CONTRIBUTING.md`](../CONTRIBUTING.md)

## copilot-researcher

**[Get started with Researcher in Microsoft Copilot](https://support.microsoft.com/en-us/microsoft-365-copilot/get-started-with-researcher-in-microsoft-365-copilot)**

Microsoft; Microsoft. Year: living documentation. Edition: Current Researcher guidance, reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Rights: [Publisher document terms; links and summaries only](https://support.microsoft.com/en-us/microsoft-365-copilot/get-started-with-researcher-in-microsoft-365-copilot); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Choose the available research workflow for complex source-backed questions, keep retrieval targeted, and verify cited support before concluding.
  **Supporting section:** Researcher versus standard chat, source scope, eligible subscriptions and administrator enablement
  **Limits:** Researcher availability and source access must be observed in the account. Instructions cannot force a reasoning mode, grant work-source permissions, remove quotas or ensure that every relevant record was retrieved.
  **Paths:** [`skills/work-tool-routing/SKILL.md`](../skills/work-tool-routing/SKILL.md), [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`docs/COPILOT.md`](../docs/COPILOT.md), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`adapters/workflow-controls.md`](../adapters/workflow-controls.md), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)

## copilot-skills

**[Create and edit skills with Copilot](https://support.microsoft.com/en-gb/microsoft-365-copilot/create-edit-skills-copilot)**

Microsoft; Microsoft. Year: living documentation. Edition: Current Copilot skill guidance, reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Related primary sources: [https://learn.microsoft.com/en-us/plugins/declarative-agent-skills](https://learn.microsoft.com/en-us/plugins/declarative-agent-skills).

Rights: [Publisher document terms; links and summaries only](https://support.microsoft.com/en-gb/microsoft-365-copilot/create-edit-skills-copilot); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Package individual native skills and document the available import/invocation route, with declarative-agent limits clearly scoped.
  **Supporting section:** Personal skill imports, invocation and Advanced Reasoning; separate declarative-agent support matrix
  **Limits:** Availability, licensing, preview runtime, network/package installation and admin controls are host-specific. A skill cannot override them or turn a personal skill package into a deployed agent.
  **Paths:** [`docs/COPILOT.md`](../docs/COPILOT.md), [`scripts/build.py`](../scripts/build.py), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)

## crossref-updates

**[Retraction Watch and Crossref metadata retrieval](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/)**

Crossref; Crossref. Year: living documentation. Edition: Current public metadata documentation.

Type: `metadata-guidance`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Related primary sources: [https://www.crossref.org/documentation/retrieve-metadata/rest-api/](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).

Rights: [Publisher document terms; metadata and summaries only](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Crossref

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Flag DOI metadata updates for publisher review; block unresolved or retracted sources still referenced by skills.
  **Supporting section:** Post-publication changes and Retraction Watch coverage
  **Limits:** Metadata can be incomplete and corrections are less comprehensive than retractions. No-update-reported is not proof of no correction or retraction.
  **Paths:** [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`research/sources.json`](../research/sources.json), [`scripts/research_registry.py`](../scripts/research_registry.py), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)
  **Tests:** `tests/test_research_registry.py::ResearchRegistryTests.test_retracted_source_blocks_release`, `tests/test_research_registry.py::ResearchRegistryTests.test_update_failure_is_unknown`

## datacite-metadata

**[DataCite Metadata Schema and versioning guidance](https://schema.datacite.org/)**

DataCite; DataCite. Year: 2026. Edition: Metadata Schema 4.7, released 3 March 2026.

Type: `metadata-guidance`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Related primary sources: [https://support.datacite.org/docs/versioning](https://support.datacite.org/docs/versioning).

Rights: [Publisher document terms; metadata and summaries only](https://schema.datacite.org/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: DataCite

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Keep stable source identifiers, editions, links to notices and distinct access/review dates in the canonical registry.
  **Supporting section:** Core citation properties; Version and RelatedIdentifier version relationships
  **Limits:** The project does not register DOIs or claim DataCite schema conformance; these are selected metadata design concepts.
  **Paths:** [`research/sources.json`](../research/sources.json), [`scripts/research_registry.py`](../scripts/research_registry.py)

## ecb-data-usage

**[Use of ECB statistics and other statistical information](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html)**

European Central Bank; European Central Bank. Year: living documentation. Edition: Current policy reviewed 25 November 2026.

Type: `data-license`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [ECB statistics reuse policy](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: ECB statistics; series identifier, period and retrieval/snapshot identifier.

Keep ECB observations and metadata unmodified. Label currency crosses separately as project calculations from ECB observations; do not imply ECB approval. Third-party series require their own rights check.

- **Use:** Gate publication of selected ECB observations and label separately derived calculations.
  **Supporting section:** Free reuse, attribution, unchanged statistics and third-party information
  **Limits:** The policy does not license third-party data merely because the ECB displays it.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_rights_gate_blocks_before_fetch`

## ecb-exr-api

**[ECB Data Portal API: data examples](https://data.ecb.europa.eu/help/api/data-examples)**

European Central Bank; European Central Bank. Year: living documentation. Edition: EXR daily reference rates; reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Official API examples and the official reference-rate page were reviewed. A normal keyless CSV request succeeded; the dataset records actual retrieval time.

Related primary sources: [https://data.ecb.europa.eu/help/api/data](https://data.ecb.europa.eu/help/api/data); [https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

Rights: [ECB statistics reuse policy](https://www.ecb.europa.eu/stats/ecb_statistics/governance_and_quality_framework/html/usage_policy.en.html); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: ECB statistics; series identifier, period and retrieval/snapshot identifier.

Keep ECB observations and metadata unmodified. Label currency crosses separately as project calculations from ECB observations; do not imply ECB approval. Third-party series require their own rights check.

- **Use:** Retrieve daily JPY, USD, CNY and THB per EUR as original series; retain provider keys and quote direction.
  **Supporting section:** EXR series keys, startPeriod/endPeriod, CSV output and updatedAfter
  **Limits:** Reference rates are public context, not approved planning or booked rates. updatedAfter is an update query, not a guarantee of complete historical vintages.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/fx-allocation-preflight/SKILL.md`](../skills/fx-allocation-preflight/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_reversed_fx_quote_is_rejected`

## estat-api

**[e-Stat API User Guide](https://www.e-stat.go.jp/api/api/api/index.php/en/api-info/api-guide)**

Statistics Bureau of Japan / National Statistics Center; Statistics Bureau of Japan / National Statistics Center. Year: living documentation. Edition: API 3.0 user guide and current service terms.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Related primary sources: [https://www.e-stat.go.jp/api/en/terms-of-use](https://www.e-stat.go.jp/api/en/terms-of-use); [https://api.e-stat.go.jp/swagger-ui/e-statapi3.0.html](https://api.e-stat.go.jp/swagger-ui/e-statapi3.0.html).

Rights: [e-Stat terms compatible with CC BY 4.0](https://www.e-stat.go.jp/en/terms-of-use); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: Monthly Labour Survey (Ministry of Health, Labour and Welfare), via e-Stat; identify processing.

Source attribution and edited-content labels required; third-party and API service terms remain separate. No exact wage/hour table has been enabled without verified table and category metadata.

- **Use:** Require a separately supplied application ID and verified statistical table/category metadata before enabling wage/hour retrieval.
  **Supporting section:** Application registration, application ID and statistical table metadata
  **Limits:** The API is credentialed. No application ID, exact MHLW table selection or successful credentialed request is supplied by this repository.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_credential_metadata_is_rejected`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_outage_preserves_last_good_and_redacts_credentials`

## estat-terms

**[e-Stat Terms of Use](https://www.e-stat.go.jp/en/terms-of-use)**

Statistics Bureau of Japan / National Statistics Center; Statistics Bureau of Japan / National Statistics Center. Year: living documentation. Edition: Government of Japan Standard Terms of Use 2.0, compatible with CC BY 4.0.

Type: `data-license`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [e-Stat terms compatible with CC BY 4.0](https://www.e-stat.go.jp/en/terms-of-use); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: Monthly Labour Survey (Ministry of Health, Labour and Welfare), via e-Stat; identify processing.

Source attribution and edited-content labels required; third-party and API service terms remain separate. No exact wage/hour table has been enabled without verified table and category metadata.

- **Use:** Record public-content reuse conditions separately from credentialed API access requirements.
  **Supporting section:** Source citation, edited content, third-party rights and API terms
  **Limits:** General content terms do not establish that all linked external data is covered or permit disclosure of an API application ID.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)

## fair-principles

**[The FAIR Guiding Principles for scientific data management and stewardship](https://www.nature.com/articles/sdata201618)**

Scientific Data; Mark D. Wilkinson et al.. Year: 2016. Edition: Scientific Data 3, 160018; 2019 addendum reviewed.

Type: `empirical-research`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

DOI: [10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18).

Related primary sources: [https://pmc.ncbi.nlm.nih.gov/articles/PMC4792175/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792175/); [https://www.nature.com/articles/s41597-019-0009-6](https://www.nature.com/articles/s41597-019-0009-6).

Rights: [CC BY 4.0 (article); metadata and summaries only](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792175/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Wilkinson et al. (2016), DOI 10.1038/sdata.2016.18.

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Use stable identifiers, machine-readable metadata, explicit provenance and reuse terms.
  **Supporting section:** Box 2, F1–F4 and R1–R1.3
  **Limits:** This is a lightweight local catalog, not a claim of full standards conformance or of fitness for a particular business decision.
  **Paths:** [`skills/reproducible-analysis/SKILL.md`](../skills/reproducible-analysis/SKILL.md), [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`research/sources.json`](../research/sources.json), [`scripts/research_registry.py`](../scripts/research_registry.py)

**Recorded addendum:** [https://www.nature.com/articles/s41597-019-0009-6](https://www.nature.com/articles/s41597-019-0009-6); reviewed 2026-11-25. Publisher addendum dated 19 March 2019 changes the maintained-principles URL. No change to the metadata and provenance principles used here; canonical publication and addendum links retained. Disposition: `reviewed-no-method-change`.

## fpp-tscv

**[Forecasting: Principles and Practice](https://otexts.com/fpp3/toolbox.html)**

OTexts; Rob J. Hyndman, George Athanasopoulos. Year: living documentation. Edition: Third edition; online book updated 20 November 2026.

Type: `method-guide`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://otexts.com/fpp3/toolbox.html); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: OTexts

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Compare proposed methods with simple baselines at rolling forecast origins and the intended horizon; keep future revisions outside training information.
  **Supporting section:** Chapter 5, simple methods, forecast accuracy and time-series cross-validation
  **Limits:** The source uses R examples. This project supplies method instructions, not a bundled forecasting engine or an assurance of improved accuracy.
  **Paths:** [`skills/forecast-variance/SKILL.md`](../skills/forecast-variance/SKILL.md), [`skills/scenario-planning/SKILL.md`](../skills/scenario-planning/SKILL.md), [`skills/reproducible-analysis/SKILL.md`](../skills/reproducible-analysis/SKILL.md)

## gemini-deep-research

**[Use Deep Research in Gemini Apps](https://support.google.com/gemini/answer/15719111?hl=en)**

Google; Google. Year: living documentation. Edition: Current Deep Research guidance, reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official Deep Research guidance and the Gems-to-skills transition FAQ were reviewed. The FAQ says skills do not yet work with Deep Research; no imported-skill execution inside that mode is claimed.

Related primary sources: [https://support.google.com/gemini/answer/18560919?hl=en](https://support.google.com/gemini/answer/18560919?hl=en).

Rights: [Publisher document terms; links and summaries only](https://support.google.com/gemini/answer/15719111?hl=en); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Google

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** When Deep Research is available, transfer a manual research brief into that separate mode, choose permitted sources, then bring cited findings back for independent verification.
  **Supporting section:** Source selection, research-plan editing, available models and daily/concurrent request limits
  **Limits:** Imported skills do not yet run inside Deep Research or Canvas. Google Search is included by default unless deselected; connected sources need enabled connections. Model choice, runtime and quotas remain host-controlled.
  **Paths:** [`skills/work-tool-routing/SKILL.md`](../skills/work-tool-routing/SKILL.md), [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`docs/GEMINI.md`](../docs/GEMINI.md), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`adapters/workflow-controls.md`](../adapters/workflow-controls.md), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)

## gemini-skills

**[Transfer skills from other platforms to Gemini Apps](https://support.google.com/gemini/answer/18977944?hl=en)**

Google; Google. Year: living documentation. Edition: Current skill import guidance and account rollout, reviewed 25 November 2026.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official import and transition guidance was reviewed. The transition FAQ explicitly says skills do not yet work with Canvas or Deep Research. Native skill availability and this interoperability limit must be rechecked for the actual work account.

Related primary sources: [https://support.google.com/gemini/answer/18560919?hl=en](https://support.google.com/gemini/answer/18560919?hl=en); [https://support.google.com/gemini/answer/17094296?hl=en](https://support.google.com/gemini/answer/17094296?hl=en).

Rights: [Publisher document terms; links and summaries only](https://support.google.com/gemini/answer/18977944?hl=en); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Google

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Provide individual cleaned skill packages and retain a Gems/instructions route where the work account has not received native skills.
  **Supporting section:** One-skill imports, root SKILL.md, supported packaging/files, script restrictions and Gems transition
  **Limits:** A bulk download is not a bulk import. Skills do not yet work inside Canvas or Deep Research, and skill scripts cannot make external requests. Personal-account rollout does not establish work-account availability.
  **Paths:** [`docs/GEMINI.md`](../docs/GEMINI.md), [`scripts/build.py`](../scripts/build.py), [`docs/STANDARDS.md`](../docs/STANDARDS.md), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)

## json-schema-2020-12

**[JSON Schema Draft 2020-12: Core and Validation](https://json-schema.org/draft/2020-12)**

JSON Schema project; Austin Wright, Henry Andrews, Ben Hutton, Greg Dennis. Year: 2022. Edition: 2020-12; revised specification published 16 June 2022.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Related primary sources: [https://json-schema.org/draft/2020-12/json-schema-core](https://json-schema.org/draft/2020-12/json-schema-core); [https://json-schema.org/draft/2020-12/json-schema-validation](https://json-schema.org/draft/2020-12/json-schema-validation).

Rights: [Publisher document terms; links and summaries only](https://json-schema.org/draft/2020-12); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: JSON Schema project

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Declare the dataset/API/workflow contracts and validate the documented keyword subset with explicit local reference resolution.
  **Supporting section:** Dialects, vocabularies, type/assertion keywords and format annotation versus assertion
  **Limits:** The standard-library checker is a strict project subset, not a general JSON Schema implementation. It rejects unsupported keywords and performs no network schema resolution.
  **Paths:** [`scripts/schema_validation.py`](../scripts/schema_validation.py), [`schemas/benchmark-catalog.schema.json`](../schemas/benchmark-catalog.schema.json), [`schemas/benchmark-snapshot.schema.json`](../schemas/benchmark-snapshot.schema.json), [`schemas/benchmark-api.schema.json`](../schemas/benchmark-api.schema.json), [`schemas/workflow-request.schema.json`](../schemas/workflow-request.schema.json), [`docs/STANDARDS.md`](../docs/STANDARDS.md)
  **Tests:** `tests/test_workflow_controls.py::SchemaSubsetTests.test_enforced_keywords_refs_formats_and_unknown_keyword_fail_closed`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_all_registered_openapi_routes_match_schema`

## m4-competition

**[The M4 Competition: 100,000 time series and 61 forecasting methods](https://pure.unic.ac.cy/en/publications/the-m4-competition-100000-time-series-and-61-forecasting-methods/)**

International Journal of Forecasting / University of Nicosia; Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos. Year: 2020. Edition: Volume 36, issue 1, pages 54–74.

Type: `empirical-research`. Review: `needs-review`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Original article metadata and abstract were verified through the publisher and author institution. Live Crossref metadata on 25 November 2026 links an erratum concerning missing competing-interest statements. Finding that title is not a completed impact review; direct notice/API requests returned 403.

**Candidate only — no active method support:** A publisher erratum linked by Crossref was detected, but its full text could not be retrieved. This paper is not active support for any skill or method until the notice is reviewed; FPP supports the current evaluation guidance.

Skills to reconsider after review: `forecast-variance`, `scenario-planning`, `reproducible-analysis`.

DOI: [10.1016/j.ijforecast.2019.04.014](https://doi.org/10.1016/j.ijforecast.2019.04.014).

Rights: [CC BY-NC-ND 4.0 (article); links and original summaries only](https://www.sciencedirect.com/science/article/pii/S0169207019301128); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: International Journal of Forecasting / University of Nicosia

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.


**Recorded correction:** [https://doi.org/10.1016/j.ijforecast.2021.01.013](https://doi.org/10.1016/j.ijforecast.2021.01.013); detected 2026-11-25; review incomplete. Publisher metadata identifies a missing-competing-interest-statements erratum that includes this paper. Full notice content is unavailable here; no claim about the declarations or methodological impact is made. Disposition: `needs-review`.

## meti-iip

**[Historical Data: Indices of Industrial Production, base 2020](https://www.meti.go.jp/english/statistics/tyo/iip/b2020_result-2.html)**

Ministry of Economy, Trade and Industry, Japan; Ministry of Economy, Trade and Industry, Japan. Year: living documentation. Edition: 2020-base original and seasonally adjusted monthly industry tables.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Official search-indexed landing page verified filenames b2020_gom1e.xlsx and b2020_gsm1e.xlsx and 2020 base. Fetch failure is retained as a verification gap; no URL path or series code was guessed.

Rights: [METI Public Data License 1.0 terms](https://www.meti.go.jp/english/other/terms_of_use.html); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: Ministry of Economy, Trade and Industry (METI), Indices of Industrial Production; indicate any processing.

Official indexed terms allow reuse with attribution and processing labels, with third-party exceptions. Exact monthly workbook and series selection remain pending; no real METI observations are bundled.

- **Use:** Prepare separate transport-equipment production series for original and seasonally adjusted context.
  **Supporting section:** Monthly by-industry original and seasonally adjusted indices
  **Limits:** Landing metadata is official-indexed, but direct retrieval returned 403 and exact workbook row/URL has not been verified. This is a configured adapter candidate, not a supported live series or a proxy for customer schedules.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/forecast-variance/SKILL.md`](../skills/forecast-variance/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)

## meti-terms

**[METI Website: Terms of Use](https://www.meti.go.jp/english/other/terms_of_use.html)**

Ministry of Economy, Trade and Industry, Japan; Ministry of Economy, Trade and Industry, Japan. Year: living documentation. Edition: Public Data License 1.0, official indexed terms.

Type: `data-license`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Official search-indexed terms reviewed; direct page retrieval returned 403. Recheck current provider terms when enabling an actual series.

Rights: [METI Public Data License 1.0 terms](https://www.meti.go.jp/english/other/terms_of_use.html); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: Ministry of Economy, Trade and Industry (METI), Indices of Industrial Production; indicate any processing.

Official indexed terms allow reuse with attribution and processing labels, with third-party exceptions. Exact monthly workbook and series selection remain pending; no real METI observations are bundled.

- **Use:** Record the conditions that must accompany an eventual verified METI snapshot.
  **Supporting section:** Source citation, edited-content labeling and third-party rights
  **Limits:** Rights metadata does not establish a successful fetch, a verified row selection or permission for third-party content.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)

## mhlw-monthly-labour

**[Monthly Labour Survey: national survey results](https://www.mhlw.go.jp/toukei/list/30-1a.html)**

Ministry of Health, Labour and Welfare, Japan; Ministry of Health, Labour and Welfare, Japan. Year: living documentation. Edition: Current survey publication index and revision notices.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [e-Stat terms compatible with CC BY 4.0](https://www.e-stat.go.jp/en/terms-of-use); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Source: Monthly Labour Survey (Ministry of Health, Labour and Welfare), via e-Stat; identify processing.

Source attribution and edited-content labels required; third-party and API service terms remain separate. No exact wage/hour table has been enabled without verified table and category metadata.

- **Use:** Use wage and hours publications as contextual candidates and retain revision/version metadata.
  **Supporting section:** Survey releases, corrected indices and seasonal-adjustment revisions
  **Limits:** Table IDs, employment coverage, industry, establishment-size classes and units must be verified before support. A public wage index cannot reconstruct internal job-grade costs.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/workforce-reconciliation/SKILL.md`](../skills/workforce-reconciliation/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)

## openapi-3.1

**[OpenAPI Specification](https://spec.openapis.org/oas/v3.1.2.html)**

OpenAPI Initiative; OpenAPI Initiative. Year: 2025. Edition: 3.1.2, 19 September 2025.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://spec.openapis.org/oas/v3.1.2.html); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: OpenAPI Initiative

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Describe bounded read-only routes, query parameters, responses and schemas in an inspectable API contract.
  **Supporting section:** Paths, Parameter Object, Responses Object and Schema Object
  **Limits:** Targets the requested 3.1 family; does not claim that 3.1.2 is the latest OpenAPI family or that the local service is publicly deployed.
  **Paths:** [`api/openapi.yaml`](../api/openapi.yaml), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`scripts/benchmark_api.py`](../scripts/benchmark_api.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_all_registered_openapi_routes_match_schema`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_api_contract_pagination_errors_and_no_provider_calls`

## project-finance-design

**[Finance Skills product and operating design](https://github.com/mim1hat-prog/finance-skills)**

Finance Skills maintainers; Finance Skills maintainers. Year: 2026. Edition: Repository product decisions, versioned with release.

Type: `project-design`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

A local design choice is linked to its actual implementation. No employer documents, identifiers, mappings or real cases were used as examples.

Rights: [Repository MIT licence; original project text](https://github.com/mim1hat-prog/finance-skills/blob/main/LICENSE); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Finance Skills maintainers.

Original project decisions are distinguished from external evidence; this software licence does not extend to upstream data.

- **Use:** Keep approved figures, workflow status and public context separate; preserve existing workbook logic and avoid unsolicited audit outputs.
  **Supporting section:** Operating boundaries and source priority
  **Limits:** This is an original project design decision, not a cited industry standard or evidence that a particular company uses these controls.
  **Paths:** [`skills/excel-agent-core/SKILL.md`](../skills/excel-agent-core/SKILL.md), [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`PRODUCT.md`](../PRODUCT.md), [`scripts/project_gates.py`](../scripts/project_gates.py), [`scripts/check_release.py`](../scripts/check_release.py), [`scripts/check_publication.py`](../scripts/check_publication.py), [`tools/publication-policy.json`](../tools/publication-policy.json)
  **Tests:** `tests/test_project_gates.py::ProjectGates.test_generated_skill_and_citation_drift_are_rejected_before_freeze`, `tests/test_project_gates.py::ProjectGates.test_unresolved_research_reference_prevents_release_gate`, `tests/test_publication_gate.py::PublicationGate.test_nested_native_packages_are_inspected_not_just_source`
- **Use:** Require supported granularity, explicit confirmation states, versioned assumptions and reconciled inputs before concluding completion.
  **Supporting section:** Validation and release decision boundaries
  **Limits:** Generic procedures and invented fixtures are not accounting policy, employer rules or proof of approval.
  **Paths:** [`skills/provision-reconciliation/SKILL.md`](../skills/provision-reconciliation/SKILL.md), [`skills/close-controls/SKILL.md`](../skills/close-controls/SKILL.md), [`skills/workforce-reconciliation/SKILL.md`](../skills/workforce-reconciliation/SKILL.md), [`skills/fx-allocation-preflight/SKILL.md`](../skills/fx-allocation-preflight/SKILL.md), [`PRODUCT.md`](../PRODUCT.md)
- **Use:** Document contribution checks, safe issue reporting and the evidence required before publication.
  **Supporting section:** Project maintenance and disclosure boundaries
  **Limits:** These are original project procedures, not a security certification, service-level agreement or claim that incidents are continuously monitored.
  **Paths:** [`CONTRIBUTING.md`](../CONTRIBUTING.md), [`SECURITY.md`](../SECURITY.md), [`docs/STANDARDS.md`](../docs/STANDARDS.md)
- **Use:** Continue targeted retrieval while material evidence gaps remain, independently recheck consequential results and checkpoint only useful sources, calculations and decisions.
  **Supporting section:** Bounded diligence, evidence sufficiency and independent verification
  **Limits:** These are original operating instructions. They cannot guarantee exhaustive retrieval, increase host context or runtime limits, override permissions, or justify repeated identical failed requests.
  **Paths:** [`skills/excel-agent-core/SKILL.md`](../skills/excel-agent-core/SKILL.md), [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`adapters/workflow-controls.md`](../adapters/workflow-controls.md), [`docs/RESEARCH-POLICY.md`](../docs/RESEARCH-POLICY.md)

## rfc9457

**[Problem Details for HTTP APIs](https://datatracker.ietf.org/doc/html/rfc9457)**

IETF; Mark Nottingham, Erik Wilde, Sanjay Dalal. Year: 2023. Edition: RFC 9457, July 2023.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://datatracker.ietf.org/doc/html/rfc9457); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: IETF

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Return application/problem+json failures with stable type, title, status and detail.
  **Supporting section:** Sections 3 and 3.1, problem JSON and extension members
  **Limits:** Problem details communicate failures; they do not establish upstream availability or authorization.
  **Paths:** [`api/openapi.yaml`](../api/openapi.yaml), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`scripts/benchmark_api.py`](../scripts/benchmark_api.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_api_contract_pagination_errors_and_no_provider_calls`

## semantic-versioning-2.0.0

**[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)**

Semantic Versioning project; Tom Preston-Werner. Year: living documentation. Edition: SemVer 2.0.0.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Rights: [CC BY 3.0 for the specification](https://creativecommons.org/licenses/by/3.0/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Semantic Versioning project

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Version documented skill/package/API contracts and preserve previously released archives unchanged.
  **Supporting section:** Rules 1–3 and 6–10: public API, version increments, immutable releases and metadata
  **Limits:** SemVer communicates compatibility intent; it is not proof that a change is compatible. The v prefix belongs to a Git tag, not the numeric version itself.
  **Paths:** [`catalog.json`](../catalog.json), [`scripts/release.py`](../scripts/release.py), [`docs/RELEASES.md`](../docs/RELEASES.md), [`docs/STANDARDS.md`](../docs/STANDARDS.md)
  **Tests:** `tests/test_release.py::ReleaseTests.test_semver_is_strict_and_index_sorts_numerically_preserving_older_versions`, `tests/test_release.py::ReleaseTests.test_source_notes_or_ref_change_cannot_rewrite_existing_version`

## spdx-license-identifiers

**[SPDX License List and short identifiers](https://spdx.org/licenses/)**

SPDX project; SPDX project. Year: 2026. Edition: License List 3.29.0, 16 September 2026.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and release maintainer.

Official primary documentation was reviewed for the stated implementation use. No certification or production deployment is claimed.

Related primary sources: [https://spdx.org/licenses/MIT.html](https://spdx.org/licenses/MIT.html); [https://spdx.org/licenses/Apache-2.0.html](https://spdx.org/licenses/Apache-2.0.html).

Rights: [Publisher document terms; links and summaries only](https://spdx.org/licenses/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: SPDX project

Only source links, factual metadata and original implementation summaries are included. No full specification or documentation is copied into this registry.

- **Use:** Use exact identifiers such as MIT and Apache-2.0 in software metadata while retaining the full applicable licence text and separate provider data terms.
  **Supporting section:** Standard short identifiers, canonical licence links and deprecated identifiers
  **Limits:** An SPDX identifier describes a licence; it does not grant new rights, establish compatibility or relicense upstream data and documents.
  **Paths:** [`LICENSE`](../LICENSE), [`CITATION.cff`](../CITATION.cff), [`upstream.lock.json`](../upstream.lock.json), [`docs/STANDARDS.md`](../docs/STANDARDS.md)

## synthetic-fixtures

**[Independently invented public-benchmark test fixtures](https://github.com/mim1hat-prog/finance-skills)**

Finance Skills maintainers; Finance Skills maintainers. Year: 2026. Edition: Fixture data versioned with this repository.

Type: `project-design`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Test and data maintainer.

These are deliberately invented observations and metadata for deterministic offline tests. They are not current market data, values from an employer, or reconstructed provider observations.

Rights: [MIT for original project fixtures](https://github.com/mim1hat-prog/finance-skills/blob/main/LICENSE); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Finance Skills maintainers; synthetic demonstration data.

Applies to the original test fixtures only; this repository licence does not relicense actual provider data.

- **Use:** Exercise revisions, outages, partial periods, rebasing, FX direction and rights failures without sending private content or requiring credentials.
  **Supporting section:** Offline fixture generation and failure-mode tests
  **Limits:** Synthetic observations are explicitly separate from the actual public dataset and never used as an unannounced fallback.
  **Paths:** [`tests/test_benchmarks.py`](../tests/test_benchmarks.py), [`benchmarks/README.md`](../benchmarks/README.md)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_after_cutoff_revision_never_uses_latest`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_partial_month_and_rebase_reject_changes`

## tool-fabric

**[Lineage in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/governance/lineage)**

Microsoft; Microsoft. Year: living documentation. Edition: Living Microsoft Fabric documentation.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher documentation was directly reviewed for the limited capabilities and constraints stated here. No tenant connection or software installation is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://learn.microsoft.com/en-us/fabric/governance/lineage); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Use available lineage as partial dependency evidence, including the limits of cross-workspace and manually constructed connections.
  **Supporting section:** Workspace lineage scope and limitations
  **Limits:** The view includes workspace items and one upstream level; cross-workspace downstream dependencies and some manual connections are not fully shown.
  **Paths:** [`skills/power-bi-analysis/SKILL.md`](../skills/power-bi-analysis/SKILL.md), [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-m365

**[Use connectors in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors)**

Microsoft; Microsoft. Year: living documentation. Edition: Living Copilot Studio documentation.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher documentation was directly reviewed for the limited capabilities and constraints stated here. No tenant connection or software installation is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-connectors); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Route a task through an actually enabled and authorized connection, and state when the host can only provide instructions.
  **Supporting section:** Connectors as actions and connection requirements
  **Limits:** A Microsoft 365 subscription or prompt import does not establish a Copilot Studio connector, authenticated access, a published agent or a working local API integration.
  **Paths:** [`skills/work-tool-routing/SKILL.md`](../skills/work-tool-routing/SKILL.md), [`skills/sharepoint-evidence/SKILL.md`](../skills/sharepoint-evidence/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-planning-analytics

**[Planning Analytics for Microsoft Excel report types](https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=types-planning-analytics-microsoft-excel-report)**

IBM; IBM. Year: living documentation. Edition: Planning Analytics documentation 3.1.0.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher text was reviewed through indexed primary-source results; direct page retrieval was blocked or exposed no readable content. No installed software version is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=types-planning-analytics-microsoft-excel-report); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: IBM

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Recognize connected Planning Analytics report areas before editing a workbook or interpreting formulas.
  **Supporting section:** Report types and managed report regions
  **Limits:** Product documentation describes capabilities, not the installed version, current connection, user permissions or a completed refresh.
  **Paths:** [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-planning-writeback

**[Automatically commit data in Planning Analytics for Microsoft Excel](https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=reports-automatically-commit-data)**

IBM; IBM. Year: living documentation. Edition: Planning Analytics documentation 2.1.0.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher text was reviewed through indexed primary-source results; direct page retrieval was blocked or exposed no readable content. No installed software version is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=reports-automatically-commit-data); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: IBM

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Check whether cell edits commit to the connected planning source before changing managed report cells.
  **Supporting section:** Automatic data commit and AutoWriteback mode
  **Limits:** The documented mode can commit upon Enter or leaving a cell; the project does not assume this setting is enabled, use it to authorize writes, or change a planning model.
  **Paths:** [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-power-bi

**[Data refresh in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data)**

Microsoft; Microsoft. Year: living documentation. Edition: Living Power BI documentation.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher documentation was directly reviewed for the limited capabilities and constraints stated here. No tenant connection or software installation is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Distinguish source-data updates, model refresh and the visuals currently displayed before explaining a result.
  **Supporting section:** Data, schema and visual refresh
  **Limits:** A refreshed visual or successful model refresh does not by itself prove every upstream business input is complete or approved.
  **Paths:** [`skills/power-bi-analysis/SKILL.md`](../skills/power-bi-analysis/SKILL.md), [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-power-query

**[Using data profiling tools in Power Query](https://learn.microsoft.com/en-us/power-query/data-profiling-tools)**

Microsoft; Microsoft. Year: living documentation. Edition: Living Power Query documentation.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher documentation was directly reviewed for the limited capabilities and constraints stated here. No tenant connection or software installation is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://learn.microsoft.com/en-us/power-query/data-profiling-tools); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: Microsoft

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Check profiling scope and inspect all relevant rows before claiming full-data quality.
  **Supporting section:** Column quality/distribution/profile and first-1000-row versus entire-dataset profiling
  **Limits:** Preview profiling over the first 1000 rows is not proof of complete dataset coverage, and changing a profile option is not an approval to refresh external sources.
  **Paths:** [`skills/power-query-etl/SKILL.md`](../skills/power-query-etl/SKILL.md), [`skills/excel-data-coverage/SKILL.md`](../skills/excel-data-coverage/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## tool-sap-analysis

**[Analysis for Microsoft Office: Information tab](https://help.sap.com/docs/SAP_BUSINESSOBJECTS_ANALYSIS_OFFICE/ca9c58444d64420d99d6c136a3207632/f26f9dfa6c9b1014bf2c9a7eb0e91070.html)**

SAP; SAP. Year: living documentation. Edition: Analysis for Microsoft Office official documentation.

Type: `provider-documentation`. Review: `reviewed-with-limitations`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Tool and research maintainer.

Official publisher text was reviewed through indexed primary-source results; direct page retrieval was blocked or exposed no readable content. No installed software version is inferred.

Rights: [Publisher document terms; metadata and summaries only](https://help.sap.com/docs/SAP_BUSINESSOBJECTS_ANALYSIS_OFFICE/ca9c58444d64420d99d6c136a3207632/f26f9dfa6c9b1014bf2c9a7eb0e91070.html); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: SAP

Public links and original summaries only; no documentation text, application binaries or customer information is redistributed.

- **Use:** Separate workbook/query refresh evidence from source-system update evidence and preserve filter context.
  **Supporting section:** Information tab: variables, filters, Last Refreshed At and Last Data Update
  **Limits:** An add-in capability does not prove that a connection, current variable set, backend data or all workbook ranges are complete.
  **Paths:** [`skills/connected-reporting/SKILL.md`](../skills/connected-reporting/SKILL.md), [`tools/catalog.json`](../tools/catalog.json), [`TOOLS.md`](../TOOLS.md)

## upstream-addy-agent-skills

**[addyosmani/agent-skills — pinned source review](https://github.com/addyosmani/agent-skills/tree/e997ac5b9a74eab332d5e9793bb38a38c8cfdd74)**

addyosmani; addyosmani. Year: living documentation. Edition: Commit e997ac5b9a74eab332d5e9793bb38a38c8cfdd74.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/addyosmani/agent-skills/tree/e997ac5b9a74eab332d5e9793bb38a38c8cfdd74); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: addyosmani/agent-skills

Existing pinned-source licence observation: MIT (previous pinned inspection, unchanged commit). Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Record the reason, source version and impact of material mapping or recurring-report decisions in a concise handoff.
  **Supporting section:** skills/documentation-and-adrs/SKILL.md
  **Limits:** No separate documentation system or unsolicited workbook audit sheet is created; the source does not establish employer policy.
  **Paths:** [`skills/business-document/SKILL.md`](../skills/business-document/SKILL.md), [`skills/project-context/SKILL.md`](../skills/project-context/SKILL.md), [`skills/account-mapping/SKILL.md`](../skills/account-mapping/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-anthropic-skills

**[anthropics/skills — pinned source review](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba)**

anthropics; anthropics. Year: living documentation. Edition: Commit e4bb5d960d87126ff3b3a8af1a104b7db67560ba.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Apache-2.0](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: anthropics/skills

Existing pinned-source licence observation: Apache-2.0 for inspected xlsx/docx/pdf/pptx folders; check individual folder notices for other skills. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Preserve spreadsheet formulas and source lineage, require recalculation evidence, and use concise document/presentation structures for finance output.
  **Supporting section:** skills/xlsx/SKILL.md
  **Limits:** Original portable procedures are provided; upstream spreadsheet/document runtimes and recalculation dependencies are not installed by importing a skill.
  **Paths:** [`skills/excel-data-coverage/SKILL.md`](../skills/excel-data-coverage/SKILL.md), [`skills/spreadsheet-modeling/SKILL.md`](../skills/spreadsheet-modeling/SKILL.md), [`skills/management-presentation/SKILL.md`](../skills/management-presentation/SKILL.md), [`skills/business-document/SKILL.md`](../skills/business-document/SKILL.md), [`skills/cash-working-capital/SKILL.md`](../skills/cash-working-capital/SKILL.md), [`skills/scenario-planning/SKILL.md`](../skills/scenario-planning/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-claude-mem

**[thedotmack/claude-mem — pinned source review](https://github.com/thedotmack/claude-mem/tree/4dc8e48cddee663edc3e401109f836d11f926a45)**

thedotmack; thedotmack. Year: living documentation. Edition: Commit 4dc8e48cddee663edc3e401109f836d11f926a45.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Apache-2.0](https://github.com/thedotmack/claude-mem/tree/4dc8e48cddee663edc3e401109f836d11f926a45); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: thedotmack/claude-mem

Existing pinned-source licence observation: Apache-2.0. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Keep concise project decisions, source pointers and next actions in an approved portable handoff.
  **Supporting section:** Pinned README and source metadata
  **Limits:** This is a procedural adaptation; there is no automatic memory worker, session recording, cloud sync or provider subscription.
  **Paths:** [`skills/project-context/SKILL.md`](../skills/project-context/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-d3-viz

**[chrisvoncsefalvay/claude-d3js-skill — pinned source review](https://github.com/chrisvoncsefalvay/claude-d3js-skill/tree/e198c87d03f1c9811acbff681886fac24baee53d)**

chrisvoncsefalvay; chrisvoncsefalvay. Year: living documentation. Edition: Commit e198c87d03f1c9811acbff681886fac24baee53d.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Redistribution permission unverified](https://github.com/chrisvoncsefalvay/claude-d3js-skill/tree/e198c87d03f1c9811acbff681886fac24baee53d); checked 2026-11-25. Raw redistribution: `unknown`; derived redistribution: `unknown`.

Attribution: chrisvoncsefalvay/claude-d3js-skill

Existing pinned-source licence observation: No licence file or licence frontmatter observed at inspected commit. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Design an interactive view only when filtering or comparison helps explain a finance result.
  **Supporting section:** SKILL.md
  **Limits:** The finance skill is independently authored; upstream text/code is not bundled because redistribution permission was not established.
  **Paths:** [`skills/interactive-visualization/SKILL.md`](../skills/interactive-visualization/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-diagram-design

**[cathrynlavery/diagram-design — pinned source review](https://github.com/cathrynlavery/diagram-design/tree/1acb8776bab34f5055399fbac96a693c8d5cf7b3)**

cathrynlavery; cathrynlavery. Year: living documentation. Edition: Commit 1acb8776bab34f5055399fbac96a693c8d5cf7b3.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/cathrynlavery/diagram-design/tree/1acb8776bab34f5055399fbac96a693c8d5cf7b3); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: cathrynlavery/diagram-design

Existing pinned-source licence observation: MIT. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Draw a clearly scoped reporting or close-process diagram from supplied steps and source relationships.
  **Supporting section:** skills/diagram-design/SKILL.md
  **Limits:** The diagram describes retrieved evidence; it cannot establish undocumented dependencies or prove a workflow has completed.
  **Paths:** [`skills/process-diagram/SKILL.md`](../skills/process-diagram/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-dot-brand-kit

**[Somamill/dot-brand-kit — pinned source review](https://github.com/Somamill/dot-brand-kit/tree/1bd44c0909747258cddd8f4110ff70684f6bb3e7)**

Somamill; Somamill. Year: living documentation. Edition: Commit 1bd44c0909747258cddd8f4110ff70684f6bb3e7.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/Somamill/dot-brand-kit/tree/1bd44c0909747258cddd8f4110ff70684f6bb3e7); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Somamill/dot-brand-kit

Existing pinned-source licence observation: MIT licence retained with the vendored foundation. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Retain the actual pinned dot. typography, spacing and visual foundation described in DESIGN.md.
  **Supporting section:** Pinned README and source metadata
  **Limits:** A changed upstream kit is a review candidate; it does not automatically replace project design decisions or an employer output template.
  **Paths:** [`upstream.lock.json`](../upstream.lock.json), [`DESIGN.md`](../DESIGN.md)

## upstream-duckdb-skills

**[duckdb/duckdb-skills — pinned source review](https://github.com/duckdb/duckdb-skills/tree/44dfbbb414e54187964a2212eae28495f6ae21d9)**

duckdb; duckdb. Year: living documentation. Edition: Commit 44dfbbb414e54187964a2212eae28495f6ae21d9.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/duckdb/duckdb-skills/tree/44dfbbb414e54187964a2212eae28495f6ae21d9); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: duckdb/duckdb-skills

Existing pinned-source licence observation: MIT. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Use typed local SQL, explicit grain and join/cardinality checks to validate large-file aggregations and mappings.
  **Supporting section:** skills/query/SKILL.md, skills/read-file/SKILL.md
  **Limits:** The capability depends on approved local packages and resources. No fixed dataset-size capacity, host support or automatic extension download is promised.
  **Paths:** [`skills/analytical-sql/SKILL.md`](../skills/analytical-sql/SKILL.md), [`skills/account-mapping/SKILL.md`](../skills/account-mapping/SKILL.md), [`skills/power-query-etl/SKILL.md`](../skills/power-query-etl/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-ecc

**[affaan-m/ECC — pinned source review](https://github.com/affaan-m/ECC/tree/4adeee6732a12d1540f49a4d50a38ce8c97f9a53)**

affaan-m; affaan-m. Year: living documentation. Edition: Commit 4adeee6732a12d1540f49a4d50a38ce8c97f9a53.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/affaan-m/ECC/tree/4adeee6732a12d1540f49a4d50a38ce8c97f9a53); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: affaan-m/ECC

Existing pinned-source licence observation: MIT (previous pinned inspection, unchanged commit). Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Compare primary-source evidence before writing a market-driver research briefing.
  **Supporting section:** skills/market-research/SKILL.md
  **Limits:** No Firecrawl/Exa dependency or external upload of work context is implied; a bibliography alone does not prove a causal claim.
  **Paths:** [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-hallmark

**[Nutlope/hallmark — pinned source review](https://github.com/Nutlope/hallmark/tree/04977e15f3dfd6ee4b74c887dac3eb52665d6c92)**

Nutlope; Nutlope. Year: living documentation. Edition: Commit 04977e15f3dfd6ee4b74c887dac3eb52665d6c92.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/Nutlope/hallmark/tree/04977e15f3dfd6ee4b74c887dac3eb52665d6c92); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: Nutlope/hallmark

Existing pinned-source licence observation: MIT. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Apply layout, legibility and visual-consistency review to repository and work-output design.
  **Supporting section:** skills/hallmark/SKILL.md
  **Limits:** The project design kit and employer template remain authoritative; an upstream coding-host skill does not provide a Microsoft 365 or Gemini runtime.
  **Paths:** [`skills/design-review/SKILL.md`](../skills/design-review/SKILL.md), [`skills/corporate-style/SKILL.md`](../skills/corporate-style/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-hyperframes

**[heygen-com/hyperframes — pinned source review](https://github.com/heygen-com/hyperframes/tree/c890cb38f0d0786831c99ab515587f5750185cb8)**

heygen-com; heygen-com. Year: living documentation. Edition: Commit c890cb38f0d0786831c99ab515587f5750185cb8.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Apache-2.0](https://github.com/heygen-com/hyperframes/tree/c890cb38f0d0786831c99ab515587f5750185cb8); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: heygen-com/hyperframes

Existing pinned-source licence observation: Apache-2.0. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Plan a finance explainer as a sequenced storyboard with explicit figures, narration and review points.
  **Supporting section:** skills/hyperframes/SKILL.md
  **Limits:** Native editions contain a storyboard procedure, not an installed video renderer or a claim that a Copilot/Gemini subscription supplies rendering.
  **Paths:** [`skills/video-storyboard/SKILL.md`](../skills/video-storyboard/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-impeccable

**[pbakaus/impeccable — pinned source review](https://github.com/pbakaus/impeccable/tree/b49177d32788f2dc585c42831d845dacf1ebed2c)**

pbakaus; pbakaus. Year: living documentation. Edition: Commit b49177d32788f2dc585c42831d845dacf1ebed2c.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Apache-2.0](https://github.com/pbakaus/impeccable/tree/b49177d32788f2dc585c42831d845dacf1ebed2c); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: pbakaus/impeccable

Existing pinned-source licence observation: Apache-2.0. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Review the repository interface for clear hierarchy, accessible reading and consistent interactions.
  **Supporting section:** skill/SKILL.src.md, .github/skills/impeccable/SKILL.md, .agents/skills/impeccable/SKILL.md
  **Limits:** Project DESIGN.md takes priority. Source review does not mean the optional design engine is installed on a work PC.
  **Paths:** [`skills/design-review/SKILL.md`](../skills/design-review/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-markitdown

**[microsoft/markitdown — pinned source review](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e)**

microsoft; microsoft. Year: living documentation. Edition: Commit ed178952a6672abdfd35b5f9e76a80b6cefc086e.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: microsoft/markitdown

Existing pinned-source licence observation: MIT. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Check extraction coverage and source/page/table references before using converted document content in analysis.
  **Supporting section:** Pinned README and source metadata
  **Limits:** Conversion alone does not prove OCR accuracy or preserve every spreadsheet formula and layout feature; no cloud conversion is enabled by these instructions.
  **Paths:** [`skills/document-extraction/SKILL.md`](../skills/document-extraction/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-mattpocock-skills

**[mattpocock/skills — pinned source review](https://github.com/mattpocock/skills/tree/d65391149dbb5fe76478e76fa8d5122b2aa5a70e)**

mattpocock; mattpocock. Year: living documentation. Edition: Commit d65391149dbb5fe76478e76fa8d5122b2aa5a70e.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/mattpocock/skills/tree/d65391149dbb5fe76478e76fa8d5122b2aa5a70e); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: mattpocock/skills

Existing pinned-source licence observation: MIT (previous pinned inspection, unchanged commit). Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Compress the current goal, verified state and next action into a portable project handoff.
  **Supporting section:** skills/productivity/handoff/SKILL.md
  **Limits:** A handoff preserves useful context but is not a durable background memory service.
  **Paths:** [`skills/project-context/SKILL.md`](../skills/project-context/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-scientific-skills

**[K-Dense-AI/scientific-agent-skills — pinned source review](https://github.com/K-Dense-AI/scientific-agent-skills/tree/c21d13b3cc2894680229ba9959a53281acb9200e)**

K-Dense-AI; K-Dense-AI. Year: living documentation. Edition: Commit c21d13b3cc2894680229ba9959a53281acb9200e.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/K-Dense-AI/scientific-agent-skills/tree/c21d13b3cc2894680229ba9959a53281acb9200e); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: K-Dense-AI/scientific-agent-skills

Existing pinned-source licence observation: MIT root and inspected modules; individual dependencies can differ. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Retain reproducible inputs, explicit assumptions and sensitivity/validation reasoning in quantitative finance workflows.
  **Supporting section:** skills/statistical-analysis/SKILL.md, skills/exploratory-data-analysis/SKILL.md, skills/scientific-critical-thinking/SKILL.md, skills/database-lookup/SKILL.md
  **Limits:** Selected methodological inspiration is used, not the full scientific skill collection, an installed environment or proof that a model fits business data.
  **Paths:** [`skills/reproducible-analysis/SKILL.md`](../skills/reproducible-analysis/SKILL.md), [`skills/scenario-planning/SKILL.md`](../skills/scenario-planning/SKILL.md), [`skills/workforce-reconciliation/SKILL.md`](../skills/workforce-reconciliation/SKILL.md), [`skills/forecast-variance/SKILL.md`](../skills/forecast-variance/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-superpowers

**[obra/superpowers — pinned source review](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7)**

obra; obra. Year: living documentation. Edition: Commit 22f0b463e7a5e579904dd6211a520321035526f7.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [MIT](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: obra/superpowers

Existing pinned-source licence observation: MIT (previous pinned inspection, unchanged commit). Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Require fresh checks of the actual result before declaring a reporting or workbook task complete.
  **Supporting section:** skills/verification-before-completion/SKILL.md
  **Limits:** The finance adaptation is a verification procedure, not a coding harness or an approval mechanism.
  **Paths:** [`skills/work-tool-routing/SKILL.md`](../skills/work-tool-routing/SKILL.md), [`skills/close-controls/SKILL.md`](../skills/close-controls/SKILL.md), [`skills/excel-data-coverage/SKILL.md`](../skills/excel-data-coverage/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## upstream-valyu

**[valyuAI/skills — pinned source review](https://github.com/valyuAI/skills/tree/be57c51696fa74a0fce129e3dc165c93c599a0c9)**

valyuAI; valyuAI. Year: living documentation. Edition: Commit be57c51696fa74a0fce129e3dc165c93c599a0c9.

Type: `software-reference`. Review: `carried-forward`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Provenance carried forward from the existing upstream.lock.json review dated 2026-11-25. Not represented as a new independent source-content audit by this registry update.

Rights: [Redistribution permission unverified](https://github.com/valyuAI/skills/tree/be57c51696fa74a0fce129e3dc165c93c599a0c9); checked 2026-11-25. Raw redistribution: `unknown`; derived redistribution: `unknown`.

Attribution: valyuAI/skills

Existing pinned-source licence observation: MIT declared in skill frontmatter/README; no root license file observed. Only links and independently authored procedural adaptations are included here; this registry does not bundle upstream code or wording.

- **Use:** Collect source-backed claims, compare evidence quality and retain useful references for a finance research answer.
  **Supporting section:** valyu-search/valyu-best-practices/SKILL.md
  **Limits:** Independent instructions do not call the Valyu service or redistribute its skill text; source licence permission remains unresolved.
  **Paths:** [`skills/evidence-research/SKILL.md`](../skills/evidence-research/SKILL.md), [`skills/sharepoint-evidence/SKILL.md`](../skills/sharepoint-evidence/SKILL.md), [`upstream.lock.json`](../upstream.lock.json)

## w3c-dcat3

**[Data Catalog Vocabulary (DCAT) — Version 3](https://www.w3.org/TR/2024/REC-vocab-dcat-3-20240822/)**

W3C; W3C. Year: 2024. Edition: W3C Recommendation, 22 August 2024.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://www.w3.org/TR/2024/REC-vocab-dcat-3-20240822/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: W3C

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Keep dataset discovery, distribution files, API access and snapshot versions distinguishable.
  **Supporting section:** Dataset, Distribution, Data Service and dataset versioning
  **Limits:** This is a lightweight local catalog, not a claim of full standards conformance or of fitness for a particular business decision.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json)

## w3c-dwbp

**[Data on the Web Best Practices](https://www.w3.org/TR/dwbp/)**

W3C; W3C. Year: 2017. Edition: W3C Recommendation, 31 January 2017.

Type: `normative-standard`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Rights: [Publisher document terms; metadata and summaries only](https://www.w3.org/TR/dwbp/); checked 2026-11-25. Raw redistribution: `not-applicable`; derived redistribution: `not-applicable`.

Attribution: W3C

Only links, bibliographic metadata and original summaries are included; no source document is redistributed.

- **Use:** Record series identifiers, units, provenance, licensing and immutable snapshot versions.
  **Supporting section:** Best Practices 1–8: metadata, licences, provenance, quality and versions
  **Limits:** This is a lightweight local catalog, not a claim of full standards conformance or of fitness for a particular business decision.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/reproducible-analysis/SKILL.md`](../skills/reproducible-analysis/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_partial_month_and_rebase_reject_changes`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_retrieval_time_follows_completed_fetch_or_import_not_request_start`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_public_origin_cannot_bypass_frozen_series_kind`

## worldbank-data-terms

**[World Bank Terms of Use for Datasets](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets)**

World Bank; World Bank. Year: living documentation. Edition: Current terms and dataset catalog 0038238 reviewed 25 November 2026.

Type: `data-license`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Primary publisher material was checked on the access date. Scope is limited to the stated uses.

Related primary sources: [https://datacatalog.worldbank.org/search/dataset/0038238/commodity-prices-history-and-projections](https://datacatalog.worldbank.org/search/dataset/0038238/commodity-prices-history-and-projections); [https://datacatalog.worldbank.org/public-licenses](https://datacatalog.worldbank.org/public-licenses); [https://reproducibility.worldbank.org/catalog/377](https://reproducibility.worldbank.org/catalog/377).

Rights: [CC BY 4.0 with World Bank additional dataset terms](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: The World Bank: Commodity Prices - History and Projections (Pink Sheet): underlying providers identified in the workbook Description; series and snapshot.

The dataset-specific catalog lists CC BY 4.0. Selected workbook descriptions contain provider attribution and no contrary selected-series licence notice. Keep those credits and the terms URL, label transformations, and recheck future metadata exceptions. No raw workbook or PDF is bundled.

- **Use:** Permit the selected Pink Sheet observations with dataset-specific attribution and maintain a per-series rights gate.
  **Supporting section:** Licenses, attribution and exceptions for some third-party data
  **Limits:** The decision covers the reviewed selected dataset. It does not license all World Bank-hosted material or unpublished third-party series.
  **Paths:** [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
  **Tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_rights_gate_blocks_before_fetch`

## worldbank-pink-sheet

**[Commodity Markets: World Bank Pink Sheet](https://www.worldbank.org/en/research/commodity-markets)**

World Bank Prospects Group; World Bank Prospects Group. Year: 2026. Edition: November 2026 release; historical monthly workbook.

Type: `provider-documentation`. Review: `reviewed`. Accessed: 2026-11-25; last reviewed: 2026-11-25. Maintainer: Research and data maintainer.

Official monthly XLSX was retrieved and exact labels/units checked against the official November publication. The selected numeric rows are independently normalized; original worksheet and publisher metadata are not mirrored.

Related primary sources: [https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx).

Rights: [CC BY 4.0 with World Bank additional dataset terms](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets); checked 2026-11-25. Raw redistribution: `allowed-with-conditions`; derived redistribution: `allowed-with-conditions`.

Attribution: The World Bank: Commodity Prices - History and Projections (Pink Sheet): underlying providers identified in the workbook Description; series and snapshot.

The dataset-specific catalog lists CC BY 4.0. Selected workbook descriptions contain provider attribution and no contrary selected-series licence notice. Keep those credits and the terms URL, label transformations, and recheck future metadata exceptions. No raw workbook or PDF is bundled.

- **Use:** Provide aluminium/copper in USD per metric ton, Brent in USD per barrel and Japan LNG in USD per MMBtu; keep currency conversions separate.
  **Supporting section:** Monthly Prices and Description worksheets: Aluminum, Copper, Crude oil Brent, Natural Gas Japan
  **Limits:** Commodity benchmarks are context for sensitivity, not supplier contract prices or plant tariffs. Observed current history does not reconstruct past publication vintages.
  **Paths:** [`skills/benchmark-lookup/SKILL.md`](../skills/benchmark-lookup/SKILL.md), [`skills/scenario-planning/SKILL.md`](../skills/scenario-planning/SKILL.md), [`scripts/benchmark_data.py`](../scripts/benchmark_data.py), [`benchmarks/catalog.json`](../benchmarks/catalog.json), [`scripts/benchmark_collect.py`](../scripts/benchmark_collect.py)
