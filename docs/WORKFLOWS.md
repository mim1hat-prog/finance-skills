# Finance workflows and acceptance

Version **1.2.0** adds shared controls to every native skill package and four workflows around the existing library. Use the skills as instructions in the approved account. The local Python checks operate on supplied snapshots; they do not connect to, refresh or write an enterprise system.

## Three separate data streams

| Stream | Establishes | Must remain separate from |
| --- | --- | --- |
| Approved internal figures | Actuals, approved plans/forecasts, rates, exposures and mappings for their stated scope | Draft versions, workflow status and public proxies |
| Internal workflow status | Whether a requested input, confirmation, transfer, approval or close action is evidenced | The numeric figure itself and an assumed completion state |
| Public benchmarks | Market context for a question, scenario or forecast challenge | A booked amount, approved assumption or replacement for a missing internal input |

Align period and cutoff/timezone, scenario/version, entity scope, reporting basis, currency/unit, sign convention and source snapshot before comparison. Keep a requested frozen submission distinct from a newer working file. Retrieve relevant authorized evidence before guessing at an unexplained change.

The model's useful answer order is **approved result → verified internal driver → relevant public benchmark → unresolved gap and next source**. Keep intermediate checks in working context. No extra worksheet, audit table, log or process report is required unless the user requests one.

## Pilot 1: provision calculation through reporting readback

Use `provision-reconciliation` with `connected-reporting` when the task spans a frozen overview, detailed calculation, staged payload and reporting readback.

1. Establish the requested version and scope. Identify the authoritative overview, detailed inputs, signed movement definitions, target coordinates and effective tolerance.
2. Reconcile opening, additions, releases, utilization, other movements and closing independently. Keep gross components and detailed keys visible in working context even when closing totals match.
3. Test each explanation against the entire difference. Deduplicate evidence/components; retain any unexplained residual at source precision. Newer working numbers cannot establish that a frozen submission changed.
4. Prepare the existing upload format without changing add-in regions, dimension order or business logic. Check every target intersection, not only the grand total.
5. For an explicitly authorized action, use the actual approved system and verify its result independently. If execution is uncertain, inspect status and readback before any retry. The repository helpers perform no upload or submission.

Keep case ownership, requested scope and dated confirmation distinct from reserve amounts. `not-requested`, `awaiting-confirmation`, `confirmed-none` and `cases-received` are separate statuses. An empty inbox does not establish a confirmed zero.

Acceptance requires the requested comparison to reconcile or retain its exact residual, with source and action evidence stated separately. A validated payload is not a submitted result. [Synthetic movement and readback cases](../examples/workflows/README.md)

## Pilot 2: workforce and Power Query change

Use `workforce-reconciliation` with `power-query-etl` for a scoped repair to an accepted workbook or query pipeline.

1. Capture the accepted input/output grain, ordered column names and types, business keys, protected records, formulas, query dependencies, load targets and downstream consumers.
2. Identify whether the task appends new records or replaces one explicit scope. Preserve history and every unaffected record. Keep headcount, average capacity, direct/indirect cost, contingent labour, overtime and productivity definitions distinct.
3. Resolve effective mappings through approved evidence. A cost-centre total does not establish a missing job-rank split; identify the required detailed source instead of allocating the total into invented detail.
4. Apply the smallest correct change in the existing scope. When replacement M code is requested, provide the complete affected query and preserve its dependencies. Do not silently suppress a required connector error or replace missing data with zero.
5. Refresh in the actual native environment, then compare protected populations, schema, formulas, load targets and downstream results with the accepted contract. A successful refresh alone does not prove that the result preserved the required population.

Acceptance requires both the requested change and preserved invariants. A local exported-artifact comparison is useful evidence but does not establish native refresh, workbook recalculation or downstream publication. [Synthetic protected-record/schema case](../examples/workflows/README.md)

## Other connected workflows

`fx-allocation-preflight` keeps planning, realized and public rates separate, checks quote direction and exposure/scope changes, and validates the approved sender/receiver configuration. Exact target/payload binding, effective weights, permissions, locks and prior-run status are prerequisites. Its helper has no execution command.

`benchmark-lookup` is the single public-data lookup used by forecast, FX, cost and variance workflows. Cite provider, series, period, unit and snapshot. A cutoff query must use a retained information vintage; a current revised history is not a substitute. [Dataset and API](../benchmarks/README.md)

## Migration from v1.1.0

| Existing workflow | v1.2.0 extension |
| --- | --- |
| Excel agent core, evidence research and work-tool routing | Further targeted retrieval, independent rechecks, compact continuation at host limits and concise output |
| Power Query and workforce reconciliation | Protected artifact contracts, effective mappings and explicit granularity gaps |
| Close controls | Distinct readiness/transfer/closed evidence and effective calendar/materiality rules |
| Forecast variance and scenarios | Frozen versus current scope, separate public vintages and rolling-origin baseline guidance |
| Power BI analysis | Separate source/model/visual refresh, publication and reader visibility evidence |
| New connected reporting and provisions | Detailed source → calculation → payload → readback comparison |
| New FX/allocation preflight and benchmark lookup | Exact configuration checks and shared public context |

All 25 previous skill IDs and individual package shapes are retained. Replace or refresh existing installed copies; import new skills only where useful. Every skill's required inputs, outputs, modes, optional capabilities and exact automated coverage are in [the generated contracts](SKILL-CONTRACTS.md). The [tool inventory](../TOOLS.md) distinguishes available, unconfirmed and optional capabilities.

## Run the local acceptance cases

```powershell
py -3 scripts\workflow_controls.py check examples\workflows\provision-residual.json
py -3 scripts\workflow_controls.py check examples\workflows\workforce-regression.json
py -3 scripts\workflow_controls.py check examples\workflows\readback-intersections.json
```

All three are intentional failure cases and return **exit 2**, with `evidenceStatus: blocked`. Exit 0 means the supplied contract/check passed; exit 1 means invalid input or a file/configuration error. Results retain `actionState: not-executed` and `submissionState: not-established`. Run results from real work remain private in the approved environment.

See [the schema and precision notes](../examples/workflows/README.md) before preparing your own request. Numeric and evidence checks cannot authenticate supplied sources or replace native acceptance. No workflow here adds credentials, activates a connector or changes approved company configuration.
