import csv
import requests
import json


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
# 2. Sort by ICP score
# ---------------------------------

leads.sort(
    key=lambda lead: int(lead["icp_score"]),
    reverse=True
)


# ---------------------------------
# 3. Select Top 10 leads
# ---------------------------------

top_leads = leads[:10]

print("===== STRUCTURED GTM OUTREACH =====")


# ---------------------------------
# 4. Create output CSV
# ---------------------------------

with open(
    "day-06/structured_outreach.csv",
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
    # 5. Process each lead
    # ---------------------------------

    for index, lead in enumerate(top_leads, start=1):

        print("\n------------------------------")
        print("Processing Lead:", index)
        print("Company:", lead["company"])
        print("ICP Score:", lead["icp_score"])
        print("------------------------------")


        # ---------------------------------
        # 6. Create structured AI prompt
        # ---------------------------------

        prompt = f"""
You are a B2B GTM personalization assistant.

Analyze the following lead.

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

Return ONLY valid JSON.

Use exactly this structure:

{{
    "personalization_angle": "...",
    "pain_point": "...",
    "value_proposition": "...",
    "outreach_message": "..."
}}

Rules:

- Do not invent company facts.
- Do not claim that a pain point is confirmed.
- Treat pain points as potential problems.
- Do not invent technologies.
- Keep the outreach message concise and professional.
- The outreach message should be suitable for LinkedIn.
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

            try:#These values didn't come from the original CSV.They came from Ollama.

                structured_data = json.loads(ai_response)#json.loads()-->convert AI JSON text into 'Python data'

                print("Personalization:",
                      structured_data["personalization_angle"])

                print("Pain Point:",
                      structured_data["pain_point"])

                print("Value Proposition:",
                      structured_data["value_proposition"])

                print("Outreach Message:",
                      structured_data["outreach_message"])


                # ---------------------------------
                # 9. Save structured data
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
                    "personalization_angle":
                        structured_data["personalization_angle"],
                    "pain_point":
                        structured_data["pain_point"],
                    "value_proposition":
                        structured_data["value_proposition"],
                    "outreach_message":
                        structured_data["outreach_message"]
                })

            except json.JSONDecodeError:#handle the case where AI didn't follow the JSON format

                print("AI returned invalid JSON.")
                print("Raw response:")
                print(ai_response)

        else:

            print("Ollama API request failed.")
            print("Status Code:", response.status_code)
            print(response.text)


print("\n================================")
print("Structured outreach completed.")
print("Processed leads:", len(top_leads))
print("Output:")
print("day-06/structured_outreach.csv")
print("================================")