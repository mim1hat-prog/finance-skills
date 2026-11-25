---
name: connected-reporting
description: "Prepare and validate connected finance reports and planning uploads using Excel, planning-cube or SAP/BW exports. Use when report type, target model, ordered dimensions, stale caches, suppressed connector errors, upload/readback parity or submission status must be established."
---

# Connected reporting and readback

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

Establish the report's real system context before editing. Work from a live connection only when that capability is exposed and authorized; otherwise inspect the supplied export or cached workbook and state that scope. A skill does not install a connector or grant write access.

## Inspect the connection and report

Identify the software and report type, model/cube or report ID, ordered dimensions, members/hierarchies, scenario, version, period, measure, currency/unit, selection variables and filters. Keep this configuration private. Use a known-good, supported read to establish connection health; do not test a connection by entering a value in a write-enabled cell.

Preserve add-in-managed formulas, named ranges, hidden controller cells, parameter areas, expansion regions and formatting outside the requested change. Inspect writeback mode before changing connected input cells. Some planning report modes can commit when a value is entered; do not assume leaving an edited cell only changes the workbook. Do not change connection, writeback or refresh settings merely to make a review easier.

Distinguish the workbook's saved values, workbook refresh time, underlying data update time and actual live response. A blank behind an error-suppressing formula is an unverified or failed read until the underlying condition is checked; it is not zero activity. For a reporting export, record its variables, filters, hierarchy/grain and source snapshot before comparison.

## Prepare and validate the target payload

1. Preserve the existing upload format and target order. Identify data-entry versus derived/consolidated cells and reject absent, duplicate or ambiguous target coordinates.
2. Match approved source data to complete target intersections. Check entity, account, period, scenario/version, measure, currency and any other required dimensions individually. Matching grand totals cannot compensate for swapped detailed values.
3. Verify mappings, source scope, signed amounts, units and rounding at the required grain. Keep rejected/unmatched values visible in working context and quantify the unresolved amount.
4. Keep inspect, prepare, validate, execute and independently verify distinct. A review or upload-preparation request does not authorize posting or submitting. Reuse explicit authorization when it covers this exact target and payload; ask only for material missing authorization or ambiguity.
5. Before an authorized action, recheck target/model, permissions, locks, version, source freshness and prior execution status. After an uncertain result or timeout, read the existing state and execution receipt before retrying. Do not replace a locked sender or change a master mapping as a workaround.
6. Compare independent readback with the staged payload at the same ordered coordinates and tolerance. Check row/key completeness and each detailed value, then totals. Keep any receipt as evidence of the action it actually proves; upload, publication visibility, review approval and final submission are separate states.

## Return

Give the requested report or prepared payload and the compact result: evidence state, action state, detailed residual/blocker and next source. Do not add a new sheet, query, comment or audit register unless requested. If only export comparison ran, label it export validation and identify the live check still needed.

Official mechanics: [IBM report types](https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=types-planning-analytics-microsoft-excel-report), [IBM automatic commit behavior](https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=reports-automatically-commit-data), and [SAP Analysis source information](https://help.sap.com/docs/SAP_BUSINESSOBJECTS_ANALYSIS_OFFICE/ca9c58444d64420d99d6c136a3207632/f26f9dfa6c9b1014bf2c9a7eb0e91070.html). Match documentation to the installed version; these references do not prove a connection is available.

## Edition record

Finance skills 1.4.3; copilot edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
