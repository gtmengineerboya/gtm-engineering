
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

PROJECT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_DIR / "day-09" / ".env")

TOKEN = (
    os.getenv("HUBSPOT_ACCESS_TOKEN")
    or os.getenv("HUBSPOT_TOKEN")
)

if not TOKEN:
    raise RuntimeError("HubSpot token not found.")

url = "https://api.hubapi.com/crm/v3/properties/companies"
headers = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get(url, headers=headers, timeout=30)
print("HTTP Status:", response.status_code)
response.raise_for_status()

properties = response.json().get("results", [])

targets = {
    "hs_lead_status",
    "gtm_lead_status",
    "icp_score",
    "outreach_message",
}

for prop in properties:
    if prop.get("name") in targets:
        print(f"\nProperty: {prop.get('name')}")
        print(f"Label: {prop.get('label')}")
        print(f"Type: {prop.get('type')}")
        print(f"Field type: {prop.get('fieldType')}")

        options = prop.get("options", [])
        if options:
            print("Allowed values:")
            for option in options:
                print(
                    f"  Value: {option.get('value')} | "
                    f"Label: {option.get('label')}"
                )

print("\nInspection complete. No CRM records modified.")
