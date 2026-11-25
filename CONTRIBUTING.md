# Contributing

Make a finance workflow more reliable, easier to use or better supported by evidence. Keep contributions company-neutral and compatible with the Windows, Copilot and Gemini environment described in `AGENTS.md` and the host guides.

## Edit the authoritative source

- Update instructions in `skills/` and shared host controls in `adapters/`.
- Update workflow contracts and source IDs in `catalog.json`; update tools and availability labels in `tools/catalog.json`.
- Record research, primary documentation, rights and corrections in `research/sources.json`, with the exact decision, skill, path and test supported.
- Keep benchmark source selection, lineage, terms and status in its catalogue. An unverified provider configuration remains a candidate.
- Generate editions, packages, profiles, tool lists, contract documentation and `CITATION.cff`; do not maintain separate manual copies.

Use only independently invented test data and verified public sources with recorded rights. Do not submit employer cases, private links, names, identifiers, mappings, thresholds, rules, screenshots, cached workbook values or business outputs, including sanitized versions of real cases. Do not send confidential prompts or data to public providers.

## Validate the actual change

Add a focused regression for a material failure mode. Prefer tests that distinguish a correct result from a plausible false pass: incomplete populations, wrong grain, reversed FX, a post-cutoff revision, a failed fetch, or an uncertain action state. Avoid tests that merely repeat implementation steps.

```powershell
py -3 scripts\research_registry.py
py -3 scripts\build.py
py -3 scripts\check_release.py
```

The default gate is offline and runs the test suite. Inspect optional dependency skips. Changes to an optional workbook or DuckDB helper require its approved pinned dependencies and an actual passing check. No check should fetch business data, start a daemon or modify company systems. Provider refreshes and native account verification are separate explicit activities.

For substantial instruction changes, perform a fresh synthetic task from raw inputs with only the relevant skills. Inspect the answer and affected artifact independently. Record limitations accurately; local Python tests do not prove native Copilot/Gemini behavior. Review the rendered catalogue after presentation changes when rendering is available.

## Release and review

Bump `catalog.json` using the documented public contract and SemVer policy, set the actual `releasedOn`, add release notes and update the changelog. Keep source review dates tied to actual reviews. Finalize the validation record before freezing, then run:

```powershell
py -3 scripts\release.py
py -3 scripts\check_release.py --require-release
```

Review the exact changed source and generated artifacts. Preserve every published version and its checksums. Publish through an authorized GitHub operation or authenticated Git transport that preserves the verified public commit identities, with a current-head check, then verify the remote tree and release hashes. A history repair needs an explicit expected-head lease and reviewed replacement history. Do not enable GitHub Actions, deploy a public endpoint, activate an enterprise connector or install an upstream runtime as part of an ordinary documentation or skill update.

Use public issues only for non-sensitive reproducible questions. Give the affected version, a minimal invented example, observed behavior and expected contract. See `SECURITY.md` for private concerns. Cite the software through `CITATION.cff`; preserve upstream notices and data terms.

For onboarding and presentation changes, use `site/index.template.html` and `tools/discovery-profile.json`, then rebuild the generated catalogue, metadata and coverage report. Follow [the code of conduct](CODE_OF_CONDUCT.md); [support](SUPPORT.md) and the issue templates describe useful public reports. The [evaluation protocol](docs/EVALUATION.md) defines a future native comparison; do not present it as completed evidence.

Before creating public commits, verify author and committer identity separately from source-file checks. Use a public no-reply address and follow the [metadata publication boundary](SECURITY.md#commit-identity-is-a-separate-publication-check). Do not commit raw history exports or private addresses used for a review.
