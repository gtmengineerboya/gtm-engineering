import os
import requests
from dotenv import load_dotenv

load_dotenv("day-09/.env")

token = os.getenv("HUBSPOT_ACCESS_TOKEN")

if not token:
    print("ERROR: HubSpot token not found.")
    exit()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# --------------------------------
# 1. Create Company
# --------------------------------

company_url = "https://api.hubapi.com/crm/v3/objects/companies"

company_payload = {
    "properties": {
        "name": "Company41"
    }
}

company_response = requests.post(
    company_url,
    headers=headers,
    json=company_payload
)

print("Company Status:", company_response.status_code)

if company_response.status_code != 201:
    print("Company creation failed.")
    print(company_response.text)
    exit()

company_id = company_response.json()["id"]

print("Company created:", company_id)


# --------------------------------
# 2. Create Contact
# --------------------------------

contact_url = "https://api.hubapi.com/crm/v3/objects/contacts"

contact_payload = {
    "properties": {
        "jobtitle": "Chief Growth Officer"
    }
}

contact_response = requests.post(
    contact_url,
    headers=headers,
    json=contact_payload
)

print("Contact Status:", contact_response.status_code)

if contact_response.status_code != 201:
    print("Contact creation failed.")
    print(contact_response.text)
    exit()

contact_id = contact_response.json()["id"]

print("Contact created:", contact_id)


# --------------------------------
# 3. Associate Contact → Company
# --------------------------------

association_url = (
    f"https://api.hubapi.com/crm/v4/objects/contacts/"
    f"{contact_id}/associations/companies/{company_id}"
)

association_payload = [
    {
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 1
    }
]

association_response = requests.put(
    association_url,
    headers=headers,
    json=association_payload
)

print("Association Status:", association_response.status_code)

if association_response.status_code in [200, 201, 204]:
    print("Contact successfully associated with Company.")
else:
    print("Association failed.")
    print(association_response.text)