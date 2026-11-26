# Finance Agent Skills for Microsoft 365 Copilot and Gemini

![Finance skills: practical methods for clear numbers and sound decisions](assets/readme-hero.svg)

[![Copilot edition](https://img.shields.io/badge/Copilot-edition-31573F?style=flat)](docs/COPILOT.md) [![Gemini edition](https://img.shields.io/badge/Gemini-edition-31573F?style=flat)](docs/GEMINI.md) [![License MIT](https://img.shields.io/badge/license-MIT-4C5054?style=flat)](LICENSE)

**29 repeatable workflows for Excel reconciliation, FP&A, forecasting, financial controlling and management reporting.** Import a complete suite or individual skills, with optional Python and Power BI tools for Windows.

[**Excel / OneDrive — all workflows, one folder**](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-excel-onedrive.zip) · [**Copilot Chat — suite ZIP**](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-copilot-suite.zip) · [**Gemini — suite ZIP**](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-gemini-suite.zip)

Each suite packages **one `finance-suite` skill with all 29 workflows in nine reference files**. For Excel, extract the download and add its inner `finance-suite` folder to the OneDrive skills folder opened by Excel. [Setup by host](docs/SINGLE-IMPORT.md) · [Markdown for pasting only](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-markdown.zip) · [Full project](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-full.zip)

[Quick start](#quick-start) · [Coverage](#coverage-at-a-glance) · [All skills](SKILLS.md) · [Downloads](#downloads) · [Copilot setup](docs/COPILOT.md) · [Gemini setup](docs/GEMINI.md) · [Help](SUPPORT.md)

## Coverage at a glance

<!-- project-coverage-summary:start -->
[![Descriptive coverage of skill evidence and public benchmark data, showing numerators, denominators and retained observation dates](assets/coverage.svg)](metrics/README.md)

**29 skills** · **12/29** with workflow-test links · **0/29** with native execution evidence · **11/17** configured benchmark series with observations.

Active empirical-research sources: 0; excluded empirical candidates: 1. Source mappings describe stated uses, not measured model efficacy.

Repository measurements: **v1.6.0**, release **2026-11-26**. The release date is not a provider retrieval date.

- **`ecb-exr-api` (daily):** latest retained observation period per series **2026-11-24**; retrieval timestamp (UTC) **2026-11-25T03:07:56.456028Z**.
- **`worldbank-pink-sheet` (monthly):** latest retained observation period per series **2026-10**; retrieval timestamp (UTC) **2026-11-25T03:07:50.858358Z**.

Dates describe retained snapshots. Rebuilding these graphs does not fetch providers or establish current market-data freshness.
<!-- project-coverage-summary:end -->

Generated from the canonical catalogue, research mappings, declared tests and retained public snapshots. **These counts describe scope and gaps, not model accuracy or native task success.**

[Methods and full results](metrics/README.md) · [Machine-readable measurements](metrics/summary.json) · [Validation record](docs/VALIDATION.md) · [Synthetic evaluation kit](docs/EVALUATION.md)

## Quick start

1. **Choose [Excel / OneDrive](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-excel-onedrive.zip), [Copilot Chat](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-copilot-suite.zip) or [Gemini](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-gemini-suite.zip).**
2. **Excel:** extract, upload the inner `finance-suite` folder into Excel's OneDrive skills location, then Refresh. **Chat/Gemini:** upload the complete suite ZIP through the supported Skills screen. Select or mention `finance-suite` for the first task. [Exact setup steps](docs/SINGLE-IMPORT.md)
3. **Run the [invented reconciliation example](examples/QUICKSTART.md).** The CSVs reconcile from 350.30 to 365.35: a 15.05 difference with two unmatched records. Verify that the host reads the selected workflow reference and obtains the expected result.

**Native import and execution remain unverified in the target accounts.** Availability depends on the host, permissions and rollout. The current suite has nine companion files; v1.5.0 had 29, exceeding Cowork's documented 20-companion limit. [Import limits and troubleshooting](docs/COPILOT.md#troubleshoot-unsupported-invalid-import-limit-or-responsible-ai-errors).

For a focused installation, choose an [individual Copilot](packages/copilot) or [Gemini](packages/gemini) workflow. For an Instructions field, use the [Markdown download](#downloads) and paste the relevant file's full text.

The instructions prioritize relevant internal evidence, preserve workbook logic and verify calculations. They request no unsolicited audit tables, extra worksheets or process commentary. The instruction workflow needs no local coding agent or API subscription.

## Downloads

**Current package: v1.6.0.**

| Package | What you receive | Download |
| --- | --- | --- |
| **Excel / OneDrive** | A correctly named `finance-suite` folder with all 29 workflows; extract and upload the folder | [Excel folder ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-excel-onedrive.zip) |
| **Copilot complete suite** | All 29 workflows in one native skill package | [Copilot suite ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-copilot-suite.zip) |
| **Gemini complete suite** | All 29 workflows with Gemini host instructions | [Gemini suite ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-gemini-suite.zip) |
| **Markdown only** | 60 `.md` files: 29 Copilot skills, 29 Gemini skills, Excel agent instructions and a start guide | [Markdown ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-markdown.zip) |
| **Copilot** | 29 individual skill ZIPs, matching folders and Excel agent instructions | [Copilot ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-copilot.zip) |
| **Gemini** | 29 individual skill ZIPs, matching folders, Gem-ready text and Excel agent instructions | [Gemini ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-gemini.zip) |
| **All skills** | Both editions, 58 individual ZIPs, folders, Gem-ready text and Excel agent instructions | [All-skills ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-all.zip) |
| **Full release** | All skills plus project sources, guides, public benchmark components, Python tools, tests and the visual catalogue | [Full ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.6.0/finance-skills-v1.6.0-full.zip) |

**Excel / OneDrive:** extract and upload the inner matching-name folder. **Chat/Gemini suite ZIPs:** upload unchanged through the supported Skills screen. **Other bundles:** extract first, then choose a native package or copy-only Markdown file. Markdown omits native metadata and is for pasting. [Package formats and replacement](docs/SINGLE-IMPORT.md)

[Release notes and SHA-256 checksums](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/v1.6.0/README.md) · [All releases](releases/README.md) · [Versioning and verification](docs/RELEASES.md)

## Find a workflow

| Your task | Start here | Expected result |
| --- | --- | --- |
| Monthly personnel reporting | Excel data coverage, workforce reconciliation, forecast variance | Headcount/FTE reconciliation and an explanation of verified drivers and exceptions |
| Actuals and mappings | Power Query ETL, account mapping, SharePoint evidence | Traceable sources, repeatable refresh and unresolved mappings retained |
| Month-end close | Close controls, spreadsheet modeling, business document | Opening-to-closing checks, material exceptions and proposed adjustments |
| Cash and planning | Cash and working capital, scenario planning | Comparable KPIs and explicit assumption-based scenarios |
| Management reporting | Power BI analysis, management presentation, corporate style | Measures and slides tied to source totals and the approved template |
| Research and communication | Evidence research, document extraction, process diagram | Primary-source findings, checked extraction and readable process maps |

[**Browse all 29 skills**](SKILLS.md) · [Exact inputs, outputs and acceptance criteria](docs/SKILL-CONTRACTS.md) · [Tool list and availability](TOOLS.md)

> Use finance-suite's workforce-reconciliation workflow on the two attached monthly files. Reconcile headcount and FTE, separate hires and leavers from transfers, and identify unmapped cost centres and material unresolved differences.

Let Excel, Power Query or a local calculation tool do the arithmetic. Use the assistant to select the method, investigate exceptions, explain the result and prepare the requested deliverable.

### Save your Excel agent defaults

[**Download ready-to-paste Excel agent instructions**](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/profiles/excel-agent-instructions.txt) and paste them into the **Instructions** field you already use. Compare and preserve approved company additions before saving.

The profile and individual [Copilot](packages/copilot/excel-agent-core.zip?raw=1) and [Gemini](packages/gemini/excel-agent-core.zip?raw=1) skills share one [canonical source](skills/excel-agent-core/SKILL.md). Importing a skill does not make it the default for every request.

## Choose your assistant

| | Microsoft 365 Copilot | Gemini |
| --- | --- | --- |
| Setup | [Copilot guide](docs/COPILOT.md) | [Gemini guide](docs/GEMINI.md) |
| Native packages | [Individual ZIPs](packages/copilot) | [Individual ZIPs](packages/gemini) |
| Read instructions | [Copilot skill folders](editions/copilot) | [Gemini skill folders](editions/gemini) |
| Work surface | Chat, Excel, PowerPoint or an eligible custom agent | Native Skills when exposed by the approved account |
| Fallback | Paste one workflow into an approved conversation | [Gem-ready text](editions/gemini-gems) or an approved conversation |
| Update an installed copy | Replace/edit, or update the app-created OneDrive folder and Refresh | Replace the skill; update Gem instructions separately |

Microsoft 365 Copilot and Gemini Apps are the primary targets; GitHub Copilot and Gemini CLI are separate products. Respect the selected host's skill slots and available tools. The [research policy](docs/RESEARCH-POLICY.md) requires targeted retrieval and independent checks within host limits. Native Gemini Skills do not run inside Deep Research.

## Evidence, standards and public data

Keep **approved internal figures**, **internal workflow status** and **public benchmarks** separate. Align periods, cutoffs, scenarios, units and snapshots before comparing. Public data cannot fill missing internal inputs or prove approval or submission.

The full release contains **119 ECB FX observations**—68 published rates and 51 separately derived JPY crosses—and **48 World Bank commodity observations** for aluminum, copper, Brent and Japan LNG. Two retained public snapshots record periods, retrieval timestamps, units, source IDs, rights and transformations. Synthetic vintage fixtures are separate.

The local read-only API serves retained snapshots. Use `snapshot_id`, or `as_of` only when a snapshot existed by the cutoff. An observation period alone does not establish what was known at a forecast date. Failed refreshes preserve the last good snapshot.

**Source status:** ECB and the selected World Bank extracts were exercised. BOJ values are excluded pending reproduction permission. METI transport-production and MHLW wage/hour configurations remain candidates pending exact source validation.

[Dataset and API guide](benchmarks/README.md) · [Data dictionary](benchmarks/DATA_DICTIONARY.md) · [OpenAPI contract](api/openapi.yaml) · [Research registry](research/README.md) · [Workflow pilots](docs/WORKFLOWS.md)

The registry maps sources to their exact implementation uses. [Standards](docs/STANDARDS.md) records Agent Skills, SemVer, CFF, SPDX, JSON Schema, OpenAPI and RFC 9457, plus provenance informed by W3C and FAIR. This is not a certified or peer-reviewed project.

## Optional local tools

Finance calculation helpers use Python's standard library, preserve inputs and make no network calls. Benchmark collection and the local API run only through explicit commands.

```powershell
py -3 scripts\finance_tools.py profile examples\actual.csv --keys cost_center account --amounts amount
py -3 scripts\finance_tools.py reconcile examples\plan.csv examples\actual.csv --keys cost_center account --amount amount
py -3 scripts\finance_tools.py bridge --plan-quantity 100 --actual-quantity 110 --plan-rate 20 --actual-rate 21 --plan-fx 150 --actual-fx 145
```

Optional openpyxl and DuckDB helpers inspect stored workbook cells and local CSV/Parquet files. They do not recalculate Excel formulas or guarantee a large-file capacity. [Windows setup and output definitions](docs/WINDOWS.md)

### Visual catalogue

Open `site/index.html` from the extracted full release, or serve the repository locally:

```powershell
py -3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/site/` to search workflows and copy prompts. Descriptions, prompts and Copilot links also work without JavaScript. No public website deployment is claimed.

## Maintain and contribute

Edit canonical instructions in `skills/`. The deterministic build generates editions, downloads, profiles, statistics and catalogue; versioned releases preserve their checksums and contents.

```powershell
py -3 scripts\research_registry.py
py -3 scripts\build.py
py -3 scripts\check_release.py
```

The offline gate checks generated files, evidence mappings, dataset/API contracts, tests and packages. Git identity is reviewed separately. [Maintenance](docs/UPDATES.md) · [Release procedure](docs/RELEASES.md)

Weekly maintenance is scheduled for Wednesdays at **08:00 Asia/Tokyo** (confirmed 2026-11-25). Updates require validation; this repository uses no GitHub Actions. Replace or refresh imported skills separately after a repository update.

| Read or contribute | Where to go |
| --- | --- |
| Setup help or a reproducible bug | [Support](SUPPORT.md) |
| Propose a skill or improve a workflow | [Contributing](CONTRIBUTING.md) · [Code of conduct](CODE_OF_CONDUCT.md) |
| Inspect completed checks and remaining work | [Validation](docs/VALIDATION.md) · [Roadmap](docs/ROADMAP.md) |
| Review the methods and design decisions | [Research registry](research/README.md) · [Discovery design](docs/DISCOVERY.md) |
| Cite a specific version | [CITATION.cff](CITATION.cff) |

Keep business data, internal links, credentials and private templates in approved company storage. Examples and test cases are independently invented; public observations retain their own attribution and rights. [Security and data boundaries](SECURITY.md)

[Upstream notes](docs/UPSTREAMS.md) record reviewed commits, licences and host requirements. Acquiring source archives does not activate plugins or install their runtimes.

---

Designed with the pinned [dot. foundation](branding/dot/source.json). Use your employer's approved templates for work outputs. Original library and tooling: [MIT](LICENSE); upstream projects and data retain their own licences and attribution.
