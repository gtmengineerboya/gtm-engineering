import csv
import requests
import json


# ---------------------------------
# 1. Read AI research results
# ---------------------------------

leads = []

with open(
    "day-08/ai_research_results.csv",
    "r",
    newline="",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file)

    for lead in reader:
        leads.append(lead)


# ---------------------------------
# 2. Create output CSV
# ---------------------------------

with open(
    "day-08/personalized_outreach.csv",
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
        "outreach_message"
    ]

    writer = csv.DictWriter(
        output_file,
        fieldnames=fieldnames
    )

    writer.writeheader()


    # ---------------------------------
    # 3. Ollama API
    # ---------------------------------

    url = "http://localhost:11434/api/generate"


    # ---------------------------------
    # 4. Process each lead
    # ---------------------------------

    for index, lead in enumerate(leads, start=1):

        print("\n================================")
        print("PERSONALIZATION - LEAD", index)
        print("================================")

        print("Company:", lead["company"])
        print("ICP Score:", lead["icp_score"])


        # ---------------------------------
        # 5. Create personalization prompt
        # ---------------------------------

        prompt = f"""
You are a B2B GTM personalization assistant.

Create personalized outreach based ONLY on the research provided.

Company: {lead["company"]}
Industry: {lead["industry"]}
Employees: {lead["employees"]}
Country: {lead["country"]}
Technology: {lead["technology"]}
Target Contact: {lead["job_title"]}
ICP Score: {lead["icp_score"]}

Company Fit:
{lead["company_fit"]}

Potential Pain Points:
{lead["potential_pain_points"]}

Buyer Relevance:
{lead["buyer_relevance"]}

GTM Opportunity:
{lead["gtm_opportunity"]}

Research Limitations:
{lead["research_limitations"]}

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
- Treat pain points as potential problems.
- Do not claim assumptions are confirmed facts.
- Keep the message concise.
- Write a professional LinkedIn-style outreach message.
- Do not use exaggerated claims.
"""


        # ---------------------------------
        # 6. Send request to Ollama
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
        # 7. Process response
        # ---------------------------------

        if response.status_code == 200:

            result = response.json()

            ai_response = result["response"]


            try:

                personalization = json.loads(
                    ai_response
                )


                # ---------------------------------
                # 8. Display result
                # ---------------------------------

                print(
                    "Personalization:",
                    personalization["personalization_angle"]
                )

                print(
                    "Pain Point:",
                    personalization["pain_point"]
                )

                print(
                    "Value Proposition:",
                    personalization["value_proposition"]
                )

                print(
                    "Outreach Message:",
                    personalization["outreach_message"]
                )


                # ---------------------------------
                # 9. Save result
                # ---------------------------------

                output_data = {
                    "company": lead["company"],
                    "job_title": lead["job_title"],
                    "icp_score": lead["icp_score"],
                    "personalization_angle":
                        personalization["personalization_angle"],
                    "pain_point":
                        personalization["pain_point"],
                    "value_proposition":
                        personalization["value_proposition"],
                    "outreach_message":
                        personalization["outreach_message"]
                }

                writer.writerow(output_data)


            except json.JSONDecodeError:

                print("AI returned invalid JSON.")
                print(ai_response)


        else:

            print("Ollama API request failed.")
            print("Status Code:", response.status_code)
            print(response.text)


# ---------------------------------
# 10. Completion
# ---------------------------------

print("\n================================")
print("AI personalization completed.")
print("Processed leads:", len(leads))
print("Output:")
print("day-08/personalized_outreach.csv")
print("================================")