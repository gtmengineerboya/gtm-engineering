


import argparse
import csv
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR / "day-09" / ".env"
INPUT_FILE = PROJECT_DIR / "day-11" / "outreach_review.csv"
OUTPUT_FILE = Path(__file__).resolve().parent / "sync_results.csv"

load_dotenv(ENV_FILE)

TOKEN = (
    os.getenv("HUBSPOT_ACCESS_TOKEN")
    or os.getenv("HUBSPOT_TOKEN")
)

if not TOKEN:
    raise RuntimeError(f"HubSpot token not found in {ENV_FILE}")

BASE_URL = "https://api.hubapi.com"
COMPANIES_URL = f"{BASE_URL}/crm/v3/objects/companies"
SEARCH_URL = f"{COMPANIES_URL}/search"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

APPROVED_STATUSES = {"APPROVED_AI", "APPROVED_FALLBACK"}


def normalize_domain(value):
    value = (value or "").strip().lower()
    if not value:
        return ""

    if "://" not in value:
        value = "https://" + value

    domain = (urlparse(value).hostname or "").lower()

    if domain.startswith("www."):
        domain = domain[4:]

    return domain.rstrip(".")


def api_request(method, url, **kwargs):
    response = requests.request(
        method,
        url,
        headers=HEADERS,
        timeout=30,
        **kwargs,
    )
    response.raise_for_status()

    if response.status_code == 204 or not response.content:
        return {}

    return response.json()


def find_company_by_exact_domain(domain):
    if not domain:
        return None, "Missing website/domain"

    result = api_request(
        "POST",
        SEARCH_URL,
        json={
            "filterGroups": [{
                "filters": [{
                    "propertyName": "domain",
                    "operator": "EQ",
                    "value": domain,
                }]
            }],
            "properties": ["name", "domain", "outreach_message"],
            "limit": 10,
        },
    )

    exact_matches = [
        company
        for company in result.get("results", [])
        if normalize_domain(
            company.get("properties", {}).get("domain", "")
        ) == domain
    ]

    if len(exact_matches) != 1:
        return None, (
            f"Expected exactly one domain match; "
            f"found {len(exact_matches)}"
        )

    return exact_matches[0], ""


def update_and_verify(company_id, message):
    api_request(
        "PATCH",
        f"{COMPANIES_URL}/{company_id}",
        json={
            "properties": {
                "outreach_message": message,
            }
        },
    )

    saved = api_request(
        "GET",
        f"{COMPANIES_URL}/{company_id}",
        params={"properties": "outreach_message"},
    )

    saved_message = (
        saved.get("properties", {}).get("outreach_message") or ""
    )

    if saved_message != message:
        raise RuntimeError(
            "HubSpot read-back did not match the submitted message"
        )


def main():
    parser = argparse.ArgumentParser(
        description="Sync approved AI outreach messages to HubSpot."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply live updates. Without this flag, run a dry run.",
    )
    args = parser.parse_args()

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Review report not found: {INPUT_FILE}. Run Day 11 first."
        )

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)

        required = {
            "company_name",
            "website",
            "personalized_message",
            "validation_status",
        }

        if not reader.fieldnames:
            raise RuntimeError("Review report has no headers.")

        missing = required - set(reader.fieldnames)
        if missing:
            raise RuntimeError(
                "Missing report columns: " + ", ".join(sorted(missing))
            )

        leads = list(reader)

    mode = "LIVE UPDATE" if args.apply else "DRY RUN"
    print(f"Mode: {mode}")
    print(f"Review records: {len(leads)}")

    results = []

    for lead in leads:
        name = (lead.get("company_name") or "").strip()
        domain = normalize_domain(lead.get("website"))
        message = (lead.get("personalized_message") or "").strip()
        validation_status = (
            lead.get("validation_status") or ""
        ).strip()

        result = {
            "company_name": name,
            "domain": domain,
            "validation_status": validation_status,
            "hubspot_company_id": "",
            "sync_status": "",
            "details": "",
        }

        if validation_status not in APPROVED_STATUSES:
            result["sync_status"] = "SKIPPED"
            result["details"] = "Message is not approved"
            print(f"SKIPPED {name}: not approved")
            results.append(result)
            continue

        if not domain or not message:
            result["sync_status"] = "FAILED"
            result["details"] = (
                "Missing website/domain or personalized message"
            )
            print(f"FAILED {name}: missing domain or message")
            results.append(result)
            continue

        try:
            company, error = find_company_by_exact_domain(domain)

            if company is None:
                result["sync_status"] = "SKIPPED"
                result["details"] = error
                print(f"SKIPPED {name}: {error}")
                results.append(result)
                continue

            company_id = company["id"]
            result["hubspot_company_id"] = company_id

            if not args.apply:
                result["sync_status"] = "DRY_RUN"
                result["details"] = (
                    "Exact domain matched; no changes made"
                )
                print(f"DRY RUN {name}: {domain}")
            else:
                update_and_verify(company_id, message)
                result["sync_status"] = "SUCCESS"
                result["details"] = (
                    "outreach_message updated and read-back verified"
                )
                print(f"SUCCESS {name}: updated and verified")

        except (requests.RequestException, RuntimeError, ValueError) as error:
            result["sync_status"] = "FAILED"

            if isinstance(error, requests.HTTPError) and error.response is not None:
                result["details"] = (
                    f"HTTP {error.response.status_code}: "
                    f"{error.response.text[:300]}"
                )
            else:
                result["details"] = str(error)[:500]

            print(f"FAILED {name}: {result['details']}")

        results.append(result)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        fields = [
            "company_name",
            "domain",
            "validation_status",
            "hubspot_company_id",
            "sync_status",
            "details",
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print("\n--- SUMMARY ---")
    print(f"Records processed: {len(results)}")
    for status in ("DRY_RUN", "SUCCESS", "SKIPPED", "FAILED"):
        count = sum(row["sync_status"] == status for row in results)
        print(f"{status}: {count}")

    print(f"Results: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
