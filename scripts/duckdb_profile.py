"""Profile a complete local CSV/Parquet file with DuckDB; preserve CSV IDs as text.

Requires requirements-duckdb.txt. Local inputs only, no extensions downloaded,
no arbitrary SQL, no database writes. This is a coverage helper, not a benchmark.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
from finance_tools import source_info, write_result


def identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def inspect(path: Path, keys: list[str], delimiter: str = ",") -> dict:
    try:
        import duckdb
    except ImportError as exc:
        raise ValueError("DuckDB is unavailable. Use an approved Python 3.11+ environment with requirements-duckdb.txt.") from exc
    path = path.expanduser().resolve(strict=True)
    if not path.is_file() or path.suffix.lower() not in (".csv", ".parquet"):
        raise ValueError("Select a local .csv or .parquet file")
    if any(character in str(path) for character in '*?[]'):
        raise ValueError("Rename a copy to remove wildcard characters so DuckDB reads exactly one file")
    if len(delimiter) != 1:
        raise ValueError("Delimiter must be one character")
    if len(keys) != len(set(keys)):
        raise ValueError("Key columns must not repeat")
    before = source_info(path)
    connection = duckdb.connect(":memory:", config={"autoinstall_known_extensions": "false", "autoload_known_extensions": "false"})
    try:
        if path.suffix.lower() == ".csv":
            # Reject duplicate headers before the CSV reader can rename them.
            from finance_tools import csv_rows
            header_rows = csv_rows(path, keys, delimiter)
            try:
                headers, _ = next(header_rows)
            finally:
                header_rows.close()
            if len({h.casefold() for h in headers}) != len(headers):
                raise ValueError("DuckDB requires column names unique without regard to case")
            relation = connection.read_csv(
                str(path), header=True, auto_detect=False, columns={h: "VARCHAR" for h in headers},
                skiprows=0, delimiter=delimiter, quotechar='"', escapechar='"', comment="",
                strict_mode=True, ignore_errors=False, null_padding=False, hive_partitioning=False,
            )
            if relation.columns != headers:
                raise ValueError("CSV reader changed the validated header; analysis stopped")
        else:
            relation = connection.read_parquet(str(path), hive_partitioning=False)
        relation.create_view("finance_input")
        columns = relation.columns
        if set(keys) - set(columns):
            raise ValueError(f"Unknown key columns: {sorted(set(keys) - set(columns))}")
        count = connection.execute("SELECT COUNT(*) FROM finance_input").fetchone()[0]
        empty = {}
        for column in columns:
            q = identifier(column)
            empty[column] = connection.execute(f"SELECT COUNT(*) FILTER (WHERE {q} IS NULL OR TRIM(CAST({q} AS VARCHAR)) = '') FROM finance_input").fetchone()[0]
        key_info = None
        if keys:
            key_sql = ", ".join(identifier(k) for k in keys)
            valid = " AND ".join(f"{identifier(k)} IS NOT NULL AND TRIM(CAST({identifier(k)} AS VARCHAR)) <> ''" for k in keys)
            distinct, duplicate_groups, excess = connection.execute(
                f"SELECT COUNT(*), COUNT(*) FILTER (WHERE n > 1), COALESCE(SUM(n - 1),0) "
                f"FROM (SELECT COUNT(*) AS n FROM finance_input WHERE {valid} GROUP BY {key_sql})"
            ).fetchone()
            missing = connection.execute(f"SELECT COUNT(*) FROM finance_input WHERE NOT ({valid})").fetchone()[0]
            key_info = {"columns": keys, "missingKeyRows": missing, "distinctNonblankKeys": distinct,
                        "duplicateKeyGroups": duplicate_groups, "excessDuplicateRows": int(excess)}
        result = {"operation": "duckdb-profile", "source": before, "duckdbVersion": duckdb.__version__,
                  "rows": count, "schema": [{"name": c, "type": str(t)} for c, t in zip(columns, relation.types)],
                  "blankOrNullCounts": empty, "keys": key_info,
                  "scope": "Complete local file; no sampling for row/key counts",
                  "limits": "File capacity and performance depend on the local machine. This scan can make several passes and is not a 1–100 GB capacity guarantee."}
    finally:
        connection.close()
    if source_info(path) != before:
        raise ValueError("Input changed during analysis")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--keys", nargs="*", default=[])
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        write_result(inspect(args.file, args.keys, args.delimiter), args.output)
        return 0
    except Exception as exc:
        # DuckDB uses its own error classes; report their text without a private traceback.
        print(f"DuckDB profile stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
