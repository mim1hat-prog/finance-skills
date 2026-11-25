# Workflow contracts and validation coverage

Generated from catalog.json for version 1.4.2.

These contracts describe triggers, inputs, outputs, modes and source support. Shared controls are included in every generated host skill. Package tests do not prove that a live finance workflow is production-ready. Conditional execution requires the actual host, authorization, exact target and payload, preconditions and independent verification. Native work-account validation remains outstanding.

## Excel agent instructions (`excel-agent-core`)

**Triggers:** Excel work objective; enterprise evidence and workbook corrections.

**Inputs:** requested objective; existing workbook or relevant approved sources.

**Outputs:** concise completed result; material unresolved gap.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_granularity_and_three_streams_do_not_backfill_internal_inputs`.

**Native status:** not validated in the approved work account. **Research IDs:** `project-finance-design`.

## Work tool routing (`work-tool-routing`)

**Triggers:** choose a finance work surface.

**Inputs:** requested deliverable; available authorized capabilities.

**Outputs:** selected workflow; usable result or capability-limited next step.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `copilot-researcher`, `gemini-deep-research`, `tool-m365`, `upstream-superpowers`.

## Excel data coverage (`excel-data-coverage`)

**Triggers:** check workbook scope or source coverage.

**Inputs:** workbook or export; required population and independent control when available.

**Outputs:** scoped result; material coverage gaps and residual.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `tool-power-query`, `upstream-anthropic-skills`, `upstream-superpowers`.

## Workforce reconciliation (`workforce-reconciliation`)

**Triggers:** reconcile headcount, capacity or personnel cost.

**Inputs:** approved populations and dates; workforce/cost snapshots; effective mappings and measure definitions.

**Outputs:** separate headcount/FTE/cost bridges; unresolved mapping or granularity gap.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_granularity_and_three_streams_do_not_backfill_internal_inputs`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_missing_ambiguous_future_unapproved_and_incomplete_mappings_are_not_guessed`.

**Native status:** not validated in the approved work account. **Research IDs:** `mhlw-monthly-labour`, `project-finance-design`, `upstream-scientific-skills`.

## Forecast variance (`forecast-variance`)

**Triggers:** forecast/budget variance or driver bridge.

**Inputs:** baseline and comparison versions; approved actual horizon; driver inputs and units.

**Outputs:** nonoverlapping driver bridge; residual and concise commentary.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `alfred-realtime`, `fpp-tscv`, `meti-iip`, `upstream-scientific-skills`.

## Power BI analysis (`power-bi-analysis`)

**Triggers:** DAX, model totals or reporting freshness.

**Inputs:** model grain/relationships/measures; filters and source controls; refresh/visibility evidence when available.

**Outputs:** measure/model review; scope-specific tie-out and freshness result.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `tool-fabric`, `tool-power-bi`.

## Management presentation (`management-presentation`)

**Triggers:** management slides or decision update.

**Inputs:** validated figures; audience and decision; approved template.

**Outputs:** editable requested presentation; material unresolved evidence.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-anthropic-skills`.

## Business document (`business-document`)

**Triggers:** business document or report.

**Inputs:** purpose and audience; approved source content; requested format/template.

**Outputs:** requested document; concise source/decision references.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-addy-agent-skills`, `upstream-anthropic-skills`.

## Corporate style (`corporate-style`)

**Triggers:** apply an approved corporate template.

**Inputs:** approved template; requested artifact; content to preserve.

**Outputs:** styled requested artifact; material template limitation.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-hallmark`.

## Spreadsheet modeling (`spreadsheet-modeling`)

**Triggers:** create or correct an Excel model.

**Inputs:** existing workbook or requested new-model scope; approved inputs/assumptions; calculation dependencies.

**Outputs:** working model or exact proposed formulas; recalculation status and residual.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-anthropic-skills`.

## Analytical SQL (`analytical-sql`)

**Triggers:** analytical SQL over approved exports.

**Inputs:** dataset/schema; grain and keys; requested query/result.

**Outputs:** reviewed query or executed result; scope and residual.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-duckdb-skills`.

## Evidence research (`evidence-research`)

**Triggers:** research with primary evidence.

**Inputs:** question and cutoff; authorized source access; needed decision/scope.

