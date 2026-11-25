# Upstream sources and optional tools

Reviewed **25 November 2026**. The 24 native finance skills are original,
company-neutral instructions. The repositories below informed selected methods;
their applications, providers, hooks and runtimes are separate products.

## What is prepared, and what is installed

| Stage | Evidence in this release |
|---|---|
| Upstream review | 15 full commit pins, licence observations, selected skill paths and finance mappings in [upstream.lock.json](../upstream.lock.json) |
| Source preparation | Five clean pinned source checkouts were prepared during development: Hallmark, Anthropic skills, Claude-mem, HyperFrames and Impeccable |
| Archive verification | The four explicitly requested ZIP archives were downloaded; all 16,165 contained file blobs matched the corresponding pinned Git checkouts; their SHA-256 values are locked |
| Native packages | Original Copilot and Gemini packages are generated from this repository's own skill sources |
| Runtime on the work PC | Not installed or tested by this repository build |
| Copilot/Gemini account import | Not performed or verified by this repository build |

The four locked source archives total approximately 233 MiB at these revisions.
They are optional reference downloads and are not bundled into the much smaller
native finance packages. An acquired ZIP is not an activated agent plugin, a
running memory worker, a video renderer, or an installed Python dependency.

Microsoft 365 Copilot and GitHub Copilot in VS Code are different hosts. Gemini
Apps and Gemini CLI are also different hosts. Windows 11, Python, Power BI,
VS Code and SharePoint do not by themselves establish a coding-agent licence,
Node/Bun availability, API access, or permission to install services.

## Reviewed sources

