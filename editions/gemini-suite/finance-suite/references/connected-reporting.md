# Connected reporting and readback

Establish the report's real system context before editing. Work from a live connection only when that capability is exposed and authorized; otherwise inspect the supplied export or cached workbook and state that scope. A skill does not install a connector or grant write access.

## Inspect the connection and report

Identify the software and report type, model/cube or report ID, ordered dimensions, members/hierarchies, scenario, version, period, measure, currency/unit, selection variables and filters. Keep this configuration private. Use a known-good, supported read to establish connection health; do not test a connection by entering a value in a write-enabled cell.

Preserve add-in-managed formulas, named ranges, hidden controller cells, parameter areas, expansion regions and formatting outside the requested change. Inspect writeback mode before changing connected input cells. Some planning report modes can commit when a value is entered; do not assume leaving an edited cell only changes the workbook. Do not change connection, writeback or refresh settings merely to make a review easier.

Distinguish the workbook's saved values, workbook refresh time, underlying data update time and actual live response. A blank behind an error-suppressing formula is an unverified or failed read until the underlying condition is checked; it is not zero activity. For a reporting export, record its variables, filters, hierarchy/grain and source snapshot before comparison.

## Prepare and validate the target payload

1. Preserve the existing upload format and target order. Identify data-entry versus derived/consolidated cells and reject absent, duplicate or ambiguous target coordinates.
2. Match approved source data to complete target intersections. Check entity, account, period, scenario/version, measure, currency and any other required dimensions individually. Matching grand totals cannot compensate for swapped detailed values.
3. Verify mappings, source scope, signed amounts, units and rounding at the required grain. Keep rejected/unmatched values visible in working context and quantify the unresolved amount.
4. Keep inspect, prepare, validate, execute and independently verify distinct. A review or upload-preparation request does not authorize posting or submitting. Reuse explicit authorization when it covers this exact target and payload; ask only for material missing authorization or ambiguity.
5. Before an authorized action, recheck target/model, permissions, locks, version, source freshness and prior execution status. After an uncertain result or timeout, read the existing state and execution receipt before retrying. Do not replace a locked sender or change a master mapping as a workaround.
6. Compare independent readback with the staged payload at the same ordered coordinates and tolerance. Check row/key completeness and each detailed value, then totals. Keep any receipt as evidence of the action it actually proves; upload, publication visibility, review approval and final submission are separate states.

## Return

Give the requested report or prepared payload and the compact result: evidence state, action state, detailed residual/blocker and next source. Do not add a new sheet, query, comment or audit register unless requested. If only export comparison ran, label it export validation and identify the live check still needed.

Official mechanics: [IBM report types](https://www.ibm.com/docs/en/planning-analytics/3.1.0?topic=types-planning-analytics-microsoft-excel-report), [IBM automatic commit behavior](https://www.ibm.com/docs/en/planning-analytics/2.1.0?topic=reports-automatically-commit-data), and [SAP Analysis source information](https://help.sap.com/docs/SAP_BUSINESSOBJECTS_ANALYSIS_OFFICE/ca9c58444d64420d99d6c136a3207632/f26f9dfa6c9b1014bf2c9a7eb0e91070.html). Match documentation to the installed version; these references do not prove a connection is available.
