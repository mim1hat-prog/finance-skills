# Further implementation priorities

Version 1.2.0 contains 29 skills, shared workflow contracts, a public benchmark dataset and a research registry. The next useful work is to validate those methods in the actual approved work environment, with company-only details kept private. Local checks and generic instructions are already implemented; live connections and enterprise acceptance are separate work.

## Next acceptance work

Prioritize the two [workflow pilots](WORKFLOWS.md): provision calculation through detailed reporting readback, and a workforce/Power Query change that preserves the accepted artifact contract. Use actual approved sources and native capabilities inside the work environment. Keep every resulting private contract, example and acceptance record outside this public repository.

For public benchmarks, complete the exact METI transport-equipment source/code selection and distinguish it from vehicle counts. Then select the MHLW/e-Stat wage and hours table/classifications, with approved application-ID handling. BOJ reproduction remains permission-gated. Trade flows and recall alerts remain future candidates; they require separate source, coverage and rights review before implementation. Keep one shared benchmark lookup and provider adapters rather than adding a skill per feed.

The professional standards are implemented in [STANDARDS.md](STANDARDS.md). Further research adds value when it resolves a particular method decision or test; source counts alone are not a quality target.

| Priority | Next implementation | Why it earns its place | Completion evidence |
| --- | --- | --- | --- |
| 1 | Private finance data contract | Stable columns, grain, period cutoffs, units, identifiers and mapping versions eliminate repeated ambiguity | A supplied export passes known row/amount controls; bad schema and duplicate periods fail visibly |
| 2 | SharePoint-to-Power Query monthly refresh | Your existing SharePoint and Power BI can support a repeatable reporting input | Exact folder/file filters, source lineage, refresh timestamp, schema checks and reconciled totals |
| 3 | Power BI measure tie-outs | A DAX expression can parse while producing the wrong total under filters | A small approved reference dataset; expected totals at company/entity/cost-centre/time levels; explicit distinct-count and FTE rules |
| 4 | Effective-dated mapping register | Account and organization changes are a frequent source of reporting differences | Approved owner/version; overlap, allocation and unmatched exceptions; reclassification bridge using unchanged source data |
| 5 | Monthly commentary with evidence | Commentary becomes more useful when every stated driver has an amount and a source | Each material claim links to a reconciled driver and source; arithmetic contribution is distinguished from demonstrated cause |
| 6 | Close evidence index in approved SharePoint | The team can retrieve what supported a conclusion after the reporting cycle | Versioned source links, period, owner, preparation/review status and unresolved differences; no invented sign-offs |
| 7 | Measured local large-file workflow | DuckDB can avoid a spreadsheet-first workflow for larger extracts | Measure your actual file size, RAM, runtime and output checks; document when CSV profiling, DuckDB or Power Query is the better route |
| 8 | Explainable anomaly review | Reproducible prioritization can focus investigation on meaningful exceptions | Stated baseline/seasonality/materiality, sensitivity checks and source rows; no unsupported fraud or employee-performance conclusions |

## Already implemented from the expanded review

- **Power Query ETL:** filtered ingestion, file/row scope, schema/locale checks and control totals.
- **SharePoint evidence:** exact source/version provenance and access-aware research.
- **Account mapping:** cardinality, effective dates, allocations and unresolved-value reconciliation.
- **Close controls:** balances, evidence, exceptions and proposed adjustments without claiming ERP posting.
- **Cash and working capital:** cash versus balance movement, aging, denominator alignment and modeled improvements.
- **Scenario planning:** independent drivers, units, assumptions and sensitivity checks.
- **Document extraction:** layout/OCR/table checks with source locators and completeness limits.
- **Process diagram:** owners, transformations, evidence and decision points.

## Optional upstream capabilities

Hallmark and Impeccable can support repository/UI review in a coding environment. Anthropic's xlsx resources can support an approved local workbook pipeline. MarkItDown can support local extraction after its formats/dependencies are checked. Select scientific modules for a defined statistical question instead of importing the entire collection.

Claude-mem requires a supported coding host and local runtime; a manual project-context skill remains useful without it. HyperFrames is appropriate when a rendered video is actually needed; a finance storyboard is useful before installing a renderer. Valyu requires separate approved API access. D3 is valuable for a visualization that needs custom interaction; use Power BI's existing capabilities first when they already meet the task.

These are implementation choices based on the available software and reviewed primary sources, not an assertion that all tools are installed or enabled in the work tenant. [Source decisions and requirements](UPSTREAMS.md)
