import os
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv("day-09/.env")

# Get HubSpot token
token = os.getenv("HUBSPOT_ACCESS_TOKEN")

if not token:
    print("ERROR: HubSpot token not found.")
    exit()

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
    json=payload
)

print("Status Code:", response.status_code)

if response.status_code == 201:
    print("Contact created successfully!")
    print(response.json())
else:
    print("Contact creation failed.")
    print(response.text)