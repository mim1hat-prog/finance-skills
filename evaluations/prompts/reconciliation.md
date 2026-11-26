# Reconcile two invented extracts

Use only the independently invented data below. Amounts are EUR, signed as shown,
at the same reporting basis and period. IDs are unique business keys. Do not infer
business reasons, match different IDs or treat an absent row as a confirmed zero.

Earlier extract:

| ID | Amount |
| --- | ---: |
| R101 | 150.25 |
| R102 | 40.50 |
| R103 | -10.75 |

Later extract:

| ID | Amount |
| --- | ---: |
| R101 | 157.75 |
| R102 | 38.25 |
| R104 | -4.00 |

Return only a JSON object with these keys: `earlier_total`, `later_total`,
`change`, `matched_change`, `removed_effect`, `added_effect`, `residual`,
`earlier_only`, `later_only`, `cause_status`.

Calculate change as later minus earlier. For the bridge, removed effect is the
negative of earlier-only amounts, and added effect is the later-only amount.
Residual is change minus all three bridge components. Return unmatched IDs as
alphabetically sorted arrays. Use JSON numbers for amounts and `unconfirmed`
for the cause status unless the inputs establish the business reason.
