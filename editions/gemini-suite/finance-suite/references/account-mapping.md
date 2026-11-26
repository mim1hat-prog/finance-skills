# Account and reporting mapping

Validate or apply the requested mapping from source records to reporting categories. Treat the supplied approved mapping as business logic, not a suggestion to guess missing classifications. Use available spreadsheet, SQL or Python tools for actual calculation. If execution is unavailable, return the exact necessary formulas or query and mark them unexecuted; include a proposed mapping table only when a mapping change or table is requested. Do not create a separate audit artifact.

## Define the mapping contract

Confirm the source grain and key, target hierarchy, entity scope, effective-date basis, currency and amount sign. Include every field needed to distinguish a rule, such as account, entity, cost centre, product, ledger or scenario. Preserve identifier text and leading zeros. Record trimming, case normalization and aliases; do not remove punctuation or merge codes without an agreed rule.

Capture the mapping owner/version, approval evidence if supplied, effective-from and effective-to dates, target category, rule type and any explicit priority. Choose and document interval semantics; for example, inclusive start and exclusive end. Convert other date conventions visibly before comparing rules.

Distinguish these relationships:

- Many source accounts to one reporting category is a normal aggregation if each source row has one valid destination.
- One source row to multiple categories requires an explicit allocation rule and valid weights.
- Multiple full-value matches for the same source row are ambiguous until a documented rule resolves them.
- Roll-up ancestors in a hierarchy are presentation levels; do not count a leaf amount again as a second allocation.

## Validate before applying

1. **Inspect keys and targets.** Report blank keys, unknown target codes, invalid hierarchy parents, cycles and orphan categories. Check reserved/unmapped buckets separately from actual accounts. Do not manufacture a target because its label looks similar.
2. **Find duplicate rules.** Count exact duplicate rows and conflicting rules sharing the same key and active interval. Even identical duplicate rules can multiply values after a join. Propose removal or normalization with the affected count and source references; do not silently discard them or create an unsolicited audit trail.
3. **Check time and scope overlaps.** For each relevant key, detect overlapping effective intervals and wildcard/range rules that can match the same record. An overlap requires both date and scope evaluation. A general rule and an entity-specific rule can coexist only with documented precedence. Do not choose the first row or newest file arbitrarily.
4. **Validate ranges.** Treat code ranges as numeric only when the source identifiers are defined as numeric. Lexical order and numeric order can differ. Test boundary accounts and dates, including an effective-date change and a missing date.
5. **Validate allocations.** Require numeric, finite, non-negative weights unless an explicitly approved method permits signed weights. Confirm whether weights are fractions or percentages. For each source key and active allocation set, the weights must sum to one within a stated tolerance. Check for missing targets, duplicate destination lines and incomplete sets. Do not normalize 0.95 to 1.00 automatically; expose the missing 5%.
6. **Measure match cardinality.** For each source record, retain its identifier, candidate rule IDs and number of matches. Classify it as one-to-one mapped, valid allocation, unmapped or ambiguous. Fuzzy text matches are review suggestions only; never use them as approved ledger classification.

## Apply and reconcile

For a unique rule, carry the full source amount to its target. For a valid allocation, calculate `allocated amount = source amount × weight` using sufficient precision and apply the agreed currency rounding only at the defined stage. If rounding leaves a residual, show it separately or use a documented approved remainder method. Do not bury it in the largest category.

Keep source amount, target amount, mapping rule ID/version, effective date, weight and source locator so the output can be traced back. Quarantine ambiguous records rather than duplicating their full value. Retain unmapped records in an exception population; excluding them from the report does not remove their value from the reconciliation.

Reconcile by period, entity and currency:

`source total = uniquely mapped total + valid allocated total + unresolved source amount`

The unresolved source amount counts each source record once. Report ambiguous and unmapped subsets separately. Check positive, negative and absolute-value totals as well as net totals so offsetting mistakes are visible. Use row counts and distinct source keys to expose multiplication. Do not sum currencies without an explicit conversion basis.

For a mapping change, apply old and proposed rules to the same source population and build a reclassification bridge. Separate changed classification from changed source data or FX. State the amount moved between categories, the effect on subtotals and unchanged overall total, or explain the residual. A successful reconciliation does not establish that the business classification is approved.

## Deliver

Return the requested mapped result, correction, or reproducible query/formulas with execution status. Include concise mapping/version references, the reconciliation difference, and material unresolved rules or records needed to act. Keep routine rule-quality and match-cardinality checks internal; create a rule register, full exception table, audit trail, or separate report only when specifically requested. Preserve every unresolved amount in the calculation even when the answer describes exceptions concisely.

Example request: “Map these ledger lines to the reporting hierarchy using the dated mapping table. Check overlapping rules and 60/40 allocations, show every unresolved account, and prove that totals reconcile before and after mapping.”
