
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load the token from the project's existing .env file.
PROJECT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_DIR / "day-09" / ".env"
load_dotenv(ENV_FILE)

TOKEN = (
    os.getenv("HUBSPOT_ACCESS_TOKEN")
    or os.getenv("HUBSPOT_TOKEN")
)

if not TOKEN:
    raise RuntimeError(f"HubSpot token not found: {ENV_FILE}")

URL = "https://api.hubapi.com/crm/v3/properties/companies"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

response = requests.get(URL, headers=HEADERS, timeout=30)

print("HTTP Status:", response.status_code)

if not response.ok:
    print(response.text[:1000])
    raise SystemExit(1)

properties = response.json().get("results", [])
keywords = ("gtm", "icp", "outreach", "lead status")

matches = [
    prop for prop in properties
    if any(
        keyword in prop.get("name", "").lower()
        or keyword in prop.get("label", "").lower()
        for keyword in keywords
    )
]

if matches:
    print("\nMatching existing properties:")
    for prop in matches:
        print(
            f"Internal name: {prop.get('name')} | "
            f"Label: {prop.get('label')} | "
            f"Type: {prop.get('type')}"
        )
else:
    print("No matching custom properties found.")

print("\nNo CRM records were modified.")
