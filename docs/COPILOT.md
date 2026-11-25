# Use finance skills with Copilot

Verified against official documentation on **2026-11-25**. This guide targets **Microsoft 365 Copilot on a Windows 11 work PC**. The repository contains importable packages; native installation is complete only after your work account saves the skill and a representative task succeeds.

[Browse the Copilot edition](../editions/copilot) · [Download individual Copilot packages](../packages/copilot) · [Gemini guide](GEMINI.md)

## Choose the Copilot surface

| Where you work | Install here | Best fit |
|---|---|---|
| Microsoft 365 Copilot Chat | Agents & Skills, using a standalone SKILL.md or individual ZIP | Research, evidence, analysis and general finance workflows |
| Excel's Copilot pane | The OneDrive skills folder opened by Excel | Workbook calculations, reconciliation, mappings and models |
| PowerPoint's Copilot pane | Add skill, or the OneDrive skills folder opened by PowerPoint | Management presentations, document structure and corporate style |
| A custom Agent Builder agent | Configure → Skills → Add, using individual ZIPs | A focused assistant with up to eight selected skills |
| GitHub Copilot in VS Code, if separately available | Its supported project/user skill location | Local coding and Python work; this is a separate Copilot product |

Microsoft currently limits personal Copilot Chat skills to the experience labeled **Premium**, excludes Basic, and does not support them in Information Barriers tenants. Excel/PowerPoint availability depends on the app, subscription and organization settings; the Chat restriction should not be applied indiscriminately to every Office surface. Check the menu in the work account you intend to use. [Chat requirements](https://learn.microsoft.com/en-us/plugins/build-copilot-chat-skills) · [Excel requirements](https://support.microsoft.com/en-gb/excel/copilot/frequently-asked-questions-about-copilot-in-excel)

## 1. Get an individual skill

For one download, choose the [Copilot release bundle](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.1.0/finance-skills-v1.1.0-copilot.zip) or the [full release](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/releases/v1.1.0/finance-skills-v1.1.0-full.zip), then extract it. The bundle contains every individual Copilot ZIP and skill folder; the full release also includes offline guides, the catalogue and local Python tools. [Versions and checksums](RELEASES.md)

Open [packages/copilot](../packages/copilot), choose a skill ZIP and use GitHub's file download control. Each ZIP contains `SKILL.md` at its root. Download a few useful skills first; do not upload the entire repository ZIP as one skill.

Start with `excel-data-coverage`, `workforce-reconciliation`, `forecast-variance`, `account-mapping` and `power-query-etl`. Add `close-controls` and `cash-working-capital` for close and cash work. Use `corporate-style` with the approved company template supplied inside your work environment; the dot repository design is not your employer's brand.

If you download the whole repository for convenience, extract it first and navigate to an individual skill under `editions/copilot`. The package and the corresponding generated skill directory represent the same workflow.

## 2. Microsoft 365 Copilot Chat

1. Open Microsoft 365 Copilot with your work account.
2. From Home, right-click **Agents**, choose **More agents**, then choose **Upload skill** from the **Add** menu. The interface may also expose the management area as **Agents & Skills**.
3. Upload the individual ZIP or its standalone `SKILL.md`.
4. Review the name, description, instructions and included files, then save.
5. Select the installed skill explicitly for the first task. Enable automatic invocation only for skills you want Copilot to choose on its own.

Attaching `SKILL.md` to an ordinary conversation supplies context for that conversation; it does not establish native skill registration. Follow Microsoft's [create/edit guide](https://support.microsoft.com/en-gb/microsoft-365-copilot/create-edit-skills-copilot) if your menu changes.

## 3. Copilot in Excel

1. Open Excel's Copilot pane and select **… → Manage plugins & skills → Custom skills**.
2. Select **Create OneDrive folder**, then **Open skills folder**. Use the folder Excel opens, rather than guessing its location.
3. Extract each selected ZIP into its own folder. The folder name must exactly match `name:` in the file; for example, `account-mapping/SKILL.md`.
4. Copy the complete skill folder into the location opened by Excel.
5. Select **Refresh** in Custom skills.
6. Choose it through **Add → Choose plugins and skills**, or use an explicit mention such as `@account-mapping`.

Keep the company workbook, source data and company-only instructions in approved work locations. Use workbook tools for actual calculations and verify source coverage and control totals. Skill scripts do not give Excel new execution permissions. [Excel skill instructions](https://support.microsoft.com/en-gb/excel/copilot/copilot-in-excel-skills)

## 4. Copilot in PowerPoint

In the Copilot pane, select **+ → Choose skills → Manage skills → Add skill**. Upload the individual skill package or use the form to paste its instructions. PowerPoint also supports matching-name skill folders in its app-created OneDrive skills location. If a change does not appear, use **Refresh** in the skill manager.

PowerPoint's ZIP upload currently rejects PNG, PDF and nested ZIP content. These standalone text packages avoid that issue; supply your approved presentation template as task context through a supported work flow rather than adding arbitrary files to the skill ZIP. A saved skill is personal to the account, and its presence in one host should not be assumed in every other host. [PowerPoint guide](https://support.microsoft.com/en-us/powerpoint/copilot/copilot-in-powerpoint-skills)

## 5. Agent Builder

To reuse your Excel agent's operating rules, copy [the ready-to-paste Instructions text](../profiles/excel-agent-instructions.txt?raw=1) into the Instructions field you already use and save. It prioritizes relevant available enterprise evidence, preserves existing workbook logic and keeps output concise without unsolicited audit tables, new sheets or audit text. Internal checks and material unresolved issues remain required. Review it alongside company-specific instructions.

The same content is available as the individual `excel-agent-core` skill. Importing it consumes one skill slot and does not guarantee that it is invoked on every request. Use saved agent Instructions for the default behavior and verify it on a representative task. A selected task skill still supplies the detailed finance method.

Open or create the agent, go to **Configure → Skills → Add**, and upload the complete ZIP for each selected skill. Review the content, then try a representative request in **Try it**.

Agent Builder permits **eight skills per agent**. Its current package limits are 50 MB per ZIP, 25 MB per file, 350 total files across skills and directory depth three; skill instructions must remain below 20,000 characters. These are Agent Builder limits, not personal Chat-upload limits. Builder access and optional agent capabilities have different licensing requirements. [Agent Builder guide](https://learn.microsoft.com/en-us/plugins/agent-builder-add-skills) · [Support matrix](https://learn.microsoft.com/en-us/plugins/declarative-agent-skills)

A practical operations agent can use: `work-tool-routing`, `excel-data-coverage`, `workforce-reconciliation`, `forecast-variance`, `spreadsheet-modeling`, `account-mapping`, `close-controls` and `cash-working-capital`. Choose a different set for reporting or research rather than trying to fit the entire library into one agent.

## Python, Power BI and SharePoint

The Copilot edition directs the model to use the tools available in the current host. Microsoft 365 Chat/agent skill scripts run in a cloud sandbox: they cannot install packages or make authenticated network calls. Existing enabled connectors operate separately through the orchestrator. A Python installation on your Windows PC is not available automatically to that cloud sandbox. [Runtime boundary and inventory](https://learn.microsoft.com/en-us/plugins/declarative-agent-skills)

Use local Python in VS Code for larger approved exports or calculations that need a local package. Run the code locally, inspect its reconciliation/exception output, then supply the appropriate result to your approved Copilot work session. Copilot should distinguish code it proposed from code that actually ran. For SharePoint ingestion, use the approved native Power Query connector where available and preserve source file, version and period evidence. [SharePoint connector](https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-folder)

VS Code's GitHub Copilot uses project `.github/skills/` or personal `~/.copilot/skills/` directories. Those locations do not install Microsoft 365 skills. Use this route only if your organization already provides or permits that separate product. [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

## Check the first task

Use a small synthetic file or an approved non-sensitive sample with a total you know. Ask the skill to report the population checked, calculation result, exceptions and any tools or sources it could not access. Confirm that an actual output file exists if a file was requested. For workbook workflows, verify the formulas and totals in Excel. For SharePoint evidence, verify the cited source location and version.

Example: “Use account-mapping to validate these five sample ledger lines against this mapping table. Show unmatched and multiply matched lines and reconcile the source amount to the mapped result.”

## Keep your installed copy current

GitHub is the maintained source. An already imported Chat or Agent Builder skill is a separate installed copy; the reviewed Microsoft documentation does not describe automatic synchronization from this repository.

When a skill changes, compare the new instructions with any company-specific additions before replacing the installed version. In Chat/Agent Builder, open the existing item and update its instructions/resources using that host's supported editor or replacement flow. In Excel/PowerPoint, update the matching skill folder or use the editor, then **Refresh**. Test the changed workflow again. Keep company-only additions outside the public repository.

Record the repository release/commit or package hash, host, skill name and imported date in your work notes. This lets you distinguish a fresh repository package from the version actually running in your account. If native Skills is unavailable, paste one skill's body into an approved chat with the task; that is a manual fallback and must be repeated or saved through an approved feature.
