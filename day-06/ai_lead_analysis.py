# import csv

# leads = []

# with open("day-06/enriched_leads.csv", "r", newline="") as file:

#     reader = csv.DictReader(file)

#     for lead in reader:
#         leads.append(lead)


# # Sort by ICP score
# leads.sort(
#     key=lambda lead: int(lead["icp_score"]),
#     reverse=True
# )


# # Analyze the top lead
# lead = leads[0]

# print("===== AI LEAD ANALYSIS =====")

# print("Company:", lead["company"])
# print("Industry:", lead["industry"])
# print("Employees:", lead["employees"])
# print("Country:", lead["country"])
# print("Technology:", lead["technology"])
# print("Target Contact:", lead["job_title"])
# print("ICP Score:", lead["icp_score"])
# print("Qualification:", lead["qualification"])
# print("Priority:", lead["priority"])

# # print("\nPotential GTM Analysis:")

# # if lead["qualification"] == "Qualified":
# #     print("This company is a qualified prospect.")
# # else:
# #     print("This company does not currently meet the qualification threshold.")

# # print("The target contact is:", lead["job_title"])
# # print("Company technology:", lead["technology"])
# # print("Further research can be used for personalized outreach.")

# # -----------------------------
# # 5. Create dynamic GTM prompt
# # -----------------------------

# prompt = f"""
# You are a GTM research assistant.

# Analyze this company as a potential B2B sales prospect.

# Company: {lead["company"]}
# Industry: {lead["industry"]}
# Employees: {lead["employees"]}
# Country: {lead["country"]}
# Technology: {lead["technology"]}
# Target Contact: {lead["job_title"]}
# ICP Score: {lead["icp_score"]}
# Qualification: {lead["qualification"]}
# Priority: {lead["priority"]}

# Provide:

# 1. Company fit
# 2. Potential business pain points
# 3. Why the target contact may care
# 4. Recommended GTM approach
# 5. Suggested outreach angle
# """


# # -----------------------------
# # 6. Display generated prompt
# # -----------------------------

# print("\n===== GENERATED GTM PROMPT =====")

# print(prompt)

# import csv
# import requests


# # -----------------------------
# # 1. Read enriched leads
# # -----------------------------

# leads = []

# with open("day-06/enriched_leads.csv", "r", newline="") as file:

#     reader = csv.DictReader(file)

#     for lead in reader:
#         leads.append(lead)


# # -----------------------------
# # 2. Sort by ICP score
# # -----------------------------

# leads.sort(
#     key=lambda lead: int(lead["icp_score"]),
#     reverse=True
# )


# # -----------------------------
# # 3. Select the top lead
# # -----------------------------

# lead = leads[0]


# # -----------------------------
# # 4. Create GTM prompt
# # -----------------------------

# prompt = f"""
# You are a GTM research assistant.

# Analyze this company as a potential B2B sales prospect.

# Company: {lead["company"]}
# Industry: {lead["industry"]}
# Employees: {lead["employees"]}
# Country: {lead["country"]}
# Technology: {lead["technology"]}
# Target Contact: {lead["job_title"]}
# ICP Score: {lead["icp_score"]}
# Qualification: {lead["qualification"]}
# Priority: {lead["priority"]}

# Provide:

# 1. Company fit
# 2. Potential business pain points
# 3. Why the target contact may care
# 4. Recommended GTM approach
# 5. Suggested outreach angle

# Keep the answer practical and concise.
# """


# # -----------------------------
# # 5. Send prompt to Ollama
# # -----------------------------

# url = "http://localhost:11434/api/generate"

# payload = {
#     "model": "llama3.2:3b",
#     "prompt": prompt,
#     "stream": False
# }


# response = requests.post(url, json=payload)


# # -----------------------------
# # 6. Check API response
# # -----------------------------

# if response.status_code == 200:

#     result = response.json()

