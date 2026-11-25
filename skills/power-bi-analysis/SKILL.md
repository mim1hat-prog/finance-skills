---
name: power-bi-analysis
description: "Analyze or draft Power BI measures, DAX, Power Query transformations, and semantic-model checks for headcount, FTE, workforce cost, actual-versus-plan, and management reporting. Use when a measure has wrong totals, duplicate counts, filter-context issues, or a reporting definition needs implementation."
---

# Power BI analysis

For freshness or release checks, trace the available source-to-report dependencies through queries/dataflows, semantic model measures, report filters and intended audience. Check upstream period coverage and corrections as well as the latest successful refresh event. Separate source refresh, semantic model refresh, report publication and changes actually visible to readers. A lineage view is evidence about the dependencies it exposes, not proof that every upstream or cross-workspace dependency was inspected.

Produce an explainable model change or analysis from the actual model definition and business question. This skill can assist in Copilot or Gemini using supplied schema and measures. It does not enable Power BI access, refresh a dataset, or install a skill into Power BI itself.

## Inputs

Read the relevant tables, columns, data types, keys, relationships, existing measures, date/calendar definition, reporting period, refresh timestamp, and expected business result. Use supplied schema, model exports, examples, or an enabled capability. Ask for only the missing pieces needed for the specific measure; do not request a complete employee dataset when a schema and anonymized example suffice.

Establish these definitions before calculating:

- Population and grain: person, assignment, contract, position, transaction, or person-period snapshot.
- Metric: distinct headcount, contractual FTE, paid hours, average FTE, or monetary cost.
- Time basis: closing snapshot, average during a period, or sum of flows; fiscal calendar and effective-date boundaries.
- Currency, conversion basis, unit scale, actual/plan scenario, and favorable/unfavorable convention.
- Handling of blanks, unmapped keys, zero denominators, starters/leavers, transfers, and concurrent assignments.

## Workflow

1. Reproduce the issue at a named filter context: period, entity, cost center, scenario, and relevant slicers. Record the observed value and independent expected value if supplied. A screenshot alone cannot establish model relationships or full data coverage.
2. Inspect the model grain and relationship cardinality/direction. Check dimension-key uniqueness, unmatched fact keys, inactive relationships, and many-to-many paths before changing DAX. Keep a stable fact/dimension model where appropriate. Do not recommend bidirectional relationships as an unexplained fix for a bad total.
3. Select the correct calculation layer. Use Power Query for repeatable source shaping and type handling. Use a measure for context-dependent aggregations; use a calculated column only when row-level stored values are needed. Explain the choice briefly.
4. Write DAX or M against observed table/column names. If names are missing, label the code as a template and list the mappings needed; do not present placeholders as runnable code. Preserve existing security filters and do not remove filters merely to force agreement with a desired answer.
5. Make aggregation semantics explicit. Distinct people are not generally additive across cost centers or months. Snapshot FTE must not be summed across periods unless the metric is explicitly FTE-periods. Compute ratios from appropriate numerator/denominator aggregates, not a simple average of row ratios unless that is the requested definition.
6. Handle blank or zero denominators deliberately. DAX `DIVIDE(numerator, denominator)` defaults to BLANK when division is undefined; provide a different constant result only when the business definition supports it. Do not relabel missing data as zero actuals.
7. Explain filter context, any context transition, and which date relationship the measure uses. Where a calculation changes filters, name the exact filters retained and removed. Do not claim a grand total should equal displayed rows when the metric is non-additive.
8. Validate with independently understandable cases: one period/entity, a known employee with multiple assignments, a transfer, a missing key, a zero/blank denominator, multiple periods, and the total. Use the cases relevant to this metric. Compare monetary/FTE totals to a separately calculated source control; use explicit rounding tolerance.
9. Run queries or apply changes only if the session exposes the authorized capability. Otherwise return the code, insertion location, and validation steps with **not executed in the model** clearly stated. Do not infer refresh, publication, access, or row-level-security testing from a syntactically plausible formula.

## Output

Provide:

1. The metric definition and the reason for the discrepancy or proposed change.
2. DAX or Power Query code with exact model names, or a clearly labeled template.
3. A short explanation of grain, aggregation, time basis, and relevant filters.
4. Concise material exceptions or failed/unperformed checks that affect the measure. Keep case-by-case validation internal unless the user requests it; do not add a validation table or log by default. Mark unsupported expected results as unknown.
5. Material unresolved data quality, model access, refresh, or security checks.

Keep the deliverable in the approved work environment. Use aggregated or synthetic examples in explanations that do not require personal records. Do not publish model schemas, connection strings, employee rows, or work measures into a public skill repository.

## Quality checks

- Confirm all identifiers and data types against the available schema.
- Check headcount versus FTE and stock versus flow before checking arithmetic.
- Reconcile at the same filters, currency, reporting date, and source revision.
- Distinguish a formula review, an executed query, an independently reconciled result, and a published model. Report only the achieved level.
- Preserve row-level-security assumptions; test access roles only through an available authorized testing capability.

## Reference guidance

Use the following official references when documentation access is available; the workflow above remains usable without fetching them:

- [Microsoft: star schema guidance](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [Microsoft: DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax)

## Example prompt

“Use power-bi-analysis to review this monthly FTE measure. The total across three months is triple the expected closing FTE. Here are the snapshot grain, date relationship, DAX, and an anonymized sample. Propose the corrected measure, explain the total behavior, and list the checks you actually ran.”