**Outputs:** sourced conclusion; unresolved material evidence gap.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `copilot-researcher`, `crossref-updates`, `gemini-deep-research`, `project-finance-design`, `upstream-ecc`, `upstream-valyu`.

## Reproducible analysis (`reproducible-analysis`)

**Triggers:** repeatable quantitative analysis.

**Inputs:** input snapshot; method and environment; acceptance controls.

**Outputs:** reproducible calculation or proposed code; limits and residual.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `fair-principles`, `fpp-tscv`, `upstream-scientific-skills`, `w3c-dwbp`.

## Design review (`design-review`)

**Triggers:** review an artifact design.

**Inputs:** actual artifact; audience and design requirements.

**Outputs:** located findings or requested edits.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-hallmark`, `upstream-impeccable`.

## Project context (`project-context`)

**Triggers:** resume or hand off a work task.

**Inputs:** current objective; authoritative decisions and artifacts.

**Outputs:** concise relevant context; next unresolved decision.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-addy-agent-skills`, `upstream-claude-mem`, `upstream-mattpocock-skills`.

## Video storyboard (`video-storyboard`)

**Triggers:** create a requested video storyboard.

**Inputs:** validated message; audience and duration; approved assets/template.

**Outputs:** storyboard or supported output; render status.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-hyperframes`.

## Interactive visualization (`interactive-visualization`)

**Triggers:** create an interactive finance visualization.

**Inputs:** validated dataset; question and audience; supported runtime.

**Outputs:** requested interactive artifact; data/interaction limitations.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-d3-viz`.

## Power Query pipeline (`power-query-etl`)

**Triggers:** repair or extend a Power Query pipeline.

**Inputs:** actual dependency graph and query text; accepted baseline; approved change and downstream contract.

**Outputs:** complete affected replacement M; population/interface compatibility result.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-power-query-refresh, downstream-export-inspection.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_successful_refresh_cannot_hide_protected_population_or_schema_regression`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_scoped_replacement_and_append_preserve_history_with_native_checks_separate`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_duplicate_business_keys_and_typed_cells_fail_even_if_refresh_succeeded`.

**Native status:** not validated in the approved work account. **Research IDs:** `tool-power-query`, `upstream-duckdb-skills`.

## SharePoint evidence (`sharepoint-evidence`)

**Triggers:** identify authoritative work files or versions.

**Inputs:** question and cutoff; authorized source locations or exports.

**Outputs:** traceable authoritative source; version/coverage gap.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `tool-m365`, `upstream-valyu`.

## Account mapping (`account-mapping`)

**Triggers:** validate effective account or organizational mapping.

**Inputs:** source records and keys; approved mapping with effective dates; declared relationship/weights.

**Outputs:** mapped and unresolved amounts; cardinality/effectivity blockers.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_missing_ambiguous_future_unapproved_and_incomplete_mappings_are_not_guessed`.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-addy-agent-skills`, `upstream-duckdb-skills`.

## Period-close controls (`close-controls`)

**Triggers:** period close or anomaly disposition.

**Inputs:** approved period/calendar/control scope; source evidence; effective thresholds and owner roles.

**Outputs:** specific control/anomaly outcome; readiness blockers and separately evidenced action states.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `project-finance-design`, `upstream-superpowers`.

## Cash and working capital (`cash-working-capital`)

**Triggers:** working-capital movement or cash sensitivity.

**Inputs:** balances and flows; period/unit/averaging definitions; approved scope.

**Outputs:** scoped KPI/cash bridge; modeled versus received-cash distinction.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-anthropic-skills`.

## Scenario planning (`scenario-planning`)

**Triggers:** forecast scenarios or sensitivity.

**Inputs:** approved baseline; versioned assumptions; scenario bounds and decision.

**Outputs:** comparable scenarios; assumptions and residual.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `fpp-tscv`, `upstream-anthropic-skills`, `upstream-scientific-skills`, `worldbank-pink-sheet`.

## Document extraction (`document-extraction`)

**Triggers:** extract structured facts from documents.

**Inputs:** accessible documents and versions; required fields and output contract.