#     print("===== TOP GTM LEAD =====")
#     print("Company:", lead["company"])
#     print("ICP Score:", lead["icp_score"])
#     print("Priority:", lead["priority"])

#     print("\n===== AI GTM ANALYSIS =====")
#     print(result["response"]) #Because result contains the entire response from Ollama, and we only want to print the AI-generated answer.

# else:

#     print("Ollama API request failed.")
#     print("Status Code:", response.status_code)
#     print(response.text)


    ##### saving the AI analysis back into a structured output file,######

# import csv
# import requests


# # -----------------------------
# # 1. Read enriched leads
# # -----------------------------

# leads = []

# with open("day-06/enriched_leads.csv", "r", newline="") as file:

#     reader = csv.DictReader(file)

#     for lead in reader:
#         leads.append(lead)


# # -----------------------------
# # 2. Sort by ICP score
# # -----------------------------

# leads.sort(
#     key=lambda lead: int(lead["icp_score"]),
#     reverse=True
# )


# # -----------------------------
# # 3. Select the top lead
# # -----------------------------

# lead = leads[0] #this gives only --->one lead/top lead (not works for top 10 leads)


# # -----------------------------
# # 4. Create GTM prompt
# # -----------------------------

# prompt = f"""
# You are a GTM research assistant.

# Analyze this company as a potential B2B sales prospect.

# Company: {lead["company"]}
# Industry: {lead["industry"]}
# Employees: {lead["employees"]}
# Country: {lead["country"]}
# Technology: {lead["technology"]}
# Target Contact: {lead["job_title"]}
# ICP Score: {lead["icp_score"]}
# Qualification: {lead["qualification"]}
# Priority: {lead["priority"]}

# Provide:

# 1. Company fit
# 2. Potential business pain points
# 3. Why the target contact may care
# 4. Recommended GTM approach
# 5. Suggested outreach angle

# Keep the answer practical and concise.
# """


# # -----------------------------
# # 5. Send prompt to Ollama
# # -----------------------------

# url = "http://localhost:11434/api/generate"

# payload = {
#     "model": "llama3.2:3b",
#     "prompt": prompt,
#     "stream": False  #send the complete answer at once
# }

# response = requests.post(url, json=payload)


# # -----------------------------
# # 6. Process AI response
# # -----------------------------

# if response.status_code == 200:

#     result = response.json()

#     ai_analysis = result["response"]

#     print("===== TOP GTM LEAD =====")
#     print("Company:", lead["company"])
#     print("ICP Score:", lead["icp_score"])
#     print("Priority:", lead["priority"])

#     print("\n===== AI GTM ANALYSIS =====")
#     print(ai_analysis)


#     # -----------------------------
#     # 7. Save AI analysis
#     # -----------------------------

#     output_data = {
#         "company": lead["company"],
#         "website": lead["website"],
#         "industry": lead["industry"],
#         "employees": lead["employees"],
#         "country": lead["country"],
#         "technology": lead["technology"],
#         "job_title": lead["job_title"],
#         "icp_score": lead["icp_score"],
#         "qualification": lead["qualification"],
#         "priority": lead["priority"],
#         "ai_analysis": ai_analysis
#     }


#     with open(
#         "day-06/ai_enriched_leads.csv",
#         "w",
#         newline="",
#         encoding="utf-8"
#     ) as output_file:

#         fieldnames = [
#             "company",
#             "website",
#             "industry",
#             "employees",
#             "country",
#             "technology",
#             "job_title",
#             "icp_score",
#             "qualification",
#             "priority",
#             "ai_analysis"
#         ]

#         writer = csv.DictWriter(output_file,fieldnames=fieldnames)

#         writer.writeheader() #This writes the column names as the first row from fieldnmes--->is normally called once,
#         writer.writerow(output_data) #called many times—once for each lead.


#     print("\nAI analysis saved to:")
#     print("day-06/ai_enriched_leads.csv")


# else:

#     print("Ollama API request failed.")
#     print("Status Code:", response.status_code)
#     print(response.text)


