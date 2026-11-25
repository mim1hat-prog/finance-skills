"""Read an xlsx/xlsm workbook without saving it; inspect formula caches, not recalculation.

Requires the optional openpyxl dependency. No macros or connections are run.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import zip_longest
from pathlib import Path
import sys
from finance_tools import source_info, write_result


def audit(path: Path) -> dict:
    try:
        import openpyxl
    except ImportError as exc:
        raise ValueError("openpyxl is unavailable. Use an approved local environment with requirements-xlsx.txt.") from exc
    if path.suffix.lower() not in (".xlsx", ".xlsm"):
        raise ValueError("Use .xlsx or .xlsm; this helper does not convert legacy workbooks")
    before = source_info(path)
    formulas = openpyxl.load_workbook(path, read_only=True, data_only=False, keep_links=False)
    cached = openpyxl.load_workbook(path, read_only=True, data_only=True, keep_links=False)
    sheets = []
    try:
        for ws in formulas.worksheets:
            values = cached[ws.title]
            try:
                claimed_dimension = ws.calculate_dimension()
            except ValueError:
                claimed_dimension = None
            # Discard possibly incorrect producer dimensions; scan all stored rows.
            ws.reset_dimensions()
            values.reset_dimensions()
            nonempty_rows = formula_count = missing_caches = populated = 0
            maximum_row = maximum_column = 0
            errors: Counter = Counter()
            locations = []
            for formula_row, value_row in zip_longest(ws.iter_rows(), values.iter_rows(), fillvalue=()):
                row_has_content = False
                for cell, value in zip_longest(formula_row, value_row, fillvalue=None):
                    if cell is None or cell.value is None:
                        continue
                    row_has_content = True
                    populated += 1
                    maximum_row = max(maximum_row, cell.row)
                    maximum_column = max(maximum_column, cell.column)
                    cached_value = value.value if value is not None else None
                    cached_type = value.data_type if value is not None else None
                    if cell.data_type == "f":
                        formula_count += 1
                        if cached_value is None:
                            missing_caches += 1
                    error = cell.value if cell.data_type == "e" else cached_value if cached_type == "e" else None
                    if error is not None:
                        errors[str(error)] += 1
                        if len(locations) < 100:
                            locations.append({"cell": cell.coordinate, "error": str(error)})
                nonempty_rows += int(row_has_content)
            sheets.append({"sheet": ws.title, "visibility": ws.sheet_state, "declaredDimension": claimed_dimension,
                           "lastNonemptyRow": maximum_row, "lastNonemptyColumn": maximum_column,
                           "nonemptyRowsIncludingHeaders": nonempty_rows, "populatedCells": populated,
                           "formulaCells": formula_count, "formulaCachesBlankOrAbsent": missing_caches,
                           "storedErrorCounts": dict(errors), "errorLocationsFirst100": locations})
    finally:
        formulas.close()
        cached.close()
    if source_info(path) != before:
        raise ValueError("Workbook changed while being inspected; use a stable copy")
    return {"operation": "workbook-audit", "source": before, "openpyxlVersion": openpyxl.__version__,
            "sheets": sheets, "recalculation": "not performed", "businessRowCount": "not inferred from nonempty rows",
            "limits": ["A blank formula cache may represent an intentional blank result or missing calculation.",
                       "Existing numeric caches can be stale; this audit does not establish freshness or formula correctness.",
                       "Visual layout, pivots, external connections, macros and embedded objects were not executed or validated."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        write_result(audit(args.file), args.output)
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(f"Audit stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
