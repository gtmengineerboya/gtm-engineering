# import csv

# with open("day-06/companies.csv", "r", newline="") as file:

#     reader = csv.DictReader(file) # 'DictReader' reads each row as a 'python dictionry'
#     # {    "company": "...",    "website": "...",    "industry": "...",    "employees": "...",    "country": "...",    "technology": "...",    "job_title": "..."}
# # 1st row---> company,website,industry,employees,country,technology,job_title
# # next row---> CyberSecure,cybersecure.com,Cybersecurity,900,USA,AWS,VP of Business Development
# # DictReader' uses the '1st row' as 'keys':
# # Then' each following row 'becomes a' dictionary'.
# # So:
# # company["company"]--->CyberSecure (this is like value)

#     # print("CSV Headers:")
#     # print(reader.fieldnames)


#     for company in reader:
#         # print(company)
#         print("--------------------")
#         print("Company:", company["company"])
#         print("website:", company["website"])
#         print("Industry:", company["industry"])
#         print("Employees:", company["employees"])
#         print("Country:", company["country"])
#         print("Technology:", company["technology"])
#         print("Job Title:", company["job_title"])


# import csv


# def calculate_score(company):
#     score = 0

#     if company["industry"] == "SaaS":
#         score += 25

#     if int(company["employees"]) >= 500:
#         score += 20

#     if company["country"] == "USA":
#         score += 15

#     return score


# with open("day-06/companies.csv", "r", newline="") as file:

#     reader = csv.DictReader(file)

#     for company in reader:

#         score = calculate_score(company)

#         if score >= 50:
#             qualification = "Qualified"
#         else:
#             qualification = "Not Qualified"

#         print("--------------------")
#         print("Company:", company["company"])
#         print("Industry:", company["industry"])
#         print("Employees:", company["employees"])
#         print("Country:", company["country"])
#         print("ICP Score:", score)
#         print("Qualification:", qualification)


import csv

def calculate_score(company):
    score = 0

    if company["industry"] == "SaaS":
        score += 25

    if int(company["employees"]) >= 500:
        score += 20

    if company["country"] == "USA":
        score += 15

    return score

def calculate_priority(score):

    if score >= 80:
        return "High"

    elif score >= 50:
        return "Medium"

    else:
        return "Low"


with open("day-06/companies.csv", "r", newline="") as file:

    reader = csv.DictReader(file) # reader-->contains the CSV rows.
    #CSV → Python dictionaries
    with open("day-06/enriched_leads.csv", "w", newline="") as output_file: #output_file represents:day-06/enriched_leads.csv

        fieldnames = [
            "company",
            "website",
            "industry",
            "employees",
            "country",
            "technology",
            "job_title",
            "icp_score",
            "qualification",
            "priority"
        ]

        writer = csv.DictWriter(output_file, fieldnames=fieldnames) ##Python dictionaries → CSV
        #imp--->Create a CSV writing tool that will take Python dictionaries and write them into output_file using the column names in fieldnames.
        writer.writeheader() # This create header--> company,website,industry,employees,country,technology,job_title,icp_score,qualification

        for company in reader:

            score = calculate_score(company)

            if score >= 50: #This is your business rule.
                qualification = "Qualified"
            else:
                qualification = "Not Qualified"

            priority = calculate_priority(score)
            
            writer.writerow({ #Now you write one dictionary into the output CSV.
                "company": company["company"],
                "website": company["website"],
                "industry": company["industry"],
                "employees": company["employees"],
                "country": company["country"],
                "technology": company["technology"],
                "job_title": company["job_title"],
                "icp_score": score,
                "qualification": qualification,
                "priority": priority
            })

print("Lead intelligence processing completed.")
print("Output saved to day-06/enriched_leads.csv")