import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from gtm_engine.crm import (
    dry_run_plan,
    hubspot_token,
    read_leads,
    validate_and_normalize,
)
from gtm_engine.deduplication import review_duplicates
from gtm_engine.funnel import route
from gtm_engine.http_client import request_with_retries


class FakeResponse:
    def __init__(self, status_code, headers=None, body=None):
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body or {}
        self.content = b"response" if body is not None else b""

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return self.body


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


class Day14CrmTests(unittest.TestCase):
    def test_normalizes_valid_record(self):
        record = validate_and_normalize({
            "company_name": "  Northstar   Labs ",
            "website": "HTTPS://WWW.NORTHSTAR.EXAMPLE/path",
            "email": " Jamie@Northstar.example ",
            "job_title": "VP Revenue",
        })
        self.assertEqual(record["company_name"], "Northstar Labs")
        self.assertEqual(record["domain"], "northstar.example")
        self.assertEqual(record["email"], "jamie@northstar.example")

    def test_rejects_bad_email(self):
        with self.assertRaisesRegex(ValueError, "Invalid email"):
            validate_and_normalize({
                "company_name": "Northstar",
                "website": "northstar.example",
                "email": "not-an-email",
                "job_title": "VP Revenue",
            })

    def test_dry_run_never_calls_a_gateway(self):
        plan = dry_run_plan([{
            "email": "jane@example.test",
            "company_name": "Example",
            "domain": "example.test",
        }])
        self.assertEqual(plan[0]["mode"], "DRY_RUN")
        self.assertEqual(plan[0]["planned_contact_operation"],
                         "UPSERT_BY_UNIQUE_EMAIL")

    def test_reads_csv_with_absolute_path(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leads.csv"
            path.write_text(
                "company_name,website,email,job_title\n"
                "Example,example.test,person@example.test,CEO\n",
                encoding="utf-8",
            )
            self.assertEqual(len(read_leads(path)), 1)

    def test_row_limit_and_placeholder_token_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "leads.csv"
            path.write_text(
                "company_name,website,email,job_title\n"
                "Example,example.test,one@example.test,CEO\n"
                "Example,example.test,two@example.test,CEO\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "limit of 1"):
                read_leads(path, max_records=1)
        with patch.dict("os.environ", {
            "HUBSPOT_ACCESS_TOKEN": "your_placeholder_token",
            "HUBSPOT_TOKEN": "",
        }):
            with self.assertRaisesRegex(RuntimeError, "non-placeholder"):
                hubspot_token()

    def test_live_adapter_creates_then_reads_back_contact(self):
        session = FakeSession([
            FakeResponse(200, body={"results": []}),
            FakeResponse(201, body={"id": "mock-contact-1"}),
            FakeResponse(200, body={"properties": {
                "email": "jane@example.test",
                "jobtitle": "VP Revenue",
            }}),
        ])
        from gtm_engine.crm import HubSpotGateway

        result = HubSpotGateway("mock-token", session=session).upsert_contact({
            "email": "jane@example.test",
            "contact_name": "Jane Doe",
            "job_title": "VP Revenue",
        })
        self.assertEqual(result, "CREATED:mock-contact-1")
        self.assertEqual(len(session.calls), 3)
        self.assertEqual(session.calls[-1][0], "GET")

    def test_live_adapter_fails_when_readback_disagrees(self):
        session = FakeSession([
            FakeResponse(200, body={"results": []}),
            FakeResponse(201, body={"id": "mock-contact-1"}),
            FakeResponse(200, body={"properties": {
                "email": "wrong@example.test",
                "jobtitle": "VP Revenue",
            }}),
        ])
        from gtm_engine.crm import HubSpotGateway

        with self.assertRaisesRegex(RuntimeError, "read-back"):
            HubSpotGateway("mock-token", session=session).upsert_contact({
                "email": "jane@example.test",
                "contact_name": "Jane Doe",
                "job_title": "VP Revenue",
            })


class Day15HttpTests(unittest.TestCase):
    def test_get_retries_503_with_exponential_backoff(self):
        session = FakeSession([
            FakeResponse(503),
            FakeResponse(200),
        ])
        sleeps = []
        result = request_with_retries(
            "GET", "https://example.test", session=session,
            sleep=sleeps.append, backoff_seconds=0.25,
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(sleeps, [0.25])

    def test_post_without_idempotency_key_is_not_retried(self):
        session = FakeSession([FakeResponse(503)])
        with self.assertRaises(requests.HTTPError):
            request_with_retries(
                "POST", "https://example.test", session=session,
                sleep=lambda _: None,
            )
        self.assertEqual(len(session.calls), 1)

    def test_post_with_idempotency_key_can_retry(self):
        session = FakeSession([
            FakeResponse(429, headers={"Retry-After": "2"}),
            FakeResponse(200),
        ])
        sleeps = []
        result = request_with_retries(
            "POST", "https://example.test", session=session,
            headers={"Idempotency-Key": "synthetic-run-1"},
            sleep=sleeps.append,
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(len(session.calls), 2)
        self.assertEqual(sleeps, [2.0])

    def test_get_retries_timeout_and_passes_timeout_value(self):
        session = FakeSession([
            requests.Timeout("synthetic timeout"),
            FakeResponse(200),
        ])
        result = request_with_retries(
            "GET", "https://example.test", session=session,
            timeout=4, sleep=lambda _: None,
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(session.calls[0][2]["timeout"], 4)
        self.assertEqual(len(session.calls), 2)

    def test_client_error_is_not_retried(self):
        session = FakeSession([FakeResponse(400), FakeResponse(200)])
        with self.assertRaises(requests.HTTPError):
            request_with_retries(
                "GET", "https://example.test", session=session,
                sleep=lambda _: None,
            )
        self.assertEqual(len(session.calls), 1)

    def test_retry_limit_is_bounded(self):
        session = FakeSession([FakeResponse(503), FakeResponse(503)])
        with self.assertRaises(requests.HTTPError):
            request_with_retries(
                "GET", "https://example.test", session=session,
                max_attempts=2, sleep=lambda _: None,
            )
        self.assertEqual(len(session.calls), 2)


class Day17RoutingTests(unittest.TestCase):
    def test_demo_request_is_sql_and_routes_by_country(self):
        result = route({
            "icp_score": "20",
            "buying_signal": "Demo Request",
            "country": "Canada",
            "employee_segment": "Growth",
        })
        self.assertEqual(result["lifecycle_stage"], "SQL")
        self.assertEqual(result["owner_queue"], "International - growth")

    def test_invalid_score_is_reviewed_not_qualified(self):
        result = route({"icp_score": "101", "country": "USA"})
        self.assertEqual(result["lifecycle_stage"], "Lead")
        self.assertIn("between 0 and 100", result["routing_reason"])


class Day18DeduplicationTests(unittest.TestCase):
    def test_duplicate_is_a_review_not_a_merge(self):
        rows = [
            {"email": "same@example.test", "company_name": "A",
             "website": "a.example"},
            {"email": " SAME@example.test ", "company_name": "A",
             "website": "www.a.example"},
        ]
        result = review_duplicates(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(
            {item["match_key"] for item in result},
            {"contact_email", "company_domain_and_name"},
        )
        self.assertTrue(all(
            item["safe_merge_candidate"] == "NO" for item in result
        ))
        self.assertTrue(all(
            item["review_status"] == "HUMAN_REVIEW_REQUIRED"
            for item in result
        ))

    def test_null_and_malformed_values_are_not_silently_merged(self):
        rows = [
            {"company_name": "", "website": "", "email": ""},
            {"company_name": "", "website": "", "email": ""},
            {"company_name": "A", "website": "a.example",
             "email": "not-an-email"},
            {"company_name": "A", "website": "a.example",
             "email": "not-an-email"},
        ]
        result = review_duplicates(rows)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            item["review_status"] == "HUMAN_REVIEW_REQUIRED"
            for item in result
        ))

    def test_same_company_with_different_contact_emails_is_company_only(self):
        rows = [
            {"company_name": "Acme, Inc.", "website": "acme.example",
             "email": "one@acme.example"},
            {"company_name": "Acme Inc", "website": "www.acme.example",
             "email": "two@acme.example"},
        ]
        result = review_duplicates(rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["match_key"], "company_domain_and_name")


if __name__ == "__main__":
    unittest.main()
