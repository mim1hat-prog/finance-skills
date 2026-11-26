# Validation and remaining evidence gaps

## Current release: v1.9.0

The individual Copilot and Gemini editions, grouped suites and Excel profile carry the quality-first defaults. The Excel OneDrive download carries the complete Copilot suite folder. The suites contain 30 workflow sections in nine supporting files and their roots stay below the 20,000-character limit.

Offline verification covers deterministic generation, exact packaged workflows, source mappings, evaluation fixture integrity and historical releases. The [quality-first guide](QUALITY-FIRST.md) records the reasoning-project review and what managed hosts expose. The release gate ran 200 tests with both pinned optional libraries present under Python 3.12 using a case-sensitive temporary volume. The generated catalogue loaded 30 workflows in a headless browser, exposed the new workflow through search and loaded the coverage image at desktop and phone widths. Local tests cover repository and helper behavior. Native import, tool availability, editing, recalculation and model outcomes in the intended accounts remain unverified.

## Historical validation for v1.6.0

This page separates software and package checks from actual assistant behavior. **Native Copilot/Gemini import, supporting-file access and task execution remain unverified.** The owner identified Copilot in Excel with its OneDrive folder route; a documentation match is not an installation receipt.

**Pre-freeze gate passed on 2026-11-26:** 200 Python tests, zero skips, and exact reproduction of 191 generated artifacts. The optional pinned DuckDB 2.0.1 checks ran in a separate maintainer validation environment; nothing was installed on the work PC. Publication inspection covered the current project and 11 prior frozen versions in 12 bounded batches with no findings. All 92 prior frozen files retained their hashes. The registry's five pre-existing rights/correction warnings remain explicit.

An independent package audit used strict YAML parsing and separate ZIP/section extraction rather than the builder. It verified all 29 complete procedures, routing, metadata, byte ranges, hashes, regular-file modes and the Excel wrapper against both native suites and expanded folders. All 74 inspected inputs remained stable through the check.

The exact 1200 × 963 coverage SVG was rendered and visually inspected with no overlap or clipping observed. Its 12/29 partial helper-test links, 0/29 native evidence, 89 registered sources and source-type composition agree with independent counts. This is a figure review, not a new desktop/mobile browser-layout check.

## What is checked

- **Excel folder format:** a single matching `finance-suite` folder contains `SKILL.md` and nine reference files. Its name matches the YAML metadata; every resource equals the generated Copilot suite. The dedicated download must be extracted before adding its inner folder to Excel's app-created OneDrive location and selecting Refresh.
- **Complete procedures:** both suites retain all 29 canonical workflows, valid frontmatter, explicit section routing, source/body hashes and byte ranges. Individual skill and copy-only formats are generated from the same sources. Copying the suite root alone does not supply its procedures.
- **Instruction cleanup:** the Copilot root decreased from 18,846 to 17,404 characters; Gemini from 18,876 to 17,434. Shared controls remain in every individual edition. Authorized actions still require available capabilities, scoped permission, preconditions and independent verification.
- **Calculation checks:** 12 of 29 workflows now link to existing partial helper tests. The four newly declared links cover forecast bridges, SQL population checks, workbook coverage and close reconciliation. A resolvable test link does not mean a model completed the workflow. The release report records actual executed/skipped checks separately.
- **Scientific evidence:** source-type composition is generated from the registry. FAIR is metadata guidance rather than an empirical evaluation. Unresolved candidates stay outside active support. The figure measures a complete repository inventory, not task accuracy or statistical significance.
- **Evaluation kit:** four invented development cases have separate hashed prompts and answer keys. The local grader checks exact responses, preserves every planned run and distinguishes incomplete/failure statuses. A prepared plan, a grader self-test or a manually filled record does not prove native execution. Public keys are not a hidden holdout.
- **Release and publication:** deterministic generated output, all frozen release schemas, dataset/API contracts, research references and nested archives are checked offline. Private-marker scanning and public Git identity checks remain separate gates. No public provider refresh occurs in these commands.

## Independent local task

A fresh assistant received only the revised suite and independently invented CSV inputs. It verified the approved old amount, changed only that amount in the existing current extract, then reconciled the corrected total of **104.20** against **95.00**. Matched movement **6.20**, removed-record effect **5.00** and added-record effect **-2.00** explain the **9.20** difference with a **0.00** residual. It retained the unmatched records' explanation as unresolved, independently checked integer-cent and decimal arithmetic, and created no extra files. Independent file inspection confirmed the permitted edit and unchanged prior extract.

This is one local behavior check, not a native Excel task, a blinded comparative study, or evidence of general model effectiveness.

## Unchanged data and history

The retained public dataset still contains 11 observed series out of 17 configured, with 116 original rows and 51 separate derived rows across two snapshots. This release does not fetch providers or redate their observations. See the [generated methods and dates](../metrics/README.md).

All previous frozen releases remain available and are integrity checked. The repetitive historical narratives were removed from this current page; their exact earlier record remains in [the v1.5.2 source revision](https://github.com/mim1hat-prog/finance-skills/blob/bc11c32c31089fb50e5972765b8e5c27328f403d/docs/VALIDATION.md) and its frozen full-project archive. [Release history](../releases/README.md)

## Reproduce and interpret

```powershell
py -3 scripts\research_registry.py
py -3 scripts\build.py
py -3 scripts\evaluation.py validate-kit
py -3 scripts\check_release.py
py -3 scripts\check_release.py --require-release
```

The last command requires the frozen current release. The JSON report records actual tests, skips, source warnings and publication batches. Optional workbook/SQL dependencies must be present to execute their checks. Private marker policies and Git history exports stay outside the project; see [release verification](RELEASES.md).

**Still outstanding:** native installation and reference retrieval in the work account; a representative task in each target host; matched baseline/suite runs from the evaluation kit; and independent external replication. Local Python checks do not establish Excel recalculation, enterprise access or completed writes. No certification, peer review, live data refresh or measured assistant-performance improvement is claimed.
