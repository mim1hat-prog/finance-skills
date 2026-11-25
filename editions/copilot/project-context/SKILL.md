---
name: project-context
description: "Create or update a concise project handoff, decision log, or working context note from the current conversation and supplied project documents. Use when the user asks to preserve progress, resume work, record decisions, hand a task over, or prepare context for another Copilot or Gemini session."
---

# Project context

## Microsoft 365 Copilot edition

Use this skill in the approved work account and the current Microsoft 365 host. Prefer the open Excel workbook or PowerPoint presentation when native editing is available. A connection to SharePoint, a Power BI model, or a local computer exists only if this session exposes and authorizes it. A Microsoft 365 Copilot subscription does not imply GitHub Copilot or a VS Code agent.

For uploaded files, use available sandbox tools and preinstalled libraries only. Do not run installers or authenticated HTTP requests inside a cloud skill script. Use enabled work connectors for authorized SharePoint retrieval. Preserve source locators, the reporting cutoff and the actual permission scope. Never treat a search result or file preview as the complete source population.

Windows Python and VS Code are a separate, optional route. When the task needs local files or a package absent from this session, prepare an inspectable Python script or query for the user to run in the approved local environment. State that it has not run on their PC. Continue analysis only from returned results and reconciled control totals. A generated DAX measure or Power Query expression is a proposal until it has been applied and checked in the model.

Use the requested skill explicitly when available. If the tenant cannot import skills, the user can paste this workflow into a conversation or an authorized agent's instructions. A file attachment alone does not register a reusable skill. Do not claim this imported copy automatically tracks GitHub; updates require replacement or the host's documented folder refresh.

Preserve the project facts needed to continue accurately in an explicit, reviewable work note. This skill is a document workflow, not an automatic memory system. It requires no local service, database, hooks, or software installation.

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

Use this structure, omitting empty sections. Aim for roughly 300-600 words for an ordinary handoff, expanding only for essential detail.

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

Keep a small decision log when the task needs it:

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

Provide the completed handoff or the actual saved document, followed by a short status: what was updated, which sources were used, and any unresolved gap that matters for continuing. If the user also requested the next project action, continue from the verified context rather than stopping after the summary.

## Example request

"Use project-context to update our approved forecast project note with today's accepted decisions, completed workbook changes, unresolved reconciliation issue, and next three steps. Keep it short enough for me to bring into a new work Copilot or Gemini session, and distinguish what was verified from what remains a proposal."

## Edition record

Finance skills 1.0.0; copilot edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
