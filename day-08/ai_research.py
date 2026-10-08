#“Why might this lead be a good GTM opportunity, and how should we approach it?”
# import csv
# import requests


# # ---------------------------------
# # 1. Read scored leads
# # ---------------------------------

# leads = []

# with open(
#     "day-06/enriched_leads.csv",
#     "r",
#     newline="",
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     for lead in reader:
#         leads.append(lead)


# # ---------------------------------
# # 2. Sort by ICP score
# # ---------------------------------

# leads.sort(
#     key=lambda lead: int(lead["icp_score"]),
#     reverse=True
# )


# # ---------------------------------
# # 3. Select Top 5 leads
# # ---------------------------------

# top_leads = leads[:5]


# # ---------------------------------
# # 4. AI Research
# # ---------------------------------

# url = "http://localhost:11434/api/generate"


# for index, lead in enumerate(top_leads, start=1): #enumerate() --->gives us both the position and the item.

#     print("\n================================")
#     print("AI RESEARCH - LEAD", index)
#     print("================================")

#     print("Company:", lead["company"])
#     print("ICP Score:", lead["icp_score"])

#     prompt = f"""
# You are a B2B GTM research assistant.

# Analyze this potential sales prospect using ONLY the information provided.

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

# 1. Company Fit
# Explain why this company matches the available ICP criteria.

# 2. Potential Business Pain Points
# Identify possible problems based only on the available information.
# Clearly label them as potential problems.

# 3. Buyer Relevance
# Explain why the target job title may care about these problems.

# 4. GTM Opportunity
# Suggest how a sales team could approach this company.

# 5. Research Limitations
# Clearly state what information is missing and cannot be confirmed.

# Important:
# - Do not invent company facts.
# - Do not claim unverified problems are facts.
# - Do not invent technologies.
# - Separate facts from hypotheses.
# - Keep the response concise.
# """

#     payload = {
#         "model": "llama3.2:3b",
#         "prompt": prompt,
#         "stream": False
#     }

#     response = requests.post(
#         url,
#         json=payload
#     )


#     # ---------------------------------
#     # 5. Process AI response
#     # ---------------------------------

#     if response.status_code == 200:

#         result = response.json()

#         ai_analysis = result["response"]

#         print("\n===== AI RESEARCH =====")
#         print(ai_analysis)

#     else:

#         print("Ollama API request failed.")
#         print("Status Code:", response.status_code)
#         print(response.text)

# import csv
# import requests
# import json


# # ---------------------------------
# # 1. Read scored leads
# # ---------------------------------

# leads = []

# with open(
#     "day-06/enriched_leads.csv",
#     "r",
#     newline="",
#     encoding="utf-8"
# ) as file:

#     reader = csv.DictReader(file)

#     for lead in reader:
#         leads.append(lead)


# # ---------------------------------
# # 2. Sort by ICP score
# # ---------------------------------

# leads.sort(
#     key=lambda lead: int(lead["icp_score"]),
#     reverse=True
# )


# # ---------------------------------
# # 3. Select Top 5 leads
# # ---------------------------------

# top_leads = leads[:5]


# # ---------------------------------
# # 4. Ollama API
# # ---------------------------------

# url = "http://localhost:11434/api/generate"


# # ---------------------------------
# # 5. Process each lead
# # ---------------------------------

# for index, lead in enumerate(top_leads, start=1):

#     print("\n================================")
#     print("AI RESEARCH - LEAD", index)
#     print("================================")

#     print("Company:", lead["company"])
#     print("ICP Score:", lead["icp_score"])


#     # ---------------------------------
#     # 6. Create AI prompt
#     # ---------------------------------

#     prompt = f"""
# You are a B2B GTM research assistant.

# Analyze this potential sales prospect using ONLY the information provided.

# Company: {lead["company"]}
# Industry: {lead["industry"]}
# Employees: {lead["employees"]}
# Country: {lead["country"]}
# Technology: {lead["technology"]}
# Target Contact: {lead["job_title"]}
# ICP Score: {lead["icp_score"]}
# Qualification: {lead["qualification"]}
# Priority: {lead["priority"]}

# Return ONLY valid JSON.

# Use exactly this structure:

# {{
#     "company_fit": "...",
#     "potential_pain_points": "...",
#     "buyer_relevance": "...",
#     "gtm_opportunity": "...",
#     "research_limitations": "..."
# }}

# Rules:

# - Do not invent company facts.
# - Clearly treat pain points as potential problems.
# - Do not invent technologies.
# - Separate facts from assumptions.
# - Keep each field concise.
# """


#     # ---------------------------------
#     # 7. Prepare API request
#     # ---------------------------------

#     payload = {
#         "model": "llama3.2:3b",
#         "prompt": prompt,
#         "stream": False
#     }


#     # ---------------------------------
#     # 8. Send request to Ollama
#     # ---------------------------------

#     response = requests.post(
#         url,
#         json=payload
#     )


#     # ---------------------------------
#     # 9. Process API response
#     # ---------------------------------

#     if response.status_code == 200:

#         result = response.json()

