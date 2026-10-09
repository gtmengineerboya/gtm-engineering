

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# 1. Load the .env file using an absolute path
PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR / "day-09" / ".env"

load_dotenv(ENV_FILE)

# 2. Read the HubSpot access token
TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN") or os.getenv("HUBSPOT_TOKEN")

if not TOKEN:
    raise RuntimeError(
        f"HubSpot token not found. Check environment variable names in: {ENV_FILE}"
    )

# 3. Configure HubSpot API
SEARCH_URL = "https://api.hubapi.com/crm/v3/objects/companies/search"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

# 4. Companies to inspect
COMPANY_NAMES = [
    "Company1",
    "Company25",
    "Company33",
    "Company41",
    "Company49",
    "Company57",
    "Company65",
    "Company73",
    "Company81",
    "Company89",
    "Company97",
]


def search_companies(names):
    """Search for existing companies without modifying CRM records."""

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "name",
                        "operator": "EQ",
                        "value": name,
                    }
                ]
            }
            for name in names
        ],
        "properties": ["name", "domain"],
        "limit": 100,
    }

    response = requests.post(
        SEARCH_URL,
        headers=HEADERS,
        json=payload,
        timeout=30,
    )

    if not response.ok:
        print(f"HTTP Error: {response.status_code}")
        print(response.text[:1000])
        return []

    return response.json().get("results", [])


def main():
    print("HubSpot company inspection")
    print(f"Environment file found: {ENV_FILE.exists()}")
    print("Searching existing companies only...\n")

    all_results = []

    # HubSpot allows a maximum of five filter groups per request.
    for start in range(0, len(COMPANY_NAMES), 5):
        batch = COMPANY_NAMES[start:start + 5]

        try:
            results = search_companies(batch)
            all_results.extend(results)
        except requests.RequestException as error:
            print(f"API request failed: {error}")
            return

    if not all_results:
        print("No matching companies found.")
        return

    print(f"Matching records found: {len(all_results)}\n")

    for company in all_results:
        properties = company.get("properties", {})

        print(
            f"ID: {company.get('id')} | "
            f"Name: {properties.get('name')} | "
            f"Domain: {properties.get('domain') or '(missing)'}"
        )


if __name__ == "__main__":
    main()
