---
name: fx-allocation-preflight
description: "Review FX sensitivities, accounting FX scope and allocation preconditions without conflating them. Use for rate-direction errors, changed exposure or opportunity/risk scope, original versus replicated postings, sender/receiver sets, effective weights, locked masters and uncertain prior runs."
---

# FX and allocation preflight

Keep operating sensitivity, accounting FX and allocation execution separate. Use approved internal rate/exposure/configuration records for finance results. Public FX is separately cited market context, never a replacement for booked FX, an approved planning rate, exposure or missing allocation membership.

## Establish the comparison

Record period/cutoff, scenario and assumption version, accounting/reporting perimeter, currency/unit, sign convention and source snapshots. Identify the approved rate's direction, rate type, observation/effective date, averaging method and use. Keep planning rate, realized rate, public reference and exposure as separate fields. A changed opportunity/risk perimeter is not an FX-rate effect.

## Review FX sensitivity

1. Align comparable sales and cost exposures and their currency pairs. Verify quote direction with a simple dimensional check. Do not invert a rate or convert an index without retaining the original series, formula and declared transformation.
2. Separate rate, volume, mix, price, scope and mitigation effects. State the bridge order and allocate interactions once. Reconcile the bridge to the observed total and retain the residual; do not attribute every difference to FX.
3. Label modeled sensitivity, approved forecast, realized accounting result and public benchmark separately. Keep base forecast and incremental opportunities/risks distinct. An indicator correlation is not proof of an internal driver.
4. When combining accounting and management extracts, identify ledger, currency type, document key, original versus replicated posting and elimination scope. Prevent duplicate postings while retaining unresolved identities. Do not assume a management view is the full accounting population.

## Review allocation preconditions

Validate the approved sender and receiver sets, member IDs, effective dates, weights and weight total, allocation basis, period, version, permissions and locks. An account description does not establish approved set membership. A saved cycle does not establish that it can run.

Treat a missing approved set, overlapping mapping, invalid weight, locked object or uncertain previous run as a blocker. Keep the approved configuration unchanged. Do not substitute a sender or normalize an incomplete allocation silently. Establish previous-run status from authorized evidence before considering a retry.

The default deliverable is a checked calculation or preflight result. Actual execution requires authorization covering the exact target and payload, validated preconditions and an available authorized host. If execution times out, inspect independent status/readback before retrying. A prepared configuration or successful preflight is not a posted allocation.

## Return

Give the requested sensitivity or preflight conclusion, verified internal drivers, relevant separately labeled benchmark, residual/blocker and next approved source. Keep routine checks internal; no audit sheets or configuration changes are required. State explicitly what was calculated and whether any action was actually executed.
