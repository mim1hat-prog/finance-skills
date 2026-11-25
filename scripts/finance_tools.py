"""Offline, read-only CSV controls and an exact quantity/rate/FX bridge.

Money is represented as decimal strings in JSON. Inputs remain unchanged.
No packages, API keys, network calls, telemetry or background process.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
from decimal import Decimal, DecimalException, Inexact, InvalidOperation, localcontext
import hashlib
from functools import wraps
import json
from pathlib import Path
import sys


def exact(function):
    @wraps(function)
    def run(*args, **kwargs):
        with localcontext() as context:
            context.prec = 512
            context.traps[Inexact] = True
            return function(*args, **kwargs)
    return run


def number(value: str, label: str) -> Decimal:
    try:
        result = Decimal(value.strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError(f"{label}: expected a decimal with '.' and no thousands separators") from exc
    if not result.is_finite():
        raise ValueError(f"{label}: missing or non-finite number")
    if len(result.as_tuple().digits) > 28 or abs(result.adjusted()) > 28:
        raise ValueError(f"{label}: exceeds the supported 28-digit input range")
    return result


def source_info(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return {"file": path.name, "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def csv_rows(path: Path, columns: list[str], delimiter: str = ",", encoding: str = "utf-8-sig"):
    if len(delimiter) != 1:
        raise ValueError("Delimiter must be exactly one character")
    with path.open("r", encoding=encoding, newline="") as stream:
        reader = csv.DictReader(stream, delimiter=delimiter, strict=True)
        fields = reader.fieldnames
        if not fields or any(not h.strip() for h in fields) or len(set(fields)) != len(fields):
            raise ValueError("CSV requires nonblank, unique, exact column headers")
        missing = set(columns) - set(fields)
        if missing:
            raise ValueError(f"Missing columns: {sorted(missing)}")
        yield fields, None
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"CSV record ending on line {reader.line_num} has a different column count")
            yield reader.line_num, row


@exact
def profile(path: Path, keys: list[str], amounts: list[str], delimiter=",", encoding="utf-8-sig") -> dict:
    if len(keys) != len(set(keys)) or len(amounts) != len(set(amounts)):
        raise ValueError("Requested columns must not repeat")
    initial = source_info(path)
    rows = csv_rows(path, keys + amounts, delimiter, encoding)
    fields, _ = next(rows)
    blanks = Counter({h: 0 for h in fields})
    totals = {h: Decimal(0) for h in amounts}
    keys_seen: Counter = Counter()
    count = missing_keys = 0
    for line, row in rows:
        count += 1
        for h, value in row.items():
            if not value.strip():
                blanks[h] += 1
        if keys:
            key = tuple(row[k] for k in keys)
            if any(not v.strip() for v in key):
                missing_keys += 1
            else:
                keys_seen[key] += 1
        for column in amounts:
            totals[column] += number(row[column], f"line {line}, {column}")
    if source_info(path) != initial:
        raise ValueError("Input changed while profiling; run again on a stable copy")
    return {"operation": "profile", "source": initial, "scope": "all parsed records; no row limit",
            "rows": count, "columns": fields, "blankCounts": dict(blanks), "keyColumns": keys,
            "missingKeyRows": missing_keys, "distinctNonblankKeys": len(keys_seen) if keys else None,
            "duplicateKeyGroups": sum(v > 1 for v in keys_seen.values()) if keys else None,
            "excessDuplicateRows": sum(v - 1 for v in keys_seen.values()) if keys else None,
            "totals": {k: str(v) for k, v in totals.items()},
            "limits": "Exact key counts retain distinct keys in memory; large files may need DuckDB."}


def aggregate(path: Path, keys: list[str], amount: str, allow_aggregate: bool, delimiter: str, encoding: str):
    initial = source_info(path)
    values: dict[tuple, Decimal] = defaultdict(Decimal)
    counts: Counter = Counter()
    rows = csv_rows(path, keys + [amount], delimiter, encoding)
    next(rows)
    count = 0
    for line, row in rows:
        key = tuple(row[k] for k in keys)
        if any(not v.strip() for v in key):
            raise ValueError(f"line {line}: blank reconciliation key")
        counts[key] += 1
        if counts[key] > 1 and not allow_aggregate:
            raise ValueError("Duplicate reconciliation key; correct the grain or explicitly choose --aggregate")
        values[key] += number(row[amount], f"line {line}, {amount}")
        count += 1
    if source_info(path) != initial:
        raise ValueError("Input changed during reconciliation")
    return values, {"source": initial, "rows": count, "keys": len(values),
                    "duplicateKeyGroups": sum(v > 1 for v in counts.values()),
                    "total": str(sum(values.values(), Decimal(0)))}


@exact
def reconcile(left: Path, right: Path, keys: list[str], amount: str, allow_aggregate=False,
              delimiter=",", encoding="utf-8-sig", tolerance=Decimal(0)) -> dict:
    if not keys:
        raise ValueError("At least one key is required")
    if len(keys) != len(set(keys)):
        raise ValueError("Key columns must not repeat")
    if tolerance < 0:
        raise ValueError("Tolerance cannot be negative")
    a, ac = aggregate(left, keys, amount, allow_aggregate, delimiter, encoding)
    b, bc = aggregate(right, keys, amount, allow_aggregate, delimiter, encoding)
    details = []
    for key in sorted(a.keys() | b.keys()):
        av, bv = a.get(key, Decimal(0)), b.get(key, Decimal(0))
        status = "right_only" if key not in a else "left_only" if key not in b else "matched" if abs(bv - av) <= tolerance else "different"
        details.append({"key": dict(zip(keys, key)), "status": status, "left": str(av), "right": str(bv), "deltaRightMinusLeft": str(bv - av)})
    delta = sum((b.get(k, Decimal(0)) - a.get(k, Decimal(0)) for k in a.keys() | b.keys()), Decimal(0))
    residual = Decimal(bc["total"]) - Decimal(ac["total"]) - delta
    return {"operation": "reconcile", "keyColumns": keys, "amountColumn": amount,
            "aggregateRepeatedKeys": allow_aggregate, "tolerance": str(tolerance), "left": ac, "right": bc,
            "statuses": dict(Counter(r["status"] for r in details)), "deltaRightMinusLeft": str(delta),
            "reconciliationResidual": str(residual), "details": details,
            "interpretation": "Missing-side amounts use zero only for the numeric bridge; the missing-key status is retained."}


@exact
def bridge(pq: Decimal, aq: Decimal, pr: Decimal, ar: Decimal, pf: Decimal, af: Decimal) -> dict:
    plan, actual = pq * pr * pf, aq * ar * af
    quantity = (aq - pq) * pr * pf
    rate = aq * (ar - pr) * pf
    fx = aq * ar * (af - pf)
    residual = actual - plan - quantity - rate - fx
    return {"operation": "quantity-rate-fx", "order": ["quantity", "rate", "fx"],
            "inputs": {"planQuantity": str(pq), "actualQuantity": str(aq), "planRate": str(pr),
                       "actualRate": str(ar), "planFx": str(pf), "actualFx": str(af)},
            "plan": str(plan), "actual": str(actual), "deltaActualMinusPlan": str(actual - plan),
            "quantityEffect": str(quantity), "rateEffect": str(rate), "fxEffect": str(fx), "residual": str(residual),
            "definition": "FX is reporting-currency units per source-currency unit. Rate is source currency per quantity unit.",
            "scope": "One homogeneous quantity/rate pair. Apply per comparable item before summing; mix and timing require separate definitions.",
            "interpretation": "Sequential arithmetic decomposition, not evidence of business causation. Positive cost delta means higher cost."}


def write_result(result: dict, output: Path | None) -> None:
    data = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        print(data, end="")
    else:
        # Exclusive creation keeps original inputs and previous results intact.
        with output.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(data)
        print(f"Created {output.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prof = commands.add_parser("profile", help="Full CSV coverage and amount controls")
    prof.add_argument("file", type=Path)
    prof.add_argument("--keys", nargs="*", default=[])
    prof.add_argument("--amounts", nargs="*", default=[])
    rec = commands.add_parser("reconcile", help="Reconcile two CSVs at an explicit grain")
    rec.add_argument("left", type=Path)
    rec.add_argument("right", type=Path)
    rec.add_argument("--keys", nargs="+", required=True)
    rec.add_argument("--amount", required=True)
    rec.add_argument("--aggregate", action="store_true")
    rec.add_argument("--tolerance", default="0")
    calc = commands.add_parser("bridge", help="Exact sequential quantity/rate/FX bridge")
    for key in ("plan-quantity", "actual-quantity", "plan-rate", "actual-rate", "plan-fx", "actual-fx"):
        calc.add_argument("--" + key, required=True)
    for sub in (prof, rec):
        sub.add_argument("--delimiter", default=",")
        sub.add_argument("--encoding", default="utf-8-sig")
    for sub in (prof, rec, calc):
        sub.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        with localcontext() as context:
            context.prec = 128
            if args.command == "profile":
                result = profile(args.file, args.keys, args.amounts, args.delimiter, args.encoding)
            elif args.command == "reconcile":
                result = reconcile(args.left, args.right, args.keys, args.amount, args.aggregate, args.delimiter, args.encoding, number(args.tolerance, "tolerance"))
            else:
                result = bridge(*(number(getattr(args, k), k) for k in ("plan_quantity", "actual_quantity", "plan_rate", "actual_rate", "plan_fx", "actual_fx")))
        write_result(result, args.output)
        return 0
    except (ValueError, OSError, UnicodeError, csv.Error, DecimalException) as exc:
        print(f"Analysis stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