#         ai_analysis = result["response"]


#         # ---------------------------------
#         # 10. Convert JSON text to Python
#         # ---------------------------------

#         try:

#             research = json.loads(ai_analysis)


#             # ---------------------------------
#             # 11. Display structured research
#             # ---------------------------------

#             print("\n===== STRUCTURED AI RESEARCH =====")

#             print(
#                 "Company Fit:",
#                 research["company_fit"]
#             )

#             print(
#                 "Potential Pain Points:",
#                 research["potential_pain_points"]
#             )

#             print(
#                 "Buyer Relevance:",
#                 research["buyer_relevance"]
#             )

#             print(
#                 "GTM Opportunity:",
#                 research["gtm_opportunity"]
#             )

#             print(
#                 "Research Limitations:",
#                 research["research_limitations"]
#             )


#         except json.JSONDecodeError:

#             print("\nAI returned invalid JSON.")

#             print("\nRaw AI response:")
#             print(ai_analysis)


#     else:

#         print("\nOllama API request failed.")

#         print(
#             "Status Code:",
#             response.status_code
#         )

#         print(response.text)


# # ---------------------------------
# # 12. Completion message
# # ---------------------------------

# print("\n================================")
# print("AI research completed.")
# print("Processed leads:", len(top_leads))
# print("================================")



import csv
import requests
import json


# ---------------------------------
# 1. Read scored leads
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
# 2. Sort by ICP score
# ---------------------------------

leads.sort(
    key=lambda lead: int(lead["icp_score"]),
    reverse=True
)


# ---------------------------------
# 3. Select Top 5 leads
# ---------------------------------

top_leads = leads[:5]


# ---------------------------------
# 4. Create output CSV
# ---------------------------------

with open(
    "day-08/ai_research_results.csv",
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
        "company_fit",
        "potential_pain_points",
        "buyer_relevance",
        "gtm_opportunity",
        "research_limitations"
    ]

    writer = csv.DictWriter(
        output_file,
        fieldnames=fieldnames
    )

    writer.writeheader()


    # ---------------------------------
    # 5. Ollama API
    # ---------------------------------

    url = "http://localhost:11434/api/generate"


    # ---------------------------------
    # 6. Process each lead
    # ---------------------------------

    for index, lead in enumerate(top_leads, start=1):

        print("\n================================")
        print("AI RESEARCH - LEAD", index)
        print("================================")

        print("Company:", lead["company"])
        print("ICP Score:", lead["icp_score"])


        # ---------------------------------
        # 7. Create AI prompt
        # ---------------------------------

        prompt = f"""
You are a B2B GTM research assistant.

Analyze this potential sales prospect using ONLY the information provided.

Company: {lead["company"]}
Industry: {lead["industry"]}
Employees: {lead["employees"]}
Country: {lead["country"]}
Technology: {lead["technology"]}
Target Contact: {lead["job_title"]}
ICP Score: {lead["icp_score"]}
Qualification: {lead["qualification"]}
Priority: {lead["priority"]}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "company_fit": "...",
    "potential_pain_points": "...",
    "buyer_relevance": "...",
    "gtm_opportunity": "...",
    "research_limitations": "..."
}}

Rules:

- Do not invent company facts.
- Clearly treat pain points as potential problems.
- Do not invent technologies.
- Separate facts from assumptions.
- Keep each field concise.
"""


        # ---------------------------------
        # 8. Send request to Ollama
        # ---------------------------------

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
        # 9. Process AI response
        # ---------------------------------

        if response.status_code == 200:

            result = response.json()

            ai_analysis = result["response"]


            try:

                research = json.loads(ai_analysis)


                # ---------------------------------
                # 10. Display research
                # ---------------------------------

                print("\n===== AI RESEARCH =====")

                print(
                    "Company Fit:",
                    research["company_fit"]
                )

                print(
                    "Pain Points:",
                    research["potential_pain_points"]
                )

                print(
                    "Buyer Relevance:",
                    research["buyer_relevance"]
                )

                print(
                    "GTM Opportunity:",
                    research["gtm_opportunity"]
                )

                print(
                    "Research Limitations:",
                    research["research_limitations"]
                )


                # ---------------------------------
                # 11. Save research to CSV
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
                    "company_fit": research["company_fit"],
                    "potential_pain_points":
                        research["potential_pain_points"],
                    "buyer_relevance":
                        research["buyer_relevance"],
                    "gtm_opportunity":
                        research["gtm_opportunity"],
                    "research_limitations":
                        research["research_limitations"]
                }

                writer.writerow(output_data)

                print("\nSaved to CSV.")


            except json.JSONDecodeError:

                print("\nAI returned invalid JSON.")

                print(ai_analysis)


        else:

            print("\nOllama API request failed.")

            print(
                "Status Code:",
                response.status_code
            )

            print(response.text)


# ---------------------------------
# 12. Completion
# ---------------------------------

print("\n================================")
print("AI research completed.")
print("Processed leads:", len(top_leads))
print("Output:")
print("day-08/ai_research_results.csv")
print("================================")