
import csv
import os
import requests
from dotenv import load_dotenv

load_dotenv("../day-09/.env")

TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN") or os.getenv("HUBSPOT_TOKEN")

if not TOKEN:
    raise RuntimeError("HubSpot token not found.")

URL = "https://api.hubapi.com/crm/v3/objects/companies"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

with open("../day-11/personalized_leads.csv", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for lead in reader:
        name = lead.get("company_name", "").strip()
        domain = lead.get("website", "").strip()

        if not name or not domain:
            continue

        response = requests.post(
            URL,
            headers=HEADERS,
            json={"properties": {"name": name, "domain": domain}},
            timeout=30,
        )

        if response.status_code == 201:
            print(f"CREATED: {name}")
        elif response.status_code == 409:
            print(f"ALREADY EXISTS: {name}")
        else:
            print(f"FAILED: {name} | {response.status_code} | {response.text[:200]}")
