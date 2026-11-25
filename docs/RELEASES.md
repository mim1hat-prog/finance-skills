# Download and verify a release

[Ready-to-download releases](https://github.com/mim1hat-prog/finance-skills/blob/main/releases/README.md) · [Current release notes](../release-notes/v1.1.0.md)

## Choose a package

Each published version has four ZIP downloads under `releases/v<version>/`:

- **Copilot:** every Copilot skill as an individual native-import ZIP and matching folder, plus the Excel agent Instructions text.
- **Gemini:** every Gemini skill as an individual native-import ZIP and matching folder, Gem-ready text and the Excel agent Instructions text.
- **All skills:** both editions in one transport download.
- **Full:** the complete useful project, including both editions, individual packages, transport bundles, the profile, canonical source, offline setup guides, catalogue, local Python helpers, examples and tests.

Extract the outer ZIP in Windows File Explorer. For a native import, choose one of the individual ZIPs under `packages/copilot/` or `packages/gemini/`. For Excel's supported folder workflow, choose matching-name folders under `editions/copilot/` and follow the [Copilot guide](COPILOT.md). Full and transport ZIPs contain multiple skills and are not themselves native skill imports.

The full ZIP keeps the project at the archive root. Open its `README.md` or `site/index.html` after extraction. It excludes Git history, private work files, local environments, caches and previous release archives. It does not include third-party source archives or install optional packages, desktop tools, workers or APIs.

These downloads are hosted as versioned repository files. The available ChatGPT GitHub plugin supports repository publication but does not expose Git tag creation, GitHub Release creation or release-asset upload. No GitHub Release object or tag is implied by the download directory. All links work through the repository files; GitHub Actions is not required.

## Verify a download on Windows

Download `SHA256SUMS.txt` from the same version directory. In PowerShell:

```powershell
Get-FileHash .\finance-skills-v1.1.0-full.zip -Algorithm SHA256
```

Compare the resulting hash with the line for that exact filename. The release manifest also records file sizes and hashes. A checksum confirms that the downloaded bytes match the published manifest; it is not a digital signature or a guarantee of model behavior.

Versioned edition ZIPs are byte-for-byte copies of the validated transport bundles at the time of release. Each bundle contains its own manifest covering every other member. Every native skill ZIP still contains exactly one root `SKILL.md`.

## Version policy

`catalog.json` is the single version source. Use stable `MAJOR.MINOR.PATCH` numbers, without a `v` prefix in that field. Release directories and download filenames add `v`.

- **Major:** incompatible package formats, changed installation contracts or intentionally incompatible finance definitions.
- **Minor:** new compatible skills, profiles, tools or download capabilities.
- **Patch:** compatible instruction, documentation, packaging or implementation corrections.

Any change to the published package contents receives a new version. Preserve existing version directories and checksums. The release command refuses to overwrite an existing version with different bytes; generating identical bytes is a no-op. Do not delete a published snapshot to bypass that check. Previous packages remain available for rollback.

`releases/latest.json` and `releases/README.md` point to the highest verified stable version. The unversioned files under `packages/`, `editions/` and `profiles/` represent the current source build. Download a versioned release when you need a fixed package; record its version and hash in your private work notes.

## Prepare and publish a version

1. Finish the source, guide and catalogue changes. Bump `catalog.json` and add `release-notes/v<version>.md` plus the changelog entry. Only change a source-review date when that review actually occurred.
2. Generate and validate the current build:

   ```powershell
   py -3 scripts\build.py
   py -3 scripts\build.py --check
   py -3 -m unittest discover -s tests -v
   ```

3. Complete relevant synthetic task checks and document the actual results in `docs/VALIDATION.md`. Resolve material failures before freezing. Finalize all files included in the full ZIP.
4. Freeze and check the release:

   ```powershell
   py -3 scripts\release.py
   py -3 scripts\release.py --check
   ```

5. Review the release inventory, download links, notes and checksums. Publish source changes and generated release files together through the ChatGPT GitHub plugin, preserving concurrent edits. Verify the remote file hashes after publication.

The release tool is local and uses Python's standard library. It does not contact GitHub, create tags, publish a GitHub Release or activate a host skill. Its checks include the current generated build, exact release bytes, older snapshot integrity and the release index. Changing a frozen input requires a new version; a successful earlier check does not excuse later changes.

## Update or roll back your agent

Repository updates do not replace an imported Copilot/Gemini skill. Download the chosen version, preserve any company additions, replace the host's existing copy and follow the applicable Refresh or Save step. Replace the saved Excel agent Instructions text separately if you use that form. Run a representative task in the approved account.

For rollback, use the previous version's package and repeat the same host replacement step. A package rollback does not uninstall a separate Python dependency or external service.
