# Discovery and community design

Repository settings checked **2026-11-26**; comparable-project practices reviewed **2026-11-25**. This project uses clear onboarding, useful finance examples and reproducible evidence to help people find and assess the library. Repository changes cannot guarantee indexing, search position, adoption or a particular user base.

## Practices adopted from comparable projects

| Primary source | Practice used here | Scope |
| --- | --- | --- |
| [Anthropic financial services](https://github.com/anthropics/financial-services) | Describe work by finance workflow and reuse canonical instructions across packages. | Repository organization; its Claude connectors and deployment commands do not establish Copilot/Gemini support. |
| [Microsoft skills](https://github.com/microsoft/skills/blob/main/README.md) | Select relevant skills and define acceptance criteria with invented cases. | The [evaluation protocol](EVALUATION.md) adapts this approach; Microsoft SDK tests are not evidence about this library. |
| [Scientific Agent Skills](https://github.com/K-Dense-AI/scientific-agent-skills) | Present examples, version provenance, citations and validation limits. | Use the existing source registry and software citation; do not borrow another project's adoption or scientific-performance claims. |
| [OpenBB](https://github.com/openbq-org/OpenBB) | Offer distinct bug, improvement and contribution routes. | [Support](../SUPPORT.md), issue templates and the contribution process. No OpenBB runtime is installed by these changes. |
| [VoltAgent curation policy](https://github.com/VoltAgent/awesome-agent-skills/blob/main/CONTRIBUTING.md) | Prioritize working documentation and demonstrated use before seeking a curated listing. | No listing, endorsement or external submission is claimed. |
| [uv](https://github.com/astral-sh/uv) | Introduce the purpose briefly, make an evidenced graphic prominent, and provide a short installation route. | The homepage uses its own descriptive coverage figure; no upstream benchmark numbers or performance claims are copied. |
| [FastAPI](https://github.com/fastapi/fastapi) | Put clear documentation links and a small working example within easy reach. | The invented reconciliation example illustrates this project's output; it is not a FastAPI implementation or efficacy study. |
| [Ollama](https://github.com/ollama/ollama) | Separate downloads by target platform and connect getting started to deeper documentation. | Copilot, Gemini and Markdown choices remain explicit; no Ollama runtime, compatibility or privacy claims are inherited. |

The comparison records observed practices, not a study of what caused those projects' popularity. It copies no upstream prose or assets and does not advance reviewed runtime pins. GitHub's [README guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) and [community profile guidance](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories) support a clear purpose, [invented quick-start example](../examples/QUICKSTART.md), support route and contributor expectations. The [issue-template format](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository) provides the public reporting entry points.

## Homepage layout

The [main README](../README.md) uses a compact original [dot-style hero](../assets/readme-hero.svg), followed by the generated coverage figure before the quick start. A short numerical fallback keeps the main results available if the image does not render. Download choices identify their platform and contents; detailed account setup, methods and validation remain one link away. This follows the observed presentation patterns above while keeping all figures specific to this repository. Neither the layout nor those projects' popularity establishes a future adoption result.

## Search visibility

Follow [Google's SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide): write original useful content, use descriptive headings and link text, and keep titles and descriptions accurate. The repository README should identify Microsoft 365 Copilot, Gemini, Excel and the supported finance tasks in natural language. A static catalogue should expose useful explanatory text and navigation even before someone uses its filters.

The generated JSON-LD uses [Schema.org SoftwareSourceCode](https://schema.org/SoftwareSourceCode) to describe the actual repository, version and source languages. It adds no ratings, user counts or academic affiliation. [Google's structured-data guidance](https://developers.google.com/search/docs/appearance/structured-data/sd-policies) requires markup to represent visible content; correct markup does not guarantee a rich result. No Google rich-result eligibility or deployment is claimed for this source-code description.

Keep all visible counts generated from canonical sources. State the unit, denominator and scope. Skill counts, references and stored observations describe the repository; they are not accuracy scores, market coverage, endorsements or active-user measurements. [Evaluation limits](EVALUATION.md) · [Actual validation](VALIDATION.md)

## Observed repository settings

The authenticated repository metadata read on **2026-11-26** confirmed that the About description and all 12 topics match [tools/discovery-profile.json](../tools/discovery-profile.json). The default branch is `main`. The repository reports no GitHub Pages deployment and no homepage URL. These observations supersede the earlier empty-description/topic check; they do not measure search indexing or adoption.

- **About description and topics:** the profile is the canonical text and set of relevant topics. [PROJECT-METADATA.json](PROJECT-METADATA.json) is the generated record; edit the source profile, rebuild and verify the remote settings separately.
- **Social preview:** [assets/social-preview.svg](../assets/social-preview.svg) is an original 1280 × 640 source asset. Its selection in GitHub settings has not been verified. Export it as a PNG, then select that image in the repository's settings. GitHub recommends a PNG, JPG or GIF below 1 MB, ideally 1280 × 640 pixels. A committed image alone does not configure that setting.

GitHub documents [topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics) and [social-preview setup](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview). Use only relevant public topics. Do not invent a published website, set a canonical URL to an unlaunched site or claim a sitemap is being served without a deployment.

## Measure use honestly

Prioritize reproducible bug reports, onboarding friction and public contributions when deciding what to improve. If maintainers later publish traffic or download statistics, record the source, observation window and counting method; distinguish visits, downloads, stars and users. This repository does not collect work prompts, workbook contents or usage telemetry.
