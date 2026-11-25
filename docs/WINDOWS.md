# Windows 11 work setup

This repository supports two independent paths: import a portable skill into your approved Copilot/Gemini account, or run optional calculations in the Python environment on your work PC. No script here gives a cloud assistant control of your PC.

## Get the files

Download the [full versioned release](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.2.0/finance-skills-v1.2.0-full.zip), extract it into an approved work folder and open that folder in VS Code. It includes all skills, packages, guides, the catalogue and local tools. Use the [release checksums](RELEASES.md) to verify the download. Git is optional. You can also use GitHub's **Code → Download ZIP** for the current repository tree. If Git is installed and you cloned the repository, use `git pull --ff-only` from a clean checkout to obtain reviewed updates.

If you only want skill instructions, choose a smaller [Copilot, Gemini or combined bundle](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/README.md). Extract it before choosing individual native imports or matching-name skill folders. These smaller bundles do not contain the Python tools below. The included `profiles/excel-agent-instructions.txt` can be pasted into the existing Excel agent Instructions field.

Keep business inputs and outputs outside the public checkout. Example paths below such as `C:\Work\FinanceData` are illustrative; use the location your company approves. The bundled `examples/` files are synthetic.

In VS Code's PowerShell terminal, check Python:

```powershell
py -3 --version
```

Use Python 3.10 or later for the standard-library scripts. DuckDB 2.0.1 requires Python 3.11 or later. If your Python installation does not include the Windows `py` launcher, use the actual `python` command or the approved interpreter's full path instead. VS Code is an editor; it does not imply access to GitHub Copilot or install Python packages.

## Core controls without package installation

Run from the extracted repository's root:

```powershell
py -3 scripts\finance_tools.py profile examples\actual.csv --keys cost_center account --amounts amount
py -3 scripts\finance_tools.py reconcile examples\plan.csv examples\actual.csv --keys cost_center account --amount amount
```

The examples reconcile plan **350.30** to actual **365.35**, with **15.05** actual-minus-plan difference and zero reconciliation residual. Cost centre `003` is left-only; `004` is right-only. Both remain visible rather than disappearing in an inner join.

For your own approved files:

```powershell
py -3 scripts\finance_tools.py profile "C:\Work\FinanceData\actual.csv" --keys cost_center account --amounts amount --output "C:\Work\FinanceData\actual-controls.json"
```

The output path must not already exist. Each analysis records the input file's name, byte size and SHA-256, plus the complete parsed row scope. It does not include the local directory path. Treat the resulting JSON as company data if it contains company totals or keys.

### CSV conventions

Use exact, unique column headers. Identifiers stay as text, so `001` and `01` remain distinct. The tools do not silently trim or normalize identifiers. Blank keys are reported by profiling and rejected for reconciliation. A malformed row, missing amount or non-finite number stops the requested calculation rather than silently dropping data.

Numbers use a decimal point and no thousands separators; for example `1234.56` and `-25.00`. Use `--delimiter ';'` and an explicit `--encoding` when required. A locale conversion is a separate documented transformation, not an inference from a few sample rows. Decimal values in JSON remain strings to retain exact precision. Convert them using the intended type/locale when loading into Excel or Power Query.

Repeated reconciliation keys fail by default. If repeated source rows are legitimate and summation at the requested grain is intended, use `--aggregate`; the report retains duplicate-group counts. `--tolerance 0.01` changes the matched/different classification only, not the amounts or residual. Distinct-key profiling keeps keys in memory; use the optional DuckDB path if the data is too large for that approach.

### Quantity/rate/FX bridge

```powershell
py -3 scripts\finance_tools.py bridge --plan-quantity 100 --actual-quantity 110 --plan-rate 20 --actual-rate 21 --plan-fx 150 --actual-fx 145
```

