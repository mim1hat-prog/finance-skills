# Skills

29 skills · version 1.6.0 · reviewed 2026-11-25

Choose one edition. Import its finance suite once for bundled workflows, or import selected individual skills. Suggested Agent Builder groups each contain at most eight skills; they are optional selections, not dependencies.

## Download a complete edition

[Copilot bundle](packages/bundles/finance-skills-copilot.zip?raw=1) · [Gemini bundle](packages/bundles/finance-skills-gemini.zip?raw=1) · [Both editions](packages/bundles/finance-skills-all.zip?raw=1)

Extract a bundle first, then use its individual skill ZIPs or follow its folder-copy guide. The bundle does not provide a bulk native import or automatic activation.

[Excel agent instructions](profiles/excel-agent-instructions.txt) · [Bundle checksums](packages/bundles/manifest.json)

[Tool inventory](TOOLS.md) · [Workflow contracts](docs/SKILL-CONTRACTS.md) · [Research registry](research/README.md)

## One native import for the finance suite

[Copilot suite ZIP](packages/suites/finance-suite-copilot.zip?raw=1) · [Gemini suite ZIP](packages/suites/finance-suite-gemini.zip?raw=1) · [Member hashes and provenance](packages/suites/manifest.json)

Each suite is one native skill named `finance-suite`, with a root `SKILL.md` and 9 category reference files containing all 29 complete workflows. Upload the selected suite ZIP unchanged. The host must be able to read its bundled references; verify this in the target account. This registers one skill, not every workflow separately, and does not increase host limits. Individual packages remain available.

## Copilot in Excel: upload one OneDrive folder

[Download Excel OneDrive folder ZIP](packages/excel/finance-suite-onedrive.zip?raw=1) · [Folder inventory and checksum](packages/excel/manifest.json)

Extract this download first. Use Upload Folder to upload the inner `finance-suite` folder to the OneDrive skills location opened by Excel. Keep `SKILL.md` and all references together, select Refresh in Excel, then invoke `@finance-suite`. This archive is a folder transport, not a native ZIP import. Account activation and workflow execution remain unverified.

## Copy and paste

[Download Markdown-only ZIP](packages/markdown/finance-skills-markdown.zip?raw=1) · [File inventory and checksum](packages/markdown/manifest.json)

60 Markdown files: both editions, Excel agent instructions and a start guide. Extract, open the relevant file, copy its complete contents and paste into an available Instructions field or approved conversation. YAML headers are removed; the full host instructions and shared controls are retained.

[Worked example](examples/QUICKSTART.md) · [Coverage and limitations](metrics/README.md) · [Help](SUPPORT.md) · [Contribute](CONTRIBUTING.md)

## Individual skills

