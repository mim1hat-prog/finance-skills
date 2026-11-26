# Tool and capability inventory

Reviewed 2026-11-25 · 30 entries.

One skill per finance workflow; tools supply the capabilities available in the approved session. This inventory does not install products, activate connections or certify native integrations.

Start with Excel/Power Query, planning-report coordinates and SAP/BW export validation. Then verify Power BI/Fabric freshness and release visibility. Use approved work sources for authority and ownership.

## Availability labels

- **user-reported:** The user reported access; native integration was not tested here.
- **partial-user-reported:** Python or Microsoft 365 Copilot was reported; SQL connections or Copilot Studio availability still require verification.
- **confirm-at-work:** Product, version, licensing, permissions and enabled capabilities must be confirmed.
- **optional-evaluation:** Candidate only; not assumed installed or approved.
- **capability-only:** The underlying proprietary software is not verified.
- **local-implementation:** Code exists in this repository; a helper or service runs only when explicitly started locally. No native host execution is implied.

## Core finance

### Microsoft Excel

**P0 · user-reported · instructions-and-export-checks**

Models, reconciliation, pivots and upload preparation.

Trace formulas, named ranges, tables and pivots to the source. Preserve unrelated workbook structure; distinguish saved caches from evaluated formulas.

**Evidence required:** Workbook/version; formula and recalculation evidence; approved scope.

**Workflow skills:** [excel-agent-core](skills/excel-agent-core/SKILL.md), [excel-data-coverage](skills/excel-data-coverage/SKILL.md), [spreadsheet-modeling](skills/spreadsheet-modeling/SKILL.md), [workforce-reconciliation](skills/workforce-reconciliation/SKILL.md), [provision-reconciliation](skills/provision-reconciliation/SKILL.md).

### Microsoft Power Query

**P0 · confirm-at-work · instructions-and-export-checks**

Repeatable ingestion and repair of existing queries.

Inspect the dependency chain and accepted baseline. Return complete affected M; validate protected rows and ordered schema.

**Evidence required:** Query/dependency text; source-selection rules; native refresh and downstream parity.

**Workflow skills:** [power-query-etl](skills/power-query-etl/SKILL.md), [account-mapping](skills/account-mapping/SKILL.md).

**Source registry:** `tool-power-query`.

### IBM Planning Analytics / TM1 / PAfE

**P0 · confirm-at-work · instructions-and-export-checks**

Planning-cube reports and staged uploads.

Identify report type and writeback mode before editing. Preserve managed regions and compare complete target intersections.

**Evidence required:** Installed version and report type; model/cube and ordered dimensions; known-good read and independent readback.

**Workflow skills:** [connected-reporting](skills/connected-reporting/SKILL.md), [provision-reconciliation](skills/provision-reconciliation/SKILL.md), [fx-allocation-preflight](skills/fx-allocation-preflight/SKILL.md).

**Source registry:** `tool-planning-analytics`, `tool-planning-writeback`.

### SAP ERP / SAP S/4HANA: FI, CO and CO-PA

**P0 · confirm-at-work · instructions-and-export-checks**

Ledger, cost/profit centers, costing, inventory and allocation extracts.

Validate accounting grain, scope, effective masters and duplicates. Prepare allocation checks without posting or substituting locked objects.

**Evidence required:** Ledger/period/currency; approved extract and document keys; master validity and execution evidence.

**Workflow skills:** [close-controls](skills/close-controls/SKILL.md), [account-mapping](skills/account-mapping/SKILL.md), [fx-allocation-preflight](skills/fx-allocation-preflight/SKILL.md), [connected-reporting](skills/connected-reporting/SKILL.md).

### SAP BW / Analysis for Microsoft Office

**P0 · confirm-at-work · instructions-and-export-checks**

Repeatable reporting and workbook-based analysis.

Capture variables, filters, hierarchies and units. Compare equal selections and distinguish saved values from refresh.

**Evidence required:** Report variables and key date; source update and workbook refresh evidence; aggregation level.

**Workflow skills:** [connected-reporting](skills/connected-reporting/SKILL.md), [excel-data-coverage](skills/excel-data-coverage/SKILL.md).

**Source registry:** `tool-sap-analysis`.

### Power BI Desktop / Service, DAX and Power Query

