# All finance workflows in one import

Download the **Copilot complete suite** or **Gemini complete suite** from the [current versioned release](../releases/README.md). Each ZIP registers one skill named `finance-suite`, containing all 29 complete finance workflows grouped into nine reference files. Upload the suite ZIP itself through the host's supported Skills screen.

Current build downloads: [Copilot suite](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/suites/finance-suite-copilot.zip) · [Gemini suite](https://github.com/mim1hat-prog/finance-skills/raw/refs/heads/main/packages/suites/finance-suite-gemini.zip). Use a versioned release when a fixed version and checksum are required.

## What one import means

The suite contains one root `SKILL.md` with valid `name` and `description` metadata, plus nine `references/<category>.md` files. Each category file has an index and explicitly named workflow sections. The main instructions retain the shared operating rules and route the task to the relevant file and complete procedure. The external manifest records each workflow's canonical source hash, body hash and exact byte range within its category file.

**Packaging correction in v1.5.1:** the earlier v1.5.0 suite has 29 companions, exceeding Cowork's documented 20-companion limit. The grouped layout retains every complete workflow while reducing the suite to ten files overall. The generic import rejection does not prove that this limit was the cause on an unidentified Copilot screen. [Host-specific limits and troubleshooting](COPILOT.md#troubleshoot-unsupported-invalid-import-limit-or-responsible-ai-errors)

This is one installed skill with multiple workflows. It does not register 29 separate skills, install Python or Power BI, enable a connector, or expand a host's permissions or limits. The individual packages remain available for more narrowly scoped installations. No native import or model-routing success is inferred from a valid ZIP.

Microsoft documents a root `SKILL.md` with supporting files for [Copilot Chat](https://learn.microsoft.com/en-us/plugins/build-copilot-chat-skills), while [Agent Builder](https://learn.microsoft.com/en-us/plugins/agent-builder-add-skills) requires a complete ZIP. Google documents [one skill with reference files per import](https://support.google.com/gemini/answer/18977944?hl=en) and [reading supporting files as needed](https://support.google.com/gemini/answer/17102773). These package-format sources were reviewed on **2026-11-26**; routing behavior is the project's design and still needs a representative check in the actual host.

## Copilot Chat or Agent Builder

1. Download the Copilot suite ZIP. Keep it intact; do not extract and upload only `SKILL.md`, because this suite needs its reference files.
2. In Copilot Chat, use **Agents → More agents → Add → Upload skill**. In Agent Builder, open **Configure → Skills → Add**.
3. Upload the complete suite ZIP, review the `finance-suite` entry and save.
4. Explicitly select `finance-suite` for the first task. In an Agent Builder agent this is one skill entry.

Example: “Use finance-suite to validate this dated account mapping, retain unmatched records and reconcile the mapped result to the source total.”

## Copilot in Excel

Use the OneDrive skills folder opened by Excel through **Manage plugins & skills → Custom skills**. Copy the complete `finance-suite` folder from `editions/copilot-suite/finance-suite/` in the full release, including its `references/` folder, into that location. Alternatively, extract the suite ZIP into a folder named exactly `finance-suite`. Select **Refresh**, then choose `finance-suite` for the task. When upgrading from v1.5.0, replace the old folder rather than combining its 29 reference files with the new nine; first preserve any approved private customizations separately. This is one folder addition; availability and sync still depend on the work account. [Excel setup](COPILOT.md#3-copilot-in-excel)

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

If upload reports missing `name` or `description`, confirm that you selected a **suite ZIP** or an **individual native ZIP**. The Markdown-only and outer transport/full downloads have different purposes. Use the [Copilot troubleshooting steps](COPILOT.md#troubleshoot-invalid-skill-information) and identify the exact file and host if the unmodified suite still fails.
