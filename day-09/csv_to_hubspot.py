import os
import csv
import requests
from dotenv import load_dotenv

# Load HubSpot credentials
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent  # repo root, independent of the working folder

if __name__ == "__main__":
    load_dotenv(str(ROOT_DIR / "day-09/.env"))

    token = os.getenv("HUBSPOT_ACCESS_TOKEN")

    if not token:
        print("ERROR: HubSpot token not found.")
        sys.exit(1)

    # HubSpot Contacts API
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Read GTM leads
    with open(
        str(ROOT_DIR / "day-08/crm_ready_leads.csv"),
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        # Send each lead to HubSpot
        for lead in reader:

            payload = {
                "properties": {
                    "firstname": lead["company"],
                    "jobtitle": lead["job_title"]
                }
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload, timeout=30
            )

            print("--------------------------------")
            print("Company:", lead["company"])
            print("Status Code:", response.status_code)

            if response.status_code == 201:
                print("HubSpot Contact: CREATED")
            else:
                print("HubSpot Contact: FAILED")
                print(response.text)

    print("--------------------------------")
    print("CSV → HubSpot process completed.")