#####################10 leads#########################
#ai analysis to top 10 leads -->same above code few changes for 10 leads 
import csv
import requests


# ---------------------------------
# 1. Read enriched leads
# ---------------------------------

leads = []

with open(
    "day-06/enriched_leads.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:
        leads.append(lead)


# ---------------------------------
# 2. Sort leads by ICP score
# ---------------------------------

leads.sort(
    key=lambda lead: int(lead["icp_score"]),
    reverse=True
)


# ---------------------------------
# 3. Select Top 10 leads
# ---------------------------------

top_leads = leads[:10]

print("===== TOP 10 GTM LEADS =====")


# ---------------------------------
# 4. Create output CSV
# ---------------------------------

with open(
    "day-06/ai_enriched_leads.csv",
    "w",
    newline="",
    encoding="utf-8"
) as output_file:

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
        "priority",
        "ai_analysis"
    ]

    writer = csv.DictWriter(
        output_file,
        fieldnames=fieldnames
    )

    writer.writeheader()


    # ---------------------------------
    # 5. Process Top 10 leads
    # ---------------------------------

    for index, lead in enumerate(top_leads, start=1):

        print("--------------------")
        print("Lead:", index)
        print("Company:", lead["company"])
        print("ICP Score:", lead["icp_score"])


        # ---------------------------------
        # 6. Create AI prompt
        # ---------------------------------

        prompt = f"""
You are a B2B GTM research assistant.

Analyze this company as a potential B2B sales prospect.

Use ONLY the information provided below.

Company: {lead["company"]}
Industry: {lead["industry"]}
Employees: {lead["employees"]}
Country: {lead["country"]}
Technology: {lead["technology"]}
Target Contact: {lead["job_title"]}
ICP Score: {lead["icp_score"]}
Qualification: {lead["qualification"]}
Priority: {lead["priority"]}

Provide:

1. Company Fit
Explain why the company matches the available ICP criteria.

2. Potential Business Pain Points
Give realistic hypotheses based on the available data.
Clearly label them as potential or possible pain points.
Do not present assumptions as facts.

3. Why the Target Contact May Care
Explain why the job title could potentially care about the identified problem.
Do not claim to know the person's actual priorities.

4. Recommended GTM Approach
Suggest a practical sales approach based on the available information.

5. Suggested Outreach Angle
Give one evidence-based personalization angle.

Important rules:
- Do not invent company facts.
- Do not claim the company is a market leader.
- Do not claim the company uses products that are not listed.
- Do not invent business problems.
- Clearly distinguish facts from hypotheses.
- Keep the analysis concise and practical.
"""


        # ---------------------------------
        # 7. Send prompt to Ollama
        # ---------------------------------

        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            url,
            json=payload
        )


        # ---------------------------------
        # 8. Process AI response
        # ---------------------------------

        if response.status_code == 200:

            result = response.json()

            ai_analysis = result["response"]

            print("AI analysis completed.")


            # ---------------------------------
            # 9. Create output dictionary
            # ---------------------------------

            output_data = {
                "company": lead["company"],
                "website": lead["website"],
                "industry": lead["industry"],
                "employees": lead["employees"],
                "country": lead["country"],
                "technology": lead["technology"],
                "job_title": lead["job_title"],
                "icp_score": lead["icp_score"],
                "qualification": lead["qualification"],
                "priority": lead["priority"],
                "ai_analysis": ai_analysis
            }


            # ---------------------------------
            # 10. Write dictionary to CSV
            # ---------------------------------

            writer.writerow(output_data)


        else:

            print("Ollama API request failed.")
            print("Status Code:", response.status_code)
            print(response.text)


# ---------------------------------
# 11. Completion message
# ---------------------------------

print("\n================================")
print("AI enrichment completed.")
print("Processed leads:", len(top_leads))
print("Output:")
print("day-06/ai_enriched_leads.csv")
print("================================")