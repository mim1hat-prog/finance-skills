---
name: power-query-etl
description: "Build or review repeatable finance data preparation in Excel or Power BI Power Query. Use for combining monthly exports, cleaning ledger or forecast files, repairing refresh errors, handling schema drift, joining mappings, and proving that transformation totals reconcile."
---

# Power Query finance pipeline

## Microsoft 365 Copilot edition

Default output: Give the requested result directly with concise source references, necessary calculations, recommendations, and material unresolved exceptions. Keep routine verification internal. Do not create audit tables, audit logs, audit text, new worksheets, or unrelated reports unless specifically requested; a requested data table, model, or report remains allowed. Preserve existing business logic and avoid filler, AI/process commentary, and unnecessary summaries or tables.

Use this skill in the approved work account and the current Microsoft 365 host. Prefer the open Excel workbook or PowerPoint presentation when native editing is available. A connection to SharePoint, a Power BI model, or a local computer exists only if this session exposes and authorizes it. A Microsoft 365 Copilot subscription does not imply GitHub Copilot or a VS Code agent.

For uploaded files, use available sandbox tools and preinstalled libraries only. Do not run installers or authenticated HTTP requests inside a cloud skill script. Use enabled work connectors for authorized SharePoint retrieval. Preserve source locators, the reporting cutoff and the actual permission scope. Never treat a search result or file preview as the complete source population.

Windows Python and VS Code are a separate, optional route. When the task needs local files or a package absent from this session, prepare an inspectable Python script or query for the user to run in the approved local environment. State that it has not run on their PC. Continue analysis only from returned results and reconciled control totals. A generated DAX measure or Power Query expression is a proposal until it has been applied and checked in the model.

Use the requested skill explicitly when available. If the tenant cannot import skills, the user can paste this workflow into a conversation or an authorized agent's instructions. A file attachment alone does not register a reusable skill. Do not claim this imported copy automatically tracks GitHub; updates require replacement or the host's documented folder refresh.

## Shared workflow controls

Use all relevant available, authorized capabilities needed for the objective. For company questions, retrieve enterprise evidence first. Before treating a missing search result as missing data, inspect the source content and try a materially different query, period, linked reference or responsible-source route. Continue while another available step can resolve a material uncertainty; do not repeat unchanged searches or browse unrelated sources to inflate coverage. Use an available deeper research/reasoning mode when appropriate and supported; instructions cannot select a hidden mode, grant permissions or exceed platform limits.

Independently recheck consequential results with a second calculation, source record or alternative method. Rereading the same answer is not an independent check. Investigate contradictions and failed checks, correct them, then rerun the affected checks. Finish when the requested scope is complete and material claims are supported, or report the specific unresolved gap after useful retrieval routes are exhausted. At a host limit, preserve the objective, source locators, versions, decisions and pending work in a compact continuation; never claim that unseen work was completed. Keep this diligence internal and the final response precise.

Keep three streams distinct: approved internal figures; internal workflow status; public benchmarks. An internal blank stays unresolved until the authorized source supplies it. A benchmark can challenge an assumption but cannot become an actual, approved forecast, booked rate, mapping, case confirmation or close receipt.

Before comparing numbers, align period and cutoff/timezone, scenario and version, entities, accounting/reporting basis, currency/unit, sign convention and source snapshot. Keep a requested frozen submission separate from newer working files. Record exact source locations and what each source establishes in working context; do not create an audit artifact merely to store these checks.

Validate business keys, join cardinality, effective dates, gross movements and detailed coordinates as well as totals. Normalize units/signs only from explicit declarations. Calculate residuals at source precision and use an approved, versioned, effective tolerance. An unexplained residual is not rounding by default.

Preserve the baseline workbook/query, protected records, ordered names/types, formulas, load targets, add-in regions and downstream consumers outside the requested change. Successful refresh alone does not establish population or interface parity. Return complete replacement code only for the affected existing scope when code is requested.

Keep evidence state separate from action state: found, calculated, refreshed, uploaded, reconciled, approved and submitted require different evidence. Default to inspection/preparation. For an authorized write, reuse authorization that covers the exact target and payload, check preconditions and verify independently. If the outcome is uncertain or a write times out, read back before retrying; do not substitute locked or unapproved objects. Local validation helpers execute no enterprise writes.

Return the useful answer concisely: approved result, verified internal driver, relevant public benchmark, then material residual/blocker and next source. State only the statuses supported by evidence. Keep diagnostic detail in working context; do not add unsolicited sheets, audit tables, comments, queries, logs or process narration.

Turn supplied source files into a repeatable, traceable dataset with explicit exceptions. Work with the user's actual schema and approved sources. Use Power Query when available; otherwise return precise M code or numbered editor steps and label them as unexecuted. Local Python can prepare or inspect approved exports, but this skill does not grant access to the user's Windows PC or install packages.

## Establish the data contract

Confirm the output grain, reporting period, entity scope, currency, amount sign, required columns and expected control totals. Ask only for information that changes the transformation; continue useful profiling while details are missing. Record whether each source contains transactions, monthly movements, cumulative YTD values or balance snapshots. Never append YTD balances and then treat their sum as monthly activity.

For each input, capture its filename or approved tenant locator, sheet/table, version or modified time, period, extract timestamp, row count and amount totals by currency. Keep company paths, credentials and data inside the approved work environment. Do not embed authentication tokens in M code or public documentation.

