# Finance skills v1.1.0

## Downloads

These are repository-hosted release files, not GitHub Release assets.

| Download | File |
| --- | --- |
| Copilot skills | [finance-skills-v1.1.0-copilot.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/finance-skills-v1.1.0-copilot.zip) |
| Gemini skills | [finance-skills-v1.1.0-gemini.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/finance-skills-v1.1.0-gemini.zip) |
| Both editions | [finance-skills-v1.1.0-all.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/finance-skills-v1.1.0-all.zip) |
| Full project, tools and documentation | [finance-skills-v1.1.0-full.zip](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/finance-skills-v1.1.0-full.zip) |

Extract a transport bundle before importing individual native skill ZIPs. The full project archive contains source, tools and documentation; it is not a native skill import.

[SHA-256 checksums](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/SHA256SUMS.txt) · [Release manifest](https://raw.githubusercontent.com/mim1hat-prog/finance-skills/main/releases/v1.1.0/manifest.json)

## Release notes

Released 2026-11-25. A compatible feature release for Microsoft 365 Copilot and Gemini on the Windows work environment.

### Added

- Your Excel agent operating instructions as `excel-agent-core`, both native editions and `profiles/excel-agent-instructions.txt` for the existing agent's Instructions field.
- Enterprise-source-first retrieval, another reasonable search when evidence is incomplete, preservation of existing workbook logic, internal calculation checks and concise outcomes.
- Copilot, Gemini and combined download-all bundles with extraction instructions and a manifest for every bundled file.
- Four versioned release downloads: Copilot, Gemini, all skills and the full project, with release notes, SHA-256 checksums and a release index.
- A deterministic local release command that preserves published version directories and rejects changed bytes under an existing version.
- Prominent download-all, edition download and Excel agent Instructions links in the dot catalogue, with no-JavaScript fallbacks.

### Changed

- The library now has 25 canonical skills and 50 individual native-import ZIPs.
- Both host adapters prohibit unsolicited audit tables, new worksheets and audit text by default.
- Existing skills retain their checks while removing conflicting mandatory audit tables, evidence registers, extra-sheet layouts and repetitive process reports. Requested business tables and reports remain supported.

### Use this release

Extract the outer ZIP first. Import individual ZIPs under `packages/<edition>/`, or use the supported Office folder workflow. Paste `profiles/excel-agent-instructions.txt` into the agent's Instructions field for the default behavior you already configure there. Selecting or importing a skill does not guarantee automatic invocation on every request.

The full ZIP includes offline guides, the catalogue and optional local Python tools. Edition and all-skills ZIPs contain the portable instructions and packages. No package activates a work-account skill, grants enterprise access or installs a background service.

### Compatibility and checks

Individual native package format is unchanged: one root `SKILL.md`, simple YAML frontmatter and standalone text. Existing folder-copy behavior and checksum manifests remain supported.

Build checks, archive/hash tests, installer regressions and synthetic task evidence are recorded in `docs/VALIDATION.md` in the full package and repository. Native imports, Windows/OneDrive behavior and real enterprise-source access still require the approved target account. The catalogue's rendered desktop/mobile check remains unavailable in the build environment; DOM and static checks are recorded separately.

### Updating from 1.0.0

Choose the new individual packages you use and replace the corresponding saved host copies; use Refresh where the Office guide requires it. Add the new Instructions text to your existing agent configuration. Preserve company-specific additions in approved work storage. This repository update does not silently replace any installed copy.
