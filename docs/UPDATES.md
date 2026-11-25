# Keep the library and installed copies current

Reviewed **2026-11-25**. A repository update and an installed Copilot/Gemini update are separate events. This workflow keeps that distinction visible.

| Layer | Source of truth | Update mechanism | Evidence |
| --- | --- | --- | --- |
| Financial workflow | `skills/<name>/SKILL.md` | Review and edit canonical instructions | Focused task checks and a documented change |
| Host behavior | `adapters/` and platform guides | Compare current official Microsoft/Google docs | Dated sources, account caveats and actual restrictions |
| Upload packages | `editions/`, `packages/` | Deterministic `scripts/build.py` | Exact bytes and SHA-256 manifest |
| Copy-and-paste Markdown | Generated edition bodies and Excel profile | Generate `packages/markdown/` with `scripts/build.py` | Markdown-only ZIP with external file inventory; replace pasted copies manually |
| Coverage and discovery | Canonical catalogues, research, public snapshots, `tools/discovery-profile.json` | Generate metrics and static catalogue in the main build | Exact generated counts, denominators, source hashes and no implied adoption/performance score |
| Excel agent defaults | `skills/excel-agent-core/SKILL.md` | Generate `profiles/excel-agent-instructions.txt` with the editions | Body-only text from one canonical source |
| Release downloads | `releases/v<version>/` | Freeze with `scripts/release.py` after validation | Versioned ZIPs, release notes, SHA-256 checksums and no-overwrite check |
| Upstream ideas/tools | `upstream.lock.json` | Check commits, then review relevant diffs/licences | Pinned reviewed revision; new head is only a candidate |
| Tool routing | `tools/catalog.json` and `catalog.json` | Review availability/evidence requirements and regenerate lists/contracts | Every route resolves to an existing skill; a listing does not claim installation |
| Research and standards | `research/sources.json` | Review publisher corrections, superseding editions and exact implementation uses | Resolved source IDs, rights and review status; generated registry agrees |
| Public benchmarks | `benchmarks/catalog.json` and immutable snapshots | Run an explicit reviewed collector/import command | Source, unit, period, rights, lineage, retrieval time and exact snapshot hashes |
| Work account | The host's saved/imported copy | Replace/edit or OneDrive folder update plus Refresh | Local installed-version record and a representative task |

## Check what changed

Run the read-only checker from the repository root:

```powershell
py -3 scripts\check_updates.py --output .local\upstream-check.json
```

Read the command's `--help` for lock, output and timeout options. The checker uses public HTTPS endpoints and no credentials. A changed upstream commit is **not** a verified compatibility update. Network failures, rate limits and inaccessible documentation must remain visible; they must not be labeled current.

The lock records reviewed repository commits and primary documentation URLs. Review official product pages directly for rollout, licensing, file import, script/network, OneDrive refresh and replacement changes. An HTTP response or changed page hash alone is not semantic review. Do not adopt a moving `main`, `latest` package or a third-party ranking as a quality guarantee.

For research metadata, `py -3 scripts\research_registry.py --check-updates` performs an explicit public update check. Review publisher/Crossref results and the applicable notice before changing a method. Flag affected skills when a correction, retraction or superseding edition is unresolved; do not silently treat a candidate as active support. Regenerate the readable registry only after updating its canonical source records.

Public benchmark refresh is separate from repository maintenance and offline defaults. Review exact series, units, rights and adapter status, then use the explicit commands in [the dataset guide](../benchmarks/README.md). Preserve prior vintages and failed-refresh evidence. Do not redate source reviews, silently replace a series, overwrite a last-good snapshot or reconstruct an internal blank with a public proxy.

## Apply a reviewed change

1. Compare the source diff and read the relevant primary documentation. Check the project's licence, resource dependencies, data transmission and supported host.
2. Adapt only the useful procedure. Keep the work instructions executable within the selected host; move optional local setup into the Windows guide. Do not copy an unavailable service's capability into a Markdown promise.
3. Edit the canonical skill once. Change the host overlay only if Copilot or Gemini behaves differently. Keep company-only logic/templates outside the public repository.
4. Bump the version in `catalog.json` according to the [release policy](RELEASES.md), set the actual `releasedOn`, add `release-notes/v<version>.md` and update `CHANGELOG.md`. Change the actual review date and the affected `upstream.lock.json` entry only when that review occurred. Do not refresh dates simply because a checker ran.
5. Generate and validate:

   ```powershell
   py -3 scripts\research_registry.py
   py -3 scripts\build.py
   py -3 scripts\check_release.py
   ```

6. Run a representative synthetic task for changed financial logic. Run optional dependency tests when those helpers change. Review desktop/mobile output for catalogue changes when a browser is available. Record skipped or blocked checks honestly.
7. Finalize the validation record, then freeze and verify with `py -3 scripts\release.py` and `py -3 scripts\check_release.py --require-release`. Keep every previous version directory. A changed frozen input requires a new version.
8. Verify public no-reply author/committer identities and relevant history separately from source contents. A local Git identity does not establish a connector identity. If a private identity is unresolved and the connector cannot select a safe identity, retain prepared work. Once publication checks pass, publish reviewed files and exact versioned packages together, verify remote paths/hashes and preserve concurrent changes.