**P1 · user-reported · instructions-and-export-checks**

Semantic models and finance dashboards.

Trace measures, filters, source dependencies and detailed totals. Separate data refresh, publication and reader visibility.

**Evidence required:** Model grain/relationships; DAX and filter context; source/model/visual refresh evidence.

**Workflow skills:** [power-bi-analysis](skills/power-bi-analysis/SKILL.md), [power-query-etl](skills/power-query-etl/SKILL.md), [forecast-variance](skills/forecast-variance/SKILL.md).

**Source registry:** `tool-power-bi`.

### Microsoft Fabric

**P1 · confirm-at-work · instructions-and-export-checks**

Dataflows, pipelines, notebooks and lakehouse tables.

Locate the first stale/failed dependency. Validate keys, period coverage, corrections and incremental-refresh assumptions.

**Evidence required:** Actual lineage and coverage limits; run status and source snapshot; downstream control totals.

**Workflow skills:** [power-bi-analysis](skills/power-bi-analysis/SKILL.md), [power-query-etl](skills/power-query-etl/SKILL.md), [reproducible-analysis](skills/reproducible-analysis/SKILL.md).

**Source registry:** `tool-fabric`.


## Workflow and delivery

### SharePoint / OneDrive

**P0 · user-reported · instructions-and-export-checks**

Authoritative files, approved templates and version history.

Resolve working versus approved or frozen copies. Preserve permissions and keep work files outside the public repository.

**Evidence required:** Source locator/version; approval or submission evidence; actual access scope.

**Workflow skills:** [sharepoint-evidence](skills/sharepoint-evidence/SKILL.md), [evidence-research](skills/evidence-research/SKILL.md), [project-context](skills/project-context/SKILL.md).

### Teams / Outlook / OneNote

**P1 · confirm-at-work · instructions-and-export-checks**

Handoffs, decisions, deadlines and confirmations.

Find the authoritative decision, role, deadline and next action. Keep agreed, implemented and confirmed complete separate.

**Evidence required:** Message/document version; owner role and effective decision; numeric evidence from approved sources.

**Workflow skills:** [project-context](skills/project-context/SKILL.md), [sharepoint-evidence](skills/sharepoint-evidence/SKILL.md), [close-controls](skills/close-controls/SKILL.md), [provision-reconciliation](skills/provision-reconciliation/SKILL.md).

### Microsoft Forms / Power Automate

**P1 · confirm-at-work · candidate-only**

Structured submissions, routing and notifications.

Validate fields and duplicate-notification controls. Distinguish a draft action from a send and inspect failed connections.

**Evidence required:** Flow ownership/connections; approved routing and action scope; independent completion receipt.

**Workflow skills:** [work-tool-routing](skills/work-tool-routing/SKILL.md), [close-controls](skills/close-controls/SKILL.md), [project-context](skills/project-context/SKILL.md).

### Microsoft PowerPoint

**P1 · confirm-at-work · instructions-and-export-checks**

Editable decision slides and management commentary.

Use validated figures and the approved template. Keep baseline and signs consistent; state driver, impact and decision.

**Evidence required:** Source tie-out; audience/template; actual editable output.

**Workflow skills:** [management-presentation](skills/management-presentation/SKILL.md), [corporate-style](skills/corporate-style/SKILL.md), [forecast-variance](skills/forecast-variance/SKILL.md).

### Microsoft 365 Copilot / Copilot Studio

**P0 · partial-user-reported · instructions-and-export-checks**

Agent entry point, retrieval and orchestration.

Route by finance workflow and available capabilities. Separate retrieval, calculation, preparation and action authorization.

**Evidence required:** Actual host and enabled tools; approved connection scope; native task verification.

**Workflow skills:** [work-tool-routing](skills/work-tool-routing/SKILL.md), [excel-agent-core](skills/excel-agent-core/SKILL.md), [connected-reporting](skills/connected-reporting/SKILL.md).

**Source registry:** `tool-m365`.

### Gemini Apps / approved Gems

**P0 · user-reported · instructions-and-export-checks**

Alternative skill entry point and snapshot analysis.

Use the account-supported skill or Instructions route. Inspect approved exports when enterprise/native capabilities are absent.

**Evidence required:** Actual account features; authorized input files; import and representative task.

