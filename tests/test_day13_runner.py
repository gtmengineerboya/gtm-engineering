"""Day 13: the runner must reject a report left over from an earlier run."""

import importlib.util
import os
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "pipeline_runner", ROOT / "day-13" / "pipeline_runner.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)

CSV = ("company_name,personalized_message,validation_status\n"
       "Acme,Hello,APPROVED_AI\nBeta,,NEEDS_REVIEW\n")


class StaleReportTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.report = Path(self.tmp.name) / "review.csv"
        self.report.write_text(CSV, encoding="utf-8")
        self.original = runner.REVIEW_FILE
        runner.REVIEW_FILE = self.report

    def tearDown(self):
        runner.REVIEW_FILE = self.original
        self.tmp.cleanup()

    def test_fresh_report_is_counted(self):
        self.assertEqual(runner.validate_output(time.time() - 5), (2, 1, 1))

    def test_stale_report_is_rejected(self):
        old = time.time() - 3600
        os.utime(self.report, (old, old))
        with self.assertRaises(RuntimeError):
            runner.validate_output(time.time())

    def test_without_start_time_old_behaviour_is_kept(self):
        old = time.time() - 3600
        os.utime(self.report, (old, old))
        self.assertEqual(runner.validate_output(), (2, 1, 1))


if __name__ == "__main__":
    unittest.main()