The default tests skip optional openpyxl/DuckDB checks when their packages are unavailable. A maintainer changing those helpers must run with the pinned dependencies and confirm those checks actually executed.

The offline gate checks generated sources and packages, research references, tool/workflow contracts, data/API contracts, tests and nested publication artifacts. It does not search the internet, call public providers or prove native account execution. [Standards](STANDARDS.md) · [Contribution procedure](../CONTRIBUTING.md)

## Ongoing maintenance

Check the GitHub homepage on `main` as an output: the root README must embed
the generated coverage figure before quick start, and its image and numerical
block must agree with the current canonical inputs. Regenerate these outputs
for every reviewed skill, evidence or dataset change and publish them in the
same commit. A mismatch is actionable even if no new skill is being added.
Verify the remote README and image hashes after publication. Keep the existing
daily check as a backstop; a schedule is not a guarantee of continuous updates.

The README does not execute the collector or plotting code in a visitor's
browser. Its graph reflects the latest successfully published repository
state. Display actual retained observation periods and retrieval timestamps;
do not change those dates merely because a build or maintenance check ran.
Provider acquisition is a separate explicit operation with the existing
rights, failure and immutable-vintage controls.

Maintain **mim1hat-prog/finance-skills** through the authorized account. Prefer
the connected **ChatGPT GitHub plugin** for supported operations. An
authenticated Git transport may publish reviewed commits when the connector
cannot preserve verified public no-reply author and committer identities. Do
not use the cloud browser for GitHub authentication or put credentials in the
project. Confirm the authenticated account, actual default branch and current
head before writes, and preserve concurrent edits. For an authorized history
repair, use the exact reviewed replacement and an explicit expected-head
lease. If no authenticated route is available, retain the prepared work and
report that access gap. Source links to Somamill repositories remain
provenance; they do not select the maintenance destination.

The owner requested ongoing updates. A separate maintenance task was enabled on **2026-11-25**, with a daily check around **08:00 Asia/Tokyo** and its first scheduled check on **2026-11-26**. It checks this repository's published location, official host docs and pinned upstreams, and reports material changes and imports that need replacement. It uses neither GitHub Actions nor a work-PC daemon.

For compatible instruction/documentation changes, the maintainer can publish only after rebuilding, testing and reviewing the diff. Runtime upgrades, changed permissions/data transmission, new commercial services and changed finance definitions require a concrete reviewable proposal. If the execution environment cannot validate a change, leave it in a clearly described branch/PR and report the blocker. Do not call the library updated because a check was merely scheduled.

This file does not create or prove a running automation. The actual task confirmation in the conversation is the record of whether scheduling succeeded. The repository includes no GitHub Actions workflows and installs no poller, webhook, background worker or persistent credentials.

A publication identity hold leaves read-only review enabled. It blocks commit-creating writes until the owner resolves the identity finding and an available authorized route can preserve that correction. It does not silently disable the maintenance schedule or authorize a history rewrite. [Identity check and remediation boundary](../SECURITY.md#commit-identity-is-a-separate-publication-check)

## Refresh your work account

For the Markdown-only download, open the updated file and replace the relevant pasted Instructions text after preserving approved company additions. The Markdown ZIP is regenerated with every build; text already pasted into an agent or conversation does not synchronize automatically.

The download-all bundles and versioned releases simplify acquisition; they do not synchronize installed copies. Extract the downloaded outer ZIP, choose individual native packages and perform the host steps below. If you use the plain-text Excel agent profile, update the saved Instructions field separately after comparing company-specific additions. Both the profile and native editions derive from the same canonical skill; do not edit generated copies in this repository.

**Copilot Chat/Agent Builder:** update the existing skill through that host's supported editor/replacement flow and test it. **Excel/PowerPoint:** update the matching-name folder opened by the app, wait for OneDrive, and select Refresh. The optional local copier previews changes and preserves customized copies.

**Gemini Skills:** open the existing skill and use More → Replace skill with the complete individual package, then Save and test. **Gem fallback:** replace the Instructions text and any associated knowledge resources manually. [Copilot steps](COPILOT.md) · [Gemini steps](GEMINI.md)

Keep a private installed register containing: host/account class, skill name, version, package SHA-256, import date and a brief successful task check. The folder copier maintains `.finance-skills-install.json` for files it copied; it does not certify host activation. When a copy contains company additions, compare and preserve them before replacement. Never publish that private register if it contains internal account/source details.

## Roll back

Use GitHub history to retrieve the prior reviewed package, replace the host's existing skill, and repeat the relevant task check. Keep the previous package until the new one is verified. Source archives and generated packages remain distinct from private work data. An upstream runtime has its own rollback procedure; a skill-package rollback does not uninstall a service.