This synthetic example produces plan **300,000**, actual **334,950**, quantity effect **30,000**, rate effect **16,500**, FX effect **−11,550**, and zero residual. FX is reporting-currency units per source-currency unit. The fixed sequence is quantity, then rate, then FX. This is an arithmetic decomposition, not evidence of causation. Run it per comparable item before summing; a mixed product basket needs a separate mix definition.

## Optional workbook and DuckDB helpers

If local package installation is permitted, create a virtual environment. Invoke its interpreter directly; no PowerShell execution-policy change or activation script is needed.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-xlsx.txt
.\.venv\Scripts\python.exe -m pip install -r requirements-duckdb.txt
```

The checked pins are openpyxl 3.1.5 and DuckDB 2.0.1. The DuckDB requirement needs a 3.11+ interpreter. Package installation is a local setup step, not an instruction to run `pip` inside Copilot or Gemini's skill sandbox. [DuckDB Python requirements](https://duckdb.org/docs/2.0/clients/python/overview)

```powershell
.\.venv\Scripts\python.exe scripts\workbook_audit.py "C:\Work\FinanceData\report.xlsx" --output "C:\Work\FinanceData\workbook-audit.json"
.\.venv\Scripts\python.exe scripts\duckdb_profile.py "C:\Work\FinanceData\transactions.parquet" --keys transaction_id --output "C:\Work\FinanceData\parquet-controls.json"
```

The workbook helper opens two read-only views: formulas and saved values. It reports visible/hidden sheets, populated cells, stored errors and formula caches that are blank or absent. It does not save the workbook, run macros, refresh connections, render the layout or recalculate formulas. An absent cache can also mean an intentionally blank formula result; a populated cache can be stale. Recalculate and inspect in the authorized Excel environment before relying on formula outputs. [openpyxl read/save behavior](https://openpyxl.readthedocs.io/en/stable/tutorial.html)

The DuckDB helper reads an exact local `.csv` or `.parquet` file, keeps CSV values as text and computes complete row/key controls. It downloads no extension and accepts no arbitrary SQL. Rename a copy if the filename contains wildcard characters. It may make several passes; no file-size capacity, speed or memory guarantee is implied. Use the `analytical-sql` skill to prepare a separate reviewed SQL analysis for more complex queries.

## Workflow validation from supplied snapshots

The v1.2 helper checks JSON exports against the documented workflow contracts without changing a workbook or contacting a company system:

```powershell
py -3 scripts\workflow_controls.py validate --schema request examples\workflows\provision-residual.json
py -3 scripts\workflow_controls.py check examples\workflows\provision-residual.json
```

The first command validates the request shape. The second returns **exit 2** because this invented case deliberately retains an unexplained movement residual. It is a successful demonstration of a blocked result, not a broken installation. Exit 0 means the supplied check passed; exit 1 means invalid input or a file/configuration error.

The helper can check provisions, artifact preservation, detailed readback, mappings, granularity, case status and allocation preconditions. It does not authenticate the supplied evidence, refresh Excel, approve a result or post an allocation. Keep real request and result files outside this checkout. [Contracts, precision and examples](../examples/workflows/README.md) · [Two pilot workflows](WORKFLOWS.md)

## Public benchmark dataset and local API

The full release includes actual public ECB and selected World Bank observations plus separate synthetic fixtures. Source IDs, units, dates, rights and snapshot hashes are part of the dataset. BOJ values are not distributed pending permission; METI and MHLW/e-Stat configurations remain candidates. [Exact coverage and status](../benchmarks/README.md)

Validate the stored dataset and API contract without network access:

```powershell
py -3 scripts\benchmark_api.py --check
```

Start the read-only server only when needed:

```powershell
py -3 scripts\benchmark_api.py
```

It runs in the foreground at `http://127.0.0.1:8765`. In another PowerShell terminal, query the stored data:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8765/v1/datasets'
Invoke-RestMethod 'http://127.0.0.1:8765/v1/series/ecb-jpy-per-eur/observations?start=2026-11-01&end=2026-11-24&limit=10'
```

Stop the server with **Ctrl+C**. It makes no provider requests for API queries and installs no background service. A cloud assistant cannot automatically reach this address. Use a supported approved snapshot-import route or local client; company connectivity and public deployment are separate work.

Use an immutable `snapshot_id` for exact repetition, or a timezone-bearing `as_of` only where a retained snapshot predates that cutoff. Missing history returns `as_of_unavailable`. Invalid timestamps are rejected rather than normalized into another cutoff. Original and derived values remain distinct; consult the [dictionary](../benchmarks/DATA_DICTIONARY.md) before loading decimal strings, periods or units into Power Query/Power BI.

Refresh is a separate explicit public-network operation:

```powershell
py -3 scripts\benchmark_collect.py --adapter ecb --start 2026-11-01 --end 2026-11-24
py -3 scripts\benchmark_collect.py --adapter worldbank --start 2025-11-01 --end 2026-10-31
```

Choose the period required and review current source/rights configuration first. The command preserves last-good snapshots when a provider fails. An approved provider file can be supplied with `--input`; this does not bypass source or rights checks. Future e-Stat use requires a reviewed exact table/classification and `ESTAT_APP_ID` in the local environment, never in saved URLs, config JSON or logs. Public providers receive no private prompts or workbook values.

## Offline project checks

From a full release, run the maintained gate:

```powershell
py -3 scripts\check_release.py
```

It checks generated artifacts, source and tool references, dataset/API contracts, publication boundaries and unit tests without fetching providers. Inspect any optional-dependency skips. Maintainers use `--require-release` after freezing a repository release; the full ZIP itself omits nested previous release directories. [Release procedure](RELEASES.md) · [Standards](STANDARDS.md)

## Copy a Copilot edition into an Office skill folder

First use Excel or PowerPoint's **Manage skills** UI to create/open its OneDrive skills folder. Copy that exact path. Do not guess the folder or substitute a normal document library.

```powershell
$financeSkillFolder = Read-Host "Paste the skills folder opened by Excel or PowerPoint"
py -3 scripts\install_edition.py --edition copilot --destination "$financeSkillFolder" --skills excel-data-coverage workforce-reconciliation forecast-variance
```

The command above previews changes. To copy the inspected selection, run it with `--apply`:

```powershell
py -3 scripts\install_edition.py --edition copilot --destination "$financeSkillFolder" --skills excel-data-coverage workforce-reconciliation forecast-variance --apply
```

The copier verifies source/package hashes, records versions, refuses unmanaged/customized replacements and leaves unrelated skills alone. It never signs into Microsoft or activates a skill. Let OneDrive finish syncing, use **Refresh** in the host, and verify a task. On later updates it only replaces an unchanged copy previously managed by this installer. Preserve company-specific modifications in a separate approved location or choose a new destination.

For Gemini, use the individual ZIP import/replacement flow in the [Gemini guide](GEMINI.md). Copying a folder on Windows does not register a Gemini App skill.

## Power BI and SharePoint

Use the native SharePoint Folder connector for an approved folder-based Power Query pipeline. Start with the site address, filter the required folder and files before combining, exclude temporary/archive files deliberately, and reconcile the combined scope. The connector also lists subfolder files. [Microsoft connector guide](https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-folder)

Power BI Desktop can run Python and import pandas data frames, but its local interpreter and packages must be configured. Desktop success does not establish service refresh. Microsoft's Python-in-Power-Query service instructions include Public privacy levels and personal-gateway requirements; do not lower confidential sources' privacy classifications as an automatic fix. For finance work, prefer a separate approved local preprocessing step followed by native ingestion, or have IT configure the supported refresh design. [Python in Desktop](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-scripts) · [Python in Power Query](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-python-in-query-editor) · [Personal gateway](https://learn.microsoft.com/en-us/power-bi/connect-data/service-gateway-personal-mode)

No SharePoint credentials, tenant URLs, company extracts or Power BI model contents are needed in this public repository. The related skills work from the files/schema and permissions actually available at work.
