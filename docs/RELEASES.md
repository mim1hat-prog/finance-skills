# Download and verify a release

[Ready-to-download releases](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/README.md) · [Current release notes](../release-notes/v1.4.3.md)

## Choose a package

From v1.3.0, each published version has five ZIP downloads under `releases/v<version>/`. Earlier releases retain their original four:

- **Markdown only:** complete Copilot and Gemini instruction bodies as `.md` files, the Excel agent profile and a start guide. Extract, open the relevant file and copy its full contents into an available Instructions field or approved conversation. YAML headers are removed. Every archive member is Markdown; checksums and the file inventory are kept outside this ZIP.
- **Copilot:** every Copilot skill as an individual native-import ZIP and matching folder, plus the Excel agent Instructions text.
- **Gemini:** every Gemini skill as an individual native-import ZIP and matching folder, Gem-ready text and the Excel agent Instructions text.
- **All skills:** both editions in one transport download.
- **Full:** the complete useful project, including both editions, individual packages, transport bundles, the profile, canonical source, offline guides, catalogue, local Python helpers, workflow schemas, benchmark dataset/API contract, research registry, citation metadata, examples and tests.

The full project also includes generated coverage statistics, static discovery metadata and the explicit community contribution templates. The Markdown-only ZIP remains instructions only.

Extract the outer ZIP in Windows File Explorer. For a native import, choose one of the individual ZIPs under `packages/copilot/` or `packages/gemini/`. For Excel's supported folder workflow, choose matching-name folders under `editions/copilot/` and follow the [Copilot guide](COPILOT.md). Full and transport ZIPs contain multiple skills and are not themselves native skill imports.

The full ZIP keeps the project at the archive root. Open its `README.md` or `site/index.html` after extraction. It excludes Git history, private work files, local environments, caches and previous release archives. It does not include third-party source archives or install optional packages, desktop tools, workers or APIs.

These downloads are hosted as versioned repository files. The available ChatGPT GitHub plugin supports repository publication but does not expose Git tag creation, GitHub Release creation or release-asset upload. No GitHub Release object or tag is implied by the download directory. All links work through the repository files; GitHub Actions is not required.

## Verify a download on Windows

Download `SHA256SUMS.txt` from the same version directory. In PowerShell:

```powershell
Get-FileHash .\finance-skills-v1.4.3-full.zip -Algorithm SHA256
```

Compare the resulting hash with the line for that exact filename. The release manifest also records file sizes and hashes. A checksum confirms that the downloaded bytes match the published manifest; it is not a digital signature or a guarantee of model behavior.

Versioned edition ZIPs are byte-for-byte copies of the validated transport bundles at the time of release. Each transport bundle contains its own manifest covering every other member. Every native skill ZIP still contains exactly one root `SKILL.md`.

The versioned Markdown ZIP is a byte-for-byte copy of `packages/markdown/finance-skills-markdown.zip`. Its external `packages/markdown/manifest.json` records every member's size and SHA-256; that inventory is included in the matching full release. The version's `SHA256SUMS.txt` verifies the Markdown ZIP directly. Release manifest schema 1 retains the original four-archive inventory; schema 2 requires the additional Markdown archive. Both formats remain verifiable.

## Version policy

`catalog.json` is the single version source. Use stable `MAJOR.MINOR.PATCH` numbers, without a `v` prefix in that field. Release directories and download filenames add `v`.

Set `releasedOn` to the actual release date; `reviewedOn` records source review and is not a substitute for release or dataset retrieval time. The build generates `CITATION.cff` from the authoritative version, repository and release date.

- **Major:** incompatible package formats, installation contracts, helper/schema/API interfaces or intentionally incompatible finance definitions.
- **Minor:** new compatible skills, profiles, tools or download capabilities.
- **Patch:** compatible instruction, documentation, packaging or implementation corrections.

Any change to the published package contents receives a new version. Preserve existing version directories and checksums. The release command refuses to overwrite an existing version with different bytes; generating identical bytes is a no-op. Do not delete a published snapshot to bypass that check. Previous packages remain available for rollback.

`releases/latest.json` and `releases/README.md` point to the highest verified stable version. The unversioned files under `packages/`, `editions/` and `profiles/` represent the current source build. Download a versioned release when you need a fixed package; record its version and hash in your private work notes.

## Prepare and publish a version

1. Finish the source, guide and catalogue changes. Bump `catalog.json`, set the actual release date and add `release-notes/v<version>.md` plus the changelog entry. Only change a source-review date when that review actually occurred. Record applicable method/provider evidence and rights in the research registry.
2. Generate and validate the current build:

   ```powershell
   py -3 scripts\research_registry.py
   py -3 scripts\build.py
   py -3 scripts\check_release.py
   ```

3. Complete relevant synthetic task checks and document the actual results in `docs/VALIDATION.md`. Resolve material failures before freezing. Finalize all files included in the full ZIP.
4. Freeze and check the release:

   ```powershell
   py -3 scripts\release.py
   py -3 scripts\check_release.py --require-release
   ```

5. Review the release inventory, download links, notes and checksums. Verify the publication identity and relevant Git history separately, following [SECURITY.md](../SECURITY.md#commit-identity-is-a-separate-publication-check). Use an authorized operation that preserves public no-reply author and committer identities; an authenticated Git transport is supported when the connector cannot do so. If no such authenticated route is available, retain the prepared change and report the access gap. Once those checks pass, publish source and release files together, preserving concurrent edits, then verify remote hashes. An authorized history repair must use the exact reviewed replacement history and an explicit expected-head lease.

The release tool is local and uses Python's standard library. It does not contact GitHub, create tags, publish a GitHub Release or activate a host skill. Its checks include the current generated build, exact release bytes, older snapshot integrity and the release index. Changing a frozen input requires a new version; a successful earlier check does not excuse later changes.

The offline gate also checks research IDs and exact supported uses, tool/workflow contracts, benchmark snapshots, API responses, tests and the public inventory including nested ZIP contents. It is suitable for an approved CI runner; no GitHub Actions workflow or server-enforced branch rule is claimed. Provider refresh and external source-update review are explicit separate commands, never side effects of the build or release gate. See [standards and scope](STANDARDS.md).

Supply `--commit-export C:\PrivateReview\commits.json` to `scripts/check_release.py` when checking identities from a GitHub export. The evidence must remain outside the project. Without this option the result explicitly reports that commit identity was not checked. Export scope and complete branch/tag history still need separate review; no successful artifact check authorizes a known identity leak.

## Update or roll back your agent

Repository updates do not replace an imported Copilot/Gemini skill. Download the chosen version, preserve any company additions, replace the host's existing copy and follow the applicable Refresh or Save step. Replace the saved Excel agent Instructions text separately if you use that form. Run a representative task in the approved account.

For rollback, use the previous version's package and repeat the same host replacement step. A package rollback does not uninstall a separate Python dependency or external service.