**Workflow skills:** [work-tool-routing](skills/work-tool-routing/SKILL.md), [excel-agent-core](skills/excel-agent-core/SKILL.md), [benchmark-lookup](skills/benchmark-lookup/SKILL.md).

### Git / GitHub Enterprise / GitHub Desktop

**P0 · confirm-at-work · local-code**

Versioned code, skills, fixtures and releases.

Track canonical changes and run deterministic release gates. Keep live company configuration and artifacts out of shareable history.

**Evidence required:** Current branch/head; reviewed diff and test results; authorized publication destination.

**Workflow skills:** [project-context](skills/project-context/SKILL.md), [reproducible-analysis](skills/reproducible-analysis/SKILL.md).

### Visual Studio Code

**P1 · user-reported · local-code**

Editing and running reviewed local scripts.

Use the approved local interpreter. Distinguish editor availability from coding-agent subscriptions or production access.

**Evidence required:** Interpreter and dependencies; input/output scope; actual execution result.

**Workflow skills:** [reproducible-analysis](skills/reproducible-analysis/SKILL.md), [power-query-etl](skills/power-query-etl/SKILL.md), [analytical-sql](skills/analytical-sql/SKILL.md).


## Additional analytics

### Python / SQL

**P0 · partial-user-reported · local-code**

Deterministic checks over authorized exports.

Validate schemas, joins, mappings, weights and row-level residuals. Run synthetic regressions before considering a live connection.

**Evidence required:** Local interpreter or approved SQL engine; dataset and explicit grain; actual execution and input immutability.

**Workflow skills:** [reproducible-analysis](skills/reproducible-analysis/SKILL.md), [analytical-sql](skills/analytical-sql/SKILL.md), [account-mapping](skills/account-mapping/SKILL.md), [connected-reporting](skills/connected-reporting/SKILL.md).

### DuckDB

**P1 · optional-evaluation · local-code**

Local SQL on approved CSV/Parquet exports.

Use the optional pinned local helper or reviewed query. Reconcile scope and keys without claiming a size/performance guarantee.

**Evidence required:** Approved installation; exact file/schema; full-population controls.

**Workflow skills:** [analytical-sql](skills/analytical-sql/SKILL.md), [reproducible-analysis](skills/reproducible-analysis/SKILL.md).

### KNIME Analytics Platform

**P2 · optional-evaluation · candidate-only**

Maintainable low-code preparation and joins.

Evaluate only when the team can maintain and approve the workflow.

**Evidence required:** Available licensed/approved environment; workflow ownership; known-good outputs and failure cases.

**Workflow skills:** [power-query-etl](skills/power-query-etl/SKILL.md), [reproducible-analysis](skills/reproducible-analysis/SKILL.md).

### Databricks SQL / Unity Catalog

**P2 · optional-evaluation · candidate-only**

Governed SQL, lineage and reusable datasets.

Add an adapter only for actual approved datasets and permissions.

**Evidence required:** Dataset identifiers kept private; approved connection; lineage and query controls.

**Workflow skills:** [analytical-sql](skills/analytical-sql/SKILL.md), [power-bi-analysis](skills/power-bi-analysis/SKILL.md).

### SAP Analytics Cloud / SAP Datasphere

**P2 · optional-evaluation · candidate-only**

Optional semantic modeling and scenario analysis.

Evaluate integration against the established reporting process.

**Evidence required:** Available services and models; approved source/semantic definitions; process-owner acceptance.

**Workflow skills:** [scenario-planning](skills/scenario-planning/SKILL.md), [connected-reporting](skills/connected-reporting/SKILL.md).

### Microsoft Power Apps

**P2 · optional-evaluation · candidate-only**

Structured exception intake and confirmations.

Keep analytical review, approvals and writes distinct.

**Evidence required:** Approved app/flow ownership; access and routing; write and readback controls.

**Workflow skills:** [work-tool-routing](skills/work-tool-routing/SKILL.md), [close-controls](skills/close-controls/SKILL.md).

### REST / OpenAPI / SDMX / CSV

**P1 · local-implementation · local-code**

Public benchmark dataset and read-only local API.

Query validated immutable snapshots without provider calls per request. Preserve series, units, periods, rights, vintage and transformation lineage.

**Evidence required:** Rights-reviewed source; series and snapshot ID; freshness and as-of availability.

