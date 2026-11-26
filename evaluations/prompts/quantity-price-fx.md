# Explain an invented quantity, price and FX difference

These inputs are independently invented. Revenue equals quantity times USD price
per unit times the exchange rate quoted as **JPY per USD**. All quantities refer
to the same product and reporting period. Calculate in JPY with no rounding.

| Input | Plan | Actual |
| --- | ---: | ---: |
| Quantity, units | 80 | 92 |
| Price, USD per unit | 12.50 | 13.25 |
| FX, JPY per USD | 142 | 139 |

Use the explicitly ordered sequential bridge: **quantity, then price, then FX**.
Change one input at a time from plan to actual, retaining changes already made.
The effects are arithmetic contributions; no causal business explanations are
provided by these inputs.

Return only a JSON object with `plan_jpy`, `actual_jpy`, `change_jpy`,
`quantity_effect_jpy`, `price_effect_jpy`, `fx_effect_jpy`, `residual_jpy`,
`fx_quote`, `order`, and `cause_status`. Use JSON numbers for amounts,
`JPY per USD` for the quote, an array of the ordered input names (`quantity`,
`price`, `fx`), and `unconfirmed` for unsupported causal explanations.
