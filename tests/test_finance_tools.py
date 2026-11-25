import importlib.util
from decimal import Decimal
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import finance_tools as finance


class FinanceControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def csv(self, name, text):
        p = self.root / name
        p.write_text(text, encoding="utf-8")
        return p

    def test_profile_scans_full_population_preserves_keys_and_decimal(self):
        p = self.csv("sample.csv", "id,amount\n001,0.1\n001,0.2\n01,2.30\n,4.00\n")
        result = finance.profile(p, ["id"], ["amount"])
        self.assertEqual(result["rows"], 4)
        self.assertEqual(result["distinctNonblankKeys"], 2)
        self.assertEqual(result["missingKeyRows"], 1)
        self.assertEqual(result["duplicateKeyGroups"], 1)
        self.assertEqual(result["excessDuplicateRows"], 1)
        self.assertEqual(Decimal(result["totals"]["amount"]), Decimal("6.6"))
        self.assertEqual(p.read_text(), "id,amount\n001,0.1\n001,0.2\n01,2.30\n,4.00\n")

    def test_malformed_headers_rows_and_nonfinite_amounts_fail(self):
        for text in ["id,id\na,b\n", "id,amount\na,2,3\n", "id,amount\na\n", "id,amount\na,NaN\n", "id,amount\na,\n"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                finance.profile(self.csv("invalid.csv", text), ["id"], ["amount"])
        with self.assertRaises(ValueError):
            finance.profile(self.csv("valid.csv", "id,amount\na,2\n"), ["id"], ["amount", "amount"])

    def test_reconciliation_retains_missing_keys_and_balances(self):
        result = finance.reconcile(ROOT / "examples/plan.csv", ROOT / "examples/actual.csv", ["cost_center", "account"], "amount")
        self.assertEqual(result["statuses"], {"different": 2, "left_only": 1, "right_only": 1})
        self.assertEqual(Decimal(result["deltaRightMinusLeft"]), Decimal("15.05"))
        self.assertEqual(Decimal(result["reconciliationResidual"]), 0)
        self.assertEqual(result["details"][0]["key"]["cost_center"], "001")

    def test_duplicate_grain_requires_explicit_aggregation(self):
        a = self.csv("a.csv", "id,amount\nx,1\nx,2\n")
        b = self.csv("b.csv", "id,amount\nx,3\n")
        with self.assertRaises(ValueError):
            finance.reconcile(a, b, ["id"], "amount")
        result = finance.reconcile(a, b, ["id"], "amount", allow_aggregate=True)
        self.assertEqual(result["statuses"], {"matched": 1})
        self.assertEqual(result["left"]["duplicateKeyGroups"], 1)

    def test_quantity_rate_fx_bridge_closes_and_handles_zero_quantity(self):
        result = finance.bridge(*(Decimal(v) for v in ["100", "110", "20", "21", "150", "145"]))
        self.assertEqual([result[k] for k in ["plan", "actual", "quantityEffect", "rateEffect", "fxEffect", "residual"]],
                         ["300000", "334950", "30000", "16500", "-11550", "0"])
        zero = finance.bridge(*(Decimal(v) for v in ["0", "2", "3", "5", "1", "1"]))
        self.assertEqual(zero["residual"], "0")
        self.assertEqual(zero["actual"], "10")

    def test_output_does_not_overwrite_an_existing_file(self):
        path = self.root / "result.json"
        finance.write_result({"amount": "0.30"}, path)
        with self.assertRaises(FileExistsError):
            finance.write_result({"amount": "0"}, path)
        self.assertIn("0.30", path.read_text())

    def test_bridge_exact_at_supported_numeric_extremes(self):
        values = [finance.number(v, "input") for v in ["1e28", "1e-28", "1e28", "1e-28", "1e28", "1e-28"]]
        self.assertEqual(Decimal(finance.bridge(*values)["residual"]), 0)


@unittest.skipUnless(importlib.util.find_spec("openpyxl"), "Optional openpyxl dependency not installed")
class WorkbookControls(unittest.TestCase):
    def test_workbook_without_stored_dimension_is_scanned(self):
        import openpyxl
        from workbook_audit import audit
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "unsized.xlsx"
            workbook = openpyxl.Workbook(write_only=True)
            workbook.create_sheet().append(["id", "amount"])
            workbook.worksheets[0].append(["001", 5])
            workbook.save(path)
            sheet = audit(path)["sheets"][0]
            self.assertIsNone(sheet["declaredDimension"])
            self.assertEqual(sheet["nonemptyRowsIncludingHeaders"], 2)
            self.assertEqual(sheet["populatedCells"], 4)

    def test_formula_cache_and_hidden_sheet_are_not_calculation_claims(self):
        import openpyxl
        from workbook_audit import audit
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "example.xlsx"
            workbook = openpyxl.Workbook()
            ws = workbook.active
            ws.append(["id", "amount"])
            ws.append(["001", 5])
            ws["B3"] = "=SUM(B2:B2)"
            ws["B4"] = "#DIV/0!"
            hidden = workbook.create_sheet("Hidden")
            hidden.sheet_state = "hidden"
            hidden["A1"] = "x"
            workbook.save(path)
            before = path.read_bytes()
            result = audit(path)
            self.assertEqual(result["recalculation"], "not performed")
            self.assertEqual(result["sheets"][0]["formulaCells"], 1)
            self.assertEqual(result["sheets"][0]["formulaCachesBlankOrAbsent"], 1)
            self.assertEqual(result["sheets"][0]["storedErrorCounts"], {"#DIV/0!": 1})
            self.assertEqual(result["sheets"][1]["visibility"], "hidden")
            self.assertEqual(path.read_bytes(), before)


@unittest.skipUnless(importlib.util.find_spec("duckdb"), "Optional DuckDB dependency not installed")
class DuckDBControls(unittest.TestCase):
    def test_bad_csv_cannot_shift_the_header_or_skip_records(self):
        from duckdb_profile import inspect
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "bad.csv"
            for text in ["id,amount\na,1\nb,2,3\n", "id,amount\na,1,2\nb,2,3\nc,3,4\n", "id,amount\na\nb,2\n"]:
                p.write_text(text)
                with self.subTest(text=text), self.assertRaises(Exception):
                    inspect(p, [])

    def test_key_named_n_does_not_collide_with_internal_count(self):
        import duckdb
        from duckdb_profile import inspect
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "n.parquet"
            with duckdb.connect() as con:
                con.sql("SELECT * FROM (VALUES (10),(10),(20)) AS t(n)").write_parquet(str(p))
            counts = inspect(p, ["n"])["keys"]
            self.assertEqual(counts["distinctNonblankKeys"], 2)
            self.assertEqual(counts["duplicateKeyGroups"], 1)
            self.assertEqual(counts["excessDuplicateRows"], 1)

    def test_explicit_csv_dialect_supports_bom_crlf_and_quoted_newline(self):
        from duckdb_profile import inspect
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "windows.csv"
            p.write_bytes(b'\xef\xbb\xbfid,comment\r\n001,"first\r\nsecond"\r\n002,"quoted ""word"""\r\n')
            result = inspect(p, ["id"])
            self.assertEqual(result["rows"], 2)
            self.assertEqual([r["name"] for r in result["schema"]], ["id", "comment"])

    def test_csv_and_parquet_full_counts_and_key_rules(self):
        import duckdb
        from duckdb_profile import inspect
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "sample.csv"
            p.write_text("id,amount\n001,1\n001,2\n01,3\n,4\n")
            result = inspect(p, ["id"])
            self.assertEqual(result["rows"], 4)
            self.assertEqual(result["keys"]["distinctNonblankKeys"], 2)
            self.assertEqual(result["keys"]["missingKeyRows"], 1)
            self.assertEqual(result["keys"]["duplicateKeyGroups"], 1)
            self.assertEqual(result["schema"][0]["type"], "VARCHAR")
            parquet = Path(folder) / "sample.parquet"
            with duckdb.connect() as con:
                con.read_csv(str(p), all_varchar=True).write_parquet(str(parquet))
            self.assertEqual(inspect(parquet, ["id"])["keys"], result["keys"])

    def test_duplicate_headers_and_wildcard_paths_are_rejected(self):
        from duckdb_profile import inspect
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / "duplicate.csv"
            p.write_text("id,id\na,b\n")
            with self.assertRaises(ValueError):
                inspect(p, ["id"])
            q = Path(folder) / "data[1].csv"
            q.write_text("id\na\n")
            with self.assertRaises(ValueError):
                inspect(q, ["id"])


if __name__ == "__main__":
    unittest.main()
