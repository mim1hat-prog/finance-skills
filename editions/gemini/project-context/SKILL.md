---
name: project-context
description: "Create or update a concise project handoff, decision log, or working context note from the current conversation and supplied project documents. Use when the user asks to preserve progress, resume work, record decisions, hand a task over, or prepare context for another Copilot or Gemini session."
---

# Project context

## Gemini edition

Default output: Give the requested result directly with concise source references, necessary calculations, recommendations, and material unresolved exceptions. Keep routine verification internal. Do not create audit tables, audit logs, audit text, new worksheets, or unrelated reports unless specifically requested; a requested data table, model, or report remains allowed. Preserve existing business logic and avoid filler, AI/process commentary, and unnecessary summaries or tables.

Use this skill in the employer-approved Gemini account. Work with the attached files and capabilities actually exposed in this conversation. Do not assume a SharePoint connector, a live Power BI model, direct Office editing, Gemini CLI, or access to the user's Windows filesystem. Keep company content in approved accounts and locations.

Use available file and calculation tools for complete accessible inputs. Skill scripts must not depend on internet access, authenticated APIs, or package installation. Keep SQL in Markdown code blocks. An optional Python workflow runs separately on the work PC unless an available Gemini calculation tool actually executes it. Treat all proposed scripts, queries and output files as unexecuted until there is observable evidence; request the resulting control totals or artifact for follow-up analysis.

Do not promise that a skill can run with Canvas or Deep Research. If one of those separate tools is needed, provide an explicit task brief and source requirements for that workflow, then work from the result the user returns. Use primary citations only from sources actually accessed.

Use native Skills if the work account exposes Customize > Skills. Google documentation currently differs on work-account rollout, so check the account rather than infer availability. If Skills is absent but Gems is available, place the workflow in the Gem's Instructions; a knowledge attachment alone does not make it an instruction. Otherwise paste the task instructions into an approved conversation. Imported skills and Gem instructions do not automatically track GitHub; replace the existing copy after an update.

## Shared workflow controls

Use all relevant available, authorized capabilities needed for the objective. For company questions, retrieve enterprise evidence first. Before treating a missing search result as missing data, inspect the source content and try a materially different query, period, linked reference or responsible-source route. Continue while another available step can resolve a material uncertainty; do not repeat unchanged searches or browse unrelated sources to inflate coverage. Use an available deeper research/reasoning mode when appropriate and supported; instructions cannot select a hidden mode, grant permissions or exceed platform limits.

Independently recheck consequential results with a second calculation, source record or alternative method. Rereading the same answer is not an independent check. Investigate contradictions and failed checks, correct them, then rerun the affected checks. Finish when the requested scope is complete and material claims are supported, or report the specific unresolved gap after useful retrieval routes are exhausted. At a host limit, preserve the objective, source locators, versions, decisions and pending work in a compact continuation; never claim that unseen work was completed. Keep this diligence internal and the final response precise.

Keep three streams distinct: approved internal figures; internal workflow status; public benchmarks. An internal blank stays unresolved until the authorized source supplies it. A benchmark can challenge an assumption but cannot become an actual, approved forecast, booked rate, mapping, case confirmation or close receipt.

Before comparing numbers, align period and cutoff/timezone, scenario and version, entities, accounting/reporting basis, currency/unit, sign convention and source snapshot. Keep a requested frozen submission separate from newer working files. Record exact source locations and what each source establishes in working context; do not create an audit artifact merely to store these checks.

Validate business keys, join cardinality, effective dates, gross movements and detailed coordinates as well as totals. Normalize units/signs only from explicit declarations. Calculate residuals at source precision and use an approved, versioned, effective tolerance. An unexplained residual is not rounding by default.

Preserve the baseline workbook/query, protected records, ordered names/types, formulas, load targets, add-in regions and downstream consumers outside the requested change. Successful refresh alone does not establish population or interface parity. Return complete replacement code only for the affected existing scope when code is requested.

Keep evidence state separate from action state: found, calculated, refreshed, uploaded, reconciled, approved and submitted require different evidence. Default to inspection/preparation. For an authorized write, reuse authorization that covers the exact target and payload, check preconditions and verify independently. If the outcome is uncertain or a write times out, read back before retrying; do not substitute locked or unapproved objects. Local validation helpers execute no enterprise writes.

Return the useful answer concisely: approved result, verified internal driver, relevant public benchmark, then material residual/blocker and next source. State only the statuses supported by evidence. Keep diagnostic detail in working context; do not add unsolicited sheets, audit tables, comments, queries, logs or process narration.

Use the project facts needed to continue accurately. Create or update a work note only when the user requests a handoff, saved context or note; a request to resume work does not require a new summary or log. This skill is a document workflow, not an automatic memory system. It requires no local service, database, hooks, or software installation.

## Inputs

