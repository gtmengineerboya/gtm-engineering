# #this is for send personalized action to only the first/top lead.
# import csv
# import requests


# # -----------------------------
# # 1. Read AI-enriched lead
# # -----------------------------

# with open("day-06/ai_enriched_leads.csv", "r", newline="", encoding="utf-8") as file:

#     reader = csv.DictReader(file)

#     lead = next(reader) #--->get one row -->because here we taking only one --->top lead (in this case)
# #Another way without next()
# # for lead in reader:--->process all rows, one by one
# #    print(lead)

# # -----------------------------
# # 2. Create personalization prompt
# # -----------------------------

# prompt = f"""
# You are a B2B GTM personalization assistant.

# Create a personalized sales outreach message for this lead.

# Company: {lead["company"]}
# Industry: {lead["industry"]}
# Employees: {lead["employees"]}
# Country: {lead["country"]}
# Technology: {lead["technology"]}
# Target Contact: {lead["job_title"]}
# ICP Score: {lead["icp_score"]}
# Priority: {lead["priority"]}

# AI Company Analysis: 
# {lead["ai_analysis"]} 


# Create:

# 1. Personalization angle
# 2. Business pain point
# 3. Value proposition
# 4. Short LinkedIn outreach message

# Keep the message professional, specific and concise.
# Do not make up facts about the company.
# """
# #{lead["ai_analysis"]} is Python dictionary access. It means: --->“Take the value stored in the 'ai_analysis field' of the 'lead' dictionary.

# # -----------------------------
# # 3. Send prompt to Ollama
# # -----------------------------

# url = "http://localhost:11434/api/generate"

# payload = {
#     "model": "llama3.2:3b",
#     "prompt": prompt,
#     "stream": False
# }

# response = requests.post(url, json=payload)


# # -----------------------------
# # 4. Display AI response
# # -----------------------------

# if response.status_code == 200:

#     result = response.json()

#     print("===== PERSONALIZED GTM OUTREACH =====") #Personalized outreach generation is used to automatically create a sales message that is tailored to a specific lead instead of sending the same generic message to everyone.
#     print(result["response"])

# else:

#     print("Ollama API request failed.")
#     print("Status Code:", response.status_code)
#     print(response.text)




#send personalized action to Top 10 leads automatically:
import csv
import requests


# ---------------------------------
# 1. Read AI-enriched leads
# ---------------------------------

leads = []

with open(
    "day-06/ai_enriched_leads.csv",
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


for lead in top_leads:

    print("--------------------")
    print("Company:", lead["company"])
    print("ICP Score:", lead["icp_score"])
    print("Priority:", lead["priority"])


# ---------------------------------
# 4. Prepare output file
# ---------------------------------

output_file = open(
    "day-06/personalized_leads.csv",
    "w",
    newline="",
    encoding="utf-8"
)

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
    "personalization_angle",
    "pain_point",
    "value_proposition",
    "outreach_message"
]

writer = csv.DictWriter(
    output_file,
    fieldnames=fieldnames
)

writer.writeheader()


# ---------------------------------
# 5. Process each Top 10 lead
# ---------------------------------

for index, lead in enumerate(top_leads, start=1):

    print("\n==============================")
    print("Processing Lead:", index)
    print("Company:", lead["company"])
    print("==============================")


    # ---------------------------------
    # 6. Create personalized AI prompt
    # ---------------------------------

    prompt = f"""
You are a B2B GTM personalization assistant.

Create a personalized GTM action for this lead.

Company: {lead["company"]}
Industry: {lead["industry"]}
Employees: {lead["employees"]}
Country: {lead["country"]}
Technology: {lead["technology"]}
Target Contact: {lead["job_title"]}
ICP Score: {lead["icp_score"]}
Qualification: {lead["qualification"]}
Priority: {lead["priority"]}

AI Company Analysis:
{lead["ai_analysis"]}

Provide exactly these four sections:

Personalization Angle:
Give one specific reason this company or buyer could be relevant.

Pain Point:
Identify a realistic business problem based only on the available information.

Value Proposition:
Explain what type of value our solution could provide.

Outreach Message:
Write a short professional LinkedIn outreach message.

Important:
- Do not invent company facts.
- Do not claim that the company uses a product unless the data confirms it.
- Keep the outreach message concise.
"""


    # ---------------------------------
    # 7. Send request to Ollama
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

        ai_response = result["response"]

        print("\n===== AI PERSONALIZATION =====")
        print(ai_response)


        # ---------------------------------
        # 9. Save AI response
        # ---------------------------------

        writer.writerow({
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
            "personalization_angle": ai_response,
            "pain_point": "",
            "value_proposition": "",
            "outreach_message": ""
        })


    else:

        print("Ollama API request failed.")
        print("Status Code:", response.status_code)
        print(response.text)


# ---------------------------------
# 10. Close output file
# ---------------------------------

output_file.close()


print("\n================================")
print("Top 10 personalization completed.")
print("Output saved to:")
print("day-06/personalized_leads.csv")
print("================================")