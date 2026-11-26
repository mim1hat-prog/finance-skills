# Standards and research practice

Reviewed **2026-11-25**. These are the standards actually used by this project. Their scope is explicit: repository metadata and passing software checks do not establish peer review, certification, native host compatibility or business-data accuracy.

| Standard or practice | Implementation | What the project checks |
| --- | --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | Canonical `skills/<name>/SKILL.md`, generated host folders and individual native ZIPs | Valid names and descriptions, matching directory names, frontmatter, self-contained text and deterministic package contents |
| [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) | `catalog.json`, changelog, versioned release directories and migration policy | Stable `MAJOR.MINOR.PATCH`, immutable prior releases, exact checksums and release/source agreement |
| [Citation File Format 1.2.0](https://citation-file-format.github.io/) | Generated root `CITATION.cff` | Version, release date and repository derive from the authoritative catalogue; the v1.2.0 file was independently checked against the official CFF schema |
| [SPDX licence identifiers](https://spdx.org/licenses/) | MIT software citation metadata, upstream lock and separate data rights | Applicable licence text and attribution retained; upstream data/documents keep their own terms |
| [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) | Workflow, benchmark dataset and API schemas | A documented strict subset is enforced by the local standard-library validator; unsupported assertion keywords fail closed and references resolve locally |
| [OpenAPI 3.1](https://spec.openapis.org/oas/v3.1.2.html) | `api/openapi.yaml` declares version 3.1.2 | Four read-only routes, bounded query parameters and schema-validated response examples/actual handler results |
| [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) | Structured API problem responses | Error type, title, HTTP status, detail and request instance, with project error codes and no secret query contents |
| [W3C Data on the Web Best Practices](https://www.w3.org/TR/dwbp/), [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) and [FAIR principles](https://doi.org/10.1038/sdata.2016.18) | Dataset catalogue, stable series/snapshot IDs, provenance, terms, versions and a dictionary | Lightweight metadata and reproducibility controls; no full DCAT/RDF conformance or FAIR certification is claimed |
| [Forecasting: Principles and Practice](https://otexts.com/fpp3/) | Baseline comparisons, rolling forecast origins and cutoff-safe benchmark instructions | A method must be evaluated for the intended horizon and dataset; publication alone does not establish local forecasting benefit |

## Public contract

The versioned contract includes skill IDs and their native import shape, documented helper CLI/JSON interfaces, workflow schemas, benchmark schema versions and `/v1` API routes. Additive compatible workflows and tools use a minor version. Corrections that preserve the contract use a patch version. Removed fields, incompatible meanings, package shapes or required behavior use a major version or an explicitly versioned new contract. See [release policy](RELEASES.md).

The JSON Schema helper is intentionally limited to the keywords used by this repository. Its supported set is declared in `scripts/schema_validation.py`; it rejects unsupported validation keywords rather than ignoring them. External JSON Schema or OpenAPI conformance suites are not bundled. The CFF schema uses draft-07 and is distinct from the project's 2020-12 data schemas.

## Reproducible evidence

`research/sources.json` is the canonical registry. Each integrated source has an ID, publisher, edition, access/review dates, rights, applicable section, implementation use, limitations and exact affected paths or tests. `research/README.md` is generated. Corrections and superseding versions are recorded; an unresolved retraction or correction cannot silently remain active support. Candidate research is visibly separated from implemented method support.

Source type and demonstrated effectiveness are separate. The FAIR article supplies metadata principles; it is not an empirical test of this library. The generated coverage report shows the source-type composition and keeps unresolved empirical candidates outside active support. A method reference, passing helper check or complete package does not establish improved assistant performance.

The [evaluation kit](EVALUATION.md) supplies versioned synthetic development cases, predetermined answer keys and a local result validator. It follows the documented-test practice in the [JOSS review criteria](https://joss.readthedocs.io/en/latest/review_criteria.html#tests); this is a methodological reference, not JOSS review or a claim of publication eligibility. Public answer keys make the cases useful for development and regression checks, not an unseen benchmark.

## AI assistance and review

AI tools assist with instruction drafting, code changes and documentation. Source review, deterministic build and release checks, focused software tests and independent local synthetic tasks provide the recorded validation. These checks have different scopes; none substitutes for native Copilot/Gemini execution or external peer review. Human contributors remain responsible for reviewing changes and their applicability before work use. The repository claims no certification or independent scientific efficacy result.

The benchmark store preserves originals and derived values separately. A derived row records its inputs, formula and transformation version. A snapshot ID fixes a particular retrieved history. Observation dates and a provider release date do not prove that a snapshot existed at an earlier cutoff. The API returns `as_of_unavailable` when it cannot reconstruct that cutoff. [Dataset dictionary and operation](../benchmarks/README.md)

Use `python scripts/check_release.py` for the offline pre-release gates and `python scripts/check_release.py --require-release` after freezing. This is a command suitable for an approved CI runner; this repository does not enable GitHub Actions or claim that a server branch-protection rule enforces it. Native account checks remain explicit in [validation](VALIDATION.md).

## Citation and licensing

Cite this software using `CITATION.cff` and the exact released version. Cite benchmark providers, series, periods, units and snapshot IDs separately when using their observations. Cite a research method's original source when the method is material. The software's MIT licence does not relicense upstream data, papers, trademarks or employer materials. No DOI, academic affiliation, accreditation or peer-reviewed status is claimed for the repository.

Professional presentation is supported by traceable methods, reproducible checks and clear limitations. The dot design system supplies the repository's visual identity; employer outputs continue to use approved employer templates.
