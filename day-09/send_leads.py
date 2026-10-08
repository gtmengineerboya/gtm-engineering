# import csv
# import requests

# # 1. CRM API URL
# url = "https://jsonplaceholder.typicode.com/posts"

# # 2. Read CRM-ready leads
# with open(
#     "day-08/crm_ready_leads.csv",
#     "r",
#     newline="",
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     # 3. Send each lead
#     for lead in reader:

#         payload = { #Python reads every lead from the CSV, creates a payload for each one, and sends each lead to the API.
#             "company": lead["company"],
#             "job_title": lead["job_title"],
#             "icp_score": lead["icp_score"],
#             "lead_status": lead["lead_status"],
#             "outreach_message": lead["outreach_message"]
#         }

#         # 4. Send lead to CRM API
#         response = requests.post(
#             url,
#             json=payload
#         )

#         # 5. Print result
#         print("--------------------------------")
#         print("Company:", lead["company"])
#         print("Status Code:", response.status_code)
#         print("CRM Response:", response.json())


# import csv
# import requests

# url = "https://jsonplaceholder.typicode.com/posts"

# with open(
#     "day-08/crm_ready_leads.csv",
#     "r",
#     newline="",
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     for lead in reader:

#         payload = {
#             "company": lead["company"],
#             "job_title": lead["job_title"],
#             "icp_score": lead["icp_score"],
#             "lead_status": lead["lead_status"],
#             "outreach_message": lead["outreach_message"]
#         }

#         try:
#             response = requests.post( #Python tries to send the lead.
#                 url,
#                 json=payload,
#                 timeout=10
#             )

#             if response.status_code == 201:
#                 print("--------------------------------")
#                 print("Company:", lead["company"])
#                 print("CRM upload: SUCCESS")
#                 print("Status Code:", response.status_code)

#             else:
#                 print("--------------------------------")
#                 print("Company:", lead["company"])
#                 print("CRM upload: FAILED")
#                 print("Status Code:", response.status_code)

#         except requests.exceptions.RequestException as error: #Python catches the API/network error instead of crashing the entire program.

#             print("--------------------------------")
#             print("Company:", lead["company"])
#             print("CRM upload: FAILED")
#             print("Error:", error)

# print("--------------------------------")
# print("CRM upload process completed.")



import csv
import requests

url = "https://jsonplaceholder.typicode.com/posts" #JSONPlaceholder is the fake/test API we used in Day 9.

success_count = 0  #Now we'll make the pipeline report how many leads succeeded and failed.s
failed_count = 0

with open(
    "day-08/crm_ready_leads.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:

        payload = {
            "company": lead["company"],
            "job_title": lead["job_title"],
            "icp_score": lead["icp_score"],
            "lead_status": lead["lead_status"],
            "outreach_message": lead["outreach_message"]
        }

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=10
            )

            if response.status_code == 201:
                success_count += 1

                print("--------------------------------")
                print("Company:", lead["company"])
                print("Upload: SUCCESS")

            else:
                failed_count += 1

                print("--------------------------------")
                print("Company:", lead["company"])
                print("Upload: FAILED")

        except requests.exceptions.RequestException as error:
            failed_count += 1

            print("--------------------------------")
            print("Company:", lead["company"])
            print("Upload: FAILED")
            print("Error:", error)


print("\n================================")
print("CRM UPLOAD SUMMARY")
print("================================")
print("Successful:", success_count)
print("Failed:", failed_count)
print("Total:", success_count + failed_count)
