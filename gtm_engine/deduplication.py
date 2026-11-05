"""Conservative duplicate candidate detection; this module never deletes."""

from __future__ import annotations

import re

from gtm_engine.crm import normalize_domain, normalize_email


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (value or "").casefold())


def review_duplicates(
    records: list[dict[str, str]],
) -> list[dict[str, str]]:
    seen_emails: dict[str, int] = {}
    seen_companies: dict[str, int] = {}
    reviews = []
    for index, record in enumerate(records, start=1):
        email = normalize_email(record.get("email", ""))
        domain = normalize_domain(record.get("website", ""))
        name = normalize_name(record.get("company_name", ""))
        match_keys = []
        if email:
            match_keys.append(("contact_email", email, seen_emails))
        if domain and name:
            match_keys.append(
                ("company_domain_and_name", f"{domain}|{name}", seen_companies)
            )
        for key_name, key_value, seen in match_keys:
            first_index = seen.get(key_value)
            if first_index is None:
                seen[key_value] = index
                continue
            reviews.append({
                "record_number": str(index),
                "possible_match_record": str(first_index),
                "match_key": key_name,
                "normalized_key": key_value,
                "review_status": "HUMAN_REVIEW_REQUIRED",
                "safe_merge_candidate": "NO",
                "reason": (
                    "Matching key found; compare source fields before any merge"
                ),
            })
    return reviews
