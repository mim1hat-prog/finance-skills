# Synthetic workflow acceptance cases

Every value, identifier, date and evidence locator here was independently
invented. The `urn:synthetic:` references are labels inside a test, not live
company sources. A supplied `live` or `succeeded` flag in a fixture is test
input; no native system was queried or refreshed to produce these files.

Run from the project root with standard-library Python:

```powershell
py -3 scripts\workflow_controls.py check examples\workflows\provision-residual.json
py -3 scripts\workflow_controls.py check examples\workflows\workforce-regression.json
py -3 scripts\workflow_controls.py check examples\workflows\readback-intersections.json
```

All three cases intentionally return **exit 2** and `evidenceStatus: blocked`:

- **Provision:** additions explain 5 units, while utilization changes by -3
  and has only -2 explained. The remaining -1 is retained. The closing
  difference of 2 does not establish that every movement is reconciled.
- **Workforce/query:** the reported refresh succeeds, but a protected planning
  record disappears and an output field is renamed. The accepted workbook/query
  contract fails; no replacement is performed.
- **Readback:** expected and observed totals are both 160, but two reporting
  intersections differ by -15 and +15. Net difference is zero and gross
  absolute difference is 30. A matching grand total does not pass the check.

The command prints requested JSON diagnostics to stdout. It never adds a
worksheet, edits an input, writes a report file, contacts a provider, or executes
an allocation. Keep real requests and resulting diagnostics in approved work
storage, outside this repository.

## Contracts and supported operations

`schemas/workflow-context.schema.json` defines period/cutoff, scenario and
version, entity scope, basis, currency label, source snapshot and requested
output. The source stream is explicitly one of `approved_internal_figures`,
`internal_workflow_status` and `public_benchmarks`. A public benchmark or status
record cannot fill an internal figure requirement. A newer source observation
cannot establish what was known before its as-of time.

`schemas/workflow-artifact.schema.json` captures a read-only export of ordered
columns and their normalized types, native type labels where supplied, business
keys, records, formulas, load targets and query dependencies. Normalized types
are `text`, `decimal`, `integer`, `date` and `boolean`; source adapters must
declare the actual native type separately when that matters. A null cell stays
null. Business keys cannot be null or blank.

`schemas/workflow-request.schema.json` has seven operations:

- `provision`: compare ordered overview/detail/upload/readback stages for the
  explicitly requested scenario version. Opening plus signed additions,
  releases, utilization and other movement must equal closing. Difference
  explanations are separate for each movement and adjacent stage pair. Use
  stable `componentId` values and precise evidence locators for distinct
  drivers. Repeating a component ID within a stage pair or an evidence locator
  within the same pair/movement blocks the result; every item in that duplicate
  group is excluded from the explained amount. A single older explanation
  without `componentId` remains supported, but cannot repeat the same locator.
- `artifact`: preserve the accepted schema, keys, formulas, load targets,
  dependencies and protected records. `append` preserves every existing row;
  `replace-scoped` permits record changes only at explicit `scopeKeys`.
  Protected keys cannot also be change keys. Native refresh and downstream
  evidence remain separate requirements. The existing numeric scale and sign
  convention must also remain equivalent; unchanged raw rows with a new scale
  or sign do not preserve their meaning.
- `readback`: compare ordered model dimensions and complete member tuples,
  retaining missing intersections and blank values. A failed, cached or
  suppressed read does not become zero activity. A declared live independent
  read and a known-good connection are required for the supplied readback check.
- `mapping`: require exactly one effective rule with every requested field and
  a supplied approval reference. Missing, ambiguous, future, expired, incomplete
  or unapproved rules stay unresolved; no source or master is modified.
- `granularity`: identify absent dimensions without allocating totals into an
  unavailable split. Declared dimensional coverage does not replace record-level
  completeness and mapping checks.
- `case-status`: distinguish `not-requested`, `awaiting-confirmation`,
  `confirmed-none` and `cases-received` per owner role and scope. Confirmed
  status needs a date and evidence reference at or before the cutoff. Zero must
  be explicit; an empty inbox is not confirmation.
- `allocation-preflight`: check effective configuration, unlocked sender,
  membership/permission evidence, unique receiver weights, prior-run state and
  exact approval binding. Payload sender, configuration version and receiver
  member/weight pairs must match the checked configuration. Approval and the
  prior-run status must both identify the exact target and payload hash. A
  timed-out attempt needs a later independent status check before any retry can
  be considered. There is no execution command.

`schemas/workflow-result.schema.json` separates `evidenceStatus` from
`actionState: not-executed` and `submissionState: not-established`. These fields
cannot be promoted by a passing numeric check. Even a `reconciled` result covers
supplied snapshots and evidence; the tool does not authenticate those sources,
approve the business result, establish production readiness or submit it.

## Precision, normalization and tolerances

All financial amounts are decimal strings. The supported input range is up to
28 significant digits with adjusted exponent from -28 through 28; unsupported
precision fails rather than rounding silently. Arithmetic traps inexact results.

Amounts normalize as `raw × unitScale × signMultiplier`, where the scale is
positive and the multiplier is explicitly 1 or -1. Raw values remain in the
diagnostics. No FX rate, scenario transformation, period conversion, business
definition or missing value is inferred.

A tolerance has an ID, version, nonnegative decimal amount and inclusive
effective dates. Its amount is in normalized base currency units. The same
absolute tolerance applies to each detail difference and the gross/net
unexplained aggregate; this conservative rule prevents many small differences
or opposing differences from creating a false pass. Residuals remain visible
even when within tolerance and are never automatically called rounding.

Fully allocating an explanation while snapshot values still differ returns
`validated`, not `reconciled`. Explanation references are supplied evidence
locators, not a conclusion that the business cause was independently proven.

Receiver allocation weights are fractions and must total exactly one. They are
not silently normalized. The canonical preflight payload has exactly `sender`,
`amount`, `configurationVersion` and `receivers`; each receiver has `member` and
`weight`. Amounts and weights are decimal strings. The checked configuration
also identifies its `sender`. An arbitrary connector payload is not accepted
as this contract; prepare and validate a real connector adapter separately.

Approval binding uses SHA-256 of UTF-8 JSON with
sorted object keys, compact separators, unescaped Unicode and nonfinite numbers
rejected. The approval must reference the exact target and payload hash and be
effective at the declared cutoff. `priorRun.target` and
`priorRun.payloadSha256` must match them as well; a read for another action
cannot clear duplicate-run risk. Live freshness, permissions and approval
authority still require the approved target workflow. These metadata checks do
not authenticate the evidence supplied to the helper.

## Validation and exit codes

```powershell
py -3 scripts\workflow_controls.py validate --schema request examples\workflows\provision-residual.json
py -3 -m unittest discover -s tests -p test_workflow_controls.py -v
```

Exit 0 means the requested contract validation passed, or the supplied workflow
result is `validated`/`reconciled`. Exit 2 means a schema-valid workflow is
blocked or unverified. Exit 1 means invalid input, unsupported numeric range,
malformed configuration or a file error. Input files must be regular files,
at most 20 MiB, without duplicate JSON property names or nonfinite numbers.
Workflow identifiers, owners and evidence locators must contain a non-whitespace
character; blank business-key cells remain errors. Date-time validation checks
both the calendar and explicit offset-hour/minute bounds.

The repository's shared `schema_validation.py` enforces the explicitly
documented subset used by these schemas and rejects unknown assertion keywords
or formats. It is not a general JSON Schema or OpenAPI conformance engine.
Native workbook/planning checks and source authority require separate acceptance
in the actual approved environment.
