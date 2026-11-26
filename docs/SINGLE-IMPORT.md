# Install all finance workflows as one skill

Each complete suite contains one skill named `finance-suite`, with all 30 finance workflows in nine reference files. Choose the package for the actual host. **Excel uses an extracted folder in its app-created OneDrive location; Chat/Builder and Gemini use their supported ZIP-upload screens.**

| Host | Current download | What to add |
| --- | --- | --- |
| Copilot in Excel | [Excel OneDrive folder ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/excel/finance-suite-onedrive.zip) | Extract All, then add the inner `finance-suite` folder to the location Excel opens |
| Copilot Chat / Agent Builder / Cowork | [Copilot suite ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/suites/finance-suite-copilot.zip) | Upload this complete ZIP unchanged |
| Gemini Apps | [Gemini suite ZIP](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/suites/finance-suite-gemini.zip) | Upload this complete ZIP unchanged |

Use the [versioned release](../releases/README.md) when a fixed version and checksum are required.

## What one import means

The suite contains one root `SKILL.md` with valid `name` and `description` metadata, plus nine `references/<category>.md` files. Each category file has an index and explicitly named workflow sections. The main instructions retain the shared operating rules and route the task to the relevant file and complete procedure. The external manifest records each workflow's canonical source hash, body hash and exact byte range within its category file.

**Packaging correction in v1.5.1:** the earlier v1.5.0 suite has 29 companions, exceeding Cowork's documented 20-companion limit. The grouped layout retains every complete workflow while reducing the suite to ten files overall. The reviewed Excel page does not specify that ceiling; it cannot diagnose an Excel rejection. [Host-specific limits and troubleshooting](COPILOT.md#troubleshoot-unsupported-invalid-import-limit-or-responsible-ai-errors)

This is one installed skill with multiple workflows. It does not register each workflow separately, install Python or Power BI, enable a connector, or expand a host's permissions or limits. The individual packages remain available for more narrowly scoped installations. No native import or model-routing success is inferred from a valid ZIP.

Microsoft documents a matching-name skill folder for [Excel](https://support.microsoft.com/en-gb/excel/copilot/copilot-in-excel-skills), a root `SKILL.md` with supporting files for [Copilot Chat](https://learn.microsoft.com/en-us/plugins/build-copilot-chat-skills), and a complete ZIP for [Agent Builder](https://learn.microsoft.com/en-us/plugins/agent-builder-add-skills). Google documents [one skill with reference files per import](https://support.google.com/gemini/answer/18977944?hl=en) and [reading supporting files as needed](https://support.google.com/gemini/answer/17102773). These package-format sources were reviewed on **2026-11-26**; routing behavior remains subject to a representative check in the actual host.

## Copilot Chat or Agent Builder

1. Download the Copilot suite ZIP. Keep it intact; do not extract and upload only `SKILL.md`, because this suite needs its reference files.
2. In Copilot Chat, use **Agents → More agents → Add → Upload skill**. In Agent Builder, open **Configure → Skills → Add**.
3. Upload the complete suite ZIP, review the `finance-suite` entry and save.
4. Explicitly select `finance-suite` for the first task. In an Agent Builder agent this is one skill entry.

Example: “Use finance-suite to validate this dated account mapping, retain unmatched records and reconcile the mapped result to the source total.”

## Copilot in Excel

1. Download the **Excel OneDrive folder ZIP** above. In Windows, choose **Extract All** and find the inner `finance-suite` folder.
2. In Excel's Copilot pane, open **… → Manage plugins & skills → Custom skills**, then **Create OneDrive folder** if needed and **Open skills folder**.
3. Add the inner `finance-suite` folder there, with its `SKILL.md` and nine files under `references/`. Keep `finance-suite` identical to the name in the metadata. Uploading the archive or its version-named outer folder will not provide that required structure.
4. Wait for upload or sync, select **Refresh**, and invoke **`@finance-suite`**. Enable automatic use if desired.

This is one folder addition containing all 30 workflows. The main `SKILL.md` alone lacks their complete procedures. Preserve approved private additions before replacing an old folder; replace the previous reference set as a whole. Confirm recognition and supporting-file access in the actual account. [Requirements and exact Excel setup](COPILOT.md#3-copilot-in-excel)

## Copilot Cowork

Open **Plugins → Add → Upload** and select the complete Copilot suite ZIP. Cowork documents both archive limits and a separate per-skill limit of 20 companions. The current suite has nine companions. Keep the ZIP's root `SKILL.md` and all its reference files together. [Cowork upload guide](https://learn.microsoft.com/en-us/copilot/cowork/cowork-customize) · [Per-skill companion limit](https://learn.microsoft.com/en-us/copilot/cowork/use-cowork)

## Gemini Apps

1. Download the Gemini suite ZIP and keep it intact.
2. Open **Customize → Skills → Create → Upload** and select the ZIP.
3. Review and create the one `finance-suite` skill.
4. Explicitly select it in a new chat for the first task. Keep the packaged references attached.

The suite requires native Skills with supporting-file access. A Gem's Instructions field or a pasted chat message is a separate route: use the [copy-and-paste workflow files](../packages/markdown/finance-skills-markdown.zip?raw=1) for that route. Pasting only the suite's main file does not transfer its references. [Gemini setup and replacement](GEMINI.md)

## Check the first result

Use the [invented reconciliation example](../examples/QUICKSTART.md), a forecast-variance case or another small task with a known expected result. Confirm that the host can read the named workflow section in the relevant `references/<category>.md` and that the actual calculation agrees. If a required file is inaccessible, use its individual package or supply the approved workflow text; the suite must not pretend it read that file. Package checks do not establish task accuracy or enterprise source access.

## Updates and fallback

Replace the installed suite with the complete newer ZIP, including all reference files, or update its complete Excel folder and Refresh. Compare and preserve any approved company additions in the private work environment. A GitHub update does not replace an imported copy automatically.

If a skill is not recognized, first check the route: Excel needs the matching-name folder inside its own skills location; a ZIP-upload screen needs the complete suite or an individual native ZIP. The Markdown-only download is for pasting. Use the [Copilot troubleshooting steps](COPILOT.md#troubleshoot-invalid-skill-information) and identify the exact file or folder and host if the unchanged package still fails.
