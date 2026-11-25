# Windows 11 work setup

This repository supports two independent paths: import a portable skill into your approved Copilot/Gemini account, or run optional calculations in the Python environment on your work PC. No script here gives a cloud assistant control of your PC.

## Get the files

Download the repository with GitHub's **Code → Download ZIP**, extract it into an approved work folder and open that folder in VS Code. Git is optional. If Git is installed and you cloned the repository, use `git pull --ff-only` from a clean checkout to obtain reviewed updates.

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
