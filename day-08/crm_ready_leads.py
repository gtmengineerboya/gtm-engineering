import csv

# 1. Read personalized outreach results
leads = []

with open(
    "day-08/personalized_outreach.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:
        leads.append(lead)


# 2. Create CRM-ready CSV
with open(
    "day-08/crm_ready_leads.csv",
    "w",
    newline="",
    encoding="utf-8"
) as output_file:

    fieldnames = [
        "company",
        "job_title",
        "icp_score",
        "personalization_angle",
        "pain_point",
        "value_proposition",
        "outreach_message",
        "lead_status"
    ]

    writer = csv.DictWriter(
        output_file,
        fieldnames=fieldnames
    )

    writer.writeheader()


    # 3. Process each lead
    for lead in leads:

        # Determine lead status
        if int(lead["icp_score"]) >= 80:
            lead_status = "Hot"
        elif int(lead["icp_score"]) >= 60:
            lead_status = "Warm" #ICP Score = numerical qualification, while Lead Status = operational category.
        else:
            lead_status = "Cold"


        # 4. Create CRM record
        crm_record = {
            "company": lead["company"],
            "job_title": lead["job_title"],
            "icp_score": lead["icp_score"],
            "personalization_angle": lead["personalization_angle"],
            "pain_point": lead["pain_point"],
            "value_proposition": lead["value_proposition"],
            "outreach_message": lead["outreach_message"],
            "lead_status": lead_status
        }

        writer.writerow(crm_record)


print("\n================================")
print("CRM DATA PREPARATION COMPLETE")
print("================================")

print("Total leads:", len(leads))
print("Output:")
print("day-08/crm_ready_leads.csv")