# Use finance skills with Gemini

Verified against official documentation on **2026-11-25**. This guide targets **Gemini's web app on a Windows 11 work PC**, using the account your organization permits for the data. Repository packages are ready for import; account activation and a representative task still need to succeed in that account.

[Browse the Gemini edition](../editions/gemini) · [Download individual Gemini packages](../packages/gemini) · [Copilot guide](COPILOT.md)

## Check which interface your work account has

Look for **Customize → Skills** at [gemini.google.com](https://gemini.google.com); **Customize** may be under **More**. Use native Skills when available. If the work account still exposes Gems without Skills, use the fallback below.

Google's current pages differ on the work-account rollout. The [Workspace administrator guide](https://knowledge.workspace.google.com/admin/generative-ai/gemini-app/about-the-transition-to-skills), updated November 9, says Gemini-app skills are available across Workspace editions. The [consumer transition FAQ](https://support.google.com/gemini/answer/18560919?hl=en) still says work/school availability is coming soon. The actual approved account's interface and organization settings determine the available route. The Workspace guide keeps business/enterprise Gems available until no earlier than March 1, 2027.

Gemini App, skills in Google Workspace apps, Gemini Enterprise and Gemini CLI are different surfaces. A skill imported here should not be assumed to appear in the others. This repository's Gemini edition does not require Gemini CLI or a paid API key.

## 1. Download one skill

Open [packages/gemini](../packages/gemini), choose an individual ZIP and use GitHub's download control. Each ZIP contains `SKILL.md` at its root. Start with `excel-data-coverage`, `forecast-variance`, `account-mapping`, `evidence-research` and `business-document`, then add specialist workflows as needed.

If you download the full repository, extract it and locate a single folder under `editions/gemini`. Do not upload the entire repository or a folder containing several skills. Google permits **one skill per import**. [Transfer guide](https://support.google.com/gemini/answer/18977944)

## 2. Import and invoke

1. In the Gemini web app, select **Customize → Skills**.
2. Select **Create → Upload**.
3. Choose the individual ZIP, a single skill folder or its standalone `SKILL.md`, then select **Open**.
4. Select **Upload**, review the instructions and choose **Create**.
5. In a new chat, select the skill with `/name`, or the available `@` picker. Use explicit selection for the first verification task.

Review the entire skill before adding confidential task data. A skill file attached to an ordinary chat is context for that chat; it is not evidence that native installation succeeded. Google documents editing, activation, replacement and invocation in its [create/manage guide](https://support.google.com/gemini/answer/17094296).

## Package rules and capabilities

Google's current limits are **100 MB total, at most 100 files and 10 MB for SKILL.md**. The main file needs YAML `name` and `description` plus nonempty instructions. Names are at most 64 characters, descriptions at most 1,024. This repository uses smaller portable files and simple frontmatter.

Gemini imports do not accept nested archives, `.skill` packages, separate `.sql` files, TypeScript/TSX/JSX files or legacy `.doc`, `.xls` and `.ppt` resources. SQL in these skills is plain text inside Markdown. Scripts that depend on internet or external APIs are blocked when a skill runs. Adding a script file does not establish that its required packages or a local Windows runtime exist. [Google's transfer constraints](https://support.google.com/gemini/answer/18977944)

The current transition FAQ says native Skills do not work with Canvas or Deep Research. The research and visualization skills therefore use capabilities actually available in the session; they do not promise to invoke those features. If you choose a separate supported feature, carry over the relevant instructions as task context and verify the resulting workflow separately. [Feature limits](https://support.google.com/gemini/answer/18560919?hl=en)

Skills can be used with Keep Activity off, but connected apps that require it are then unavailable. Company account settings may be controlled by your administrator. Do not assume Gemini can access internal SharePoint merely because that source is available in Microsoft 365. Use approved connected access or supply an appropriate authorized export. [Skills and connected apps](https://support.google.com/gemini/answer/17094296)

## Windows Python and VS Code

Use the available local Python environment for calculations or larger files that require a specific local library. The Gemini skill can describe the procedure and interpret supplied outputs, but it cannot automatically execute code on your PC. Keep original inputs unchanged, run the code locally, and verify the resulting totals and exception report before using the result in a decision.

For Power BI, prefer a repeatable local/Power Query pipeline with clear grain, source coverage and refresh evidence. Supply Gemini with the relevant schema, measures or approved result when you want a review. A suggested DAX measure, M query or Python script remains a proposal until it has run successfully in the intended environment.

Use approved company templates for work output. The dot visual design in this repository is for the repository; it does not supply your company's visual identity or permission to move employer assets into a public repository.

## Verify the first task

Use a synthetic or approved small sample with known totals. Ask the selected skill to state what it inspected, which calculations it performed and which checks remain. Verify the results in the actual workbook/report where appropriate. Check that downloadable files really exist if the request asked for files, and that citations lead to the claimed evidence.

Example: “Use cash-working-capital with these synthetic opening and closing balances and 30 days of credit sales. Show your DSO numerator, denominator and averaging method, and distinguish modeled cash improvement from cash actually received.”

## Replace an installed skill when it changes

GitHub updates do not automatically replace an imported personal Gemini skill. To update:

1. Download the current individual package from [packages/gemini](../packages/gemini).
2. Open **Customize → Skills** and select the existing skill.
3. Select **More → Replace skill** and upload the complete replacement, including any reference files.
4. Review, **Save**, and repeat a representative test.

Google says file updates require uploading the skill with its reference files again. Preserve any company-specific additions in your approved work notes and compare them with the incoming version before replacement. Keep a record of the package hash or repository commit, skill name and imported date. [Replacement instructions](https://support.google.com/gemini/answer/17094296)

## Fallback: use a Gem or a manual chat instruction

If Skills is unavailable but your approved work account offers Gems:

1. Open **Settings → Gems → New Gem**; use the equivalent Gems entry if your account still shows the older navigation.
2. Choose one workflow from the [Gem-ready text files](../editions/gemini-gems), which omit YAML frontmatter.
3. Give the Gem the skill's readable name and paste the selected text into the Gem's **Instructions**. Alternatively, copy a native skill's Markdown body **after the closing YAML `---`**. Use the description in a corresponding field if your interface provides one.
4. If a future version references supporting files, add those actual files to Knowledge as permitted. An absent resource must be identified; a link or filename alone does not upload it. The current standalone skills need no supporting files.
5. Preview with a sample task, review the output and select **Save**. Previewing alone does not save the Gem.

This copies the workflow into a Gem; it is not native SKILL.md registration and will need manual updates. Uploading the Markdown only as a Knowledge file is not equivalent to placing its instructions in the Instructions field. Follow Google's [Gem creation guide](https://support.google.com/gemini/answer/15235603?hl=en).

If neither feature is available, paste the body of one skill into a normal approved Gemini chat before the task. Keep the context focused on that workflow. The instructions apply to that chat and do not install a persistent skill. Do not move company data to a personal account to obtain a feature that is unavailable in the work account.
