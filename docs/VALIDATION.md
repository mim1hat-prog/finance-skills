# Validation record

Checked **2026-11-25**. This record describes the evidence obtained in the build environment. It does not claim installation in a company account or execution on the Windows work PC.

## Current release: v1.3.0

The Markdown-only download contains **60 `.md` files**: 29 complete Copilot instruction bodies, 29 complete Gemini bodies, the canonical Excel agent profile and a start guide. The 310,404-byte archive has no YAML frontmatter, scripts, datasets, JSON members or nested ZIPs. Every skill body matched its generated edition after removing only the YAML header and normalizing the final newline. The external inventory matched all file sizes and SHA-256 hashes; repeated builds produced identical bytes.

The integrated offline gate ran **130 Python tests with zero skips**, including the focused Markdown packaging test and three new release compatibility cases. The current build has **160 deterministic generated files**. Tests exercised a transition from legacy four-archive releases to the new five-archive format, preserving earlier bytes and modification times; unknown schema versions, incorrect inventories and unsupported feature flags were rejected. Existing v1.1.0 and v1.2.0 snapshots passed their integrity checks.

Canonical finance instructions, research records and benchmark observations were unchanged. The gate revalidated the existing dataset/API, research references, workflow contracts and nested publication inventory with no publication findings, including the separate private marker policy. This packaging check does not establish import, activation or a task result in Copilot/Gemini. The source-review dates retain their existing meaning; no new upstream review is claimed.

## Previous release: v1.2.0

The current library contains **29 canonical skills, 58 individual native ZIPs and 158 deterministic generated files**, including the Excel Instructions profile, three transport bundles, tool inventory, workflow contracts and citation metadata. All generated files matched their sources. The largest native instruction file was 15,746 bytes, within the project's portable ceiling.

The integrated offline gate ran **126 Python tests with zero skips**. The environment had Python 3.12.14, openpyxl 3.1.5 and DuckDB 2.0.1; optional dependency tests actually executed. The release helper's isolated CLI test was updated to copy its new local catalogue dependency, then passed. No provider calls or enterprise actions run as part of this gate.

- **Workflow controls:** 21 focused tests passed. An independent reviewer reran all original reproductions after corrections. Duplicate explanations, blank evidence/owners, invalid timestamp offsets, changed artifact scale/sign, mismatched allocation receivers and prior-run evidence for a different target or payload now block or reject. Valid controls remain valid. A separate synthetic skill task retained an unexplained reserve difference of 50 after two approved components explained 320 of a 370 difference; the newer unsubmitted draft did not replace the submitted baseline.
- **Benchmarks:** 20 focused tests passed. Independent reproductions confirmed that a request starting before cutoff cannot make later-arriving bytes available early, a later refresh receipt cannot leak into historical status, and relabeling a derived series cannot bypass formula/input checks. Additional checks cover mixed timezone offsets, strict timestamp rejection, partial months, index rebases, reversed FX, outages, rights and credential redaction.
- **Dataset and API:** 17 catalogue series, two real public snapshots and two separate synthetic vintages passed schema, CSV, inventory and hash checks. The real snapshots contain 119 ECB rows and 48 World Bank rows. Replaying parsers against the saved public source bytes reproduced the complete snapshots and identical IDs. Seed validation receipts record the later offline validation time, separately from source acquisition. All four OpenAPI routes passed response validation; a real loopback GET/POST check passed and the server stopped.
- **Research and standards:** 56 registry records map to 29 skills, with no unresolved reference errors. All 23 registry tests passed. The M4 paper remains an inactive candidate while its erratum requires review. BOJ and selected upstream redistribution restrictions remain explicit. `CITATION.cff` passed an independent check against the official CFF 1.2.0 draft-07 schema; data/workflow schemas use 2020-12 separately.
- **Publication boundary:** the public inventory and nested packages passed the heuristic scan, including an additional private marker policy stored outside the project. The one exception is bound to the exact hash of an already published synthetic invalid-URL test; it cannot exempt another file, changed bytes, private links or other finding categories. The previous v1.1.0 release files passed their integrity checks and remain unchanged.
- **Catalogue behavior:** DOM checks passed for the actual 29-entry v1.2.0 data, edition routing, search/filter/reset, example-copy feedback, theme state, fallbacks and version-derived download links. This does not establish browser layout. Presentation code and dot assets were retained; native desktop/mobile rendering remains unverified in this environment.

`scripts/check_release.py` is the offline pre-release command. After freezing, `--require-release` additionally requires exact current release bytes and indexes. The full ZIP deliberately excludes nested release history and can run the default gate independently. Remote publication is verified separately from this local record; a GitHub Release object or native account installation is not implied.