**Outputs:** requested extracted data; material uncertainty and exact source locators.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-markitdown`.

## Finance process diagrams (`process-diagram`)

**Triggers:** map a finance process.

**Inputs:** approved process evidence; requested scope and audience.

**Outputs:** requested diagram; unverified process assumptions.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** No automated end-to-end workflow coverage claimed.

**Native status:** not validated in the approved work account. **Research IDs:** `upstream-diagram-design`.

## Connected reporting (`connected-reporting`)

**Triggers:** planning-cube/SAP/BW upload or readback checks.

**Inputs:** report type and target coordinates; staged payload and independent readback; connection/action evidence.

**Outputs:** coordinate-level parity result; separate evidence/action/submission states.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-export-inspection, known-good-live-read, authorized-write-and-independent-readback.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_readback_checks_target_intersections_not_only_grand_total`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_failed_cached_blank_or_empty_reads_never_become_zero_activity`.

**Native status:** not validated in the approved work account. **Research IDs:** `project-finance-design`, `tool-fabric`, `tool-planning-analytics`, `tool-planning-writeback`, `tool-power-bi`, `tool-sap-analysis`.

## Provision and warranty reconciliation (`provision-reconciliation`)

**Triggers:** provision additions, utilization or version difference.

**Inputs:** frozen overview and supporting detail; signed movement definitions; staged payload/readback and case confirmations when available.

**Outputs:** movement-level bridge; explicit residual and confirmation gap.

**Modes:** inspect, prepare, validate. **Conditional:** execute, verify.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_partial_provision_explanation_retains_component_and_total_residual`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_explained_difference_is_not_equal_snapshots_and_latest_cannot_replace_requested_version`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_case_coverage_requires_owner_scope_and_dated_explicit_zero_confirmation`.

**Native status:** not validated in the approved work account. **Research IDs:** `project-finance-design`.

## FX and allocation preflight (`fx-allocation-preflight`)

**Triggers:** FX exposure/scope or allocation readiness.

**Inputs:** approved rate/exposure/configuration versions; sender/receiver sets and effective weights; lock/permission/prior-run evidence.

**Outputs:** separate FX sensitivity and allocation preflight; blocking unresolved configuration/run state.

**Modes:** inspect, prepare, validate. **Conditional:** none.

**Dependencies:** shared `workflow-controls-v1`; optional approved-source-read, native-artifact-edit, local-calculation.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_workflow_controls.py::WorkflowControlsTests.test_allocation_locks_duplicate_run_risk_timeout_and_exact_binding_block_execution`, `tests/test_workflow_controls.py::WorkflowControlsTests.test_declared_scale_sign_and_source_precision_preserve_raw_values`.

**Native status:** not validated in the approved work account. **Research IDs:** `ecb-exr-api`, `project-finance-design`.

## Public benchmark lookup (`benchmark-lookup`)

**Triggers:** public context for forecast/FX/cost commentary.

**Inputs:** decision, geography and horizon; series/unit/base/adjustment; immutable snapshot or as_of cutoff.

**Outputs:** cited public benchmark; freshness/vintage/rights limits.

**Modes:** inspect, prepare, validate. **Conditional:** none.

**Dependencies:** shared `workflow-controls-v1`; optional approved-snapshot-inspection, local-read-only-benchmark-api.

**Package tests:** `tests/test_build_install.py::PackagingTests.test_all_packages_are_deterministic_standalone_and_exact`.

**Workflow tests:** `tests/test_benchmarks.py::BenchmarkDatasetTests.test_after_cutoff_revision_never_uses_latest`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_outage_preserves_last_good_and_redacts_credentials`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_reversed_fx_quote_is_rejected`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_derived_inputs_and_formula_are_independently_verified`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_rights_gate_blocks_before_fetch`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_api_contract_pagination_errors_and_no_provider_calls`, `tests/test_benchmarks.py::BenchmarkDatasetTests.test_public_origin_cannot_bypass_frozen_series_kind`.

**Native status:** not validated in the approved work account. **Research IDs:** `alfred-realtime`, `alfred-vintages`, `boj-cgpi`, `ecb-exr-api`, `fair-principles`, `meti-iip`, `mhlw-monthly-labour`, `w3c-dcat3`, `w3c-dwbp`, `worldbank-pink-sheet`.

