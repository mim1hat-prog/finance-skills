# Finance Agent Skills for Microsoft 365 Copilot and Gemini

[![Copilot edition](https://img.shields.io/badge/Copilot-edition-245844?style=flat)](docs/COPILOT.md) [![Gemini edition](https://img.shields.io/badge/Gemini-edition-245844?style=flat)](docs/GEMINI.md) [![License MIT](https://img.shields.io/badge/license-MIT-4C5054?style=flat)](LICENSE)

[Quick start](#quick-start) | [All skills](SKILLS.md) | [Coverage](metrics/README.md) | [Downloads & releases](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/README.md) | [Copilot setup](docs/COPILOT.md) | [Gemini setup](docs/GEMINI.md) | [Get help](SUPPORT.md) | [Contribute](CONTRIBUTING.md)

![Finance skills: from source to decision, with Copilot and Gemini editions](assets/readme-banner.svg)

**Open-source finance agent skills for Excel reconciliation, FP&A, forecasting, financial controlling and management reporting.** The library contains 29 skills: 28 task workflows and your Excel agent instructions. One maintained source library generates separate Microsoft 365 Copilot and Gemini editions, with optional Python and Power BI workflows for Windows.

Supply the relevant work files in your approved account and ask for the result you need. The instructions prioritize relevant internal evidence, preserve existing business logic and verify calculations without adding unsolicited audit tables, worksheets or process commentary. They work without a local coding agent or an API subscription. Python, Power BI, VS Code and SharePoint provide additional routes when those capabilities are available.

## Quick start

1. **Download and extract the [Markdown-only ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-markdown.zip).** Choose the `copilot/` or `gemini/` folder.
2. **Open one relevant `.md` file and copy all its text** into your available Instructions field or approved conversation. Start with `forecast-variance`, `excel-data-coverage` or `account-mapping`.
3. **Try the [invented reconciliation example](examples/QUICKSTART.md).** Its two tiny CSVs reconcile from 350.30 to 365.35, with an explicit 15.05 difference and two unmatched records. The expected result lets you check the assistant before using a work task.

For native skill imports, use the [Copilot guide](docs/COPILOT.md) or [Gemini guide](docs/GEMINI.md). Microsoft 365 Copilot and Gemini Apps are the primary instruction targets; GitHub Copilot and Gemini CLI are separate products. Account availability and permissions still determine which host features you can use.

## Ready to download · v1.4.0

**[Download Markdown only — ready to copy and paste](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-markdown.zip)** — 60 `.md` files: 29 Copilot skills, 29 Gemini skills, your Excel agent instructions and a short start guide. Each skill keeps its complete edition-specific instructions; YAML headers are removed.

Extract the ZIP, open the relevant file in VS Code or Notepad, copy all its contents and paste into your available agent/Gem **Instructions** field or an approved conversation. Choose one relevant workflow at a time. This download contains only Markdown files, with no scripts, datasets or nested ZIPs.

**[Download the full release](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-full.zip)** — both editions, every individual skill package, Excel agent instructions, setup guides, source files, local Python tools, tests and the dot catalogue.

| Package | Contents | Download |
| --- | --- | --- |
| Markdown only | 60 Markdown files, ready to copy and paste | [Markdown v1.4.0 ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-markdown.zip) |
| Copilot | 29 individual skill ZIPs, matching skill folders and Excel agent instructions | [Copilot v1.4.0 ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-copilot.zip) |
| Gemini | 29 individual skill ZIPs, matching folders, Gem-ready text and Excel agent instructions | [Gemini v1.4.0 ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-gemini.zip) |
| All skills | Both editions: 58 individual ZIPs, skill folders, Gem-ready text and Excel agent instructions | [All skills v1.4.0 ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-all.zip) |
| Full release | All skills plus the complete useful project, guides and optional local tools | [Full v1.4.0 ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.4.0/finance-skills-v1.4.0-full.zip) |

**For native skill packages, extract the outer ZIP first.** Then import the individual skill ZIPs you need, or follow the Office folder-copy instructions. A complete download does not bulk-install or activate skills in your account. Edition/all-skills bundles contain instructions and packages; choose the full release for local Python tools and offline guides.

[Release notes and checksums](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/v1.4.0/README.md) · [All releases](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/README.md) · [Versioning and verification](docs/RELEASES.md)

## Your Excel agent instructions

**[Download ready-to-paste instructions](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/profiles/excel-agent-instructions.txt)** and paste the text into the **Instructions** field you already use for your Excel agent. Review it alongside any company-specific instructions before saving.

The profile searches relevant available internal sources first, retries incomplete retrieval, preserves workbook logic, checks the result and keeps the response concise. It requests no audit tables, extra worksheets or audit text unless you ask for them. It does not claim access to sources your account cannot reach.

You can also import the individual `excel-agent-core` skill: [Copilot ZIP](packages/copilot/excel-agent-core.zip?raw=1) · [Gemini ZIP](packages/gemini/excel-agent-core.zip?raw=1). Importing a skill alone does not make it a guaranteed default for every request. Use the agent's Instructions field for your saved default behavior and verify a representative task. All three forms are generated from [one canonical skill](skills/excel-agent-core/SKILL.md).

## Choose your edition

| | Microsoft 365 Copilot | Gemini |
| --- | --- | --- |
| Get started | [Copilot guide](docs/COPILOT.md) | [Gemini guide](docs/GEMINI.md) |
| Import packages | [Individual ZIPs](packages/copilot) | [Individual ZIPs](packages/gemini) |
| Read instructions | [Copilot SKILL.md files](editions/copilot) | [Gemini SKILL.md files](editions/gemini) |
| Work surface | Chat, Excel, PowerPoint or an eligible custom agent | Native Skills when exposed by the approved account |
| Fallback | Paste one workflow into an approved conversation | [Gem-ready instruction text](editions/gemini-gems) or a manual conversation |
| Update installed copy | Replace/edit, or update the app-created OneDrive folder and Refresh | Replace the existing skill; update Gem instructions separately |

Each **individual skill ZIP** contains one root `SKILL.md`. Upload one skill at a time. Package checks establish integrity; work-account import and task behavior still need verification in that account.

## Start with the work you do

| Task | Skills to begin with | Expected result |
| --- | --- | --- |
| Monthly personnel reporting | Excel data coverage, workforce reconciliation, forecast variance | Reconciled headcount/FTE and a driver explanation with exceptions |
| Actuals ingestion and mappings | Power Query ETL, account mapping, SharePoint evidence | Repeatable refresh, traceable source files and unresolved mappings retained |
| Month-end close | Close controls, spreadsheet modeling, business document | Opening-to-closing checks, material exceptions and proposed adjustments |
| Cash and planning | Cash and working capital, scenario planning | Comparable KPIs and explicit assumption-based scenarios |
| Management reporting | Power BI analysis, management presentation, corporate style | Measures and slides tied to source totals and the approved company template |
| Research and communication | Evidence research, document extraction, process diagram | Primary-source findings, extraction checks and a readable process map |

[Browse all 29 skills and their download links](SKILLS.md). The core, extended and specialist groups each contain eight task skills; four additional workflow pilots cover connected reporting, provisions, allocation preflight and benchmarks. The Excel agent instructions form a separate defaults group. A custom Agent Builder agent can use a focused selection. Importing `excel-agent-core` as a skill consumes one of that agent's available skill slots.

### An example request

> Use workforce-reconciliation on the two attached monthly files. Reconcile company headcount and FTE, separate hires and leavers from transfers, show unmapped cost centres, and explain which population and checks you actually completed.

For ordinary analysis, let Excel, Power Query or a local calculation tool do the arithmetic. Use the assistant to select the method, investigate exceptions, explain the result and prepare the requested deliverable.

## Shared workflow controls

Every native edition includes the same evidence and preservation rules. Keep **approved internal figures**, **internal workflow status** and **public benchmarks** separate. Align period, cutoff, scenario, version, units and source snapshot before comparing. Check detailed coordinates and gross differences as well as totals. A successful calculation does not establish refresh, approval or submission.

Four new skills connect those rules to work: `connected-reporting`, `provision-reconciliation`, `fx-allocation-preflight` and `benchmark-lookup`. The local helpers check supplied evidence and retain unexplained residuals; they perform no enterprise writes. [Two pilot workflows and migration map](docs/WORKFLOWS.md) · [Exact skill contracts](docs/SKILL-CONTRACTS.md)

The [tool list](TOOLS.md) maps **29 tools and capabilities** to finance workflows and the evidence each requires. It distinguishes tools reported available, optional products, unconfirmed work capabilities and local implementations. Listing a product does not install a connector.

## Thorough research, concise conclusions

The shared policy requires further targeted searches when evidence is incomplete and independent checks for consequential results. Use relevant authorized enterprise sources first, resolve contradictions, correct failed checks and preserve the remaining work if the host reaches a limit. Final answers stay concise and do not add unsolicited audit artifacts. [Research policy](docs/RESEARCH-POLICY.md)

Copilot Researcher and Gemini Deep Research are separate host features with their own availability and limits. Native Gemini Skills currently do not run inside Deep Research. The guides explain how to transfer a research brief where appropriate; a skill cannot increase a quota, grant access or force unlimited reasoning.

## Public benchmarks and research evidence

The full release includes a queryable dataset with **119 ECB FX observations**—68 published rates and 51 separately derived JPY crosses—and **48 World Bank commodity observations** for aluminum, copper, Brent and Japan LNG. Two retained public snapshots record their exact periods, retrieval timestamps, units, source IDs, rights and transformations. Independently invented vintage fixtures are kept separate.

The local API serves validated stored snapshots through four read-only routes. Use an immutable `snapshot_id`, or `as_of` only where a snapshot was actually retained by that cutoff. A provider's earlier observation period does not make today's revised history an earlier information vintage. Failed refreshes preserve the last good snapshot.

**Availability:** ECB and the selected World Bank extracts were exercised. BOJ values are excluded pending reproduction permission; METI transport-production and MHLW wage/hour configurations remain candidates pending exact source validation. Public values provide market context and never fill a missing internal forecast, exposure, mapping or confirmation.

[Dataset and local API](benchmarks/README.md) · [Data dictionary](benchmarks/DATA_DICTIONARY.md) · [OpenAPI contract](api/openapi.yaml) · [Research registry](research/README.md)

The registry connects each integrated source to the exact method, skill, decision or test it supports. [Standards](docs/STANDARDS.md) documents Agent Skills, SemVer, CFF citation metadata, SPDX identifiers, JSON Schema, OpenAPI and RFC 9457, with a lightweight provenance approach informed by W3C and FAIR. No certification or peer-reviewed status is claimed.

## Measured coverage and visible gaps

![Descriptive skill evidence and public benchmark coverage, with explicit denominators and validation gaps](assets/coverage.svg)

The [coverage report](metrics/README.md) and [JSON measurements](metrics/summary.json) are generated from canonical skills, declared test links, active research mappings and retained public snapshots. They show what the repository contains and which evidence is missing. A linked test is not a successful native agent run; observation rows are not independent research samples.

Reproduce the report with `python scripts/project_metrics.py --check`. The [proposed evaluation protocol](docs/EVALUATION.md) explains how future matched baseline/skill trials should be designed and reported. No native efficacy study, model accuracy score, user count or ranking is claimed.

## Python tools that run locally

The finance calculation and workflow validation helpers use Python's standard library. They leave input files unchanged and make no network calls. The separate public benchmark collector runs only through an explicit refresh command; the read-only API starts manually in the foreground.

```powershell
py -3 scripts\finance_tools.py profile examples\actual.csv --keys cost_center account --amounts amount
py -3 scripts\finance_tools.py reconcile examples\plan.csv examples\actual.csv --keys cost_center account --amount amount
py -3 scripts\finance_tools.py bridge --plan-quantity 100 --actual-quantity 110 --plan-rate 20 --actual-rate 21 --plan-fx 150 --actual-fx 145
```

The optional `workbook_audit.py` checks stored workbook cells/formula caches with openpyxl. `duckdb_profile.py` profiles complete local CSV/Parquet files with DuckDB. Neither claims that a spreadsheet formula was recalculated or that a particular large-file capacity is guaranteed. [Windows setup and actual output definitions](docs/WINDOWS.md)

## Upstream projects, adapted to the work environment

The library draws on reviewed methods from Anthropic's document skills, DuckDB skills, scientific analysis, design review, source-based research and verification workflows. The portable finance instructions are independently authored; they do not impersonate those tools or acquire their paid APIs.

[Upstream sources and requested installation options](docs/UPSTREAMS.md) records the inspected commits, licences and host requirements for Hallmark, Anthropic skills, Claude-mem, HyperFrames, DuckDB, Valyu, D3 and the scientific skills collection. `fetch_upstreams.py` acquires pinned source archives; acquisition is separate from activating a coding-host plugin or installing a runtime on your PC.

## Keep it current

Canonical instructions live in `skills/`. A deterministic build produces both editions, 58 individual upload packages, Gem-ready text, the Excel agent profile, three native transport bundles, the Markdown-only download, coverage statistics and the readable catalogue. The offline gate checks generated files, workflow/tool/source references, dataset and API contracts, tests and public package contents. Commit identity is a separate publication check. A release step freezes versioned downloads and SHA-256 checksums; published versions are preserved. Upstream changes are checked against pinned commits and reviewed before adoption. [Update workflow](docs/UPDATES.md)

```powershell
py -3 scripts\research_registry.py
py -3 scripts\build.py
py -3 scripts\check_release.py
```

This repository includes no GitHub Actions workflows. A separately configured daily maintenance task checks relevant platform and upstream changes around 08:00 Asia/Tokyo; it was enabled on 2026-11-25. Compatible updates require validation and resolved publication-identity checks. Updating GitHub does not update an existing native Copilot or Gemini import. The folder copier preserves local edits and records the package version it copied.

## Browse the catalogue

Open `site/index.html` from the extracted repository, or serve the repository locally:

```powershell
py -3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8000/site/`. All skill descriptions, prompts and Copilot download links are readable without JavaScript; JavaScript adds edition selection, task search, prompt copying and theme controls. Its interface uses a pinned [dot. design foundation](branding/dot/source.json). The repository design does not replace your employer's approved reporting templates. This is an included static catalogue, not a claimed public website deployment.

## Evidence and next work

[Validation record](docs/VALIDATION.md) separates tests actually run from Windows, tenant and visual checks still outstanding. [Further implementation priorities](docs/ROADMAP.md) focuses on company-specific data contracts, Power BI tie-outs and repeatable close workflows.

Keep business data, internal links, credentials and private templates in approved company storage. Examples and test cases here are independently invented; the benchmark dataset contains separately attributed public observations. File scans and Git identity reviews have different scopes; see [security and data boundaries](SECURITY.md).

## Help improve the library

Use [support](SUPPORT.md) for setup questions, report a reproducible defect with an invented example, or propose a finance workflow with clear inputs and acceptance criteria. The [contribution guide](CONTRIBUTING.md), [code of conduct](CODE_OF_CONDUCT.md) and issue templates keep reports useful and free of work data. [Discovery design](docs/DISCOVERY.md) records the comparable repositories and official guidance behind the onboarding and metadata. Use [CITATION.cff](CITATION.cff) when citing a particular version.

Designed with the dot. foundation. Original library and tooling: [MIT](LICENSE). Upstream projects retain their own licences and attribution in [source notes](docs/UPSTREAMS.md).
