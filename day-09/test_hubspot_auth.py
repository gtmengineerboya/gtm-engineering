import os
import requests
from dotenv import load_dotenv

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent  # repo root, independent of the working folder

if __name__ == "__main__":
    load_dotenv(str(ROOT_DIR / "day-09/.env")) #"Read the variables from .env."

    token = os.getenv("HUBSPOT_ACCESS_TOKEN") #Give me the value stored under HUBSPOT_ACCESS_TOKEN."

    if not token:
        print("ERROR: HubSpot token not found.")
        sys.exit(1)

    url = "https://api.hubapi.com/crm/v3/objects/contacts?limit=1"

    headers = {
        "Authorization": f"Bearer {token}", #Bearer basically means:The person/system presenting this valid token is authorized to make this API request.
        "Content-Type": "application/json"
    }

    response = requests.get(
        url,
        headers=headers, timeout=30
    )

    print("Status Code:", response.status_code)

    if response.status_code == 200:
        print("HubSpot authentication SUCCESS!")
        print(response.json())
    else:
        print("HubSpot authentication FAILED!")
        print(response.text)