| Source | Reviewed commit | Licence observation | Finance use |
|---|---|---|---|
| [Nutlope/hallmark](https://github.com/Nutlope/hallmark/tree/04977e15f3dfd6ee4b74c887dac3eb52665d6c92) | 04977e15f3df | MIT | design-review, corporate-style |
| [anthropics/skills](https://github.com/anthropics/skills/tree/e4bb5d960d87126ff3b3a8af1a104b7db67560ba) | e4bb5d960d87 | Apache-2.0 for inspected document folders | excel-data-coverage, spreadsheet-modeling, management-presentation, business-document, cash-working-capital, scenario-planning |
| [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem/tree/4dc8e48cddee663edc3e401109f836d11f926a45) | 4dc8e48cddee | Apache-2.0 | project-context |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes/tree/c890cb38f0d0786831c99ab515587f5750185cb8) | c890cb38f0d0 | Apache-2.0 | video-storyboard |
| [duckdb/duckdb-skills](https://github.com/duckdb/duckdb-skills/tree/44dfbbb414e54187964a2212eae28495f6ae21d9) | 44dfbbb414e5 | MIT | analytical-sql, account-mapping, power-query-etl |
| [valyuAI/skills](https://github.com/valyuAI/skills/tree/be57c51696fa74a0fce129e3dc165c93c599a0c9) | be57c51696fa | MIT declared; no root licence file observed | evidence-research, sharepoint-evidence |
| [chrisvoncsefalvay/claude-d3js-skill](https://github.com/chrisvoncsefalvay/claude-d3js-skill/tree/e198c87d03f1c9811acbff681886fac24baee53d) | e198c87d03f1 | No licence observed; do not copy | interactive-visualization |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/c21d13b3cc2894680229ba9959a53281acb9200e) | c21d13b3cc28 | MIT | reproducible-analysis, scenario-planning, workforce-reconciliation, forecast-variance |
| [microsoft/markitdown](https://github.com/microsoft/markitdown/tree/ed178952a6672abdfd35b5f9e76a80b6cefc086e) | ed178952a667 | MIT | document-extraction |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design/tree/1acb8776bab34f5055399fbac96a693c8d5cf7b3) | 1acb8776bab3 | MIT | process-diagram |
| [obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7) | 22f0b463e7a5 | MIT | work-tool-routing, close-controls, excel-data-coverage |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/e997ac5b9a74eab332d5e9793bb38a38c8cfdd74) | e997ac5b9a74 | MIT | business-document, project-context, account-mapping |
| [mattpocock/skills](https://github.com/mattpocock/skills/tree/d65391149dbb5fe76478e76fa8d5122b2aa5a70e) | d65391149dbb | MIT | project-context |
| [affaan-m/ECC](https://github.com/affaan-m/ECC/tree/4adeee6732a12d1540f49a4d50a38ce8c97f9a53) | 4adeee6732a1 | MIT | evidence-research |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable/tree/b49177d32788f2dc585c42831d845dacf1ebed2c) | b49177d32788 | Apache-2.0 | design-review |

The discovery starting point was [AgenorIT's repository index](https://www.agenorit.com.au/insights/top-github-repositories),
last reviewed by its publisher on 11 November 2026. We screened its Top 100 and
45 Editor's Picks for finance relevance, then inspected selected primary
repositories. This is not a claim that every repository in the index was audited.
Star counts and “Official”, “Verified” or “Community” labels do not establish
compatibility with a particular workplace host.

Anthropic's inspected xlsx, docx, pdf and pptx folders use Apache-2.0 at the pinned
revision; check each folder's notices before redistribution. Other folders and
dependencies may have different terms. Valyu declares MIT in its skill and README,
but no root licence file was observed. The community D3 skill has no observed
licence, so none of its prose or code is copied here. The D3 JavaScript library
has its own separate licence. Original finance adaptations do not imply upstream
endorsement.

The dot. design foundation governs this repository. Employer documents and
presentations use the employer's approved templates, not Hallmark themes,
Anthropic brand rules, or the dot. repository branding.

## What was added for this Windows setup

| New skill | Practical purpose | Main source method |
|---|---|---|
| power-query-etl | Repeatable, typed transformations and controlled refreshes | DuckDB query discipline; Microsoft Power Query documentation |
| sharepoint-evidence | Find and cite accessible work evidence with coverage boundaries | Source provenance and evidence research methods |
| account-mapping | Effective-dated mappings, unmapped keys, overlaps and totals | DuckDB joins; decision documentation |
| close-controls | Rollforwards, close register, exceptions and evidence | Verification before completion |
| cash-working-capital | As-of aging and cash/working-capital analysis | Auditable spreadsheet calculations |
| scenario-planning | Formula-based drivers, sensitivities and assumptions | Spreadsheet modeling; reproducibility |
| document-extraction | Local extraction, coverage checks and source pointers | Microsoft MarkItDown |
| process-diagram | Reporting and close flows with owners and controls | Diagram Design; decision documentation |

These additions complement the existing workforce, forecast, Power BI,
spreadsheet, research, reporting and project-context skills. They specialize
methods for finance; they do not import a scientific, coding or memory framework
wholesale.

## Acquire pinned sources with Python

Run from this repository in PowerShell. Python 3.10 or newer is the project
baseline. These commands use only Python's standard library.

To save all four requested original archives without extracting anything:

    $Sources = Join-Path $env:LOCALAPPDATA 'dot-finance-upstream-archives'
    py -3 scripts/fetch_upstreams.py --all --archive-only --destination $Sources

The four selected ids are hallmark, anthropic-skills, claude-mem and hyperframes.
Use repeated --tool arguments for a subset. No API key or Git installation is
needed. Public GitHub must be reachable through the workplace's normal network
controls.

Hallmark and Anthropic can also be extracted into a separate destination:

    $Extracted = Join-Path $env:LOCALAPPDATA 'dot-finance-upstream-extracted'
    py -3 scripts/fetch_upstreams.py --tool hallmark --tool anthropic-skills --destination $Extracted

Omitting --destination uses the ignored upstream-sources directory in this
repository. Other directories inside the repository are refused. Each source
gets an id-and-commit directory containing a SOURCE-RECEIPT.json file and either
source.zip or a source directory. Existing targets are never overwritten;
choose a new destination or deliberately remove your own old copy before
acquiring it again.

**Why archive-only is recommended for all four:** Claude-mem has seven tracked
symlinks and HyperFrames has two at the reviewed commits. Strict extraction
rejects every symlink and special file. Archive-only preserves the exact ZIP
bytes, records the count of unextracted symlinks, and materializes none of them.
Use the upstream-supported runtime installer when you actually need those tools; archive acquisition does not configure them.

The extractor validates the pinned root, paths, Windows filenames, duplicate
and case-colliding entries, encryption flags, file count and size limits before
writing source files. It never runs upstream scripts, package managers, hooks,
telemetry or services. The limits are 256 MiB downloaded, 1 GiB expanded,
128 MiB per file and 50,000 entries.

The four archive hashes in the lock were computed from actual downloads and
checked against the pinned Git file blobs. Other sources currently have no
archive checksum; their receipts explicitly say checksum_recorded_unbaselined.
A source pin and HTTPS transport do not authenticate authorship. A checksum
mismatch stops acquisition; do not silently replace the lock value.
[GitHub documents](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives#stability-of-source-code-archives)
that archive compression can change while the extracted commit contents remain
the same. In that case, review the downloaded file contents and record a new
checksum deliberately.

## Optional coding-host activation

The commands below are prepared instructions, not evidence of execution on the
work PC. Use them only in an approved coding environment. Native Microsoft 365
Copilot and Gemini Apps setup remains in their edition guides.

### Hallmark and Anthropic xlsx in GitHub Copilot

If GitHub Copilot is available in VS Code, project skills can live in
.github/skills according to the [official VS Code guidance](https://code.visualstudio.com/docs/agent-customization/agent-skills).
After the extracted-source command above, open an approved working project and
copy only the selected source folders. This example refuses to replace an
existing skill:

    $HallmarkSource = Join-Path $Extracted 'hallmark-04977e15f3df/source/skills/hallmark'
    $XlsxSource = Join-Path $Extracted 'anthropic-skills-e4bb5d960d87/source/skills/xlsx'
    $SkillFolder = Join-Path (Get-Location) '.github/skills'
    New-Item -ItemType Directory -Path $SkillFolder -Force | Out-Null
    foreach ($Pair in @(@($HallmarkSource, 'hallmark'), @($XlsxSource, 'xlsx'))) {
        $Target = Join-Path $SkillFolder $Pair[1]
        if (Test-Path -LiteralPath $Target) { throw "Skill already exists: $Target" }
        Copy-Item -LiteralPath $Pair[0] -Destination $Target -Recurse
    }
    Copy-Item -LiteralPath (Join-Path $Extracted 'hallmark-04977e15f3df/source/LICENSE') -Destination (Join-Path $SkillFolder 'hallmark/LICENSE')

Reload the coding host and inspect its skills list before testing a synthetic
task. Copying a folder establishes files at a supported location; it does not
prove the host loaded them or that their runtime dependencies are present.
Keep the full licence notices and supporting resources.

Hallmark's static scripts need Node 18 or newer; its rendered checks additionally
need Chrome and puppeteer-core. The original xlsx workflow assumes openpyxl and
other format-specific Python packages; its recalculation helper needs
LibreOffice. openpyxl writes formulas but does not evaluate them. Do not claim
a workbook was recalculated because a formula string or cached value exists.

### HyperFrames 0.9.91

The inspected CLI requires Node 22 or newer, FFmpeg and its browser rendering
dependencies. From a separate approved video project, the upstream
CLI-matching skill route is:

    $env:HYPERFRAMES_NO_TELEMETRY = '1'
    $env:DO_NOT_TRACK = '1'
    npx.cmd --yes hyperframes@0.9.91 telemetry disable
    npx.cmd --yes hyperframes@0.9.91 skills update

Choose only the intended coding host and scope. Do not run a project-local
installer inside the HyperFrames source checkout, where it could overlap
tracked source folders. The command installs skills corresponding to CLI
0.9.91; this is distinct from the later reviewed source-commit archive.
Node package installation can resolve further dependencies and is not part of
the native finance package.

For browser-only work, video-storyboard remains useful without any renderer.
A storyboard or HTML slideshow is not a rendered MP4 or a PowerPoint file.

### Claude-mem 16.1.3

The inspected runtime requires Node ^20.19.0 or >=22.12.0, Bun >=1.1.31, a
local worker and a supported observer/model provider. Its installer can
prepare additional dependencies and register coding-host integration.
The deferred route below intentionally leaves provider/account setup for the
person operating that machine:

    $env:CLAUDE_MEM_ONLINE_OPTIN = 'false'
    npx.cmd --yes claude-mem@16.1.3 telemetry disable
    npx.cmd --yes claude-mem@16.1.3 install --setup defer

Review the installer's requested host, provider and local-service changes.
Do not enable integrations for unrelated agents. This guide does not select
a paid provider or start a trial. Usage analytics are on by default upstream;
cloud sync is opt-in. A Gemini API key is separate from Gemini Apps access.
Copilot CLI integration can search memory but does not record its sessions
at the reviewed version. Microsoft 365 Copilot and Gemini Apps do not gain
this memory service by importing SKILL.md.

Installing the claude-mem npm SDK globally alone does not register its worker
or hooks. Until the chosen coding host is configured and verified, use the
portable project-context skill with a work-approved context document.

### Impeccable 4.10.0

Impeccable is an optional repository design tool: CLI 4.10.0, engine 0.1.27,
Apache-2.0. Node >=18.19 is needed for the npx route; the skill uses a
self-contained engine binary. Windows x64 is represented in its distribution.

    npx.cmd --yes impeccable@4.10.0 install

This command can offer coding-host hooks and integrations. It is not needed
to use the finance skills and was not run on the work PC. A manual generated
host-folder copy is also documented upstream. Keep the existing dot.
DESIGN.md authoritative when reviewing this repository.

### Other optional analysis tools

- DuckDB: prefer Python on Windows to the upstream Bash-based skills.
  The [live 2.0 Python docs](https://duckdb.org/docs/2.0/clients/python/overview)
  currently state 2.0.1 and Python >=3.11. A 1.x environment needs a reviewed
  migration; do not assume database-file compatibility.
- Valyu: requires the official SDK, its own API key and network access.
  The evidence-research skill does not grant paid or licensed Valyu access.
- MarkItDown: the inspected source declares 0.1.9 and Python >=3.10,<3.15.
  Use local conversion and preserve source/page/table pointers; extracted
  text is not automatically complete or financially validated.
- Scientific skills: select EDA, evidence-quality and reproducibility
  methods. Numerical packages and optional APIs are separate dependencies.
  The original statistical-analysis and database-lookup instructions exceed
  this project's strict native-package length profile.
- D3 and process diagrams: keep independently authored finance instructions;
  use local HTML/SVG or approved Power BI functionality where suitable.

## Read-only update checks

Run:

    py -3 scripts/check_updates.py

The checker writes ignored .local/update-report.json. It requests the latest
default-branch commit for each pinned public repository and fetches the listed
primary documentation URLs. It never changes a pin, downloads source archives,
installs software, changes a work account, or runs GitHub Actions.

| Result | Meaning |
|---|---|
| unchanged | The repository head matches the reviewed commit |
| new_commit_requires_review | A different commit exists; compatibility has not been assessed |
| reachable_unbaselined | The documentation endpoint responded; no approved content checksum exists |
| unchanged_bytes | Documentation response bytes match a deliberate baseline; this is not a semantic review |
| changed_bytes_requires_review | Response bytes differ; inspect the actual content and redirects |
| unavailable | A rate limit, network failure, blocked redirect or invalid response prevented the check |

Exit code 0 means all endpoints were checked. Exit code 1 means at least one
source was unavailable or a validation/output error occurred. New commits do
not by themselves cause an error exit, because they are review candidates.
Documentation may include dynamic markup or sign-in pages; a successful HTTP
response is not proof that the relevant feature description was retrieved.

The live development check on 25 November 2026 exercised the failure path:
GitHub's anonymous API was rate-limited for all 15 source requests; 11 primary
documentation endpoints were reachable without a baseline; the two Gemini Help
URLs redirected beyond the allowed documentation hosts. It wrote these
limitations and returned exit code 1. The repository pins themselves were
independently read and verified through GitHub during research. The checker
does not turn inaccessible results into “no changes.”

For a recurring maintenance task, read the report, use the available GitHub
connection or primary-source research for unavailable endpoints, and evaluate
relevant changes. Compare licences, dependency requirements and host rules;
update original instructions and regenerate both editions only after review
and validation. Runtime, executable-code and financial-business-logic changes
need their own compatibility review. Native account imports still need
replacement or the host's OneDrive Refresh step. See [UPDATES.md](UPDATES.md)
for the maintenance workflow.

## Verification

The source helpers have focused standard-library tests for traversal,
Windows-specific filenames, case collisions, symlinks, archive limits,
checksum failure, no-overwrite behaviour, non-execution, rate-limit handling,
documentation review boundaries and preservation of lock pins.

    py -3 -m unittest discover -s tests -p test_upstream_tools.py -v

During development, these tests passed and the four downloaded archives'
16,165 file blobs matched the reviewed Git commits. These checks establish
the helper behaviour and source provenance demonstrated here; they do not
establish workplace installation or runtime compatibility. The Python
helpers were exercised in the build environment; a Windows 11 work-PC smoke
check remains separate. Actual Hallmark and Anthropic archives passed strict
extraction with their locked checksums. Claude-mem and HyperFrames were
correctly refused by strict extraction because of their tracked symlinks.

