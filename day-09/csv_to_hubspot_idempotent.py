#Idempotency--->Running the same automation multiple times should not create duplicate data or unwanted side effects.
import os
import csv
import requests
from dotenv import load_dotenv

# --------------------------------
# LOAD HUBSPOT TOKEN
# --------------------------------

load_dotenv("day-09/.env")

token = os.getenv("HUBSPOT_ACCESS_TOKEN")

if not token:
    print("ERROR: HubSpot token not found.")
    exit()

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_url = "https://api.hubapi.com/crm/v3/objects/companies"
contact_url = "https://api.hubapi.com/crm/v3/objects/contacts"


# --------------------------------
# FIND EXISTING COMPANY
# --------------------------------

def find_company(company_name):

    search_url = "https://api.hubapi.com/crm/v3/objects/companies/search"

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "name",
                        "operator": "EQ",
                        "value": company_name
                    }
                ]
            }
        ],
        "properties": ["name"],
        "limit": 1
    }

    response = requests.post(
        search_url,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code != 200:
        print("Company search failed:")
        print(response.text)
        return None

    results = response.json().get("results", [])

    if results:
        return results[0]["id"]

    return None


# --------------------------------
# CREATE COMPANY
# --------------------------------

def create_company(company_name):

    payload = {
        "properties": {
            "name": company_name
        }
    }

    response = requests.post(
        company_url,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code == 201:
        return response.json()["id"]

    print("Company creation failed:")
    print(response.text)

    return None


# --------------------------------
# CREATE CONTACT
# --------------------------------

def create_contact(lead):

    payload = {
        "properties": {
            "jobtitle": lead["job_title"],
            "icp_score": lead["icp_score"],
            "gtm_lead_status": lead["lead_status"],
            "personalization_angle": lead["personalization_angle"],
            "pain_point": lead["pain_point"],
            "value_proposition": lead["value_proposition"],
            "outreach_message": lead["outreach_message"]
        }
    }

    response = requests.post(
        contact_url,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code == 201:
        return response.json()["id"]

    print("Contact creation failed:")
    print(response.text)

    return None


# --------------------------------
# ASSOCIATE CONTACT → COMPANY
# --------------------------------

def associate_contact(contact_id, company_id):

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

    response = requests.put(
        association_url,
        headers=headers,
        json=association_payload,
        timeout=10
    )

    return response.status_code in [200, 201, 204]


# --------------------------------
# PROCESS CSV
# --------------------------------

success_count = 0
failed_count = 0

with open(
    "day-08/crm_ready_leads.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:

        company_name = lead["company"]

        print("\n==============================")
        print("Processing:", company_name)
        print("==============================")


        # -----------------------------
        # CHECK COMPANY
        # -----------------------------

        company_id = find_company(company_name)

        if company_id:

            print("Existing company found:", company_id)

        else:

            print("Company not found. Creating...")

            company_id = create_company(company_name)

            if not company_id:
                failed_count += 1
                continue

            print("New company created:", company_id)


        # -----------------------------
        # CREATE CONTACT
        # -----------------------------

        contact_id = create_contact(lead)

        if not contact_id:
            failed_count += 1
            continue

        print("Contact created:", contact_id)


        # -----------------------------
        # ASSOCIATE
        # -----------------------------

        association_success = associate_contact(
            contact_id,
            company_id
        )

        if association_success:

            print("Association: SUCCESS")
            success_count += 1

        else:

            print("Association: FAILED")
            failed_count += 1


# --------------------------------
# SUMMARY
# --------------------------------

print("\n================================")
print("GTM → HUBSPOT SUMMARY")
print("================================")

print("Successful:", success_count)
print("Failed:", failed_count)
print("Total:", success_count + failed_count)