## Build the pipeline

For a repair, inspect the actual dependency graph first: parameters, source queries, helper functions, referenced queries, loaded tables, named ranges, formulas and downstream BI consumers. Capture the accepted baseline and protect history, planning records, scenario labels, ordered column names/types, keys and load targets outside the authorized change. Diagnose the first failure separately in source selection, access, headers/types, join, transformation, load or recalculation.

Choose append versus replacement from the approved change. A full rebuild is not implied by a request to fix one source or period. Return complete, paste-ready replacement M for the affected existing query when code is requested, with its dependencies and parameters identified. Do not create additional queries or worksheets just to demonstrate a repair.

1. **Inventory before combining.** List candidate files. Apply explicit folder, extension, naming and period filters before opening binaries. Exclude temporary lock files, archived versions, generated outputs and unrelated subfolders using visible rules. Report exclusions and counts. Select a representative sample with all required columns; the first file is not automatically the right sample.
2. **Separate stages.** Keep source discovery, per-file parsing, standardization, mapping, validation and final output distinguishable. Preserve source filename and source row/key through the transformations. Add descriptive step names and parameters for dates and approved locations; avoid personal hard-coded paths.
3. **Check schema for every file.** Compare required and optional columns with the contract. Reject or quarantine missing required columns, duplicate headers and ambiguous renamed columns. Add absent optional fields as null only when allowed. Report new columns rather than silently dropping information that may change the grain. Retain failed-file identifiers and errors in the working query/context so they can be investigated; do not use skip-errors to hide missing populations or create/load a separate error table unless requested.
4. **Parse deliberately.** Specify delimiter, encoding, date format and culture for numeric/date conversion. Retain account and cost-centre identifiers as text, including leading zeros. Distinguish blank, null, zero, dash and parse error. Keep the raw value alongside a rejected conversion. Do not replace conversion failures with zero. Use a fixed decimal/currency type only when its scale fits the source and calculation; document rounding.
5. **Reshape to the defined grain.** Remove title rows and repeated headers by evidence-based rules. Separate subtotals from detail. Unpivot period columns without combining units or scenarios. Treat duplicate records according to a documented business key and version rule; never remove equal-looking transactions merely because their amounts match.
6. **Join with cardinality checks.** Establish the intended one-to-one, many-to-one or allocation relationship. Count mapping matches per input row before expansion. Zero matches and unexpected multiple matches go to exceptions. Preserve unmapped values for reconciliation. If a split mapping is intended, validate weights and reconcile allocated values to their source rows.
7. **Load and refresh.** Apply the requested load/refresh to the intended existing table/query if tools allow; a review request alone does not authorize changing the load destination or creating a worksheet. Identify whether a preview or the loaded result was checked. Disclose material refresh failures, exclusions and stale caches. Do not claim the Power BI service will refresh merely because Desktop succeeded.

## Prove completeness

Power Query profiles the first 1,000 rows by default; select entire-dataset profiling or run explicit full-table checks before claiming full coverage. Native preview limits are not evidence of a small dataset. [Microsoft profiling guidance](https://learn.microsoft.com/en-us/power-query/data-profiling-tools)

Reconcile stages internally using input rows, accepted rows, rejected rows, distinct business keys and amount totals by entity, period and currency. Do not create a reconciliation worksheet or audit table unless requested. For an append, input detail rows must equal accepted plus rejected rows after separately identified non-data rows. A deliberate aggregation changes row count; establish the grain and preserve the amount bridge. For a join, investigate row multiplication before trusting totals. Check debit, credit and net totals when netting could hide errors.

Use explicit tolerances in the source currency and unit. Show rounding residuals separately and never add a balancing adjustment to force agreement. Test a second period or changed input file when available to expose assumptions tied to the sample. If only a sample can be processed, label the output provisional and list unchecked files or rows.

For refresh errors, report the failing step, exact observed error, affected population, proposed correction and verification result. Preserve privacy classifications; do not solve a connection problem by making confidential sources Public or disabling privacy controls.

## Deliver

Check both population parity and interface parity against the accepted baseline. A refresh that drops protected planning records, changes an existing scenario's meaning, renames/reorders a downstream field or changes a load target fails compatibility even when it finishes successfully. Keep static code review, native refresh, recalculation and downstream regression results separate; do not claim tests that the current host could not perform. Do not replace the accepted output when a required compatibility check fails.

Return the requested working query/result or paste-ready M/editor steps with execution status. Briefly state the resulting grain, necessary source references/parameters, and material exclusions, errors, stale data or residuals. Keep the source inventory and stage checks internal; deliver a full inventory, exception table, audit log or validation report only when requested. Include next-period instructions only when needed to use the requested workflow.

Example request: “Combine these monthly ledger CSVs into an Actual table for Power BI. Preserve account codes, exclude archive and temporary files, flag schema changes, and reconcile totals for each entity and currency.”

Use the official [combine-files guide](https://learn.microsoft.com/en-us/power-query/combine-files-overview) for connector mechanics and [type conversion reference](https://learn.microsoft.com/en-us/powerquery-m/table-transformcolumntypes) for culture handling. These references support implementation; they do not replace the source contract.

## Edition record

Finance skills 1.5.1; copilot edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
