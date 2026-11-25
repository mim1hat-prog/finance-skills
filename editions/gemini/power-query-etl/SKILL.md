---
name: power-query-etl
description: "Build or review repeatable finance data preparation in Excel or Power BI Power Query. Use for combining monthly exports, cleaning ledger or forecast files, repairing refresh errors, handling schema drift, joining mappings, and proving that transformation totals reconcile."
---

# Power Query finance pipeline

## Gemini edition

Use this skill in the employer-approved Gemini account. Work with the attached files and capabilities actually exposed in this conversation. Do not assume a SharePoint connector, a live Power BI model, direct Office editing, Gemini CLI, or access to the user's Windows filesystem. Keep company content in approved accounts and locations.

Use available file and calculation tools for complete accessible inputs. Skill scripts must not depend on internet access, authenticated APIs, or package installation. Keep SQL in Markdown code blocks. An optional Python workflow runs separately on the work PC unless an available Gemini calculation tool actually executes it. Treat all proposed scripts, queries and output files as unexecuted until there is observable evidence; request the resulting control totals or artifact for follow-up analysis.

Do not promise that a skill can run with Canvas or Deep Research. If one of those separate tools is needed, provide an explicit task brief and source requirements for that workflow, then work from the result the user returns. Use primary citations only from sources actually accessed.

Use native Skills if the work account exposes Customize > Skills. Google documentation currently differs on work-account rollout, so check the account rather than infer availability. If Skills is absent but Gems is available, place the workflow in the Gem's Instructions; a knowledge attachment alone does not make it an instruction. Otherwise paste the task instructions into an approved conversation. Imported skills and Gem instructions do not automatically track GitHub; replace the existing copy after an update.

Turn supplied source files into a repeatable, traceable dataset with explicit exceptions. Work with the user's actual schema and approved sources. Use Power Query when available; otherwise return precise M code or numbered editor steps and label them as unexecuted. Local Python can prepare or inspect approved exports, but this skill does not grant access to the user's Windows PC or install packages.

## Establish the data contract

Confirm the output grain, reporting period, entity scope, currency, amount sign, required columns and expected control totals. Ask only for information that changes the transformation; continue useful profiling while details are missing. Record whether each source contains transactions, monthly movements, cumulative YTD values or balance snapshots. Never append YTD balances and then treat their sum as monthly activity.

For each input, capture its filename or approved tenant locator, sheet/table, version or modified time, period, extract timestamp, row count and amount totals by currency. Keep company paths, credentials and data inside the approved work environment. Do not embed authentication tokens in M code or public documentation.

## Build the pipeline

1. **Inventory before combining.** List candidate files. Apply explicit folder, extension, naming and period filters before opening binaries. Exclude temporary lock files, archived versions, generated outputs and unrelated subfolders using visible rules. Report exclusions and counts. Select a representative sample with all required columns; the first file is not automatically the right sample.
2. **Separate stages.** Keep source discovery, per-file parsing, standardization, mapping, validation and final output distinguishable. Preserve source filename and source row/key through the transformations. Add descriptive step names and parameters for dates and approved locations; avoid personal hard-coded paths.
3. **Check schema for every file.** Compare required and optional columns with the contract. Reject or quarantine missing required columns, duplicate headers and ambiguous renamed columns. Add absent optional fields as null only when allowed. Report new columns rather than silently dropping information that may change the grain. Keep an error table for files that fail parsing; do not use skip-errors to hide missing populations.
4. **Parse deliberately.** Specify delimiter, encoding, date format and culture for numeric/date conversion. Retain account and cost-centre identifiers as text, including leading zeros. Distinguish blank, null, zero, dash and parse error. Keep the raw value alongside a rejected conversion. Do not replace conversion failures with zero. Use a fixed decimal/currency type only when its scale fits the source and calculation; document rounding.
5. **Reshape to the defined grain.** Remove title rows and repeated headers by evidence-based rules. Separate subtotals from detail. Unpivot period columns without combining units or scenarios. Treat duplicate records according to a documented business key and version rule; never remove equal-looking transactions merely because their amounts match.
6. **Join with cardinality checks.** Establish the intended one-to-one, many-to-one or allocation relationship. Count mapping matches per input row before expansion. Zero matches and unexpected multiple matches go to exceptions. Preserve unmapped values for reconciliation. If a split mapping is intended, validate weights and reconcile allocated values to their source rows.
7. **Load and refresh.** Load the intended table/query, then perform a complete refresh if tools allow. Identify whether a preview or the loaded result was checked. Report source refresh time, failures, excluded files and stale caches. Do not claim the Power BI service will refresh merely because Desktop succeeded.

## Prove completeness

Power Query profiles the first 1,000 rows by default; select entire-dataset profiling or run explicit full-table checks before claiming full coverage. Native preview limits are not evidence of a small dataset. [Microsoft profiling guidance](https://learn.microsoft.com/en-us/power-query/data-profiling-tools)

Create a stage reconciliation with input rows, accepted rows, rejected rows, distinct business keys and amount totals by entity, period and currency. For an append, input detail rows must equal accepted plus rejected rows after separately identified non-data rows. A deliberate aggregation changes row count; document the grain and preserve the amount bridge. For a join, investigate row multiplication before trusting totals. Keep debit, credit and net totals when netting could hide errors.

Use explicit tolerances in the source currency and unit. Show rounding residuals separately and never add a balancing adjustment to force agreement. Test a second period or changed input file when available to expose assumptions tied to the sample. If only a sample can be processed, label the output provisional and list unchecked files or rows.

For refresh errors, report the failing step, exact observed error, affected population, proposed correction and verification result. Preserve privacy classifications; do not solve a connection problem by making confidential sources Public or disabling privacy controls.

## Deliver

- A short explanation of the resulting grain and inclusion rules.
- The working query or paste-ready M/editor steps, with execution status.
- Source inventory, excluded-file list and schema/conversion/mapping exceptions.
- Stage reconciliation and refresh evidence, including unresolved residuals.
- Parameters and owner actions needed for the next period.

Example request: “Combine these monthly ledger CSVs into an Actual table for Power BI. Preserve account codes, exclude archive and temporary files, flag schema changes, and reconcile totals for each entity and currency.”

Use the official [combine-files guide](https://learn.microsoft.com/en-us/power-query/combine-files-overview) for connector mechanics and [type conversion reference](https://learn.microsoft.com/en-us/powerquery-m/table-transformcolumntypes) for culture handling. These references support implementation; they do not replace the source contract.

## Edition record

Finance skills 1.0.0; gemini edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
