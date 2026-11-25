---
name: close-controls
description: "Prepare and review a finance period-close control pack. Use for ledger reconciliations, missing close evidence, cutoff checks, accrual review, intercompany differences, journal support and open-item tracking before an authorized reviewer approves the close."
---

# Period-close preparation and controls

## Gemini edition

Use this skill in the employer-approved Gemini account. Work with the attached files and capabilities actually exposed in this conversation. Do not assume a SharePoint connector, a live Power BI model, direct Office editing, Gemini CLI, or access to the user's Windows filesystem. Keep company content in approved accounts and locations.

Use available file and calculation tools for complete accessible inputs. Skill scripts must not depend on internet access, authenticated APIs, or package installation. Keep SQL in Markdown code blocks. An optional Python workflow runs separately on the work PC unless an available Gemini calculation tool actually executes it. Treat all proposed scripts, queries and output files as unexecuted until there is observable evidence; request the resulting control totals or artifact for follow-up analysis.

Do not promise that a skill can run with Canvas or Deep Research. If one of those separate tools is needed, provide an explicit task brief and source requirements for that workflow, then work from the result the user returns. Use primary citations only from sources actually accessed.

Use native Skills if the work account exposes Customize > Skills. Google documentation currently differs on work-account rollout, so check the account rather than infer availability. If Skills is absent but Gems is available, place the workflow in the Gem's Instructions; a knowledge attachment alone does not make it an instruction. Otherwise paste the task instructions into an approved conversation. Imported skills and Gem instructions do not automatically track GitHub; replace the existing copy after an update.

Prepare a traceable close pack from supplied approved records. Apply the organization's accounting policies, close calendar and materiality thresholds when available. Identify missing policy choices instead of inventing them. This workflow prepares analysis, evidence and draft adjustments; it does not authorize ERP postings, close a period, certify a financial statement or provide reviewer sign-off.

Use the current host's authorized tools to inspect or calculate. Report checks actually performed, their source coverage and unresolved items. If only screenshots or samples are supplied, produce a scoped review and an explicit missing-evidence list rather than claiming the full ledger was tested.

## Establish scope and baseline

Record the legal entity or consolidation boundary, ledger, reporting period, cutoff timezone, currency, chart of accounts, sign convention, close stage and extract timestamp. Identify opening balances, period movements and closing balances separately. Check whether extracts include late postings, reversals, adjustment periods, eliminated intercompany balances or year-end carry-forward entries.

Confirm the approved control list and owners where supplied. For an unfamiliar process, propose a practical checklist and label it proposed. Ask for only the missing inputs that materially affect a check. Keep source files and evidence links in the approved work tenant; use generic examples in the public skill repository.

## Run the control pack

1. **Completeness and cutoff.** Inventory files and periods, compare extract totals to the source system's control totals, and identify gaps, duplicate extracts and different extraction times. Compare accounting date, document date, service/delivery date and entry timestamp where relevant. A post-period entry can relate to the period, and an in-period invoice may concern another period; flag for policy review instead of deciding from one date alone.
2. **Ledger balance.** Test debit and credit totals according to the ledger's sign conventions and scope. Reconcile opening balance plus signed movements to closing balance per account/entity/currency. Keep currency conversion, reclassification and consolidation adjustments explicit. A zero net grand total does not establish account-level correctness.
3. **Subledger reconciliation.** Compare AP, AR, inventory, fixed assets, payroll or other applicable subledgers with the matching control accounts at the same cutoff. Separate timing differences, missing postings, mapping differences and genuine unmatched items. List source keys and aging for each residual. Do not net unrelated debit and credit differences merely to reach zero.
4. **Accrual and provision review.** Inspect supporting basis, service period, calculation, currency, owner, expected settlement and reversal logic. Separate a calculated estimate from a proposed posting. Identify stale items, duplicates, releases and prior estimates already reversed. Apply supplied accounting policy; do not infer recognition or tax treatment from an account label.
5. **Intercompany reconciliation.** Match counterpart entities, invoice/reference, transaction currency, period and gross/net basis. Expose one-sided entries, cutoff differences, FX effects and scope differences separately. Do not eliminate balances solely because totals happen to offset.
6. **Journal support.** For draft adjustments, show entity, ledger, posting period, accounts, currency, debit/credit, explanation, source evidence and reversal date if applicable. Check balance and duplicates against supplied posted/pending entries. Mark each journal draft until the authorized workflow confirms posting. Never invent a journal number or approver.
7. **Analytical review.** Compare current month, prior month, prior year and forecast using consistent scope. Identify threshold breaches in absolute and relative terms; a small denominator may make percentage changes misleading. Separate observed drivers from unsupported causal explanations. Document why each material exception is explained, carried forward or still open.

## Make status evidence-based

Use statuses such as not started, prepared, checked, exception open and reviewer approved. “Prepared” means a calculation or evidence pack exists; “checked” requires recorded verification; “reviewer approved” requires actual reviewer evidence. Do not mark a control complete merely because a file exists or a checkbox is populated.

For each control, record: control ID, purpose, source population, test, tolerance, result, difference, evidence locator, preparer, reviewer status, due date and next action. Use owner roles if names were not supplied. Preserve failed tests and unresolved differences rather than removing them from the final summary. Record follow-up needs without claiming that messages were sent.

Maintain a close bridge when a revised extract arrives: previous reported value, new postings or reversals, mapping/FX changes and revised value. Re-run affected checks on the new version and state which earlier checks remain valid. Do not silently mix pre-adjustment and post-adjustment snapshots.

## Deliver

- A concise close-readiness summary with material open items and coverage limitations.
- A control register showing evidence and current status.
- Account-level reconciliations and an aged exception list.
- Draft adjustment support where requested, clearly separated from posted entries.
- A reviewer handoff with decisions required, responsible roles and due dates.

Use explicit currency and units, keep full precision for calculation and round only presentation. A tolerance is a reporting rule, not permission to erase a residual. A complete checklist is not proof that financial statements comply with a reporting framework; use the organization's authorized review process for that conclusion.

Example request: “Prepare the November close pack from the trial balance, AP aging and accrual register. Reconcile the balances, identify cutoff and reversal issues, and give the reviewer an open-item list with source evidence. Prepare any adjustments as drafts.”

## Edition record

Finance skills 1.0.0; gemini edition; source review 2026-11-25. This date records the package review, not the freshness of a user's business data.
