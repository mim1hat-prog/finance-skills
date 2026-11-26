# Project context

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