## Historical evidence: v1.1.0 and earlier

The following results describe prior published versions. Their original counts and limitations are retained for traceability.

### Automated checks actually run

| Check | Observed result |
| --- | --- |
| Canonical skills and both generated editions | 25 source skills, 50 standalone ZIP packages; names, frontmatter, size and independent-resource rules passed |
| Deterministic build | 135 generated files reproduced; generated bytes and SHA-256 package manifests agree |
| Python tests | 48 tests passed with no skips in the tested environment |
| Excel agent profile | Plain text derives exactly from the canonical skill body; both native editions retain the host-specific notes |
| Download-all bundles | Copilot, Gemini and combined ZIPs have exact inventories, entry hashes and deterministic bytes; nested native packages each contain one root SKILL.md |
| Release generation | Tests cover exact four-archive contents/checksums, deterministic bytes, stable SemVer ordering, immutable existing versions, prior-version preservation, current-build drift and non-writing verification, including a clean CLI run without new Python cache files |
| Full-project boundary | Explicit public project roots and file types; private/runtime/cache/unlisted files and release snapshots excluded; unsafe paths, case collisions and symlinks rejected |
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
| Work-account publication | Initial import `23277e2768d8267cb5b885be229d473cce802e64` on `mim1hat-prog/finance-skills` main matched all 193 local file hashes, including 48 ZIP packages |

The test count includes 16 upstream-helper cases. Package validation does not prove that a model will follow every instruction. Optional tests intentionally skip when their dependencies are absent; inspect the run output before describing them as passed.

Release tooling tests use isolated temporary projects. The published release includes its exact project-file inventory and SHA-256 checksums in `releases/v1.1.0/manifest.json`; remote publication is verified separately from local packaging. No GitHub Release object or tag is claimed.

### Independent finance task checks

For the new Excel profile, a fresh agent received the relevant skill files, a raw synthetic request to correct a November Personnel total, an editable JSON workbook cell model and exported internal-source fixtures. It resolved an obsolete draft against the approved definition and final export. It corrected benefits from **EUR 18,000 to EUR 21,000**, retained the existing Personnel and Opex formulas, and updated their evaluated totals to **EUR 141,000 and EUR 167,000**. Only the existing workbook cell model changed; no worksheet, audit table, log or extra output file was created. The result was independently checked against the supplied fixture. This tests instruction behavior with synthetic local exports, not live enterprise retrieval, a native Copilot/Gemini import or Excel recalculation.

A fresh agent received only the relevant skill files and raw synthetic work requests. It quarantined overlapping mappings and an incomplete 95% allocation without normalizing or dropping the unresolved amount. Its bridge reconciled **320 source = −30 mapped + 350 unresolved**.

For working capital, it calculated an available **15-day** two-point-average DSO, declined to fabricate missing average balances, and separately identified a **21-day** group closing-balance proxy. A five-day improvement of **166.67 JPY-thousand** was labeled a modeled potential release, not received cash or a recurring monthly benefit.

An independent code review identified six edge issues. All six original reproductions were rerun after correction: CSV header inference, a key/count alias collision, unsized workbooks, a destination symlink introduced after preview, Git line endings and extreme decimal precision. Each reproduction now behaves as intended. Native Windows junction and OneDrive behavior were not exercised by those checks.

### Catalogue checks

The original catalogue passed DOM execution checks for edition-specific links, search, category selection, empty/reset behavior, focus restoration, example-prompt copy feedback with a mocked clipboard, theme persistence, unique IDs, visible control labels and malformed-data recovery. JavaScript syntax and SVG XML checks passed.

The generated **25-entry, v1.1.0** catalogue additionally passed focused DOM execution checks for the combined download, edition-following bundle label/path/filename, Gemini deep link, Instructions profile, extraction text, no-JavaScript and malformed-data fallback links, dynamic count, unique IDs and the full-release URL derived from the catalogue version. All three current bundle destinations and the profile existed. The versioned release destination is checked during final packaging/publication.

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

Published on **2026-11-25** to `mim1hat-prog/finance-skills`, branch `main`,
through the ChatGPT GitHub plugin connected as `mim1hat-prog`. The import uses
only the reviewed tracked tree and follows the destination's starter README
commit. Original source-pack and dot design-kit provenance, licences and
package content are preserved; the older toolsuite history was not imported.

All 193 destination files and their modes matched the staged Git hashes after
the initial import, including all 48 individual skill packages. The destination
README was read through the plugin. No cloud-browser authentication or visual
inspection was performed for this destination; the earlier visual check covers
the original publication described above. Native work-account imports remain
checks for the actual approved Copilot/Gemini account.
