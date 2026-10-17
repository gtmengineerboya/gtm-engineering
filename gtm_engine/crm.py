"""Safe lead normalization and an explicitly guarded HubSpot contact gateway."""

from __future__ import annotations

import csv
import os
import re
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

from gtm_engine.config import read_secret
from gtm_engine.http_client import request_with_retries


REQUIRED_FIELDS = ("company_name", "website", "email", "job_title")


def normalize_email(value: str) -> str:
    return (value or "").strip().casefold()


def normalize_domain(value: str) -> str:
    value = (value or "").strip().casefold()
    if not value:
        return ""
    parsed = urlparse(value if "://" in value else "https://" + value)
    host = (parsed.hostname or "").rstrip(".")
    return host[4:] if host.startswith("www.") else host


def normalize_company_name(value: str) -> str:
    value = re.sub(r"\s+", " ", (value or "").strip())
    return value


def validate_and_normalize(record: dict[str, str]) -> dict[str, str]:
    normalized = {
        key: (value or "").strip()
        for key, value in record.items()
    }
    normalized["company_name"] = normalize_company_name(
        normalized.get("company_name", "")
    )
    normalized["email"] = normalize_email(normalized.get("email", ""))
    normalized["domain"] = normalize_domain(
        normalized.get("website", "")
    )
    missing = [field for field in REQUIRED_FIELDS if not normalized.get(field)]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", normalized["email"]):
        raise ValueError("Invalid email address")
    if not normalized["domain"]:
        raise ValueError("Website must contain a valid domain")
    return normalized


def read_leads(path: Path, max_records: int = 100) -> list[dict[str, str]]:
    if max_records < 1:
        raise ValueError("max_records must be positive")
    with path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError(f"CSV has no header row: {path}")
        missing = set(REQUIRED_FIELDS) - set(reader.fieldnames)
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        rows = []
        for row in reader:
            if len(rows) >= max_records:
                raise ValueError(
                    f"CSV exceeds the configured limit of {max_records} rows"
                )
            rows.append(validate_and_normalize(row))
    if not rows:
        raise ValueError(f"CSV contains no lead rows: {path}")
    return rows


def hubspot_token() -> str:
    for name in ("HUBSPOT_ACCESS_TOKEN", "HUBSPOT_TOKEN"):
        if os.getenv(name):
            try:
                return read_secret(name)
            except ValueError:
                continue
    raise RuntimeError(
        "Set a non-placeholder HUBSPOT_ACCESS_TOKEN or HUBSPOT_TOKEN "
        "in the process environment."
    )


class ContactGateway(Protocol):
    def upsert_contact(self, lead: dict[str, str]) -> str: ...
    def find_company_by_domain(self, domain: str) -> str | None: ...


def dry_run_plan(leads: list[dict[str, str]]) -> list[dict[str, str]]:
    """Describe planned operations without making network calls."""
    return [
        {
            "email": lead["email"],
            "company_name": lead["company_name"],
            "domain_lookup": lead["domain"],
            "planned_contact_operation": "UPSERT_BY_UNIQUE_EMAIL",
            "mode": "DRY_RUN",
        }
        for lead in leads
    ]


class HubSpotGateway:
    """Minimal live adapter; instantiate only after deliberate user opt-in."""

    base_url = "https://api.hubapi.com/crm/v3/objects"

    def __init__(self, token: str, session: Any = None):
        if not token.strip():
            raise ValueError("A HubSpot access token is required for live mode")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self.session = session

    def _request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        response = request_with_retries(
            method,
            url,
            session=self.session,
            headers=self.headers,
            timeout=15,
            **kwargs,
        )
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    def find_company_by_domain(self, domain: str) -> str | None:
        if not domain:
            return None
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "domain",
                    "operator": "EQ",
                    "value": domain,
                }]
            }],
            "properties": ["name", "domain"],
            "limit": 2,
        }
        results = self._request(
            "POST",
            f"{self.base_url}/companies/search",
            json=payload,
        ).get("results", [])
        exact = [
            result for result in results
            if normalize_domain(
                result.get("properties", {}).get("domain", "")
            ) == domain
        ]
        if len(exact) > 1:
            raise RuntimeError(f"Multiple exact HubSpot companies for {domain}")
        return str(exact[0]["id"]) if exact else None

    def upsert_contact(self, lead: dict[str, str]) -> str:
        search = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": lead["email"],
                }]
            }],
            "properties": ["email", "firstname", "lastname", "jobtitle"],
            "limit": 2,
        }
        results = self._request(
            "POST",
            f"{self.base_url}/contacts/search",
            json=search,
        ).get("results", [])
        if len(results) > 1:
            raise RuntimeError(
                f"Multiple HubSpot contacts match {lead['email']}"
            )

        name_parts = lead.get("contact_name", "").split(maxsplit=1)
        properties = {
            "email": lead["email"],
            "firstname": name_parts[0] if name_parts else "",
            "lastname": name_parts[1] if len(name_parts) > 1 else "",
            "jobtitle": lead["job_title"],
        }
        if results:
            contact_id = str(results[0]["id"])
            self._request(
                "PATCH",
                f"{self.base_url}/contacts/{contact_id}",
                json={"properties": properties},
            )
            operation = "UPDATED"
        else:
            created = self._request(
                "POST",
                f"{self.base_url}/contacts",
                json={"properties": properties},
            )
            contact_id = str(created["id"])
            operation = "CREATED"

        saved = self._request(
            "GET",
            f"{self.base_url}/contacts/{contact_id}",
            params={"properties": "email,firstname,lastname,jobtitle"},
        )
        saved_properties = saved.get("properties", {})
        if (
            normalize_email(saved_properties.get("email", ""))
            != lead["email"]
            or saved_properties.get("jobtitle", "") != properties["jobtitle"]
        ):
            raise RuntimeError(
                f"HubSpot read-back did not match contact {contact_id}"
            )
        return f"{operation}:{contact_id}"


def execute_live_upserts(
    leads: list[dict[str, str]],
    gateway: ContactGateway,
) -> list[dict[str, str]]:
    results = []
    for lead in leads:
        # Resolve the company by its standard domain field; association setup
        # is a separate, schema-verified lesson (Day 21).
        company_id = gateway.find_company_by_domain(lead["domain"])
        operation = gateway.upsert_contact(lead)
        results.append({
            "email": lead["email"],
            "company_id": company_id or "",
            "contact_operation": operation,
        })
    return results
