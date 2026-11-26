# Classify an invented extract without concealing mapping gaps

All records and rules below are independently invented. Amounts are signed EUR
for March 2024. Every listed rule is in force for the reporting date. There is no
priority rule and no permission to choose between duplicate mapping targets.
Keep missing and ambiguous mappings unresolved; do not split, normalize or drop
their amounts.

| Record ID | Key | Amount |
| --- | --- | ---: |
| P11 | J1 | 200 |
| P12 | J2 | -35 |
| P13 | J3 | 65 |
| P14 | J4 | 20 |

| Key | Group |
| --- | --- |
| J1 | Red |
| J2 | Blue |
| J2 | Green |
| J4 | Red |

Return only a JSON object with `source_total`, `mapped_total`, `unresolved_total`,
`unresolved_positive`, `unresolved_negative`, `groups`, `ambiguous_keys`,
`missing_keys`, `unresolved_records`, and `residual`.

Use JSON numbers. `groups` is an object of valid group totals. Return key/record
lists alphabetically. Positive and negative unresolved amounts retain their
signs. Residual is source minus mapped minus unresolved; a zero residual does
not mean the mapping gaps have been resolved.
