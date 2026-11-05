import os
import requests
from dotenv import load_dotenv

# Load .env
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent  # repo root, independent of the working folder

if __name__ == "__main__":
    load_dotenv(str(ROOT_DIR / "day-09/.env"))

    # Get HubSpot token
    token = os.getenv("HUBSPOT_ACCESS_TOKEN")

    if not token:
        print("ERROR: HubSpot token not found.")
        sys.exit(1)

    # HubSpot Contacts API
    url = "https://api.hubapi.com/crm/v3/objects/contacts"

    # Contact data
    payload = {
        "properties": {
            "firstname": "GTM",
            "lastname": "Test User",
            "email": "gtm.test@example.com",
            "jobtitle": "VP Sales"
        }
    }

    # Authentication + content type
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create contact
    response = requests.post(
        url,
        headers=headers,
        json=payload, timeout=30
    )

    print("Status Code:", response.status_code)

    if response.status_code == 201:
        print("Contact created successfully!")
        print(response.json())
    else:
        print("Contact creation failed.")
        print(response.text)