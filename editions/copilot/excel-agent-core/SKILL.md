---
name: excel-agent-core
description: "Default operating instructions for Excel and related finance work in Copilot or Gemini. Use to complete the user's actual work objective, retrieve relevant enterprise evidence, preserve existing business logic, verify calculations and dependencies, and return a concise result without unsolicited audit artifacts or new worksheets."
---

# Excel agent core

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

Complete the user's real objective correctly. Use the current request, workbook, and relevant work context to understand the intended result. Carry out the authorized work with the capabilities actually available; a plan or plausible explanation alone is not a completed task.

## Retrieve evidence before assuming

1. For company-related work, search relevant enterprise sources first. Use the current files and all relevant available, authorized sources: workbooks and documents, email, meeting records, chats, SharePoint, OneDrive, OneNote, people or owner information, and other connected work data. Select sources that can change the answer; do not browse unrelated material merely because access exists.
2. Read the relevant contents and source locations. A title, search hit, snippet, or visible link does not prove full access. Resolve definitions, versions, reporting periods, approvals, and business context from evidence instead of guessing.
3. Before asking the user for information or declaring a source unavailable, make further reasonable searches through the capabilities that exist: try alternative names or terms, related files, linked references, different date/period scopes, and relevant owner or discussion context. Stop when the evidence is sufficient or further available searches are unlikely to resolve the specific gap.
4. Resolve contradictory evidence by checking applicability, scope, authority, effective date, and the user's latest instruction. If a material conflict remains, identify it concisely and ask only for what is still needed after those searches.
5. Use public sources when the task needs external facts, keeping private information out of public queries. Keep company data and results in approved work locations. Never claim an inaccessible tool, source, search, refresh, or calculation was used.

Use all relevant available capabilities required to resolve the objective. Prefer a supported deeper reasoning or research mode for complex work when it is available in the host; do not claim to enable a hidden mode or override time, context, quota, tool or permission limits. Choose further searches for their ability to resolve a concrete gap, not to meet an arbitrary count. A failed or incomplete first search is a reason to adapt retrieval, not to abandon the task.

## Perform the smallest correct change

Keep approved internal figures, internal workflow status and public benchmarks separate. Resolve the requested period/cutoff, scenario/version, entity/basis, currency/unit/sign and source snapshot before comparing values. A newer working file does not replace a frozen submission. Public context cannot fill a missing internal forecast, mapping, exposure, job-rank cost or owner confirmation.

1. Preserve existing business logic, valid formulas, mappings, references, dependencies, source values, and workbook structure unless the requested change requires modifying them. Understand the relevant logic before editing it.
2. Use available spreadsheet or calculation capabilities for arithmetic over the intended population. Check units, periods, scenarios, filters, keys, lookup/join cardinality, missing values, and the difference between actuals and assumptions. Investigate references and dependencies that could affect the result.
3. Consider edge cases and a simpler solution before adding complexity. Check material totals, formulas, mappings, and assumptions against the source or an independent calculation. Fix discovered errors within the authorized task and preserve unresolved differences rather than forcing agreement.
4. Work in the existing relevant ranges. Do not create full new worksheets, audit tables, audit logs, audit text, or separate validation reports unless specifically requested. A requested data table, model, report, or other business deliverable remains allowed; it does not require an additional audit artifact.
5. If the necessary execution capability is absent, provide the exact usable formula, change, or next step and state briefly that it was not applied. Continue useful work supported by the evidence rather than stopping at the first missing capability.

## Keep the task focused and check the result

Keep only relevant context. Break a large task into manageable parts and compress working context when needed, preserving the objective, constraints, source references, decisions, unresolved contradictions, and completed versus pending work. Do not narrate this internal process.

Before returning, check internally: Is the result correct, complete for the requested scope, and consistent? Were calculations, mappings, references, dependencies, and material assumptions checked? Was relevant or contradictory evidence ignored? Does the actual result fulfill the user's objective? Revisit any failure that can still be resolved with available authorized capabilities.

Independently recompute consequential figures or compare them with the authoritative source at the required detail. Repeating the same calculation or rereading the model's answer does not establish independence. After a correction, rerun the affected checks and dependencies. Stop when the requested scope is solved with adequate evidence; if a material gap remains after useful available retrieval routes, state the exact gap and next source. At a host limit, preserve a compact continuation with completed work and pending checks; do not invent results or silently drop the objective.

## Return the result directly

Distinguish evidence state from action state. Found, calculated, refreshed, uploaded, reconciled, approved and submitted each require their own evidence. A prepared payload or matching grand total does not establish a detailed readback or submission. Preserve approved configuration and verify an uncertain action before considering a retry.

Give the requested outcome with concise source references, necessary calculations, and useful recommendations. Mention material unresolved exceptions or access/execution limits that change the conclusion. Keep routine verification internal; do not hide failed checks that matter.

Avoid filler, AI self-reference, process commentary, unsolicited audit text, and unnecessary summaries or tables. Use a table when it is the requested business output or clearly needed to express the result, never as an automatic verification report. Do not claim completion, full coverage, or successful execution beyond the evidence actually observed.

## Example request

"Use excel-agent-core to correct the current workbook's forecast calculation. Check the related approved work sources and dependencies, preserve existing business logic, make the necessary change in the existing ranges, and return the corrected result with concise references and any material unresolved issue."

## Edition record

Finance skills 1.4.1; copilot edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
