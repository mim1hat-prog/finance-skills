# Driver-based scenario planning

Keep approved internal baselines, workflow status and public benchmark context separate. Public FX is not an approved planning rate or an internal exposure. Preserve the base forecast and incremental opportunities/risks as separate components, including assumption-version and scope changes. For historical challenge, use an available information-vintage snapshot; today's revised history cannot fill an unavailable cutoff.

Before adopting an external indicator or more complex forecasting method, compare it with a simple baseline at rolling forecast origins using only information available at each origin. Evaluate the intended horizon and a consistent error measure. Treat any apparent improvement as specific to the tested dataset and period; a publication does not establish predictive value for this scenario.

Build an inspectable model around a specific management decision. Use supplied actuals, forecasts and approved assumptions; label illustrative assumptions clearly. Keep the model small enough that the user can trace each material output to its drivers. Use an available spreadsheet or calculation tool. If no execution tool is available, provide formulas and a model layout without claiming results were recalculated.

## Define the decision and baseline

Confirm the decision, reporting period, entities/products, currency, units, scenario horizon and result needed: revenue, contribution, operating profit, cost, headcount, cash or another defined KPI. Record the source/version of the baseline and distinguish actuals already locked from forecast periods that can change. Use the user's sign convention and show conversions between cost-positive and profit-impact reporting.

List drivers with baseline value, unit, source, owner, allowed range, effective date and dependencies. Identify whether a percentage is relative growth, an absolute margin change or a percentage-point change. For FX, state the quote direction, translation method and timing; do not apply a currency movement twice through both local prices and conversion.

## Build the calculation logic

1. **Reproduce the baseline.** Tie modeled output to the supplied baseline before introducing scenarios. Show any residual and its cause. Keep inputs separate from formulas, expose constants and avoid replacing a formula with a desired result.
2. **Separate cost behavior.** Distinguish variable, fixed, step and one-off costs. Include capacity thresholds, timing, ramp-up, product mix and relevant lags when supplied. Do not assume fixed costs scale with sales or that incremental volume can exceed capacity without additional resources.
3. **Create coherent scenarios.** Define each scenario as a named set of driver values with a rationale. Use consistent assumptions across linked drivers, periods and entities. Make interdependencies explicit: price can affect volume, hiring affects cost and capacity after a delay, and purchasing affects inventory and cash at different times.
4. **Separate sensitivity from scenario.** A one-way sensitivity changes one driver while holding others constant. A two-way table varies two. A coherent downside may change several together. Label them accordingly and do not infer a real-world probability from a sensitivity table.
5. **Calculate full precision.** Use formulas from the same calculation path for every case. Retain meaningful decimals internally and round display only. Check units, time bases and currency before comparing values. Do not mix a monthly run rate with a full-year total or an FTE quantity with headcount.
6. **Explain the bridge.** Reconcile the baseline to each result using a documented driver order. Interactions depend on the decomposition method; show an interaction/residual or state how the sequential method assigns it. Do not add independently calculated full effects when they overlap.

For a simple single-product contribution model, the structure can be `revenue = volume × price`, `variable cost = volume × unit variable cost`, and `contribution = revenue − variable cost`. Add fixed/step costs to reach the requested profit measure. This is a starting structure only; replace it where contracts, mix, capacity or timing require different logic.

For break-even, solve the stated model and list its assumptions. In the simple fixed-cost model, units equal fixed costs divided by positive unit contribution. If contribution is zero or negative, do not produce a misleading finite break-even. Round units to a feasible operational quantity and verify the result against capacity and other constraints. More complex models require solving their actual equations.

## Treat uncertainty explicitly

Label scenarios as conditional outcomes. Do not attach probabilities unless the user supplies or explicitly approves a probability model. If probabilities are supplied, verify they are non-negative, finite and sum to one; resolve an incomplete set rather than normalizing silently. Expected value is a weighted average under that model, not a guaranteed or necessarily most likely outcome.

Use ranges grounded in supplied evidence. If asked for a simulation, specify distributions, dependencies/correlations, random seed, number of runs, convergence checks and why the model is appropriate. Avoid false precision and do not call an arbitrary best/base/worst set a statistical confidence interval. When evidence cannot support a distribution, provide deterministic scenarios instead.

For cash, distinguish profit effects from collection/payment timing, inventory, capex and financing. Do not relabel EBITDA or operating profit as cash flow. For discounted analysis, obtain the approved discount basis and ensure nominal/real, pre-/post-tax, currency and period units are consistent before calculating; do not invent a cost of capital.

## Validate and present

Test the unchanged-input case, boundary/zero cases, capacity thresholds, sign direction and scenario totals. Check that changing a driver affects only the intended periods and formulas. Summarize which checks ran and which require the user's application or source data. Identify sensitive assumptions and the information that would most improve the decision.

Return the requested scenario/model or comparison with the assumptions, calculation references and decision thresholds needed to interpret it. Keep baseline reconciliation and routine validation internal; disclose material residuals or failed checks. Do not add an assumption register, audit text, full sensitivity package or new worksheet unless requested. State which outcome changes the proposed action and which assumption crosses that threshold. Keep recommendations conditional on modeled facts; do not present a scenario as an approved budget or a committed operational action.

Example request: “Model next quarter with volume −10%, price +2% and a one-month hiring delay. Compare it with the unchanged baseline and a volume-only sensitivity. Show the profit bridge, cash timing assumptions and the capacity or margin thresholds that change the decision.”
