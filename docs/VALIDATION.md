# Validation record

Checked **2026-11-25**. This record describes the evidence obtained in the build environment. It does not claim installation in a company account or execution on the Windows work PC.

## Automated checks actually run

| Check | Observed result |
| --- | --- |
| Canonical skills and both generated editions | 24 source skills, 48 standalone ZIP packages; names, frontmatter, size and independent-resource rules passed |
| Deterministic build | 125 generated files reproduced; checked-in bytes and SHA-256 package manifests agree |
| Python tests | 37 tests passed with no skips in the tested environment |
| Optional libraries | DuckDB 2.0.1 and openpyxl 3.1.5 were available for their tests; Python 3.12.14 on Linux |
| CSV controls and reconciliation | Full synthetic populations, malformed records, duplicate grain, leading-zero keys, finite exact decimals, unmatched records and no-overwrite behavior checked |
| Quantity/rate/FX bridge | Known example reconciles exactly; supported numeric-extreme regression has zero residual |
| Workbook audit | Read-only input unchanged; formula caches, stored error, hidden sheet and a workbook without declared dimensions checked |
| DuckDB profile | CSV/Parquet controls; malformed rows cannot move the header; explicit dialect supports BOM/CRLF/quoted newline; key named `n` does not collide with aggregates |
| Edition copier | Preview, apply, repeat installation, customized-file preservation, checksum/source-change refusal and destination-link revalidation checked |
| Windows Git bytes | A real temporary Git checkout with `core.autocrlf=true` preserved hashed Markdown and ZIP bytes using `.gitattributes` |
| Upstream source acquisition | All four requested archive hashes verified; 16,165 archive blobs matched the pinned Git files with zero mismatches |
| Archive boundaries | Traversal, Windows names, case collisions, symlinks, size limits, checksums, existing files and non-execution behavior checked |
| Update checker | Rate limits and blocked document redirects were recorded as unavailable; pins stayed unchanged |
| Original GitHub publication | All 193 files published on the Somamill toolsuite finance branch matched their local Git blob hashes |

The test count includes 16 upstream-helper cases. Package validation does not prove that a model will follow every instruction. Optional tests intentionally skip when their dependencies are absent; inspect the run output before describing them as passed.

## Independent finance task checks

A fresh agent received only the relevant skill files and raw synthetic work requests. It quarantined overlapping mappings and an incomplete 95% allocation without normalizing or dropping the unresolved amount. Its bridge reconciled **320 source = −30 mapped + 350 unresolved**.

For working capital, it calculated an available **15-day** two-point-average DSO, declined to fabricate missing average balances, and separately identified a **21-day** group closing-balance proxy. A five-day improvement of **166.67 JPY-thousand** was labeled a modeled potential release, not received cash or a recurring monthly benefit.

An independent code review identified six edge issues. All six original reproductions were rerun after correction: CSV header inference, a key/count alias collision, unsized workbooks, a destination symlink introduced after preview, Git line endings and extreme decimal precision. Each reproduction now behaves as intended. Native Windows junction and OneDrive behavior were not exercised by those checks.

## Catalogue checks

The actual generated 24-entry catalogue passed DOM execution checks for edition-specific links, search, category selection, empty/reset behavior, focus restoration, example-prompt copy feedback with a mocked clipboard, theme persistence, unique IDs, visible control labels and malformed-data recovery. JavaScript syntax and SVG XML checks passed.

Impeccable's static detector returned no findings on the final product frontend files. Eight actual foreground/background token pairs passed 4.5:1; the lowest checked pair was 5.70:1. This is a token-pair check, not a complete accessibility certification.

Hallmark static review retained one finding in an unchanged vendored `.dot-button:disabled` rule. The catalogue does not use that class; product disabled states are explicitly overridden. Mixed light/dark token resolution and a numeric-selector match also required manual interpretation. These are documented detector limitations, not a claim of a clean full Hallmark pass.

**Desktop/mobile catalogue visual review is blocked in this environment.** Local Chromium failed before navigation with a socket-permission error. The cloud browser's URL policy rejected a local-file preview. No rendered catalogue screenshot or full browser-layout pass is claimed. The static catalogue can be reviewed locally using the Windows guide; it has not been deployed as a public website.

The original GitHub README on the Somamill toolsuite finance branch was separately inspected in a desktop browser after publication. Its dot banner, edition badges, navigation and introductory layout rendered correctly. That check covers the GitHub README, not the interactive catalogue or a mobile layout.

## Checks still requiring the target environment

- Native import, explicit skill invocation and a representative task in the actual approved Copilot/Gemini account.
- Windows 11 execution with the owner's installed Python version and approved packages.
- Office-created OneDrive folder behavior, syncing, Refresh and locked-file handling.
- Power BI model correctness and service refresh using the actual approved data/model.
- Real SharePoint permissions, source coverage and document versions.
- Desktop/mobile rendered catalogue inspection and any employer-template layout checks.

No original Claude-mem worker, HyperFrames renderer or paid Valyu integration was installed on the work PC. Source acquisition, repository design tooling, portable instruction adaptation and native account activation are recorded separately.

## Work-account migration

Prepared on **2026-11-25** for `mim1hat-prog/finance-skills`. The import uses
only the current tracked tree and starts its own history. Original source-pack
and dot design-kit provenance, licences and package content are preserved.
Destination publication and browser inspection remain pending until the
repository is created or made accessible through the work-account connection.
