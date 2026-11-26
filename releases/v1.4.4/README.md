# Finance skills v1.4.4

## Downloads

These are repository-hosted release files, not GitHub Release assets.

| Download | File |
| --- | --- |
| Copilot skills | [finance-skills-v1.4.4-copilot.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/finance-skills-v1.4.4-copilot.zip) |
| Gemini skills | [finance-skills-v1.4.4-gemini.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/finance-skills-v1.4.4-gemini.zip) |
| Both editions | [finance-skills-v1.4.4-all.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/finance-skills-v1.4.4-all.zip) |
| Copy-and-paste Markdown only | [finance-skills-v1.4.4-markdown.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/finance-skills-v1.4.4-markdown.zip) |
| Full project, tools and documentation | [finance-skills-v1.4.4-full.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/finance-skills-v1.4.4-full.zip) |

For copy and paste, extract the Markdown-only ZIP, open START-HERE.md, then copy the relevant Copilot or Gemini file. Every file in that ZIP is Markdown.

Extract a transport bundle before importing individual native skill ZIPs. The full project archive contains source, tools and documentation; it is not a native skill import.

[SHA-256 checksums](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/SHA256SUMS.txt) · [Release manifest](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.4.4/manifest.json)

## Release notes

Package prepared **2026-11-26**. Remote publication is verified separately.

### Choose the correct Copilot import

The README and Copilot guide now put an individual native skill ZIP beside the copy-and-paste download. Native packages contain a root `SKILL.md` with `name` and `description` in YAML frontmatter. The copy-only Markdown files deliberately omit that header and belong in an Instructions field; the outer full and edition bundles must be extracted before choosing an individual package.

The guide explains the reported invalid-skill-information error and how to check the actual file and upload surface. Microsoft 365 Copilot Chat accepts a complete individual ZIP or standalone `SKILL.md`; Agent Builder requires the complete individual ZIP. Existing native metadata meets the documented format, so this release preserves it rather than guessing a replacement parser rule. A specific rejected file and host are still required to confirm an individual import failure.

Generated bundle guides carry the format distinction, and setup guides use maintained download destinations. Three directly reviewed Microsoft references record the import requirements and troubleshooting guidance. No successful installation in a work account is claimed.

Canonical finance instructions, native headers, benchmark values, acquisition dates and earlier frozen releases remain unchanged. Generated native packages receive the current edition version record; their finance procedures are unchanged. Weekly maintenance remains on Wednesdays at 08:00 Asia/Tokyo.
