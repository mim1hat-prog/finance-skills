# Try a finance skill with invented data

This example uses the independently invented [plan.csv](plan.csv) and [actual.csv](actual.csv) already in this repository. Amounts are demonstration units; no company, currency, period or approval is implied. It illustrates reconciliation, not the economic cause of a variance.

## Copy, attach, ask

1. Extract the Markdown-only download. Open `copilot/forecast-variance.md` or `gemini/forecast-variance.md` and copy its complete contents into your available Instructions field or an approved conversation.
2. Attach the two CSV files above. You can use these public invented files without supplying a work workbook.
3. Send this request:

   > Compare actual.csv with plan.csv at cost_center and account level. Preserve leading-zero identifiers. Calculate actual minus plan, identify keys present in only one file, and reconcile the detailed differences to the total. Keep unmatched records explicit; do not infer causes or treat an absent record as a confirmed business zero. Return a concise result without creating sheets or audit tables.

## Check the result

Plan totals **350.30** and actual totals **365.35**. Actual minus plan is **15.05**, with a **0.00** reconciliation residual.

The two matched records explain **+10.05** and **−5.00**. The record `003 / 6100` appears only in plan with **50.00**, and `004 / 6100` appears only in actual with **60.00**. Their numeric bridge contributions are **−50.00** and **+60.00**, while their missing-side statuses remain explicit. The four contributions sum to **15.05**.

The files do not establish why amounts changed, whether a missing record should exist, or whether an increase is favorable. A correct response preserves those limits. The read-only helper verifies the arithmetic; this worked example is not a measured Copilot/Gemini success-rate study.

## Optional local verification

From an extracted full release, run in Windows PowerShell:

```powershell
py -3 scripts\finance_tools.py reconcile examples\plan.csv examples\actual.csv --keys cost_center account --amount amount
```

Python uses exact decimal arithmetic, prints JSON to the terminal and leaves the files unchanged. No extra packages, API key or public provider request is needed.

[Choose another skill](../SKILLS.md) · [Coverage and limitations](../metrics/README.md) · [Help](../SUPPORT.md)
