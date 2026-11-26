# Check what actually finished before answering

Everything in this case is invented. No tools or real workplace access are needed. You have four pieces of evidence for September:

- **I1, approved internal ledger:** North has 40 HC and 32 PC. South has 20 HC and no reported PC. The workbook shows a stored North value of 35 PC from before correction. An edit of the workbook formula is visible, but no recalculation or updated dependent result was observed.
- **P1, public-search preview:** A snippet says a benchmark is 81 but omits the period and unit.
- **P2, opened public release:** The September benchmark is 78 points on the published scale.
- **P3, opened public release:** The August benchmark is 81 points on the same scale.

The initial draft says, “September benchmark was 81, the workbook is verified, and regional capacity totals 35 PC.” Recheck the draft using the records above. Report verified results and any unresolved region-wide number. A public benchmark cannot fill an internal PC gap.

Return a JSON object with `total_hc`, `verified_north_pc`, `total_pc`, `september_benchmark`, `benchmark_source`, `recalculation_verified`, and `remaining_check`. Use JSON null when the total is unsupported. Give `remaining_check` as `south-pc-and-native-recalculation` if both gaps are unresolved.