Identify the project or task, the requested handoff or update, the intended work audience, the accessible source material, and the user-approved destination if saving is requested. Reuse an existing named context document when its identity is established. Ask only if several possible documents or projects would lead to materially different updates.

Use only the conversation and files actually accessible in the current session. Do not claim to remember earlier conversations, inspect other sessions, or observe work in the background. A title, search result, or reference to a past discussion is not its full content.

## Build the working picture

1. Extract the current goal, scope, constraints, deliverables, and definition of completion. Preserve explicit exclusions and accepted decisions. Keep the user's latest correction visible and record what it supersedes where that matters.
2. Distinguish requested work from completed work. For each material completion claim, retain the observed result or source reference. Keep planned actions, drafted changes, successful writes, tests performed, and real-world outcomes separate.
3. Record decisions with their reason, source, and date when known. Do not invent a decision date or convert an assistant suggestion into the user's approval. Preserve disputed or provisional choices as unresolved.
4. Record relevant failed attempts and their concrete outcome only when this prevents repeated work. Do not copy raw logs, transcripts, credentials, or unrelated personal information.
5. Resolve conflicts by checking the evidence and chronology. Use an explicit newer user correction when it supersedes an older preference. Where authority or freshness is unclear, state the conflict instead of silently choosing a version.
6. Identify the next useful action and its prerequisite. Keep actual blockers distinct from optional improvements. Do not turn an unfinished verification step into a completed result.

## Write a compact handoff

For a requested handoff, use only the relevant sections below and keep it as short as the next action allows. These are content choices, not a requirement to create a table or audit report. Follow the user's requested length.

| Section | Include |
| --- | --- |
| Goal and scope | Intended outcome, audience, requested deliverables, and completion criteria |
| Current state | What exists, what was completed, and evidence for material status claims |
| Decisions and constraints | Accepted choices, reasons, explicit exclusions, and important superseded choices |
| Sources and artifacts | Exact accessible document names or work links, relevant sections, versions or dates actually known |
| Open questions and blockers | Missing evidence, unresolved decisions, and their effect on the next step |
| Next actions | A short ordered list of concrete actions, confirmed owners if any, and prerequisites |
| Checks still needed | Calculations, visual inspections, approvals, or other checks not yet performed |

Use compact statements with enough context for another session to understand them. Preserve names, identifiers, numbers, units, dates, and status labels when necessary for correctness. Prefer document references and aggregate findings to employee-level or sensitive details. If a source is inaccessible, stale, partial, or only user-described, label that limitation.

Create or update a decision log only when the user specifically requests one:

| Decision | Status | Reason and evidence | Date or source |
| --- | --- | --- | --- |
| A concrete choice from the source | Accepted, provisional, superseded, or unresolved | Brief rationale and supporting location | Use the actual date/reference; mark unknown when necessary |

Do not fill the example row as if it were a real decision. Keep the current-state summary concise while preserving existing historical records unless the user requests an archive or deletion.

## Save or update explicitly

1. If the user requests saving and a supported write capability exists, create or update the identified work document in the approved destination. Preserve unrelated sections and the existing document identity. Check the actual current content before updating an existing note.
2. If a concurrent change or different version is observed, reconcile the relevant content instead of overwriting it blindly. Keep the source version or update date only when returned or otherwise verified.
3. Verify the write result. If saving is unavailable or fails, provide the complete handoff text and say it has not been saved. Do not invent a document link or claim future availability from text appearing in the conversation.
4. For resuming a project, read the supplied latest handoff and relevant source artifacts, check freshness, and proceed with the requested next action. Treat the note as contextual evidence, not permission for unrelated sending, publishing, or system changes.
5. Describe future use accurately: the user can supply or open the saved note in a later authorized session. Do not promise that another session, agent, or AI provider will automatically load it or that updates synchronize across services.

## Quality checks

- Confirm that the note supports a concrete next step without requiring a transcript reread.
- Check that completed, attempted, proposed, and unverified work remain distinguishable.
- Check that a summarization did not drop an important constraint, failed approach, qualification, or unresolved conflict.
- Keep evidence references useful and real. Do not invent timestamps, paths, source contents, or approvals.
- Record project context only; do not turn the handoff into broad profiling or collect unrelated personal history.
- Keep sensitive business content within approved work storage and the intended audience. Do not publish it to the public skills repository, an external memory service, or another AI provider without authorization for that destination.

## Output

For a requested handoff or saved note, provide that deliverable directly with concise source references and material unresolved gaps. Do not append a separate audit narrative or status report. For a request to resume or perform the next project action, use the verified context and complete that action without first generating an unsolicited handoff, decision log, or summary.

## Example request

"Use project-context to update our approved forecast project note with today's accepted decisions, completed workbook changes, unresolved reconciliation issue, and next three steps. Keep it short enough for me to bring into a new work Copilot or Gemini session, and distinguish what was verified from what remains a proposal."

## Edition record

Finance skills 1.4.0; gemini edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