**Workflow skills:** [benchmark-lookup](skills/benchmark-lookup/SKILL.md), [forecast-variance](skills/forecast-variance/SKILL.md), [fx-allocation-preflight](skills/fx-allocation-preflight/SKILL.md).

**Source registry:** `openapi-3.1`, `rfc9457`, `ecb-exr-api`.


## Unverified product: capability labels

### Close task tracker

**P1 · capability-only · candidate-only**

Deadlines, dependencies and completion evidence.

Keep ready, transferred, reviewed and closed separately evidenced.

**Evidence required:** Approved calendar and task version; owner role and completion receipt.

**Workflow skills:** [close-controls](skills/close-controls/SKILL.md).

### Workforce planning system

**P1 · capability-only · candidate-only**

Headcount, FTE, hiring status and movements.

Separate staffing approval from confirmed forecast movement.

**Evidence required:** Effective population and dates; approved movement status.

**Workflow skills:** [workforce-reconciliation](skills/workforce-reconciliation/SKILL.md).

### Cost-driver planning system

**P1 · capability-only · candidate-only**

Assumptions, baselines and overrides.

Verify the exact version used by the forecast.

**Evidence required:** Approved assumption version; scope and source snapshot.

**Workflow skills:** [forecast-variance](skills/forecast-variance/SKILL.md), [scenario-planning](skills/scenario-planning/SKILL.md).

### Customer forecast or order feed

**P1 · capability-only · candidate-only**

Product demand and short-horizon schedules.

Keep orders, customer forecasts and approved financial forecasts distinct.

**Evidence required:** Product-level grain; period/version and demand category.

**Workflow skills:** [forecast-variance](skills/forecast-variance/SKILL.md).

### Warranty or claims system

**P1 · capability-only · candidate-only**

Case status, ownership and confirmations.

Do not infer reserves, invoices or payments from operational status.

**Evidence required:** Case owner, requested scope and confirmation date; separate numeric support.

**Workflow skills:** [provision-reconciliation](skills/provision-reconciliation/SKILL.md).

### Master-data and access workflow

**P1 · capability-only · candidate-only**

Approved mappings, validity, locks and permissions.

Stop on missing approval or locks without substituting objects.

**Evidence required:** Approved mapping/version; effective dates and permission/lock evidence.

**Workflow skills:** [account-mapping](skills/account-mapping/SKILL.md), [fx-allocation-preflight](skills/fx-allocation-preflight/SKILL.md).

### Transfer-pricing or allocation system

**P1 · capability-only · candidate-only**

Approved rules, run parameters and receipts.

Check configuration and totals separately from actual execution.

**Evidence required:** Approved sender/receiver sets; weights and prior-run status; independent receipt/readback.

**Workflow skills:** [fx-allocation-preflight](skills/fx-allocation-preflight/SKILL.md), [connected-reporting](skills/connected-reporting/SKILL.md).


## Local maintenance

### Synthetic skill evaluation kit

**P1 · local-implementation · local-code**

Reproducible development checks for manual baseline-versus-suite comparisons.

Validate versioned invented prompts and separate answer keys. Initialize an unrun plan, then grade manually recorded structured outputs without contacting a model. Report every scheduled status and keep repeated runs separate from unique cases.

**Evidence required:** Case-set version and file hashes; Host, visible model, tool settings and package identity; Actual outputs and independently reviewable provenance; a filled record alone cannot prove native execution.

**Workflow skills:** [reproducible-analysis](skills/reproducible-analysis/SKILL.md), [forecast-variance](skills/forecast-variance/SKILL.md), [close-controls](skills/close-controls/SKILL.md), [account-mapping](skills/account-mapping/SKILL.md), [benchmark-lookup](skills/benchmark-lookup/SKILL.md).

**Source registry:** `joss-review-criteria`.

## Connection boundary

Use an approved existing connection when available. This repository provides generic interfaces and export checks, not tenant endpoints, credentials, master data or live enterprise connectors. A cloud assistant cannot automatically reach the local public-benchmark API. Public deployment or a company connector requires its own reviewed integration.

[Machine-readable inventory](tools/catalog.json) · [Source registry](research/README.md) · [Workflow contracts](docs/SKILL-CONTRACTS.md)