| Skill | Purpose | Copilot | Gemini |
| --- | --- | --- | --- |
| [Excel agent instructions](skills/excel-agent-core/SKILL.md) | Search internal evidence first, preserve workbook logic and return concise results without unsolicited audit tables or new sheets. | [ZIP](packages/copilot/excel-agent-core.zip) | [ZIP](packages/gemini/excel-agent-core.zip) |
| [Work tool routing](skills/work-tool-routing/SKILL.md) | Choose the available tool and finish with evidence. | [ZIP](packages/copilot/work-tool-routing.zip) | [ZIP](packages/gemini/work-tool-routing.zip) |
| [Excel data coverage](skills/excel-data-coverage/SKILL.md) | Check the complete workbook population before drawing conclusions. | [ZIP](packages/copilot/excel-data-coverage.zip) | [ZIP](packages/gemini/excel-data-coverage.zip) |
| [Workforce reconciliation](skills/workforce-reconciliation/SKILL.md) | Reconcile headcount, FTE, transfers and personnel costs. | [ZIP](packages/copilot/workforce-reconciliation.zip) | [ZIP](packages/gemini/workforce-reconciliation.zip) |
| [Forecast variance](skills/forecast-variance/SKILL.md) | Explain budget and forecast differences with reconciled drivers. | [ZIP](packages/copilot/forecast-variance.zip) | [ZIP](packages/gemini/forecast-variance.zip) |
| [Power BI analysis](skills/power-bi-analysis/SKILL.md) | Review model grain, DAX, filter context and control totals. | [ZIP](packages/copilot/power-bi-analysis.zip) | [ZIP](packages/gemini/power-bi-analysis.zip) |
| [Management presentation](skills/management-presentation/SKILL.md) | Build source-backed management slides with a clear decision. | [ZIP](packages/copilot/management-presentation.zip) | [ZIP](packages/gemini/management-presentation.zip) |
| [Business document](skills/business-document/SKILL.md) | Prepare a concise memo, procedure or decision record. | [ZIP](packages/copilot/business-document.zip) | [ZIP](packages/gemini/business-document.zip) |
| [Corporate style](skills/corporate-style/SKILL.md) | Apply the approved company template and visual standards. | [ZIP](packages/copilot/corporate-style.zip) | [ZIP](packages/gemini/corporate-style.zip) |
| [Spreadsheet modeling](skills/spreadsheet-modeling/SKILL.md) | Create auditable models, formulas, pivots and sensitivity views. | [ZIP](packages/copilot/spreadsheet-modeling.zip) | [ZIP](packages/gemini/spreadsheet-modeling.zip) |
| [Analytical SQL](skills/analytical-sql/SKILL.md) | Query local data with explicit grain, joins and null handling. | [ZIP](packages/copilot/analytical-sql.zip) | [ZIP](packages/gemini/analytical-sql.zip) |
| [Evidence research](skills/evidence-research/SKILL.md) | Trace consequential claims to dated primary sources. | [ZIP](packages/copilot/evidence-research.zip) | [ZIP](packages/gemini/evidence-research.zip) |
| [Reproducible analysis](skills/reproducible-analysis/SKILL.md) | Keep transformations, assumptions and checks reproducible. | [ZIP](packages/copilot/reproducible-analysis.zip) | [ZIP](packages/gemini/reproducible-analysis.zip) |
| [Design review](skills/design-review/SKILL.md) | Review clarity, accessibility and layout against the real output. | [ZIP](packages/copilot/design-review.zip) | [ZIP](packages/gemini/design-review.zip) |
| [Project context](skills/project-context/SKILL.md) | Carry decisions and open issues between work sessions. | [ZIP](packages/copilot/project-context.zip) | [ZIP](packages/gemini/project-context.zip) |
| [Video storyboard](skills/video-storyboard/SKILL.md) | Plan a financial explainer with timed scenes and source notes. | [ZIP](packages/copilot/video-storyboard.zip) | [ZIP](packages/gemini/video-storyboard.zip) |
| [Interactive visualization](skills/interactive-visualization/SKILL.md) | Specify and build interactive views with honest scales and labels. | [ZIP](packages/copilot/interactive-visualization.zip) | [ZIP](packages/gemini/interactive-visualization.zip) |
| [Power Query pipeline](skills/power-query-etl/SKILL.md) | Combine recurring exports with schema checks, explicit exclusions and totals that reconcile. | [ZIP](packages/copilot/power-query-etl.zip) | [ZIP](packages/gemini/power-query-etl.zip) |
| [SharePoint evidence](skills/sharepoint-evidence/SKILL.md) | Find approved sources, resolve versions and build a precise internal evidence register. | [ZIP](packages/copilot/sharepoint-evidence.zip) | [ZIP](packages/gemini/sharepoint-evidence.zip) |
| [Account mapping](skills/account-mapping/SKILL.md) | Check dated mappings, duplicate rules and allocation weights before reporting classifications. | [ZIP](packages/copilot/account-mapping.zip) | [ZIP](packages/gemini/account-mapping.zip) |
| [Period-close controls](skills/close-controls/SKILL.md) | Prepare reconciliations, accrual checks and a reviewer handoff with clear evidence and open items. | [ZIP](packages/copilot/close-controls.zip) | [ZIP](packages/gemini/close-controls.zip) |
| [Cash and working capital](skills/cash-working-capital/SKILL.md) | Reconcile cash and aging, calculate aligned DSO/DIO/DPO and separate scenarios from realized cash. | [ZIP](packages/copilot/cash-working-capital.zip) | [ZIP](packages/gemini/cash-working-capital.zip) |
| [Scenario planning](skills/scenario-planning/SKILL.md) | Build traceable driver scenarios, sensitivities and break-even views with explicit assumptions. | [ZIP](packages/copilot/scenario-planning.zip) | [ZIP](packages/gemini/scenario-planning.zip) |
| [Document extraction](skills/document-extraction/SKILL.md) | Turn report tables and statements into traceable data with OCR exceptions and source locators. | [ZIP](packages/copilot/document-extraction.zip) | [ZIP](packages/gemini/document-extraction.zip) |
| [Finance process diagrams](skills/process-diagram/SKILL.md) | Explain data flows, ownership, review gates and exception paths with compact diagrams. | [ZIP](packages/copilot/process-diagram.zip) | [ZIP](packages/gemini/process-diagram.zip) |
| [Connected reporting](skills/connected-reporting/SKILL.md) | Validate report context, ordered upload coordinates and independent readback. | [ZIP](packages/copilot/connected-reporting.zip) | [ZIP](packages/gemini/connected-reporting.zip) |
| [Provision and warranty reconciliation](skills/provision-reconciliation/SKILL.md) | Reconcile movement components and frozen versions, retaining residuals and missing confirmations. | [ZIP](packages/copilot/provision-reconciliation.zip) | [ZIP](packages/gemini/provision-reconciliation.zip) |
| [FX and allocation preflight](skills/fx-allocation-preflight/SKILL.md) | Separate FX sensitivity, accounting scope and allocation preconditions. | [ZIP](packages/copilot/fx-allocation-preflight.zip) | [ZIP](packages/gemini/fx-allocation-preflight.zip) |
| [Public benchmark lookup](skills/benchmark-lookup/SKILL.md) | Query rights-cleared public snapshots with explicit units, freshness and information vintage. | [ZIP](packages/copilot/benchmark-lookup.zip) | [ZIP](packages/gemini/benchmark-lookup.zip) |

## Suggested Agent Builder groups

### Agent Defaults

`excel-agent-core`.

### Core

`work-tool-routing`, `excel-data-coverage`, `workforce-reconciliation`, `forecast-variance`, `power-bi-analysis`, `management-presentation`, `business-document`, `corporate-style`.

### Extended

`spreadsheet-modeling`, `analytical-sql`, `evidence-research`, `reproducible-analysis`, `design-review`, `project-context`, `video-storyboard`, `interactive-visualization`.

### Specialist

`power-query-etl`, `sharepoint-evidence`, `account-mapping`, `close-controls`, `cash-working-capital`, `scenario-planning`, `document-extraction`, `process-diagram`.

### Workflow Pilots

`connected-reporting`, `provision-reconciliation`, `fx-allocation-preflight`, `benchmark-lookup`.

