"""Offline checks only. Fixtures are synthetic, not customer exports."""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import compare_reviews as tool


def row(**values):
    return {"source": "google_play", "appId": "demo.app", "country": "us", "language": "en",
            "reviewId": "one", "rating": 2, "text": "Synthetic text", **values}


class ReviewChecks(unittest.TestCase):
    def test_demonstration(self):
        result = tool.compare(*tool.demo_rows(), synthetic=True)
        self.assertEqual(result["counts"], {"newly_observed": 1, "changed": 1, "unchanged": 1, "missing_from_later_sample": 1})
        self.assertEqual(result["before"]["repeated_equivalent_rows"], 1)
        self.assertEqual(result["before"]["identified_reviews"], 3)
        self.assertEqual(result["after"]["groups"][1]["low_rating_share"], .5)

    def test_empty_export(self):
        result = tool.compare([], [])
        self.assertEqual(sum(result["counts"].values()), 0)
        self.assertEqual(result["coverage"], "unknown")

    def test_missing_identity_never_merges(self):
        result = tool.compare([row(reviewId=None)], [row(reviewId=None)])
        self.assertEqual(result["before"]["unresolved_rows"], 1)
        self.assertEqual(sum(result["counts"].values()), 0)

    def test_conflicts_not_reported_as_new(self):
        result = tool.compare([row(), row(rating=5)], [row()])
        self.assertEqual(result["ambiguous_keys_excluded_from_comparison"], 1)
        self.assertEqual(sum(result["counts"].values()), 0)

    def test_conflicts_not_reported_as_missing(self):
        result = tool.compare([row()], [row(), row(text="A different synthetic text")])
        self.assertEqual(sum(result["counts"].values()), 0)

    def test_request_contexts_stay_separate(self):
        rows = [row(), row(country="gb"), row(language="fr"), row(language=None), row(language="unknown"), row(appId="other"), row(source="app_store")]
        self.assertEqual(tool.compare([], rows)["counts"]["newly_observed"], 7)

    def test_invalid_ratings_have_no_denominator(self):
        rows = [row(reviewId=str(i), rating=value) for i, value in enumerate([0, 6, True, "bad", 2.5, None])]
        group = tool.compare([], rows)["after"]["groups"][0]
        self.assertEqual(group["valid_ratings"], 0)
        self.assertEqual(group["invalid_ratings"], 6)
        self.assertIsNone(group["low_rating_share"])

    def test_numerical_rating_equivalence(self):
        self.assertEqual(tool.compare([row(rating="2")], [row(rating=2)])["counts"]["unchanged"], 1)

    def test_response_change_is_identified(self):
        change = tool.compare([row()], [row(developerReply="Synthetic reply")])["changes"][0]
        self.assertEqual(change["changed_fields"], ["developerReply"])

    def test_reviewer_names_are_not_exported(self):
        result = tool.compare([], [row(userName="PRIVATE_PERSON", text="PRIVATE_REVIEW")])
        self.assertNotIn("PRIVATE_PERSON", json.dumps(result))
        self.assertNotIn("PRIVATE_REVIEW", json.dumps(result))

    def test_wrong_shape_fails(self):
        for value in ({}, ["not an object"]):
            with self.assertRaises(ValueError):
                tool.compare(value, [])

    def test_missing_country_is_not_silently_us(self):
        self.assertEqual(tool.compare([], [row(country=None)])["after"]["unresolved_rows"], 1)

    def test_spreadsheet_prefixes(self):
        for value in ("=2+2", " +2", "-2", "@cmd", "\tword", "\rword"):
            self.assertTrue(tool.csv_cell(value).startswith("'"))
        self.assertEqual(tool.csv_cell("plain"), "plain")

    def test_markdown_does_not_embed_html_or_images(self):
        rendered = tool.markdown(tool.compare([], [row(appId='<script>![x](bad)|')]))
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("![x]", rendered)

    def test_strict_json_and_utf8_bom(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            path.write_text(json.dumps([row()]), encoding="utf-8-sig")
            self.assertEqual(len(tool.load_rows(path)), 1)
            path.write_text('[{"rating":NaN}]', encoding="utf-8")
            with self.assertRaises(ValueError):
                tool.load_rows(path)

    def test_cli_real_file_path_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            before, after = base / "before.json", base / "after.json"
            before.write_text(json.dumps([row()]), encoding="utf-8")
            after.write_text(json.dumps([row(rating=5)]), encoding="utf-8")
            original = (before.read_bytes(), after.read_bytes())
            output = base / "result"
            command = [sys.executable, str(Path(tool.__file__)), str(before), str(after), "--out", str(output)]
            run = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            report = json.loads((output / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["counts"]["changed"], 1)
            with (output / "changes.csv").open(encoding="utf-8-sig", newline="") as handle:
                self.assertEqual(list(csv.DictReader(handle))[0]["changed_fields"], "rating")
            self.assertEqual(original, (before.read_bytes(), after.read_bytes()))
            old_report = (output / "report.json").read_bytes()
            repeat = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(repeat.returncode, 2)
            self.assertEqual((output / "report.json").read_bytes(), old_report)

    def test_cli_demo(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "demo"
            run = subprocess.run([sys.executable, str(Path(tool.__file__)), "--demo", "--out", str(output)], capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue(json.loads((output / "report.json").read_text(encoding="utf-8"))["synthetic_example"])


if __name__ == "__main__":
    unittest.main()
