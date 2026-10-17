import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gtm_engine.capstone import run_capstone
from gtm_engine.capstone import score_record
from gtm_engine.config import read_bounded_int, read_secret
from gtm_engine.operations import summarize_run_log
from gtm_engine.security import redact_sensitive_text


ROOT = Path(__file__).resolve().parents[1]
POLL_PATH = ROOT / "day-16" / "pipeline_status_client.py"
_SPEC = importlib.util.spec_from_file_location("pipeline_status_client", POLL_PATH)
poll_client = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(poll_client)


class Day16PollingTests(unittest.TestCase):
    class Response:
        def __init__(self, body):
            self.body = body

        def raise_for_status(self):
            return None

        def json(self):
            return self.body

    class Session:
        def __init__(self, statuses):
            self.statuses = list(statuses)
            self.posts = 0
            self.gets = 0

        def post(self, url, timeout):
            self.posts += 1
            return Day16PollingTests.Response({
                "run_id": "synthetic-run",
                "status": "running",
            })

        def get(self, url, timeout):
            self.gets += 1
            return Day16PollingTests.Response({
                "run_id": "synthetic-run",
                "status": self.statuses.pop(0),
            })

    def test_triggers_once_and_polls_same_run_to_success(self):
        session = self.Session(["running", "success"])
        with patch.object(poll_client.time, "sleep"):
            result = poll_client.run_pipeline(session=session, poll_seconds=0.1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(session.posts, 1)
        self.assertEqual(session.gets, 2)

    def test_reports_terminal_failure(self):
        session = self.Session(["failed"])
        result = poll_client.run_pipeline(session=session, poll_seconds=0.1)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(session.posts, 1)

    def test_timeout_does_not_trigger_again(self):
        session = self.Session([])
        with self.assertRaises(TimeoutError):
            poll_client.run_pipeline(
                session=session,
                timeout_seconds=0.000001,
            )
        self.assertEqual(session.posts, 1)

    def test_n8n_export_is_inactive_and_uses_one_trigger(self):
        workflow = json.loads(
            (ROOT / "day-16" / "pipeline_workflow.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(workflow["active"])
        self.assertEqual(workflow["settings"]["executionTimeout"], 900)
        self.assertNotIn("credentials", workflow)
        starts = [
            node for node in workflow["nodes"]
            if node["parameters"].get("method") == "POST"
        ]
        checks = [
            node for node in workflow["nodes"]
            if node["parameters"].get("url", "").startswith("={{")
        ]
        self.assertEqual(len(starts), 1)
        self.assertEqual(len(checks), 1)


class Day26OperationsTests(unittest.TestCase):
    def test_summarizes_without_exposing_details(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs.csv"
            path.write_text(
                "status,leads_processed,duration_seconds,details\n"
                "SUCCESS,3,1.5,private@example.test\n"
                "FAILED,0,2.5,error\n",
                encoding="utf-8",
            )
            result = summarize_run_log(path)
        self.assertEqual(result["run_count"], 2)
        self.assertEqual(result["failure_count"], 1)
        self.assertEqual(result["leads_processed_total"], 3)
        self.assertEqual(result["average_duration_seconds"], 2.0)


class Day22SqlTests(unittest.TestCase):
    def test_sql_lesson_runs_outside_repository_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT / "day-22" / "run_sql.py")],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("lead_to_mql_rate", result.stdout)
        self.assertIn("average_duration_days", result.stdout)


class Day27SecurityTests(unittest.TestCase):
    def test_redacts_tokens_and_personal_email(self):
        text = (
            "Bearer abc123 person@example.test "
            "HUBSPOT_TOKEN=pat-abcdefghijklm"
        )
        redacted = redact_sensitive_text(text)
        self.assertNotIn("abc123", redacted)
        self.assertNotIn("person@example.test", redacted)
        self.assertNotIn("pat-abcdefghijklm", redacted)

    def test_config_validation_does_not_echo_secret(self):
        with self.assertRaisesRegex(ValueError, "HUBSPOT_ACCESS_TOKEN"):
            read_secret(
                "HUBSPOT_ACCESS_TOKEN",
                {"HUBSPOT_ACCESS_TOKEN": "your_private_value"},
            )
        self.assertEqual(
            read_bounded_int("MAX_LEADS", 10, 1, 100, {"MAX_LEADS": "50"}),
            50,
        )
        with self.assertRaises(ValueError):
            read_bounded_int(
                "MAX_LEADS", 10, 1, 100, {"MAX_LEADS": "5000"}
            )


class Day28CapstoneTests(unittest.TestCase):
    def test_offline_capstone_requires_approval_and_never_mutates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "leads.csv"
            source.write_text(
                "company_name,website,contact_name,job_title,email,"
                "industry,country,employees,employee_segment,buying_signal\n"
                "Example Labs,example.test,Alex Doe,VP Sales,"
                "alex@example.test,Software,USA,120,Growth,\n",
                encoding="utf-8",
            )
            result = run_capstone(source, root / "output")
            with (root / "output" / "capstone_report.csv").open(
                newline="", encoding="utf-8"
            ) as file:
                row = next(csv.DictReader(file))
        self.assertEqual(result["crm_writes"], 0)
        self.assertEqual(result["messages_sent"], 0)
        self.assertEqual(row["approval_status"], "HUMAN_APPROVAL_REQUIRED")
        self.assertEqual(row["crm_mode"], "DRY_RUN")
        self.assertEqual(row["message_sent"], "NO")

    def test_invalid_employee_count_fails_instead_of_low_scoring(self):
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            score_record({"industry": "Software", "employees": "unknown"})


if __name__ == "__main__":
    unittest.main()
