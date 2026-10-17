import hashlib
import hmac
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

import requests

from gtm_engine.associations import (
    associate_and_verify,
    association_plan,
)
from gtm_engine.metrics import calculate_metrics
from gtm_engine.outreach import evaluate_message, model_judgment
from gtm_engine.research import (
    fallback_research,
    research_with_ollama,
    validate_research,
)
from gtm_engine.webhooks import (
    record_event,
    validate_event,
    verify_signature,
)


class Day19ResearchTests(unittest.TestCase):
    def test_fallback_uses_input_fields_only(self):
        result = fallback_research(
            {"company_name": "Sample Co", "country": "USA"},
            "offline",
        )
        self.assertEqual(
            result["observed_facts"],
            [
                {"field": "company_name", "value": "Sample Co"},
                {"field": "country", "value": "USA"},
            ],
        )
        self.assertEqual(result["hypotheses"], [])
        self.assertEqual(result["fallback_reason"], "offline")

    def test_rejects_unsupported_observed_fact(self):
        result = {
            "observed_facts": [{"field": "industry", "value": "Fintech"}],
            "hypotheses": [],
            "confidence": 0.8,
            "sources": ["industry"],
            "limitations": [],
        }
        with self.assertRaisesRegex(ValueError, "not supported"):
            validate_research(result, {"industry": "Software"})

    def test_invalid_ollama_json_uses_explicit_fallback(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"response": "not json"}
        result = research_with_ollama(
            {"company_name": "Synthetic Co"},
            enabled=True,
            post=Mock(return_value=response),
        )
        self.assertEqual(len(result["observed_facts"]), 1)
        self.assertIn("invalid", result["fallback_reason"])

    def test_unavailable_ollama_uses_fallback(self):
        result = research_with_ollama(
            {"company_name": "Synthetic Co"},
            enabled=True,
            post=Mock(side_effect=requests.ConnectionError()),
        )
        self.assertIn("unavailable", result["fallback_reason"])


class Day20OutreachTests(unittest.TestCase):
    def test_unsupported_claim_and_generic_message_require_review(self):
        result = evaluate_message(
            "Northstar",
            "Hope you're well. Northstar is best-in-class and your team needs "
            "to guarantee a better outcome this quarter.",
        )
        self.assertEqual(result["status"], "REVIEW_REQUIRED")
        self.assertTrue(result["human_review_required"])
        self.assertGreaterEqual(len(result["reasons"]), 3)

    def test_even_passing_result_still_requires_human_review(self):
        message = (
            "Northstar Labs, your public profile lists Python. I would welcome "
            "a conversation to understand your current priorities and share "
            "ideas that may be relevant to your team. Would a short discussion "
            "next week be useful for comparing approaches and learning more?"
        )
        result = evaluate_message("Northstar Labs", message, ["Python"])
        self.assertEqual(result["status"], "PASS_AUTOMATED_CHECKS")
        self.assertTrue(result["human_review_required"])

    def test_model_judgment_is_separate_and_schema_checked(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {
            "response": json.dumps({
                "tone": 4,
                "clarity": 4,
                "call_to_action": 3,
                "personalization": 4,
                "factual_grounding": 5,
                "rationale": "Synthetic mock judgment",
            })
        }
        result = model_judgment(
            "Synthetic draft", ["synthetic evidence"],
            enabled=True, post=Mock(return_value=response),
        )
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["factual_grounding"], 5)

    def test_invalid_model_judgment_does_not_pass(self):
        response = Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = {"response": "{}"}
        result = model_judgment(
            "Draft", [], enabled=True, post=Mock(return_value=response)
        )
        self.assertEqual(result["status"], "UNAVAILABLE_OR_INVALID")


class Day21AssociationTests(unittest.TestCase):
    def test_requires_schema_metadata_instead_of_guessing(self):
        plan = association_plan("contact-1", "company-1", None, None)
        self.assertEqual(plan["mode"], "DRY_RUN")
        with self.assertRaisesRegex(ValueError, "will not guess"):
            association_plan(
                "contact-1", "company-1", None, None, live=True
            )

    def test_association_readback(self):
        class FakeClient:
            def verify_objects(self, contact_id, company_id):
                self.verified = (contact_id, company_id)

            def associate(self, *args):
                self.args = args

            def read_associations(self, contact_id):
                return [{"id": "company-1"}]

        client = FakeClient()
        result = associate_and_verify(
            client, "contact-1", "company-1", "HUBSPOT_DEFINED", 1
        )
        self.assertEqual(result, "VERIFIED")
        self.assertEqual(
            client.verified, ("contact-1", "company-1")
        )
        self.assertEqual(client.args[1], "company-1")


class Day23MetricsTests(unittest.TestCase):
    def test_calculates_units_and_guards_zero_denominators(self):
        data = {
            "funnel_counts": {
                "lead": 100, "mql": 30, "sql": 0,
                "opportunity": 0, "customer": 0,
            },
            "sales_marketing_spend_usd": 1000,
            "monthly_recurring_revenue_usd": 0,
            "average_customer_lifetime_months": 12,
            "average_deal_value_usd": 500,
            "average_sales_cycle_days": 30,
        }
        result = calculate_metrics(data)
        self.assertAlmostEqual(result["lead_to_mql_rate"], 0.3)
        self.assertEqual(result["mql_to_sql_rate"], 0)
        self.assertIsNone(result["sql_to_opportunity_rate"])
        self.assertIsNone(result["customer_acquisition_cost_usd_per_customer"])
        self.assertEqual(result["arr_usd_per_year"], 0)
        self.assertIsNone(result["pipeline_velocity_usd_per_day"])


class Day24WebhookTests(unittest.TestCase):
    def test_event_validation_and_duplicate_idempotency(self):
        event = validate_event({
            "event_id": "synthetic:1",
            "event_type": "lead.created",
            "unneeded_personal_data": "not persisted",
        })
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "events.sqlite3"
            self.assertTrue(record_event(database, event))
            self.assertFalse(record_event(database, event))

    def test_rejects_unsafe_or_missing_event_ids(self):
        with self.assertRaises(ValueError):
            validate_event({"event_id": "../secret", "event_type": "x"})

    def test_hmac_signature_uses_raw_body(self):
        body = b'{"event_id":"id-1"}'
        secret = "local-test-secret"
        signature = "sha256=" + hmac.new(
            secret.encode(), body, hashlib.sha256
        ).hexdigest()
        self.assertTrue(verify_signature(body, signature, secret))
        self.assertFalse(verify_signature(body + b" ", signature, secret))


if __name__ == "__main__":
    unittest.main()
