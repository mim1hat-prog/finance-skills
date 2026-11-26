# Use finance skills with Copilot

Core setup reviewed against official documentation on **2026-11-25**; Excel's OneDrive folder setup, import limits and Cowork routing reviewed **2026-11-26**. This guide targets **Microsoft 365 Copilot on a Windows 11 work PC**. Installation is complete only after your work account recognizes the skill and a representative task succeeds.

**Using Excel:** [download the Excel OneDrive folder package](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/excel/finance-suite-onedrive.zip), extract it, then add its inner **`finance-suite` folder** to the skills location Excel opens. [Exact Excel setup](#3-copilot-in-excel)

**Using Copilot Chat, Agent Builder or Cowork:** [download the Copilot suite ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/suites/finance-suite-copilot.zip) and upload it unchanged through that host's supported skill-upload screen. Both packages provide one `finance-suite` skill with all 29 complete workflows in nine supporting files. [Choose the installation route](SINGLE-IMPORT.md)

For just the default operating rules, use [excel-agent-core.zip](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/copilot/excel-agent-core.zip); Excel needs its extracted contents inside a folder named `excel-agent-core`. Individual workflows remain available below.

[Browse the Copilot edition](../editions/copilot) · [Other individual Copilot packages](../packages/copilot) · [Gemini guide](GEMINI.md)

**Pasting into an Instructions field?** Download the [Markdown-only ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/markdown/finance-skills-markdown.zip), extract it and open a file in `copilot/`. Copy the entire file into the Instructions field or an approved conversation. For shared Excel defaults, use `EXCEL-AGENT-INSTRUCTIONS.md` or the [Excel Instructions profile](../profiles/excel-agent-instructions.txt?raw=1). These files intentionally omit native metadata: **paste their text; do not upload them as native skills**.

## Choose the Copilot surface

| Where you work | Install here | Best fit |
|---|---|---|
| Microsoft 365 Copilot Chat | Agents & Skills, using the complete suite ZIP or an individual skill | Research, evidence, analysis and general finance workflows |
| Excel's Copilot pane | The OneDrive skills folder opened by Excel | Workbook calculations, reconciliation, mappings and models |
| PowerPoint's Copilot pane | Add skill, or the OneDrive skills folder opened by PowerPoint | Management presentations, document structure and corporate style |
| A custom Agent Builder agent | Configure → Skills → Add, using the suite or individual ZIPs | One complete suite or a focused assistant with up to eight selected skills |
| Copilot Cowork | Plugins → Add → Upload, using a complete skill ZIP | One suite with supporting reference files; check Cowork-specific limits below |
| GitHub Copilot in VS Code, if separately available | Its supported project/user skill location | Local coding and Python work; this is a separate Copilot product |

Microsoft currently limits personal Copilot Chat skills to the experience labeled **Premium**, excludes Basic, and does not support them in Information Barriers tenants. Excel/PowerPoint availability depends on the app, subscription and organization settings; the Chat restriction should not be applied indiscriminately to every Office surface. Check the menu in the work account you intend to use. [Chat requirements](https://learn.microsoft.com/en-us/plugins/build-copilot-chat-skills) · [Excel requirements](https://support.microsoft.com/en-gb/excel/copilot/frequently-asked-questions-about-copilot-in-excel)

## 1. Get an individual skill

For one download, choose the [current Copilot bundle](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/bundles/finance-skills-copilot.zip) or select the full package from [versioned releases](../releases/README.md), then extract it. The bundle contains every individual Copilot ZIP and skill folder; the full release also includes offline guides, the catalogue and local Python tools. Add a selected matching-name folder for Excel, or upload a selected ZIP from `packages/copilot/` through a supported ZIP-import screen. [Versions and checksums](RELEASES.md)

Open [packages/copilot](../packages/copilot), choose a skill ZIP and use GitHub's file download control. Each ZIP contains `SKILL.md` at its root. Download a few useful skills first; do not upload the entire repository ZIP as one skill.

Start with `excel-data-coverage`, `workforce-reconciliation`, `forecast-variance`, `account-mapping` and `power-query-etl`. Add `close-controls` and `cash-working-capital` for close and cash work. Use `corporate-style` with the approved company template supplied inside your work environment; the dot repository design is not your employer's brand.

If you download the whole repository for convenience, extract it first and navigate to an individual skill under `editions/copilot`. The package and the corresponding generated skill directory represent the same workflow.

### Troubleshoot invalid skill information

> Skill information contains invalid data. Check that the SKILL.md file contains a name and description and try again.

Import-format checks reviewed **2026-11-26** against the linked Microsoft documentation. The message alone does not establish the cause. Check the actual uploaded file:

1. In **Excel**, use the extracted matching-name folder described [below](#3-copilot-in-excel). For a supported **ZIP-upload screen**, use the complete Copilot suite ZIP or an individual ZIP from `packages/copilot/`, such as `excel-agent-core.zip`. A full/individual-package release bundle must be extracted first. A file from the Markdown-only download or the Excel Instructions profile is for pasting, even if renamed `SKILL.md`.
2. Keep `SKILL.md` at the skill folder's root in Excel, or at the archive root for the Chat/Builder suite ZIP. Its first line must be `---`, followed by nonempty YAML `name` and `description` fields, then a closing `---` before the instructions. Preserve the complete header and the supporting `references/` folder.
3. Keep the file as **UTF-8 without BOM**. If you edited it, select UTF-8 when saving in VS Code and confirm that Windows has not added a second extension such as `SKILL.md.txt`.
4. Use GitHub's **Download raw file** or the direct download link. Saving the GitHub file-view webpage can produce HTML instead of the skill's Markdown.

Microsoft documents the required YAML fields in its [Copilot Chat skill format](https://learn.microsoft.com/en-us/plugins/build-copilot-chat-skills) and encoding/parser checks in its [Copilot Studio upload troubleshooting](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/skills-add-existing). These package checks do not establish a successful import in your account. If the unchanged individual package still fails, provide the exact uploaded filename, the original company-neutral file and the surface used—Microsoft 365 Copilot Chat, Excel, PowerPoint or Agent Builder—so the failed input can be inspected. Do not include company additions or work data.

### Troubleshoot unsupported, invalid, import-limit or Responsible AI errors

The combined rejection message does not identify which check failed. A valid YAML header alone does not establish acceptance. Record the exact upload screen and any detailed validation report before assigning a cause.

The inspected **v1.5.0 Copilot suite is intact and has valid metadata**, but includes 29 companion files. Microsoft documents a separate **20-companion limit per Cowork skill**. This is a confirmed Cowork portability defect; the reviewed Excel page does not specify that limit, so it does not establish the cause of an Excel failure. **Use v1.5.1 or later:** all 29 complete workflows are grouped into nine companion files.

Cowork's [personal-skill guide](https://learn.microsoft.com/en-us/copilot/cowork/use-cowork) specifies 20 companions and 10 MB total. Its [upload guide](https://learn.microsoft.com/en-us/copilot/cowork/cowork-customize) separately allows a 1 MB main file, a 10 MB compressed / 50 MB expanded archive and 100 archive files. The [plugin companion rules](https://learn.microsoft.com/en-us/copilot/cowork/cowork-plugin-development) additionally specify 5 MB per companion. The current suite conservatively checks all these size/file ceilings, using decimal MB, while retaining a main file under 20,000 characters. These project checks do not imply identical limits for personal Chat, Agent Builder or Excel.

Keep the complete ZIP intact for a supported ZIP import. In Cowork, use **Plugins → Add → Upload**. In Excel, use the **extracted `finance-suite` folder**, including its references, and then Refresh. A ZIP copied into OneDrive or a version-named outer folder is not the required matching-name skill folder. Preserve private customizations before replacement; when upgrading from v1.5.0, replace the old folder rather than merging its 29 references with the new nine.

If the current suite still fails, identify whether the screen is **Copilot Chat, Agent Builder, Excel, PowerPoint or Cowork** and retain the detailed error. The existing single-file [Excel defaults package](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/copilot/excel-agent-core.zip) can help distinguish supporting-file handling from a more general account or content issue, but a smaller package is not guaranteed to pass. Respect tenant controls and approved support routes. Microsoft's [Responsible AI validation documentation](https://learn.microsoft.com/en-us/plugins/responsible-ai-validation) describes a separate platform check; local ZIP tests cannot reproduce that service or establish its verdict.

## 2. Microsoft 365 Copilot Chat

1. Open Microsoft 365 Copilot with your work account.
2. From Home, right-click **Agents**, choose **More agents**, then choose **Upload skill** from the **Add** menu. The interface may also expose the management area as **Agents & Skills**.
3. Upload the complete suite ZIP, including its references. For an individual standalone workflow, upload its ZIP or `SKILL.md`.
4. Review the name, description, instructions and included files, then save.
5. Select the installed skill explicitly for the first task. Enable automatic invocation only for skills you want Copilot to choose on its own.

Attaching `SKILL.md` to an ordinary conversation supplies context for that conversation; it does not establish native skill registration. Follow Microsoft's [create/edit guide](https://support.microsoft.com/en-gb/microsoft-365-copilot/create-edit-skills-copilot) if your menu changes.

## 3. Copilot in Excel

**Excel uses its app-created OneDrive skills folder.** Download the [Excel folder package](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/excel/finance-suite-onedrive.zip) or the fixed [v1.6.0 Excel package](https://github.com/mim1hat-prog/finance-skills/releases/download/v1.6.0/finance-skills-v1.6.0-excel-onedrive.zip).

1. In Windows, right-click the downloaded ZIP and choose **Extract All**. Inside the extracted download, locate **`finance-suite`**, containing `SKILL.md` and `references/`.
2. Open Excel's Copilot pane, then **… → Manage plugins & skills → Custom skills**. If needed, choose **Create OneDrive folder**, then **Open skills folder**.
3. Upload or copy the inner **`finance-suite` folder** into that location. Keep its name and all contents. Do not upload the ZIP itself or the enclosing version-named download folder.
4. Wait for the files to finish uploading or syncing, return to Custom skills, and select **Refresh**.
5. Use **Add → Choose plugins and skills** or mention **`@finance-suite`**. Enable its toggle if you want automatic use; a direct mention can invoke a skill whose automatic-use toggle is off.

| Required structure | This package provides |
| --- | --- |
| Folder name matches `name:` | `finance-suite` and `name: finance-suite` |
| Main file has metadata and task instructions | `finance-suite/SKILL.md`, with nonempty `name`, `description` and body |
| Referenced procedures are available with the main file | `finance-suite/references/`, containing nine complete category files |
| Complete suite is kept together | Ten Markdown files covering all 29 workflows |

The main `SKILL.md` contains shared instructions and navigation. **Copying only that file omits the full workflow procedures.** The ten-file layout is this project's package design; Cowork's 20-companion ceiling is not presented as a documented Excel limit.

For one individual workflow, place its extracted `SKILL.md` inside a folder matching its `name:`, such as `account-mapping`. For the full project download, the complete suite is also at `editions/copilot-suite/finance-suite/`. Preserve approved private additions before replacing an older folder, then refresh and test the updated skill.

Keep workbooks, source data and company-only instructions in approved work locations. Verify the skill appears and can read a required reference on a small invented task. This documented setup and the local package checks do not establish a successful installation, reference retrieval or execution in your account. [Microsoft's Excel instructions](https://support.microsoft.com/en-gb/excel/copilot/copilot-in-excel-skills)

## 4. Copilot in PowerPoint

In the Copilot pane, select **+ → Choose skills → Manage skills → Add skill**. Upload the individual skill package or use the form to paste its instructions. PowerPoint also supports matching-name skill folders in its app-created OneDrive skills location. If a change does not appear, use **Refresh** in the skill manager.

PowerPoint's ZIP upload currently rejects PNG, PDF and nested ZIP content. These standalone text packages avoid that issue; supply your approved presentation template as task context through a supported work flow rather than adding arbitrary files to the skill ZIP. A saved skill is personal to the account, and its presence in one host should not be assumed in every other host. [PowerPoint guide](https://support.microsoft.com/en-us/powerpoint/copilot/copilot-in-powerpoint-skills)

## 5. Agent Builder

To reuse your Excel agent's operating rules, copy [the ready-to-paste Instructions text](../profiles/excel-agent-instructions.txt?raw=1) into the Instructions field you already use and save. It prioritizes relevant available enterprise evidence, preserves existing workbook logic and keeps output concise without unsolicited audit tables, new sheets or audit text. Internal checks and material unresolved issues remain required. Review it alongside company-specific instructions.

The same content is available as the individual `excel-agent-core` skill. Importing it consumes one skill slot and does not guarantee that it is invoked on every request. Use saved agent Instructions for the default behavior and verify it on a representative task. A selected task skill still supplies the detailed finance method.

Open or create the agent, go to **Configure → Skills → Add**, and upload the complete Copilot suite ZIP for all workflows in one skill entry, or individual ZIPs for a focused selection. Review the content and reference files, then try a representative request in **Try it**. The suite's workflows are not separate native skill registrations.

Agent Builder permits **eight skills per agent**. Its current package limits are 50 MB per ZIP, 25 MB per file, 350 total files across skills and directory depth three; skill instructions must remain below 20,000 characters. These are Agent Builder limits, not personal Chat-upload limits. Builder access and optional agent capabilities have different licensing requirements. [Agent Builder guide](https://learn.microsoft.com/en-us/plugins/agent-builder-add-skills) · [Support matrix](https://learn.microsoft.com/en-us/plugins/declarative-agent-skills)

A practical operations agent can use: `work-tool-routing`, `excel-data-coverage`, `workforce-reconciliation`, `forecast-variance`, `spreadsheet-modeling`, `account-mapping`, `close-controls` and `cash-working-capital`. Choose a different set for reporting or research rather than trying to fit the entire library into one agent.

## Python, Power BI and SharePoint

The Copilot edition directs the model to use the tools available in the current host. The documented declarative-agent skill runtime uses a cloud sandbox with package-installation and network restrictions; those rules describe that runtime, not every product named Copilot. Existing enabled connectors operate separately through the orchestrator. A Python installation on your Windows PC is not available automatically to a cloud skill sandbox. Check the actual surface and capabilities before choosing a route. [Runtime boundary and inventory](https://learn.microsoft.com/en-us/plugins/declarative-agent-skills)

Use local Python in VS Code for larger approved exports or calculations that need a local package. Run the code locally, inspect its reconciliation/exception output, then supply the appropriate result to your approved Copilot work session. Copilot should distinguish code it proposed from code that actually ran. For SharePoint ingestion, use the approved native Power Query connector where available and preserve source file, version and period evidence. [SharePoint connector](https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-folder)

VS Code's GitHub Copilot uses project `.github/skills/` or personal `~/.copilot/skills/` directories. Those locations do not install Microsoft 365 skills. Use this route only if your organization already provides or permits that separate product. [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

The full release also includes a manual public-benchmark collector and local read-only API. A cloud Copilot session cannot be assumed to reach `127.0.0.1` on your work PC. Supply the permitted snapshot through an approved supported route, or use an approved local client; no connector is installed by this repository. [Dataset guide](../benchmarks/README.md) · [Tool availability and workflow routing](../TOOLS.md)

## Deeper research and independent checks

For complex analysis, use an available reasoning mode appropriate to the task. For a broader source-backed question, **Researcher** is a separate Copilot feature with eligible-plan and administrator requirements. Check that it is available in the approved account, select relevant accessible sources and inspect the resulting evidence. A skill does not enable Researcher or override its limits. [Researcher requirements and use](https://support.microsoft.com/en-us/microsoft-365-copilot/get-started-with-researcher-in-microsoft-365-copilot)

The shared policy asks Copilot to search relevant enterprise evidence first, adapt incomplete searches, resolve contradictions and independently recheck material results. It continues while another available step can resolve a consequential gap, then returns a precise answer or the exact remaining blocker. Keep checkpoints when a host limit interrupts the task; do not claim unseen work was completed. [Research policy](RESEARCH-POLICY.md) · [Workflow pilots](WORKFLOWS.md)

## Check the first task

Use a small synthetic file or an approved non-sensitive sample with a total you know. Ask the skill to report the population checked, calculation result, exceptions and any tools or sources it could not access. Confirm that an actual output file exists if a file was requested. For workbook workflows, verify the formulas and totals in Excel. For SharePoint evidence, verify the cited source location and version.

Example: “Use account-mapping to validate these five sample ledger lines against this mapping table. Show unmatched and multiply matched lines and reconcile the source amount to the mapped result.”

## Keep your installed copy current

GitHub is the maintained source. An already imported Chat or Agent Builder skill is a separate installed copy; the reviewed Microsoft documentation does not describe automatic synchronization from this repository.

When a skill changes, compare the new instructions with any company-specific additions before replacing the installed version. In Chat/Agent Builder, update the existing item through that host's supported editor or replacement flow. In Excel, update the complete matching-name OneDrive folder and select **Refresh**. For PowerPoint, use its supported editor or folder flow. Test the changed workflow again. Keep company-only additions outside the public repository.

Record the repository release/commit or package hash, host, skill name and imported date in your work notes. This lets you distinguish a fresh repository package from the version actually running in your account. If native Skills is unavailable, paste one skill's body into an approved chat with the task; that is a manual fallback and must be repeated or saved through an approved feature.
