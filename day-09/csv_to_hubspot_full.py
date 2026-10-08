# #This is the key CRM concept: IDs identify records; associations connect records.
# import os
# import csv
# import requests
# from dotenv import load_dotenv

# # Load HubSpot credentials
# load_dotenv("day-09/.env")

# token = os.getenv("HUBSPOT_ACCESS_TOKEN")

# if not token:
#     print("ERROR: HubSpot token not found.")
#     exit()

# headers = {
#     "Authorization": f"Bearer {token}",
#     "Content-Type": "application/json"
# }

# company_url = "https://api.hubapi.com/crm/v3/objects/companies"
# contact_url = "https://api.hubapi.com/crm/v3/objects/contacts"

# success_count = 0
# failed_count = 0

# # Read GTM leads
# with open(
#     "day-08/crm_ready_leads.csv",
#     "r",
#     newline="",
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     for lead in reader:

#         print("\n==============================")
#         print("Processing:", lead["company"])
#         print("==============================")

#         # 1. Create Company
#         company_payload = {
#             "properties": {
#                 "name": lead["company"]
#             }
#         }

#         company_response = requests.post(
#             company_url,
#             headers=headers,
#             json=company_payload
#         )

#         if company_response.status_code != 201:
#             print("Company creation FAILED")
#             print(company_response.text)
#             failed_count += 1
#             continue

#         company_id = company_response.json()["id"]

#         print("Company created:", company_id)

#         # 2. Create Contact
#         contact_payload = {
#             "properties": {
#                 "jobtitle": lead["job_title"]
#             }
#         }

#         contact_response = requests.post(
#             contact_url,
#             headers=headers,
#             json=contact_payload
#         )

#         if contact_response.status_code != 201:
#             print("Contact creation FAILED")
#             print(contact_response.text)
#             failed_count += 1
#             continue

#         contact_id = contact_response.json()["id"]

#         print("Contact created:", contact_id)

#         # 3. Associate Contact with Company
#         association_url = ( #"HubSpot, take Contact 566468942535 and associate it with Company 351365185246."
#             f"https://api.hubapi.com/crm/v4/objects/contacts/"
#             f"{contact_id}/associations/companies/{company_id}"
#         )

#         association_payload = [
#             {
#                 "associationCategory": "HUBSPOT_DEFINED",
#                 "associationTypeId": 1
#             }
#         ]

#         association_response = requests.put(
#             association_url,
#             headers=headers,
#             json=association_payload
#         )

#         if association_response.status_code in [200, 201, 204]:

#             print("Association: SUCCESS")
#             success_count += 1

#         else:

#             print("Association: FAILED")
#             print(association_response.text)
#             failed_count += 1


# print("\n================================")
# print("GTM → HUBSPOT SUMMARY")
# print("================================")
# print("Successful:", success_count)
# print("Failed:", failed_count)
# print("Total:", success_count + failed_count)

import os
import csv
import requests
from dotenv import load_dotenv

# Load HubSpot token
load_dotenv("day-09/.env")

token = os.getenv("HUBSPOT_ACCESS_TOKEN")

if not token:
    print("ERROR: HubSpot token not found.")
    exit()

# HubSpot API headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# HubSpot API URLs
company_url = "https://api.hubapi.com/crm/v3/objects/companies"
contact_url = "https://api.hubapi.com/crm/v3/objects/contacts"

# Counters
success_count = 0
failed_count = 0

# Read GTM leads CSV
with open(
    "day-08/crm_ready_leads.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:

        print("\n==============================")
        print("Processing:", lead["company"])
        print("==============================")

        # --------------------------------
        # 1. CREATE COMPANY
        # --------------------------------

        company_payload = {
            "properties": {
                "name": lead["company"]
            }
        }

        try:
            company_response = requests.post(
                company_url,
                headers=headers,
                json=company_payload,
                timeout=10
            )

            print("Company Status:", company_response.status_code)

            if company_response.status_code != 201:
                print("Company creation FAILED")
                print(company_response.text)

                failed_count += 1
                continue

            company_id = company_response.json()["id"]

            print("Company created:", company_id)

        except requests.exceptions.RequestException as error:
            print("Company API error:", error)

            failed_count += 1
            continue

        # --------------------------------
        # 2. CREATE CONTACT
        # --------------------------------

        contact_payload = {
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

        try:
            contact_response = requests.post(
                contact_url,
                headers=headers,
                json=contact_payload,
                timeout=10
            )

            print("Contact Status:", contact_response.status_code)

            if contact_response.status_code != 201:
                print("Contact creation FAILED")
                print(contact_response.text)

                failed_count += 1
                continue

            contact_id = contact_response.json()["id"]

            print("Contact created:", contact_id)

        except requests.exceptions.RequestException as error:
            print("Contact API error:", error)

            failed_count += 1
            continue

        # --------------------------------
        # 3. ASSOCIATE CONTACT → COMPANY
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

        try:
            association_response = requests.put(
                association_url,
                headers=headers,
                json=association_payload,
                timeout=10
            )

            print(
                "Association Status:",
                association_response.status_code
            )

            if association_response.status_code in [200, 201, 204]:

                print("Association: SUCCESS")

                success_count += 1

            else:

                print("Association: FAILED")
                print(association_response.text)

                failed_count += 1

        except requests.exceptions.RequestException as error:

            print("Association API error:", error)

            failed_count += 1


# --------------------------------
# FINAL SUMMARY
# --------------------------------

print("\n================================")
print("GTM → HUBSPOT SUMMARY")
print("================================")

print("Successful:", success_count)
print("Failed:", failed_count)
print("Total:", success_count + failed_count)